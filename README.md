# Status Report - Conversor Markdown para HTML

Este projeto contém um script Python que converte automaticamente o arquivo Markdown (`Status Report COST.md`) para HTML (`index.html`).

## Como usar

### Pré-requisitos

- Python 3.6 ou superior
- O arquivo `Status Report COST.md` deve existir no diretório
- O arquivo `index.html` deve existir como template (com CSS e JavaScript)

### Execução

Execute o script usando:

```bash
uv run md_to_html.py
```

Ou diretamente com Python:

```bash
python3 md_to_html.py
```

### O que o script faz

1. **Lê o arquivo Markdown** (`Status Report COST.md`)
2. **Extrai os dados** de cada projeto:
   - Nome do projeto
   - Descrição
   - Status
   - Prazo
   - Project Manager
   - Atores envolvidos
   - Processo SEI
   - Documentos (links)
   - Etapas (com datas)
3. **Gera o HTML** substituindo apenas a seção de projetos no `index.html`
4. **Preserva** todo o CSS, JavaScript e estrutura HTML existente
5. **Atualiza** a data de atualização no header

### Estrutura do Markdown

O arquivo Markdown deve seguir este formato:

```markdown
Data de atualização: DD/MM/YYYY
## [[Nome do Projeto]]

Descrição: Descrição do projeto

Status: Em execução
Prazo: DD/MM/YYYY
Project Manager: #pm
Atores envolvidos: #ator1 #ator2 #ator3
Processo SEI: número-do-processo

### Documentos

- [Título do documento](URL)

### Etapas

- [DD/MM/YYYY] Descrição da etapa
```

### Vantagens

- ✅ Manutenção mais fácil: edite apenas o arquivo Markdown
- ✅ Evita erros de formatação HTML manual
- ✅ Garante consistência na estrutura
- ✅ Preserva toda a funcionalidade JavaScript e CSS existente
- ✅ Atualização automática da data

### Notas

- O script preserva todo o HTML existente, incluindo sidebar, filtros, CSS e JavaScript
- Apenas a seção de projetos (accordion) é substituída
- A data de atualização é automaticamente atualizada no header

