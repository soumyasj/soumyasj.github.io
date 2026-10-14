import json, os, subprocess, sys, io
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
FF='/mnt/lustre/work/kuehne/kqr828/.conda/lmms_eval/bin/ffmpeg'
FP='/mnt/lustre/work/kuehne/kqr828/.conda/lmms_eval/bin/ffprobe'
SRC='/mnt/lustre/work/kuehne/kqr828/WorkSpace/MMEvals/hf_release/meta_video_local'
OUT='/mnt/lustre/work/kuehne/kqr828/WorkSpace/MMEvals/lmms-eval-video-page/static/previews'
items=json.load(open('/mnt/lustre/work/kuehne/kqr828/WorkSpace/MMEvals/lmms-eval-video-page/static/data/metav_items.json'))
N,W,H=8,160,90
dur={}
for x in items: dur.setdefault(x['v'], x['d'])
def probe(p):
    try:
        r=subprocess.run([FP,'-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True,timeout=60)
        return float(r.stdout.strip())
    except Exception: return None
def grab(p,t):
    r=subprocess.run([FF,'-v','error','-ss',f'{t:.2f}','-i',p,'-frames:v','1','-vf',f'scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2','-f','image2pipe','-vcodec','mjpeg','-q:v','3','-'],capture_output=True,timeout=120)
    return Image.open(io.BytesIO(r.stdout)).convert('RGB') if r.stdout else None
def work(v):
    out=os.path.join(OUT, v.split('/',1)[1].rsplit('.',1)[0]+'.jpg')
    if os.path.exists(out): return v,'skip'
    p=os.path.join(SRC,v); d=probe(p) or dur[v] or 10
    strip=Image.new('RGB',(W*N,H),(20,20,20)); ok=0
    for i in range(N):
        t=d*(i+0.5)/N
        try: im=grab(p,t)
        except Exception: im=None
        if im is None and i>0: im=None
        if im is not None: strip.paste(im,(i*W,0)); ok+=1
    os.makedirs(os.path.dirname(out),exist_ok=True)
    strip.save(out,'JPEG',quality=78,optimize=True)
    return v,ok
vids=sorted(dur)
with ThreadPoolExecutor(int(sys.argv[1]) if len(sys.argv)>1 else 12) as ex:
    for i,(v,ok) in enumerate(ex.map(work,vids)):
        if i%50==0 or ok!=N and ok!='skip': print(i,v,ok,flush=True)
print('DONE',len(vids))
