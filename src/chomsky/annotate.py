"""Visual web annotator for the human gold set (zero extra deps, stdlib only).

Runs on the box; you reach it from the laptop browser over Tailscale. You select a
text fragment with the mouse, click an act (13 buttons or number keys), and it saves
a quote-based span. The working file is the same quote-JSONL that `chomsky.gold compile`
consumes, so the flow is: annotate here -> `gold compile` -> `gold score`/eval.

    python -m chomsky.annotate --file gold/to_annotate.jsonl --port 8765 --host 0.0.0.0
    # then open http://lucian-desktop.tailbb1a78.ts.net:8765  (or the 100.x tailnet IP)

No auth — bind to the tailnet IP (or keep it on a trusted box). Edits autosave to --file.
"""
import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Dict, List
from chomsky.taxonomy import load_taxonomy
from chomsky.gold import compile_gold

_FILE = ""
_ACTS: List[str] = []
_TAXONOMY = None


def read_rows(path: str) -> List[Dict]:
    """Read the working quote-JSONL: [{text, spans:[{quote,act}]}]. Missing file -> []."""
    import os
    if not os.path.exists(path):
        return []
    rows: List[Dict] = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            rows.append({"text": obj.get("text", ""), "spans": obj.get("spans", [])})
    return rows


def write_rows(path: str, rows: List[Dict]) -> None:
    """Persist rows as quote-JSONL, keeping only {quote,act} per span."""
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            spans = [{"quote": s["quote"], "act": s["act"]} for s in r.get("spans", [])]
            f.write(json.dumps({"text": r.get("text", ""), "spans": spans}, ensure_ascii=False) + "\n")


