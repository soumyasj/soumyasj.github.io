# Derives the relative compute cost (seconds per question vs. the reference run) for every run of Table 2
# of the paper from the lmms-eval run logs (logs/all_runs.csv and the per-run *_results.json files), and
# writes k_cost.json; the cost arrays are pasted into the K data block of index.html.
import csv, json, re, os, statistics as st
LM='/mnt/lustre/work/kuehne/kqr828/WorkSpace/MMEvals/lmms-eval'
DS=['videomme','tempcompass_multi_choice','mvbench','longvideobench_val_v','metav']
FULLN={'videomme':2700,'tempcompass_multi_choice':1580,'mvbench':4000,'longvideobench_val_v':1337,'metav':1000}
def parse(name, task=''):
    c={'nf':None,'cap':None,'mp':602112,'eng':'hf','vr':'torchcodec','bs':1,'T':0.0,'jpg':False,'fps':False}
    m=re.search(r'_nf(\d+)_',name); c['nf']=int(m.group(1)) if m else None
    m=re.search(r'fps1_cap(\d+)',name)
    if m: c['fps']=True; c['cap']=int(m.group(1))
    m=re.search(r'_mp(\d+)',name); c['mp']=int(m.group(1)) if m else 602112
    if '_vllm_bi_' in name or 'vllmfix' in name: c['eng']='vllm_bi'
    elif '_vllm_' in name: c['eng']='vllm'
    m=re.search(r'_vr(decord|torchvision|torchcodec)',name); c['vr']=m.group(1) if m else 'torchcodec'
    m=re.search(r'_bs(\d+)',name); c['bs']=int(m.group(1)) if m else 1
    m=re.search(r'_t(\d)p(\d)_',name); c['T']=float(m.group(1)+'.'+m.group(2)) if m else 0.0
    if 'frames' in task or re.search(r'_frames\d+_',name): c['jpg']=True
    if 'fsrandom' in name or '_pp_' in name or '_black' in name: c['bad']=True
    return c
runs={d:[] for d in DS}
for r in csv.DictReader(open(LM+'/logs/all_runs.csv')):
    if 'Qwen2.5-VL-7B' not in r['model_name'] or not r['tree'].startswith('per_dataset_results'): continue
    t=r['tasks']; base=re.sub(r'_frames\d+$','',t)
    if base not in FULLN or base=='metav': continue
    if r['n_effective']!=str(FULLN[base]): continue
    sc=float(r['score'] or 'nan'); sc=sc*100 if sc<=1 else sc
    c=parse(r['run_dir'],t)
    if c.get('bad'): continue
    runs[base].append(dict(c, score=sc, secs=float(r['total_evaluation_time_seconds']), n=FULLN[base], run=r['run_dir']))
# extra runs from result JSONs: batch-invariant vLLM sweeps, .jpg full-set runs
import statistics
def jscore(ds, res):
    if ds=='videomme':
        for t,m in res.items():
            v=m.get('videomme_perception_score,none')
            if isinstance(v,(int,float)): return v
    if ds=='tempcompass_multi_choice':
        for t,m in res.items():
            v=m.get('avg_accuracy,none')
            if isinstance(v,(int,float)): return v
    if ds=='longvideobench_val_v':
        for t,m in res.items():
            v=m.get('lvb_acc,none')
            if isinstance(v,(int,float)): return v*100
    if ds=='mvbench':
        vals=[m['mvbench_accuracy,none'] for t,m in res.items() if isinstance(m.get('mvbench_accuracy,none'),(int,float)) and t!='mvbench' and not t.startswith('mvbench_frames')]
        if vals: return statistics.mean(vals)
        for t,m in res.items():
            v=m.get('mvbench_accuracy,none')
            if isinstance(v,(int,float)): return v
    return None
seen=set(r['run'] for d in runs for r in runs[d])
for p in open('extra_results.txt').read().split()+open('vmme_full_frames.txt').read().split():
    if 'meta_videobench' in p or 'smoke' in p or 'backup' in p: continue
    m=re.search(r'/(videomme|tempcompass_multi_choice|mvbench|longvideobench_val_v)(?:_full)?(?:_frames\d+)?/', p)
    if not m: continue
    ds=m.group(1)
    try: d=json.load(open(LM+'/'+p if not p.startswith('/') else p))
    except Exception: continue
    ns=d.get('n-samples',{}); n=sum(v.get('effective',0) for v in ns.values() if isinstance(v,dict))
    if n!=FULLN[ds]: continue
    sc=jscore(ds, d.get('results',{}))
    if sc is None: continue
    secs=d.get('total_evaluation_time_seconds')
    if not secs: continue
    run=[c for c in p.split('/') if 'Qwen2.5-VL-7B-Instruct_' in c and '_20' in c]
    if not run or run[0] in seen: continue
    seen.add(run[0])
    c=parse(run[0], run[0])
    if c.get('bad'): continue
    runs[ds].append(dict(c, score=float(sc), secs=float(secs), n=n, run=run[0]))
