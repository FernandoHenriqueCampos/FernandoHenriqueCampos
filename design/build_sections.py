"""Extend the approved Horizonte system without regenerating approved artwork."""
from build_assets import svg, text, line, label, WHITE, MUTED, CYAN

def header(name,number,title):
    for mobile in (False,True):
        w=720 if mobile else 1440
        b=label(w,number,title,mobile)
        svg(name+('-mobile' if mobile else ''),w,100,title,title,b)

def focus(mobile):
    w,h=(720,350) if mobile else (1440,205)
    rows=[('FOCUS','Full Stack · APIs · Automação'),('APPROACH','Problema → sistema → impacto'),('NOW','Systems · Architecture · DevOps')]
    b=''
    for i,(title,value) in enumerate(rows):
        x,y=(40,65+i*100) if mobile else (80+i*440,65)
        b+=text(x,y,title,18,CYAN,spacing=2,family='mono')
        b+=text(x,y+44,value,27 if mobile else 24)
        b+=line(x,y+64,x+(600 if mobile else 365),y+64)
    svg('focus'+('-mobile' if mobile else ''),w,h,'Foco, abordagem e estudos','Full Stack, APIs e automação. Problema → sistema → impacto. Systems, Architecture e DevOps.',b)

def projects(mobile):
    w,h=(720,840) if mobile else (1440,505)
    b=label(w,'05','PROJETOS',mobile)
    b+=text(40 if mobile else 80,137,'Software em contexto.',39 if mobile else 47,spacing=-1)
    items=[('PÚBLICO / EM EQUIPE','Adote Já',['Aplicativo React Native para','adoção e cuidados com pets.','Autenticação · adoção · shopping.']),('MICHELC / EM DESENVOLVIMENTO','Processos internos',['Organização de processos, fluxos,','informações e responsabilidades.','Colaboração entre funcionários.'])]
    for i,(status,name,rows) in enumerate(items):
        x,y=(40,220+i*305) if mobile else (80+i*665,242)
        b+=text(x,y,status,17,CYAN,spacing=1,family='mono')+text(x,y+59,name,37)
        for j,row in enumerate(rows): b+=text(x,y+108+j*37,row,26,MUTED)
        b+=line(x,y+212,x+(640 if mobile else 590),y+212)
    svg('projects'+('-mobile' if mobile else ''),w,h,'Projetos — Adote Já e processos internos na Michelc','Adote Já: aplicativo React Native desenvolvido em equipe. Michelc: solução interna em desenvolvimento para organizar processos, fluxos, informações, responsabilidades e colaboração entre funcionários.',b)

def studies(mobile):
    w,h=(720,820) if mobile else (1440,500)
    b=label(w,'06','ATUALMENTE ESTUDANDO',mobile)
    b+=text(40 if mobile else 80,137,'Expandindo o horizonte.',39 if mobile else 47,spacing=-1)
    items=[('SAP',['ERP · processos empresariais','Sistemas corporativos']),('ARCHITECTURE / DEVOPS',['Infraestrutura · deployment','Observabilidade · ciclo de vida']),('FOUNDATIONS',['Algoritmos · engenharia de software','Bancos de dados · redes']),('ENGLISH',['Documentação · leitura','Comunicação'])]
    for i,(name,rows) in enumerate(items):
        x,y=(40,219+i*145) if mobile else (80+(i%2)*665,233+(i//2)*140)
        b+=text(x,y,name,20,CYAN,spacing=1,family='mono')
        for j,row in enumerate(rows): b+=text(x,y+43+j*34,row,26,MUTED)
        b+=line(x,y+100,x+(640 if mobile else 590),y+100)
    svg('exploration'+('-mobile' if mobile else ''),w,h,'Atualmente estudando','SAP: ERP, processos empresariais e sistemas corporativos. Arquitetura e DevOps: infraestrutura, deployment, observabilidade e ciclo de vida. Fundamentos: algoritmos, engenharia de software, bancos de dados e redes. Inglês: documentação, leitura e comunicação.',b)

def beyond(mobile):
    # An unnumbered interlude keeps the approved 08 / CONTATO footer intact.
    w,h=(720,300) if mobile else (1440,245)
    m=40 if mobile else 80
    b=line(m,52,m+24,52,CYAN)+text(m+38,58,'ALÉM DO CÓDIGO',17,CYAN,spacing=2,family='mono')
    b+=text(m,133,'Outros ritmos, novas perspectivas.',33 if mobile else 40,spacing=-1)
    if mobile:
        b+=text(m,190,'Xadrez · música e bateria · jogos',26,MUTED)+text(m,234,'Tecnologia · aprendizado contínuo',26,MUTED)
    else:
        b+=text(m,187,'Xadrez · música e bateria · jogos · tecnologia · aprendizado contínuo',26,MUTED)
    svg('beyond'+('-mobile' if mobile else ''),w,h,'Além do código','Xadrez, música e bateria, jogos, tecnologia, sistemas e aprendizado contínuo.',b)

if __name__=='__main__':
    header('about-heading','02','SOBRE MIM')
    for mobile in (False,True):
        focus(mobile); projects(mobile); studies(mobile); beyond(mobile)
    print('Generated complementary sections; approved SVGs untouched.')
