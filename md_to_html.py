#!/usr/bin/env python3

import re
from pathlib import Path
from html import escape
from typing import List, Dict, Optional

def parse_markdown_file(md_path: str) -> tuple[str, List[Dict]]:
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    update_date = None
    projects = []
    
    if lines and lines[0].startswith('Data de atualização:'):
        update_date = lines[0].replace('Data de atualização:', '').strip()
    
    current_project = None
    current_section = None
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith('## [[') and line.endswith(']]'):
            if current_project:
                projects.append(current_project)
            
            project_name = line[5:-2]
            current_project = {
                'name': project_name,
                'description': '',
                'status': '',
                'deadline': '',
                'pm': '',
                'actors': [],
                'sei_process': '',
                'documents': [],
                'etapas': []
            }
            current_section = None
            i += 1
            continue
        
        if not current_project:
            i += 1
            continue
        
        if line.startswith('Descrição:'):
            current_project['description'] = line.replace('Descrição:', '').strip()
            i += 1
            continue
        
        if line.startswith('Status:'):
            current_project['status'] = line.replace('Status:', '').strip()
            i += 1
            continue
        
        if line.startswith('Prazo:'):
            current_project['deadline'] = line.replace('Prazo:', '').strip()
            i += 1
            continue
        
        if line.startswith('Project Manager:'):
            pm_text = line.replace('Project Manager:', '').strip()
            pm_match = re.search(r'#(\w+)', pm_text)
            if pm_match:
                current_project['pm'] = pm_match.group(1)
            i += 1
            continue
        
        if line.startswith('Atores envolvidos:'):
            actors_text = line.replace('Atores envolvidos:', '').strip()
            actors = re.findall(r'#([\w-]+)', actors_text)
            current_project['actors'] = actors
            i += 1
            continue
        
        if line.startswith('Processo SEI:'):
            current_project['sei_process'] = line.replace('Processo SEI:', '').strip()
            i += 1
            continue
        
        if line == '### Documentos':
            current_section = 'documents'
            i += 1
            continue
        
        if line == '### Etapas':
            current_section = 'etapas'
            i += 1
            continue
        
        if current_section == 'documents' and line.startswith('- ['):
            link_match = re.search(r'\[([^\]]+)\]\(([^\)]+)\)', line)
            if link_match:
                doc_title = link_match.group(1)
                doc_url = link_match.group(2)
                current_project['documents'].append({
                    'title': doc_title,
                    'url': doc_url
                })
        
        if current_section == 'etapas' and line.startswith('- ['):
            etapa_match = re.search(r'\[([^\]]+)\]\s*(.+)', line)
            if etapa_match:
                etapa_date = etapa_match.group(1)
                etapa_desc = etapa_match.group(2).strip()
                current_project['etapas'].append({
                    'date': etapa_date,
                    'description': etapa_desc
                })
        
        i += 1
    
    if current_project:
        projects.append(current_project)
    
    return update_date or 'Data não especificada', projects

def get_status_badge_class(status: str) -> str:
    status_map = {
        'Em execução': 'bg-success',
        'Não iniciado': 'bg-secondary',
        'On-hold': 'bg-warning',
        'On hold': 'bg-warning',
        'Finalizado': 'bg-info'
    }
    return status_map.get(status, 'bg-secondary')