# meta-v
for p in open('metav_results.txt').read().split():
    if p.startswith('logs/backup') or 'smoke' in p or 'limit' in p: continue
    try: d=json.load(open(LM+'/'+p))
    except Exception: continue
    res=d.get('results',{}); task=list(res)[0] if res else ''
    sc=res.get(task,{}).get('meta_videobench_score')
    if sc is None: continue
    secs=d.get('total_evaluation_time_seconds')
    if not secs: continue
    ns=d.get('n-samples',{}); n=None
    for k,v in ns.items():
        if isinstance(v,dict) and v.get('effective'): n=(n or 0)+v['effective']
    if n and n!=1000: continue
    name='/'.join(p.split('/')[-3:])
    c=parse(name)
    if c.get('bad'): continue
    runs['metav'].append(dict(c, score=float(sc), secs=float(secs), n=1000, run=p))
print({d:len(v) for d,v in runs.items()})
K=json.load(open('k_table.json'))   # [{x:[...], series:[{name, rows:[[6 vals]]}]}]
def want(g, si, i, x):
    # returns a config matcher for group g, series si, x-label index i
    c={'nf':4,'cap':None,'mp':602112,'eng':'hf','vr':'torchcodec','bs':1,'T':0.0,'jpg':False,'fps':False}
    if g==0: c['eng']=['hf','vllm_bi'][si]; c['bs']=int(x)
    if g==1: c['jpg']=si==1; c['nf']=int(x)
    if g==2:
        if si==0: c['nf']=int(x)
        else: c['fps']=True; c['cap']=int(x); c['nf']=None
    if g==3: c['vr']=x
    if g==4: c['mp']=int(x.replace(',',''))
    if g==5: c['T']=float(x)
    return c
def match(ds, c, y):
    if ds=='metav' and c.get('eng')=='vllm_bi': c=dict(c, eng='vllm')  # the paper's Meta-V vLLM row is the plain vLLM sweep
    cand=[r for r in runs[ds] if all(r[k]==v for k,v in c.items())]
    if not cand and c.get('eng')=='vllm_bi': cand=[r for r in runs[ds] if all(r[k]==v for k,v in dict(c,eng='vllm').items())]
    if not cand: return None, []
    close=[r for r in cand if abs(r['score']-y)<=0.06]
    if not close:
        # seeds averaged in the paper (vLLM / temperature): accept cands whose mean is close
        m=st.mean(r['score'] for r in cand)
        close=cand if abs(m-y)<=0.35 else [min(cand,key=lambda r:abs(r['score']-y))]
    return st.mean(r['secs']/r['n'] for r in close), close
out=[]; missing=[]
base={}
for di,ds in enumerate(DS):
    b,_=match(ds, want(1,0,0,'4'), K[1]['series'][0]['rows'][0][di if di<4 else 5]); base[ds]=b
print('baseline s/item', base)
for g,k in enumerate(K):
    for si,s in enumerate(k['series']):
        s['cost']=[]; s['sitem']=[]
        for i,x in enumerate(k['x']):
            costs=[]; sitems=[]
            for di,ds in enumerate(DS):
                col=di if di<4 else 5
                y=s['rows'][i][col]
                sitem,cl=match(ds, want(g,si,i,x), y)
                if sitem is None: missing.append((g,si,x,ds)); costs.append(None); sitems.append(None); continue
                costs.append(sitem/base[ds]); sitems.append(sitem)
                dev=max(abs(r['score']-y) for r in cl)
                if dev>0.35: print(f'  loose match g{g} s{si} x={x} {ds}: paper {y} vs runs {[round(r["score"],2) for r in cl]}')
            # Avg. column (index 4): geometric mean of the four relative costs
            four=costs[:4]
            avg=(st.geometric_mean(four) if all(v is not None for v in four) else None)
            s['cost'].append(costs[:4]+[avg]+[costs[4]])
            s['sitem'].append(sitems[:4]+[None]+[sitems[4]])
print('missing', missing)
json.dump(K, open('k_cost.json','w'))
for g,k in enumerate(K):
    for s in k['series']:
        print(g, s['name'], [[round(v,2) if v else None for v in row] for row in s['cost']])
