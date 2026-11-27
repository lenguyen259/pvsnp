# auto_twolit.py: handle the current lease in poll_got.json when it is a "two-lit function on shared wires" step.
# exit 0 = handled (released: UNSAT => statement_seems_false) ; exit 3 = SAT FOUND (circuit saved, lease kept, heartbeat running: handle manually);
# exit 2 = not this family (handle manually) ; exit 4 = undecided in time budget (released other)
import json,re,subprocess,sys,os,time,threading,datetime
SC='/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad'
HERE=os.path.dirname(os.path.abspath(__file__))
d=json.load(open(SC+'/poll_got.json')); g=d['gap']; L=d['lease']['id']
st=g['statement']
FAM=None
if g['title'].startswith('The two-lit function'):
    FAM='two'
    m=re.search(r'Fin (\d+), C\.eval.*?\((\d+) : ℕ\)\.testBit',st); N=int(m.group(1)); mask=int(m.group(2)); K=int(re.search(r'C\.size ≤ (\d+)',st).group(1))
    mono='Monotone2' in st
elif g['title'].startswith('One-a-side promise') or g['title'].startswith('Table 1a'):
    FAM='rep'
    m=re.search(r'Fin (\d+)\)? \(?v?\s*:?\s*Fin (\d+)\)? => \((\d+) : ℕ\)\.testBit.*\) (\d+)\s*$',st.strip()); if m: NL,NR,mask,K=map(int,m.groups())
    else:
        m=re.search(r'fun u v : Fin (\d+) => \((\d+) : ℕ\)\.testBit.*\) (\d+)\s*$',st.strip()); NL=NR=int(m.group(1)); mask=int(m.group(2)); K=int(m.group(3))
    mono=True
else: sys.exit(2)
stop=False
def beat():
    while not stop:
        for _ in range(48):
            if stop: return
            time.sleep(5)
        subprocess.run(['curl','-s','-m','30','-X','POST','https://pequalnp.com/desk/beat?lease='+L],capture_output=True)
threading.Thread(target=beat,daemon=True).start()
def log(x): open(SC+'/poll.log','a').write(datetime.datetime.utcnow().strftime('%H:%M:%S ')+x+'\n')
if FAM=='two':
    env=dict(os.environ,NPTS=str(N)); args=['python3',HERE+'/syn3_tool.py',str(K),str(mask)]+(['mono'] if mono else [])
else:
    env=dict(os.environ); args=['python3',HERE+'/syn2_tool.py',str(K),str(mask),str(NL),str(NR)]
try: out=subprocess.run(args,capture_output=True,text=True,timeout=1500,env=env).stdout.strip()
except subprocess.TimeoutExpired: out='TIMEOUT'
def rel(reason): subprocess.run(['curl','-s','-m','30','-X','POST','https://pequalnp.com/desk/release?lease=%s&reason=%s'%(L,reason)],capture_output=True)
rec=dict(gap=g['id'],fam=FAM,mask=mask,K=K,out=out[:600])
open(SC+'/auto2lit.jsonl','a').write(json.dumps(rec)+'\n')
if out.startswith('UNSAT'):
    stop=True; rel('statement_seems_false'); log('AUTO2LIT %s UNSAT K=%d -> released false'%(g['id'],K)); sys.exit(0)
if out.startswith('SAT'):
    open(SC+'/auto2lit_SAT_%s.txt'%g['id'],'w').write(out); log('AUTO2LIT %s SAT FOUND K=%d (lease kept)'%(g['id'],K)); 
    subprocess.Popen(['setsid','sh',SC+'/beat2.sh',L],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True); sys.exit(3)
stop=True; rel('other'); log('AUTO2LIT %s undecided K=%d -> released other'%(g['id'],K)); sys.exit(4)
