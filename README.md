# Validador de Micro-Aplicações

> Skill para Claude que valida ideias de **micro-aplicações** — ferramentas web simples que resolvem **um** problema específico, de forma rápida e recorrente.

Não é para validar startup. É para o profissional que já atende clientes e percebeu uma tarefa repetitiva que dá pra virar um link: nutricionista, personal, contador, advogado, dentista, corretor, professor, dono de loja.

A skill responde uma pergunta só: **"isso vira um link que resolve uma dor e alguém paga?"**

---

## Instalação

### Opção 1 — Arquivo `.skill` (mais fácil)

1. Baixe [`dist/validador-microapp.skill`](dist/validador-microapp.skill) *(botão **Download raw file** no canto direito)*
2. Arraste o arquivo para uma conversa no Claude
3. Clique em **Save skill**

Pronto. A skill fica disponível em todas as suas conversas.

### Opção 2 — Claude Code / Cowork (pasta de skills)

```bash
git clone https://github.com/danilohmaia/validador-microapp.git ~/.claude/skills/validador-microapp
```

Ou, se preferir baixar o ZIP:

```bash
cd ~/.claude/skills
curl -L -o validador.zip https://github.com/danilohmaia/validador-microapp/archive/refs/heads/main.zip
unzip validador.zip && mv validador-microapp-main validador-microapp && rm validador.zip
```

Reinicie o Claude Code. A skill aparece como `validador-microapp`.

### Opção 3 — ZIP direto do GitHub

**Code → Download ZIP**, descompacte e mova a pasta para `~/.claude/skills/`.

---

## Como usar

Descreva a ideia em português normal:

> "Sou nutricionista. Quero que meus pacientes recebam um link em vez de um PDF gigante, onde eles veem a dieta do dia e podem trocar alimentos mantendo as calorias."

A skill conduz o resto, uma pergunta por vez.

Atalhos:

| Você diz | Ela faz |
|----------|---------|
| "quero validar essa ideia" | fluxo completo (7 etapas) |
| "só me dá o veredito" | modo rápido, só o essencial |
| "não tenho ideia nenhuma" | 3 perguntas e a ideia aparece sozinha |

---

## O que ela faz

1. **Reescreve a ideia** em uma frase testável: *[quem] usa [o quê] para [fazer o quê], no lugar de [o jeito manual de hoje]*
2. **5 filtros de corte** — matar ou passar, sem meio-termo
3. **Nota em 6 eixos** e um veredito: Constrói / Constrói com corte / Reformula / Descarta
4. **Teste de 7 dias** — o que fazer antes de escrever uma linha de código
5. **Escopo do MVP** — 3 telas, a lista do que NÃO fazer, dados mínimos e como cobrar
6. **Relatório `.md` + dashboard `.html`**

### Os 5 filtros

| Filtro | Pergunta |
|--------|----------|
| Problema único | Dá pra explicar em uma frase, sem "e também"? |
| Recorrência | Acontece toda semana ou todo mês? |
| Gambiarra atual | Já existe um jeito manual chato hoje? |
| Pagador claro | Quem tira dinheiro do bolso? |
| Entregável rápido | A v1 sai em até 2 semanas? |

O terceiro é o mais decisivo: **se ninguém faz aquilo manualmente hoje, provavelmente ninguém quer.** Uma planilha chata circulando é a melhor prova de que a dor existe.

### Os 6 eixos

Dor · Recorrência · Pagador · Simplicidade · Canal · Substituição — nota de 0 a 10 cada.

Com **veto**: se Pagador ou Substituição ficar abaixo de 4, o veredito trava em REFORMULA mesmo com nota alta. Ideia bonita que ninguém paga não passa.

---

## Regras da casa

- Um problema por app
- Máximo **3 telas** na v1
- Sem jargão de startup (nada de TAM, CAC, moat)
- Proibido sugerir marketplace, app nativo, IA desnecessária, investimento ou "escalar"
- Se a ideia é ruim, a skill diz — e oferece o recorte que salvaria

---

## Requisitos

Python 3 para os scripts de nota e dashboard. **Nenhuma chave de API.** Funciona sem internet — a pesquisa de mercado é opcional.

Teste rápido:

```bash
python3 scripts/score.py --dor 8 --recorrencia 9 --pagador 7 \
  --simplicidade 9 --canal 10 --substituicao 8 \
  --filtros passa,passa,passa,passa,falha --ideia "Link de dieta"
```

---

## Estrutura

```
SKILL.md                          orquestrador (7 etapas)
references/criterios-microapp.md  os 5 filtros de corte
references/entrevista.md          roteiro de conversa (Mom Test em português)
references/precificacao.md        3 rotas de cobrança e faixas de preço no Brasil
references/armadilhas.md          as 10 armadilhas mais comuns
references/escopo-mvp.md          como cortar escopo até caber
references/exemplos.md            3 casos calibrados
templates/relatorio.md            estrutura do relatório
templates/roteiro-entrevista.md   folha de campo para imprimir
scripts/score.py                  nota e veredito determinísticos
scripts/dashboard.py              gera o HTML visual
dist/validador-microapp.skill     pacote pronto para instalar
```

---

## Licença

MIT. Use, modifique e distribua à vontade — inclusive com seus alunos.
