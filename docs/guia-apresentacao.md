# Guia de apresentação dos níveis BMVC

Este guia reúne a preparação comum aos quatro vídeos. Os roteiros detalhados, comandos e falas estão nos documentos de cada nível:

- [Vídeo 1 — página estática](videos/nivel-1.md)
- [Vídeo 2 — CRUD completo](videos/nivel-2.md)
- [Vídeo 3 — login e área restrita](videos/nivel-3.md)
- [Vídeo 4 — WebSocket em tempo real](videos/nivel-4.md)

## Antes de gravar

1. Confirme a branch indicada no roteiro com `git branch --show-current`.
2. Execute toda a demonstração uma vez sem gravar.
3. Deixe o terminal, navegador e editor com fonte legível.
4. Feche notificações e abas pessoais.
5. Prepare os dados que serão digitados.
6. Deixe o repositório público aberto em uma aba.
7. Use um cronômetro e termine alguns segundos antes do limite.

## Ambiente recomendado

- Navegador em uma janela separada.
- Editor mostrando somente arquivos do projeto.
- Terminal com a pasta do repositório aberta.
- Resolução que permita ler código e formulários.
- Microfone conferido antes da gravação.

## Dados de demonstração

Use dados fictícios e fáceis de digitar:

| Tipo | Valor sugerido |
| --- | --- |
| Cliente principal | Ana Souza |
| E-mail principal | ana@example.com |
| Cliente do CRUD | Cliente Teste |
| E-mail do CRUD | teste@example.com |
| Produto | Caderno Executivo |
| Preço | 25,90 |
| Estoque | 10 |
| Quantidade da venda | 2 |

Não mostre senhas, cookies, tokens de sessão, conteúdo do banco ou dados pessoais reais.

## Troca entre níveis

Encerre a aplicação e o banco do nível anterior antes de trocar de branch. Cada roteiro usa um nome de projeto Compose diferente para separar os volumes:

```bash
docker compose -p bmvc_nivel2 down
docker compose -p bmvc_nivel3 down
docker compose -p bmvc_nivel4 down
```

Execute somente o comando correspondente ao nível que estiver ativo. Esses comandos preservam os dados. Evite `down -v` se quiser manter o banco preparado.

## Estrutura da explicação

Em todos os vídeos, siga a mesma ordem:

1. propósito do sistema;
2. requisito específico do nível;
3. estrutura BMVC envolvida;
4. demonstração funcionando;
5. trecho principal do código;
6. CSS e JavaScript ativos;
7. repositório público e encerramento.

## Entrega

Antes de enviar:

- assista ao vídeo completo;
- confira se o áudio está compreensível;
- confira se código e textos estão legíveis;
- confirme a duração máxima do nível;
- teste o link do vídeo em uma janela anônima;
- teste o link público do repositório;
- envie os dois links no local solicitado pelo professor.
