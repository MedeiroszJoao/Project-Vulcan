"""Capture public source bytes and receipts; blocked responses stay explicit.
Run from project root. Network required. Never treats search snippets as originals.
"""
import csv,json,hashlib
from datetime import datetime,timezone
from pathlib import Path
from urllib.request import Request,urlopen
from concurrent.futures import ThreadPoolExecutor

EXTRA={
 'northrop_q1':'https://www.sec.gov/Archives/edgar/data/1133421/000113342126000016/noc-20260331.htm',
 'northrop_q2':'https://www.sec.gov/Archives/edgar/data/1133421/000113342126000034/noc-20260630.htm',
 'northrop_q2_mirror':'https://investor.northropgrumman.com/node/44221/html',
 'gps_swap':'https://www.ssc.spaceforce.mil/DesktopModules/ArticleCS/Print.aspx?Article=4439687&ModuleId=705&PortalId=3',
 'lv01_calendar':'https://nextspaceflight.com/launches/details/7425/',
 'centaur_leo':'https://blog.ulalaunch.com/blog/vulcan-wet-dress-rehearsal-planned',
 'zenodo_enable':'https://help.zenodo.org/docs/github/enable-repository/',
 'zenodo_release':'https://help.zenodo.org/docs/github/archive-software/github-upload/',
 'evsi_tutorial':'https://pmc.ncbi.nlm.nih.gov/articles/PMC8793320/',
 'pgmpy':'https://pgmpy.org/api/generated/inference/pgmpy.inference.VariableElimination.html'
}

def capture(item):
    name,url=item
    rec={'id':name,'url':url,'retrieved_utc':datetime.now(timezone.utc).isoformat()}
    try:
        with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0 (public academic source verification)'}),timeout=18) as resp:
            raw=resp.read();rec.update(http_status=resp.status,final_url=resp.url,
                                      content_type=resp.headers.get('Content-Type',''))
        # Receipt can prove byte identity, not content truth or independent timestamp.
        rec.update(sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw))
        text=raw.decode('utf-8',errors='ignore').lower()
        block=any(x in text for x in ['checking your browser','verify you are human','request rate threshold exceeded','access denied'])
        rec['status']='blocked_content' if block else 'captured_unreviewed'
        path=Path('evidence/raw')/(name+'.html');path.parent.mkdir(exist_ok=True)
        path.write_bytes(raw);rec['local_path']=str(path)
    except Exception as e:
        rec.update(status='capture_failed',error=str(e)[:250])
    return rec

def main():
    urls={}
    for f in ['vulcan_flights','atlas_gem63','vega_timeline']:
        for i,row in enumerate(csv.DictReader(open('data/'+f+'.csv'))):
            urls.setdefault(row['source'],f+'_'+str(i+1))
    for name,url in EXTRA.items(): urls.setdefault(url,name)
    with ThreadPoolExecutor(max_workers=6) as ex: rows=list(ex.map(capture,[(n,u) for u,n in urls.items()]))
    Path('evidence/source_manifest.json').write_text(json.dumps(rows,indent=2)+'\n')
    print(json.dumps([{'id':r['id'],'status':r['status']} for r in rows],indent=2))

if __name__=='__main__': main()