_HTML = """<!doctype html><html lang="pt-br"><head><meta charset="utf-8">
<title>chomsky · anotador de atos de fala</title>
<style>
 :root{color-scheme:dark}
 body{font:16px/1.5 system-ui,sans-serif;background:#0f1115;color:#e6e6e6;margin:0;padding:20px;max-width:900px;margin:0 auto}
 header{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-bottom:14px}
 button{background:#1c1f26;color:#e6e6e6;border:1px solid #333;border-radius:6px;padding:6px 10px;cursor:pointer;font-size:14px}
 button:hover{background:#272b34}
 #text{font-size:22px;line-height:1.7;background:#161922;padding:18px;border-radius:10px;user-select:text;cursor:text;white-space:pre-wrap}
 #actbar{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0}
 #actbar button{padding:6px 12px}
 .span{display:flex;align-items:center;gap:8px;background:#161922;padding:6px 10px;border-radius:6px;margin:4px 0}
 .span button{margin-left:auto;padding:2px 8px}
 .badge{padding:2px 8px;border-radius:5px;color:#000;font-weight:600;font-size:13px}
 mark{border-radius:4px;color:#000;padding:0 2px}
 #preview{background:#161922;padding:14px;border-radius:10px;font-size:18px;line-height:1.7;white-space:pre-wrap;margin-top:10px}
 #status{margin-left:auto;color:#9fd}
 h4{margin:16px 0 4px;color:#9aa}
 .hint{color:#778;font-size:13px}
</style></head><body>
<header>
 <button onclick="go(-1)">◀ anterior</button>
 <strong id="pos">–</strong>
 <button onclick="go(1)">próximo ▶</button>
 <span id="progress" class="hint"></span>
 <span id="status"></span>
</header>
<div class="hint">selecione um trecho com o mouse e clique no ato (ou teclas 1–9). setas ← → navegam. salva sozinho.</div>
<h4>texto</h4>
<div id="text"></div>
<h4>atos</h4>
<div id="actbar"></div>
<h4>spans deste exemplo</h4>
<div id="spans"></div>
<h4>prévia</h4>
<div id="preview"></div>
<script>
let S={rows:[],acts:[],idx:0}; let pending=null;
const COLORS=["#8ecae6","#ffb703","#90be6d","#f94144","#bdb2ff","#fb8500","#43aa8b","#f9c74f","#ff8fab","#a0c4ff","#d4a373","#caffbf","#ffd6a5"];
function colorFor(a){const i=S.acts.indexOf(a);return COLORS[(i<0?0:i)%COLORS.length];}
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function curr(){return S.rows[S.idx]||{text:'',spans:[]};}
async function load(){const r=await fetch('/api/state');const j=await r.json();S.rows=j.rows;S.acts=j.acts;render();}
function render(){
 const row=curr();
 document.getElementById('pos').textContent=(S.idx+1)+' / '+S.rows.length;
 const ann=S.rows.filter(r=>r.spans&&r.spans.length).length;
 document.getElementById('progress').textContent=ann+' anotados';
 document.getElementById('text').textContent=row.text;
 const ab=document.getElementById('actbar');ab.innerHTML='';
 S.acts.forEach((a,i)=>{const b=document.createElement('button');b.textContent=(i<9?(i+1)+' ':'')+a;b.style.borderLeft='6px solid '+COLORS[i%COLORS.length];b.onclick=()=>addSpan(a);ab.appendChild(b);});
 const sl=document.getElementById('spans');sl.innerHTML='';
 (row.spans||[]).forEach((sp,j)=>{const d=document.createElement('div');d.className='span';
   d.innerHTML='<span class="badge" style="background:'+colorFor(sp.act)+'">'+esc(sp.act)+'</span> '+esc(sp.quote);
   const x=document.createElement('button');x.textContent='✕';x.onclick=()=>{row.spans.splice(j,1);render();save();};d.appendChild(x);sl.appendChild(d);});
 document.getElementById('preview').innerHTML=previewHtml(row);
}
function previewHtml(row){let html='',cur=0;const t=row.text;for(const sp of(row.spans||[])){const i=t.indexOf(sp.quote,cur);if(i<0)continue;html+=esc(t.slice(cur,i));html+='<mark style="background:'+colorFor(sp.act)+'">'+esc(t.slice(i,i+sp.quote.length))+'</mark>';cur=i+sp.quote.length;}html+=esc(t.slice(cur));return html;}
document.addEventListener('mouseup',()=>{const node=document.getElementById('text').firstChild;const sel=window.getSelection();if(!sel.rangeCount||sel.isCollapsed)return;const r=sel.getRangeAt(0);if(r.startContainer!==node||r.endContainer!==node)return;let s=r.startOffset,e=r.endOffset;if(s>e){const t=s;s=e;e=t;}pending={start:s,quote:curr().text.slice(s,e)};});
function addSpan(act){if(!pending||!pending.quote){document.getElementById('status').textContent='selecione um trecho primeiro';return;}const row=curr();row.spans=row.spans||[];row.spans.push({quote:pending.quote,act:act,_start:pending.start});row.spans.sort((a,b)=>(a._start||0)-(b._start||0));pending=null;window.getSelection().removeAllRanges();render();save();}
function go(d){S.idx=Math.max(0,Math.min(S.rows.length-1,S.idx+d));render();}
let saveT=null;function save(){clearTimeout(saveT);saveT=setTimeout(doSave,500);}
async function doSave(){const payload={rows:S.rows.map(r=>({text:r.text,spans:(r.spans||[]).map(s=>({quote:s.quote,act:s.act}))}))};const r=await fetch('/api/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});const j=await r.json();document.getElementById('status').textContent='salvo · '+j.valid+' válidos · '+j.errors.length+' erro(s)';}
document.addEventListener('keydown',(e)=>{if(e.target.tagName==='INPUT')return;if(e.key==='ArrowRight')go(1);else if(e.key==='ArrowLeft')go(-1);else if(/^[1-9]$/.test(e.key)){const i=parseInt(e.key)-1;if(i<S.acts.length)addSpan(S.acts[i]);}});
load();
</script></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        data = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *a):  # quiet
        pass

    def do_GET(self):
        if self.path == "/" or self.path.startswith("/index"):
            self._send(200, _HTML, "text/html; charset=utf-8")
        elif self.path == "/api/state":
            rows = read_rows(_FILE)
            self._send(200, json.dumps({"acts": _ACTS, "rows": rows}, ensure_ascii=False))
        else:
            self._send(404, json.dumps({"error": "not found"}))

    def do_POST(self):
        if self.path != "/api/save":
            self._send(404, json.dumps({"error": "not found"}))
            return
        n = int(self.headers.get("Content-Length", 0))
        payload = json.loads(self.rfile.read(n) or b"{}")
        rows = payload.get("rows", [])
        write_rows(_FILE, rows)
        anns, errors = compile_gold(rows, _TAXONOMY)
        self._send(200, json.dumps({"ok": True, "valid": len(anns), "errors": errors}, ensure_ascii=False))


def main(argv=None) -> int:
    global _FILE, _ACTS, _TAXONOMY
    p = argparse.ArgumentParser(prog="chomsky.annotate", description="Visual web annotator for the gold set.")
    p.add_argument("--file", required=True, help="working quote-JSONL (e.g. gold/to_annotate.jsonl)")
    p.add_argument("--taxonomy", default="config/taxonomy.yaml")
    p.add_argument("--host", default="0.0.0.0", help="bind host (use the 100.x tailnet IP for tailnet-only)")
    p.add_argument("--port", type=int, default=8765)
    args = p.parse_args(argv)
    _FILE = args.file
    _TAXONOMY = load_taxonomy(args.taxonomy)
    _ACTS = _TAXONOMY.acts
    srv = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"annotator on http://{args.host}:{args.port}  (file: {_FILE}, {len(_ACTS)} acts)")
    print("open it from the laptop via the tailnet hostname; Ctrl-C to stop.")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
