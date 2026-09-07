"""Fetch public GitHub counters and render a dated, reproducible local snapshot.

Network failure raises before output is changed. No private endpoints or tokens.
Use --from-snapshot to render without network access.
"""
import argparse
import json
import urllib.request
import os
from datetime import datetime, timezone
from build_assets import ROOT, svg, text, line, label, MUTED, CYAN

USER='FernandoHenriqueCampos'
DATA=ROOT/'assets/horizonte/telemetry.json'

def get(url):
    headers={'Accept':'application/vnd.github+json','User-Agent':'Horizonte-profile','X-GitHub-Api-Version':'2022-11-28'}
    if os.environ.get('GITHUB_TOKEN'):
        headers['Authorization']='Bearer '+os.environ['GITHUB_TOKEN']
    request=urllib.request.Request(url,headers=headers)
    with urllib.request.urlopen(request,timeout=30) as response:
        return json.load(response)

def fetch():
    account_url=f'https://api.github.com/users/{USER}'
    account=get(account_url)
    if not isinstance(account,dict) or account.get('login','').lower()!=USER.lower() or type(account.get('public_repos')) is not int:
        raise ValueError('Invalid public account response')
    repos=[]; sources=[account_url]
    for page in range(1,101):
        url=f'{account_url}/repos?type=owner&per_page=100&page={page}'
        batch=get(url)
        if not isinstance(batch,list): raise ValueError('Invalid repository page')
        repos.extend(batch); sources.append(url)
        if len(batch)<100: break
    else: raise RuntimeError('Repository pagination limit reached')
    owned=[]
    for r in repos:
        if not isinstance(r,dict) or type(r.get('private')) is not bool or type(r.get('fork')) is not bool:
            raise ValueError('Missing repository visibility or fork status')
        if not isinstance(r.get('owner'),dict) or not isinstance(r['owner'].get('login'),str):
            raise ValueError('Missing repository owner')
        if r['owner']['login'].lower()!=USER.lower() or r['private']: continue
        if not isinstance(r.get('name'),str) or not r['name'] or type(r.get('stargazers_count')) is not int or r['stargazers_count']<0:
            raise ValueError('Invalid repository name or star count')
        owned.append(r)
    owned.sort(key=lambda r:r['name'].casefold())
    if len({r['name'].casefold() for r in owned})!=len(owned) or len(owned)!=account['public_repos']:
        raise ValueError('Incomplete or changing public repository listing; retry later')
    originals=[r for r in owned if not r['fork']]
    return {'username':USER,'collected_at':datetime.now(timezone.utc).isoformat(timespec='seconds'),'sources':sources,'public_repositories_including_forks':len(owned),'public_original_repositories':len(originals),'stars_on_public_original_repositories':sum(r['stargazers_count'] for r in originals),'repositories':[{'name':r['name'],'fork':r['fork'],'stars':r['stargazers_count']} for r in owned]}

def render(data):
    date=data['collected_at'][:16].replace('T',' ')+' UTC'
    values=[('REPOSITÓRIOS PÚBLICOS',data['public_repositories_including_forks'],'Incluindo forks'),('REPOSITÓRIOS ORIGINAIS',data['public_original_repositories'],'Públicos · sem forks'),('ESTRELAS RECEBIDAS',data['stars_on_public_original_repositories'],'Nos repositórios originais')]
    for mobile in (False,True):
        w,h=(720,890) if mobile else (1440,400)
        m=40 if mobile else 80
        b=label(w,'07','TELEMETRIA / GITHUB',mobile)
        b+=text(m,138,'Atividade pública, em números.',37 if mobile else 47,spacing=-1)
        for i,(name,value,scope) in enumerate(values):
            x,y=(40,220+i*194) if mobile else (80+i*440,214)
            b+=text(x,y,name,18,CYAN,family='mono')+text(x,y+76,str(value),68)
            b+=text(x,y+114,scope,25 if mobile else 22,MUTED)
            b+=line(x,y+141,x+(640 if mobile else 365),y+141)
        b+=text(m,h-26,f'COLETA / {date}',18,MUTED,family='mono')
        svg('telemetry'+('-mobile' if mobile else ''),w,h,'Telemetria pública do GitHub',f'Coleta em {date}. '+'. '.join(f'{name}: {value}. {scope}' for name,value,scope in values)+'. Snapshot de dados públicos, sem inferência de produtividade.',b)

def comparable(data):
    """Compare source facts, ignoring collection time and API ordering."""
    return {
        'username':data['username'],
        'public_repositories_including_forks':data['public_repositories_including_forks'],
        'public_original_repositories':data['public_original_repositories'],
        'stars_on_public_original_repositories':data['stars_on_public_original_repositories'],
        'repositories':sorted(data['repositories'],key=lambda r:r['name'].casefold()),
    }

def update(from_snapshot=False):
    previous=json.loads(DATA.read_text(encoding='utf-8')) if DATA.exists() else None
    data=previous if from_snapshot else fetch()
    if data is None: raise ValueError('No saved snapshot')
    if not from_snapshot and previous is not None and comparable(previous)==comparable(data):
        print('Public data unchanged; keeping SVGs, JSON and collection date.')
        return False
    render(data)
    if not from_snapshot: DATA.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Telemetry rendered from public collection: {data["collected_at"]}')
    return True

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--from-snapshot',action='store_true'); args=parser.parse_args()
    update(args.from_snapshot)
