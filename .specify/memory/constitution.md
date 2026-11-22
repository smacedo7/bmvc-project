# Constituição do projeto BMVC

## Princípios

### I. Trabalho acadêmico verificável
As regras específicas da atividade no SIGAA prevalecem sobre escolhas deste projeto. Cada requisito confirmado deve aparecer na especificação e ter uma forma objetiva de verificação. Não declarar como concluído algo que não foi executado ou observado.

### II. Uso efetivo do BMVC
O projeto deve partir do repositório `hgmachine/bmvc_start_from_this` e manter a aplicação executável por `route.py`. Rotas HTTP ficam em `route.py`, coordenação de casos de uso em controladores, regras e estado do domínio em classes de modelo, e apresentação em templates de visão. O framework do professor deve continuar reconhecível.

### III. Orientação a objetos com propósito
Classes devem representar entidades e responsabilidades reais do domínio. Encapsular regras e invariantes nos objetos apropriados. Evitar classes sem comportamento, herança artificial e lógica de negócio dispersa por rotas ou templates.

### IV. Simplicidade e aprendizado
Escolher um escopo pequeno que possa ser explicado e demonstrado pelo estudante. Registrar decisões de projeto em linguagem clara. Implementar por etapas, com revisão do funcionamento e da compreensão antes de ampliar recursos.

### V. Verificação
Testar regras de negócio de forma isolada e percursos HTTP essenciais. Conferir execução local, erros esperados e instruções de instalação. Documentar limitações conhecidas e resultados efetivamente observados.

## Restrições atuais

- Python e o BMVC fornecido pelo professor são obrigatórios.
- O servidor inicial do BMVC usa Bottle e expõe a porta 8080.
- O tema é ERP/CRM interno simples para clientes, produtos, vendas e resumo administrativo. As entregas seguem os quatro critérios BMVC I–IV enviados pelo estudante.
- O nível 1 usa Bottle e arquivos estáticos. Do nível 2 em diante, persistência com SQLAlchemy e PostgreSQL. Login é obrigatório no nível 3 e WebSocket no nível 4.
- Cada nível deve ter branch, roteiro em `docs/videos/`, commits verificáveis e demonstração local antes da gravação.

## Fluxo de trabalho

Para cada funcionalidade: escrever a especificação com critérios de aceitação, criar o plano técnico respeitando a arquitetura do BMVC, dividir em tarefas pequenas, implementar e verificar. Atualizar a documentação quando as regras do SIGAA forem fornecidas.

## Governança

Esta constituição orienta as especificações e decisões técnicas do projeto. Mudanças de escopo ou arquitetura devem ser registradas junto com sua justificativa. As regras da disciplina, quando conhecidas, têm prioridade.

**Versão**: 0.1.0 | **Criada**: 2026-11-21 | **Última alteração**: 2026-11-21
