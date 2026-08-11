# Escopo do MVP — como cortar até caber

## A regra das 3 telas

Toda micro-aplicação útil cabe em três telas. Se não cabe, o recorte está errado.

O padrão que funciona na maioria dos casos:

| Tela | Função | Exemplo (dieta) |
|------|--------|-----------------|
| **1. Ver** | A pessoa abre o link e vê a informação que ela precisa agora | "Sua alimentação de hoje" |
| **2. Agir** | Ela faz a única ação que importa | "Trocar o almoço" / "Marcar como feito" |
| **3. Painel do dono** | O profissional cadastra e acompanha | "Cadastrar dieta do paciente" |

A tela 3 pode ser uma planilha ou um formulário no começo. Não precisa ser bonita — só o dono usa.

## O teste dos 10 segundos

A pessoa abre o link e, em 10 segundos, entende o que é e faz a ação. Se precisa de tutorial, o app está complexo demais.

## A lista do NÃO (mais importante que a lista do sim)

Escreva de 8 a 12 itens. Sugestões que quase sempre ficam de fora da v1:

- Login com e-mail e senha → **use link único** (ex: `site.com/d/a8f3k2`)
- App nativo na loja → **é site que abre no celular**
- Notificação push → **WhatsApp manual resolve**
- Pagamento dentro do app → **PIX na mão até 10 clientes**
- Relatórios e gráficos
- Histórico completo / exportar PDF
- Vários usuários com permissões diferentes
- Integração com qualquer sistema externo
- Modo escuro, idiomas, personalização visual
- Painel de administração bonito
- Chat / comentários
- IA (a menos que a IA seja literalmente o produto)

Apresente essa lista ao aluno com a frase: **"nada disso entra na v1 — e é por isso que ela vai existir."**

## Dados mínimos

Liste os campos que precisam ser guardados. Regra: **se passar de 15 campos, corte.**

Exemplo (dieta):
```
Paciente: nome, link_unico, nutricionista_id
Refeição: paciente_id, dia_semana, horario, descricao, calorias
Substituição: refeicao_id, alimento, alternativa, calorias
```
9 campos. Cabe.

## Como cortar quando não cabe

Em ordem, corte:

1. **Funcionalidades secundárias** — tudo que veio depois de "e também"
2. **Configurabilidade** — deixe fixo no código o que dá. Personalização é v3.
3. **Automação** — o que dá pra fazer na mão no começo, faça na mão. Se você tem 5 clientes, cadastrar manualmente é mais rápido que construir o importador.
4. **Casos de exceção** — resolva o caso comum. Exceção você trata por WhatsApp.
5. **Perfis de usuário** — um perfil só na v1.

## O que NÃO cortar nunca

- **Funcionar no celular.** 90% dos usuários vão abrir no celular. Se quebrar no celular, o app não existe.
- **Carregar rápido.** Mais de 3 segundos e a pessoa fecha.
- **Não perder dado.** Um backup, mesmo que manual, desde o primeiro dia.
- **Um jeito de falar com você.** Um botão de WhatsApp resolve.

## Primeiro passo de segunda-feira

Termine sempre com **uma** ação concreta que cabe em 2 horas e não envolve programar.

Bons exemplos:
- "Mandar essa mensagem para 5 pacientes: [texto pronto]"
- "Abrir uma planilha e cadastrar as dietas dos 3 pacientes mais antigos"
- "Fazer um print da tela principal no Canva e mandar pra 3 colegas perguntando se elas pagariam"

Maus exemplos:
- "Começar o projeto"
- "Estudar a ferramenta X"
- "Definir a arquitetura"
