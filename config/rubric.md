<!-- config/rubric.md -->
<!-- FROZEN v1 (2026-06-05) — 13 acts (ISO 24617-2 + Searle); rules from Fase-0 papers. -->
# Rúbrica de Anotação — Atos de Fala (PT-BR)

Você anota **atos de fala** em texto portugues. Cada span e um trecho **contiguo e literal**
do texto que realiza um ato. Spans **NAO se sobrepoem**. Use APENAS os 13 atos abaixo.

## Os 13 atos

- **informar** — prover/declarar informacao (assertivo). Ex.: "O relatorio esta pronto."
- **perguntar** — solicitar informacao. Ex.: "Que horas sao?"
- **concordar** — manifestar acordo. Ex.: "Sim, exatamente."
- **discordar** — manifestar desacordo. Ex.: "Nao acho isso."
- **pedir** — requisitar ou ordenar uma acao (inclui instrucao/comando). Ex.: "Me envia o arquivo?" / "Aperte a tecla 13."
- **sugerir** — propor sem obrigar. Ex.: "Talvez seja melhor esperar."
- **oferecer** — oferecer-se para fazer/dar algo. Ex.: "Posso te ajudar com isso."
- **prometer** — comprometer-se com acao futura. Ex.: "Eu te aviso amanha."
- **saudar** — iniciar contato. Ex.: "Bom dia!"
- **agradecer** — expressar gratidao. Ex.: "Muito obrigado!"
- **desculpar** — pedir desculpas. Ex.: "Me desculpe pelo atraso."
- **despedir** — encerrar contato. Ex.: "Ate logo!"
- **expressar_emocao** — manifestar emocao/avaliacao afetiva (inclui elogio, parabens, pesar). Ex.: "Que alivio!" / "Parabens!"

## Regras (importantes)

1. **Rotulo mais especifico.** Se um trecho e informacao E desacordo, use `discordar`. "Isso e uma vergonha" -> `discordar`, nao `informar`.
2. **Descrever um ato != realizar o ato.** Relatar que alguem fez algo e `informar`. Ex.: "Vettel pediu desculpas a equipe" -> `informar` (relata uma desculpa), NAO `desculpar`.
3. **Pedido indireto = `pedir`.** Em PT-BR, interrogativa com poder/querer/conseguir e diretivo. "Voce poderia me enviar?" -> `pedir`, nao `perguntar`.
4. **Nao distinguir o que fundimos.** Responder/elaborar/explicar/confirmar -> `informar`. Instruir/ordenar -> `pedir`. Elogiar/parabenizar/lamentar -> `expressar_emocao`.
5. **Quotes literais.** Cada "quote" deve ser uma substring EXATA e contigua do texto.
6. **Spans nao se sobrepoem.** Trechos sem ato ficam de fora (sem rotulo).

## Exemplo anotado

Texto: "Oi! Voce poderia me mandar o relatorio? Prometo revisar hoje. Obrigado!"
```json
{"text": "Oi! Voce poderia me mandar o relatorio? Prometo revisar hoje. Obrigado!",
 "spans": [
   {"quote": "Oi!", "act": "saudar"},
   {"quote": "Voce poderia me mandar o relatorio?", "act": "pedir"},
   {"quote": "Prometo revisar hoje.", "act": "prometer"},
   {"quote": "Obrigado!", "act": "agradecer"}
 ]}
```
