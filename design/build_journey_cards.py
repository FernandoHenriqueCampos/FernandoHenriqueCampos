"""Four readable trajectory cards, using the approved Horizonte design tokens."""
import textwrap
from build_assets import svg, text, line, CYAN, MUTED

CARDS=[
    ('serratec','2025','Serratec','Residência em TIC',[
        'Formação imersiva Full Stack: seis meses em período integral, com projetos práticos e colaboração.',
        'Aplicações web e mobile, APIs, bancos de dados, versionamento e metodologias ágeis.',
        'Projeto final para uma empresa parceira: da compreensão da necessidade ao planejamento, desenvolvimento, integração e entrega.',
    ]),
    ('code-academy','2026','Code Academy','Instituto 3C',[
        'Revisão e consolidação de conhecimentos, aprofundamento de fundamentos e aprendizado de novas tecnologias.',
        'Vue.js, JavaScript, TypeScript, HTML, CSS, Git, GitHub e Docker.',
        'O contato com infraestrutura fortaleceu meu interesse por DevOps e por como aplicações são estruturadas, executadas e preparadas para diferentes ambientes.',
    ]),
    ('michelc','2026 — ATUAL','Michelc','Assessoria Contábil',[
        'Full Stack Trainee: criação, manutenção e evolução de sistemas internos; novas funcionalidades e correções em aplicações existentes.',
        'Atuação em necessidades, planejamento, arquitetura, interfaces, APIs, bancos de dados, autenticação, permissões, regras de negócio, testes e decisões técnicas.',
        'Automação fiscal com React, Next.js, FastAPI e PostgreSQL para reunir, analisar e calcular informações, reduzindo a intervenção manual.',
        'Em desenvolvimento: solução interna para organizar processos, fluxos, responsabilidades, informações e colaboração entre funcionários, com elementos de uma rede social corporativa.',
        'Da compreensão da operação à definição de requisitos e decisões de arquitetura tecnicamente viáveis.',
    ]),
    ('utfpr','2026 — ATUAL','UTFPR','Tecnologia em Sistemas para Internet',[
        'Graduação escolhida para aprofundar os conhecimentos que a prática profissional começou a exigir.',
        'Algoritmos, raciocínio computacional, fundamentos, arquitetura, bancos de dados, redes, infraestrutura e engenharia de software.',
        'Aprofundamento em DevOps para entender como sistemas funcionam, por que decisões técnicas são tomadas e como aplicações são executadas e mantidas.',
        'Uma base em tecnologia e engenharia que complementa a experiência prática, para ir além dos frameworks.',
    ]),
]

def icon(key,x,y):
    paths={
        'serratec':'<path d="M2 13 24 3 46 13 24 23Z M10 18v13q14 11 28 0V18 M46 13v22"/>',
        'code-academy':'<path d="m15 10-12 14 12 14 m18-28 12 14-12 14 M28 5 20 43"/>',
        'michelc':'<rect x="7" y="3" width="34" height="42" rx="2"/><path d="M16 12h4m8 0h4m-16 9h4m8 0h4m-16 9h4m8 0h4M20 45V36h8v9"/>',
        'utfpr':'<path d="M24 10Q14 3 3 7v33q11-4 21 3 10-7 21-3V7q-11-4-21 3v33 M10 16l7 2m14 0 7-2M10 25l7 2m14 0 7-2"/>',
    }
    return f'<g transform="translate({x} {y})" fill="none" stroke="{CYAN}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{paths[key]}</g>'

def build(card,mobile):
    key,year,title,subtitle,paragraphs=card
    w=720 if mobile else 1440
    m=40 if mobile else 80
    b=icon(key,m,42)+text(m+72,71,year,19,CYAN,spacing=1,family='mono')
    b+=text(m,139,title,39,spacing=-1)
    for i,row in enumerate(textwrap.wrap(subtitle,width=36 if mobile else 29)):
        b+=text(m,181+i*31,row,25 if mobile else 22,MUTED)
    y=250 if mobile else 66
    if not mobile: b+=line(435,44,435,220)
    x=m if mobile else 480
    if key=='michelc':
        b+=text(x,y,'APROX. 90 MIN → ATÉ 10 MIN',25,CYAN)
        y+=54
    for paragraph in paragraphs:
        for row in textwrap.wrap(paragraph,width=46 if mobile else 72):
            b+=text(x,y,row,26 if mobile else 25)
            y+=36
        y+=20
    h=max(y+30,300 if not mobile else 350)
    b+=line(m,h-22,w-m,h-22)
    desc=year+' · '+title+' · '+subtitle+'. '+('Impacto fiscal: aprox. 90 min → até 10 min. ' if key=='michelc' else '')+' '.join(paragraphs)
    svg('journey-'+key+('-mobile' if mobile else ''),w,h,title+' — '+year,desc,b)

if __name__=='__main__':
    for card in CARDS:
        for mobile in (False,True): build(card,mobile)
