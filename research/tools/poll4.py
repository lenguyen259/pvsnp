import json,subprocess,time,sys,datetime
SC='/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad'
def sh(*a): return subprocess.run(a,capture_output=True,text=True).stdout
def log(m):
    open(SC+'/poll.log','a').write(datetime.datetime.utcnow().strftime('%H:%M:%S ')+m+'\n')
for i in range(400):
    raw=''
    for q in ('&kind=value&value=1','&kind=refute','&kind=search',''):
        raw=sh('curl','-s','-m','30','https://pequalnp.com/desk/next?handle=lenguyen259&another=1'+q)
        try:
            if json.loads(raw).get('gap'): break
        except Exception: pass
    try: d=json.loads(raw)
    except Exception: time.sleep(120); continue
    g=d.get('gap')
    if not g:
        time.sleep(max(120,int(d.get('retry_after_s',300)))); continue
    t=d['lease'].get('terms',{}); kind=t.get('kind'); lvl=t.get('level')
    title=(g.get('title') or g.get('statement',''))[:160].replace('\n',' ')
    if kind=='cut':
        r=sh('curl','-s','-m','30','-X','POST',d['lease']['release'].split(' ',1)[1].replace('<submitted|hypothesis_too_weak|missing_lemma|statement_seems_false|does_not_elaborate|exhausted|rechecked|recheck_failed|reduced|out_of_time|other>','other') if False else 'https://pequalnp.com/desk/release?lease=%s&reason=other'%d['lease']['id'])
        open(SC+'/autorel.jsonl','a').write(json.dumps(dict(gap=g['id'],t=datetime.datetime.utcnow().isoformat(),kind=kind,level=lvl,points=t.get('points'),title=title))+'\n')
        log('AUTO-RELEASED %s kind=%s level=%s'%(g['id'],kind,lvl)); time.sleep(20); continue
    json.dump(d,open(SC+'/poll_got.json','w')); log('GOT %s kind=%s level=%s (manual)'%(g['id'],kind,lvl)); sys.exit(0)
log('gave up'); sys.exit(1)