def generate_project_html(project: Dict, index: int) -> str:
    project_id = index + 1
    status_class = get_status_badge_class(project['status'])
    
    actors_html = ''
    if project['actors']:
        actors_badges = ''.join([
            f'<span class="badge actor-badge tag-badge">{escape(actor)}</span>'
            for actor in project['actors']
        ])
        actors_html = f'''
                        <div class="project-detail-item">
                            <span class="project-detail-label">Atores envolvidos:</span>
                            <div class="actors-container">
                                {actors_badges}
                            </div>
                        </div>'''
    
    documents_html = ''
    if project['documents']:
        doc_items = ''.join([
            f'<li><a href="{escape(doc["url"])}" target="_blank">{escape(doc["title"])}</a></li>'
            for doc in project['documents']
        ])
        documents_html = f'''
                        <div class="section-title">Documentos</div>
                        <ul class="documents-list">
                            {doc_items}
                        </ul>'''
    
    etapas_html = ''
    if project['etapas']:
        etapa_items = ''.join([
            f'<li>[{escape(etapa["date"])}] {escape(etapa["description"])}</li>'
            for etapa in project['etapas']
        ])
        etapas_html = f'''
                        <div class="section-title">Etapas</div>
                        <ul class="etapas-list">
                            {etapa_items}
                        </ul>'''
    
    description_html = ''
    if project['description']:
        description_html = f'''
                        <div class="project-detail-item">
                            <span class="project-detail-label">Descrição:</span>
                            <span>{escape(project['description'])}</span>
                        </div>'''
    
    return f'''            <!-- {escape(project['name'])} -->
            <div class="accordion-item" data-pm="{escape(project['pm'])}" data-status="{escape(project['status'])}">
                <h2 class="accordion-header" id="heading{project_id}">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{project_id}" aria-expanded="false" aria-controls="collapse{project_id}">
                        <div class="project-header w-100">
                            <span class="project-name">{escape(project['name'])}</span>
                            <div class="project-meta">
                                <span class="badge {status_class} status-badge">{escape(project['status'])}</span>
                                <span class="badge pm-badge tag-badge">{escape(project['pm'])}</span>
                            </div>
                        </div>
                    </button>
                </h2>
                <div id="collapse{project_id}" class="accordion-collapse collapse" aria-labelledby="heading{project_id}" data-bs-parent="#projetosAccordion">
                    <div class="accordion-body">
                        {description_html}
                        <div class="project-detail-item">
                            <span class="project-detail-label">Status:</span>
                            <span class="badge {status_class}">{escape(project['status'])}</span>
                        </div>
                        <div class="project-detail-item">
                            <span class="project-detail-label">Project Manager:</span>
                            <span class="badge pm-badge tag-badge">{escape(project['pm'])}</span>
                        </div>
                        {actors_html}
                        <div class="project-detail-item">
                            <span class="project-detail-label">Prazo:</span>
                            <span>{escape(project['deadline'])}</span>
                        </div>
                        <div class="project-detail-item">
                            <span class="project-detail-label">Processo SEI:</span>
                            <span>{escape(project['sei_process']) if project['sei_process'] else '-'}</span>
                        </div>
                        {documents_html}
                        {etapas_html}
                    </div>
                </div>
            </div>'''

def read_html_template() -> str:
    html_file = Path('index.html')
    if not html_file.exists():
        raise FileNotFoundError('index.html não encontrado. É necessário ter o arquivo HTML como template.')
    
    with open(html_file, 'r', encoding='utf-8') as f:
        return f.read()

def generate_html(update_date: str, projects: List[Dict], template_html: str) -> str:
    projects_html = '\n'.join([generate_project_html(project, i) for i, project in enumerate(projects)])
    
    accordion_start_pattern = r'(<div class="accordion" id="projetosAccordion">)'
    accordion_end_pattern = r'(</div>\s*</div>\s*</main>)'
    
    accordion_start_match = re.search(accordion_start_pattern, template_html)
    accordion_end_match = re.search(accordion_end_pattern, template_html)
    
    if accordion_start_match and accordion_end_match:
        start_pos = accordion_start_match.end()
        end_pos = accordion_end_match.start()
        
        new_html = (
            template_html[:start_pos] +
            '\n' + projects_html + '\n' +
            template_html[end_pos:]
        )
    else:
        print('Aviso: Não foi possível encontrar a seção de projetos. Gerando HTML completo...')
        new_html = template_html
    
    update_date_pattern = r'Data de atualização: \d{2}/\d{2}/\d{4}'
    new_html = re.sub(update_date_pattern, f'Data de atualização: {update_date}', new_html)
    
    return new_html

def main():
    md_file = Path('Status Report COST.md')
    if not md_file.exists():
        print(f'Erro: Arquivo {md_file} não encontrado.')
        return
    
    print(f'Lendo arquivo {md_file}...')
    update_date, projects = parse_markdown_file(str(md_file))
    
    print(f'Encontrados {len(projects)} projetos.')
    print(f'Data de atualização: {update_date}')
    
    print('Lendo template HTML...')
    template_html = read_html_template()
    
    print('Gerando HTML...')
    html_output = generate_html(update_date, projects, template_html)
    
    output_file = Path('index.html')
    print(f'Escrevendo arquivo {output_file}...')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_output)
    
    print('Conversão concluída!')

if __name__ == '__main__':
    main()

