"""Build the counterexample/circuit store for L-meta-612.

Reads every circuit dump of the 612 research (research folders + the scratchpad folders of earlier
sessions), verifies each circuit on all 2^n inputs against f_G, keeps only C4-free graphs,
deduplicates, and writes
  circuits.jsonl         curated core store (< ~5 MB): every circuit cited in a .md/.log file, the special
                         Petersen / config-(2) / uncertified / exact-minimum files, pinned refutation
                         witnesses (pins.json), all n >= 9 circuits, up to 40 minimum circuits per graph,
                         up to 80 circuits per (graph, slack) for subcubic non-pseudoforests, up to 40 per
                         (graph, slack) for subcubic graphs with n >= 8
  circuits_bulk.jsonl.gz all other unique verified circuits (SAT enumeration dumps, t3 fuzz pools)
  collect_report.json   per-source counts, dropped circuits with reasons

Usage: python3 -I collect.py [--no-bulk]
Light CPU: single process; run under nice.
"""
import sys, os, json, glob, re, gzip, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib612 import *

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.dirname(HERE)                       # .../L-meta-612
SCR = "/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad"

store = {}          # key -> record
order = []
report = {"sources": {}, "dropped": [], "non_c4free": 0}


def short(p):
    if p.startswith(RES):
        return "research/L-meta-612" + p[len(RES):]
    if p.startswith(SCR):
        return "scratch" + p[len(SCR):]
    return p


def add(C, src, E=None, name=None, tag=None, bulk=False):
    st = report["sources"].setdefault(re.split(r'[#:]', src)[0], {"read": 0, "kept_new": 0, "dup": 0, "dropped": 0})
    st["read"] += 1
    try:
        Eg = graph_of_circuit(C)
    except Exception as ex:  # malformed
        Eg = None
    if Eg is None:
        st["dropped"] += 1
        if len(report["dropped"]) < 400:
            report["dropped"].append({"src": src, "reason": "not an edge function f_G", "c": C.to_str()})
        return None
    if E is not None:
        En = norm_edges(E)
        if En != norm_edges(Eg):
            st["dropped"] += 1
            if len(report["dropped"]) < 400:
                report["dropped"].append({"src": src, "reason": "computes f_G of a different graph than stated",
                                          "stated": En, "computed": Eg, "c": C.to_str()})
            return None
    if not Eg:
        st["dropped"] += 1
        return None
    if not is_c4free(C.n, Eg):
        report["non_c4free"] += 1
        st["dropped"] += 1
        return None
    k = circuit_key(C, Eg)
    if k in store:
        r = store[k]
        st["dup"] += 1
        if len(r["sources"]) < 3 and src not in r["sources"]:
            r["sources"].append(src)
        r["n_sources"] += 1
        if name and not r.get("gname"):
            r["gname"] = name
        if tag and tag not in r["tags"]:
            r["tags"].append(tag)
        if not bulk and r["tier"] == "bulk":
            r["tier"] = "core"
        return r
    st["kept_new"] += 1
    gc = GraphCtx(C.n, Eg)
    R = red(C)
    r = {
        "n": C.n, "edges": [list(e) for e in norm_edges(Eg)], "gname": name or "",
        "E": len(gc.E), "tau": gc.tau, "phi": gc.phi,
        "gates": C.to_json(), "out": C.out, "size": C.size, "n_and": C.n_and(), "n_or": C.n_or(),
        "slack": C.size - gc.phi,
        "red_size": R.size, "red_and": R.n_and(), "red_or": R.n_or(), "reduced": R.size == C.size,
        "cls": graph_class(C.n, Eg), "sources": [src], "n_sources": 1, "tags": [tag] if tag else [],
        "tier": "bulk" if bulk else "core",
    }
    r["key"] = k
    r["_rstr"] = gkey(C.n, Eg) + "|" + R.to_str()
    store[k] = r
    order.append(k)
    return r


# ------------------------------------------------------------------ structured sources
def dumps():
    for d in ["s_case/circs", "tf/circs", "nf/circs", "lemDa/circs"]:
        for p in sorted(glob.glob(os.path.join(SCR, d, "*.json"))):
            D = json.load(open(p))
            E = D["E"]
            n = D["n"]
            for i, c in enumerate(D["circs"]):
                try:
                    C = from_indexed(c, n)
                except Exception as ex:
                    report["dropped"].append({"src": short(p), "reason": "parse: %s" % ex})
                    continue
                add(C, "%s#%d" % (short(p), i), E=E, tag="dump-X%s" % D.get("X", "?"))


def jsonl_pool(p, bulk=False, tag=None):
    op = open
    with op(p) as f:
        for i, line in enumerate(f):
            if not line.strip():
                continue
            r = json.loads(line)
            try:
                C = parse_str(r["c"])
            except Exception as ex:
                report["dropped"].append({"src": short(p), "reason": "parse: %s" % ex})
                continue
            add(C, "%s#%d" % (short(p), i), E=r.get("E"), name=r.get("g"), tag=tag, bulk=bulk)


def misc_json():
    # t8 uncertified circuits
    p = os.path.join(SCR, "t8/unc157.json")
    if os.path.exists(p):
        for i, r in enumerate(json.load(open(p))):
            add(parse_str(r["c"]), "%s#%d" % (short(p), i), E=r["E"], name=r.get("g"), tag="t8-uncertified")
    p = os.path.join(SCR, "t10/ex1_stuck.json")
    if os.path.exists(p):
        for i, r in enumerate(json.load(open(p))):
            add(parse_str(r[1]), "%s#%d" % (short(p), i), E=r[0], tag="t10-exchange-stuck")
    # indexed lists, graph derived from the circuit
    for p in [os.path.join(RES, "petersen/data/or13.json"), os.path.join(RES, "petersen/data/gad.json"),
              os.path.join(RES, "petersen/data/init27.json"), os.path.join(SCR, "pet19/C13.json"),
              os.path.join(SCR, "pet19/U.json")]:
        if not os.path.exists(p):
            continue
        d = json.load(open(p))
        if not d:
            continue
        if isinstance(d[0][0], str):     # [op,a,b] list, n = 10 (Petersen)
            C = Circ(10, [(o, a, b) for o, a, b in d])
        else:
            C = from_indexed(d, 10)
        add(C, short(p), name="Petersen", tag="petersen")
    for p in sorted(glob.glob(os.path.join(RES, "petersen19/known*.json"))):
        d = json.load(open(p))
        add(Circ(10, [(o, a, b) for o, a, b in d]), short(p), name="Petersen", tag="petersen19")
    p = os.path.join(RES, "petersen19/pool20.json")
    for i, d in enumerate(json.load(open(p))):
        add(Circ(10, [(o, a, b) for o, a, b in d]), "%s#%d" % (short(p), i), name="Petersen", tag="petersen19")
    # s612 exact minimum circuits (named small graphs)
    p = os.path.join(SCR, "s612/results.jsonl")
    if os.path.exists(p):
        for i, line in enumerate(open(p)):
            r = json.loads(line)
            res = r.get("res") or {}
            if not res.get("gates"):
                continue
            C = Circ(r["n"], [({'AND': '&', 'OR': '|'}[o], a, b) for o, a, b in res["gates"]])
            add(C, "%s#%d" % (short(p), i), E=r["E"], name=r.get("name"), tag="exact-min")


# ------------------------------------------------------------------ text extraction (md / txt / log)
CRE = re.compile(r'(?:\d+\s*=\s*x?\d+\s*[|&]\s*x?\d+[\s,;]*){1,}')
NAME_RE = re.compile(r'^\s*([A-Za-z][\w+\-{}]*)\s')


def text_sources():
    files = []
    for ext in ("md", "txt", "log"):
        files += glob.glob(os.path.join(RES, "**", "*." + ext), recursive=True)
        files += glob.glob(os.path.join(SCR, "**", "*." + ext), recursive=True)
    files = [f for f in files if "/ledger/" not in f and "/gct/" not in f and "/site/" not in f
             and "/petersen19/cnf" not in f]
    seen = set()
    for p in sorted(set(files)):
        try:
            txt = open(p, errors="replace").read()
        except Exception:
            continue
        if os.path.getsize(p) > 20_000_000:
            continue
        txt = txt.replace("\\|", "|")
        is_md = p.endswith(".md")
        found = []   # [line, string, first gate no, last gate no]
        for ln, line in enumerate(txt.split("\n"), 1):
            for m in CRE.finditer(line):
                s = m.group(0)
                nums = [int(x) for x in re.findall(r'(\d+)\s*=', s)]
                if not nums:
                    continue
                # a circuit wrapped over two lines: join when the gate numbering continues
                if found and found[-1][0] == ln - 1 and nums[0] == found[-1][3] + 1:
                    found[-1][1] += " " + s
                    found[-1][0] = ln
                    found[-1][3] = nums[-1]
                    continue
                found.append([ln, s, nums[0], nums[-1]])
        for ln, s, _, _ in found:
            try:
                C = parse_str(s)
            except Exception:
                continue
            if C.size < 3:
                continue
            tag = "md-witness" if is_md else "log"
            add(C, "%s:%d" % (short(p), ln), tag=tag)


def main():
    t0 = time.time()
    text_sources()
    print("text done", len(store), round(time.time() - t0, 1), flush=True)
    misc_json()
    for name in ["cex2", "cex4", "sl2", "starpool", "starpool2"]:
        jsonl_pool(os.path.join(SCR, "t3/%s.jsonl" % name), tag="t3-" + name)
    for name in ["pool", "pool2"]:
        jsonl_pool(os.path.join(SCR, "t5/%s.jsonl" % name), tag="t5-config2")
    print("misc done", len(store), round(time.time() - t0, 1), flush=True)
    dumps()
    print("dumps done", len(store), round(time.time() - t0, 1), flush=True)
    jsonl_pool(os.path.join(SCR, "t3/locpool.jsonl"), tag="t3-locpool")
    jsonl_pool(os.path.join(SCR, "t3/pool_net.jsonl"), tag="t3-pool_net")
    print("pools done", len(store), round(time.time() - t0, 1), flush=True)
    if "--no-bulk" not in sys.argv:
        jsonl_pool(os.path.join(SCR, "t3/pool_ML.jsonl"), bulk=True, tag="t3-pool_ML")
        print("bulk done", len(store), round(time.time() - t0, 1), flush=True)

    # ---- curation: a compact core store (< ~5 MB) and the gzipped bulk store
    CUR_TAGS = {"md-witness", "log", "petersen", "petersen19", "t5-config2", "t8-uncertified",
                "t10-exchange-stuck", "t3-cex2", "t3-cex4", "t3-sl2", "t3-starpool", "t3-starpool2", "exact-min"}
    pins = set()
    pp = os.path.join(HERE, "pins.json")
    if os.path.exists(pp):
        for d in json.load(open(pp)):
            pins.add(gkey(d["n"], [tuple(e) for e in d["edges"]]) + "|" + d["circuit"])
    recs = list(store.values())
    recs.sort(key=lambda r: (r["n"], r["E"], r["size"], r["key"]))
    per_min = {}
    per_sub = {}
    for r in recs:
        g = gkey(r["n"], r["edges"])
        c = r["cls"]
        core = bool(CUR_TAGS & set(r["tags"])) or r["_rstr"] in pins or r["n"] >= 9
        if r["_rstr"] in pins and "pinned-witness" not in r["tags"]:
            r["tags"].append("pinned-witness")
        if not core and r["slack"] <= 0:                       # minimum (or below-Phi) circuits
            per_min[g] = per_min.get(g, 0) + 1
            core = per_min[g] <= 40
        if not core and c["subcubic"] and not c["pseudoforest"]:  # subcubic, not covered by PF
            k2 = (g, r["slack"])
            per_sub[k2] = per_sub.get(k2, 0) + 1
            core = per_sub[k2] <= 80
        if not core and c["subcubic"] and r["n"] >= 8:          # larger subcubic graphs (partial suns, n8)
            k2 = (g, r["slack"], "big")
            per_sub[k2] = per_sub.get(k2, 0) + 1
            core = per_sub[k2] <= 40
        r["tier"] = "core" if core else "bulk"
    nc = nb = 0
    with open(os.path.join(HERE, "circuits.jsonl"), "w") as fc, \
            gzip.open(os.path.join(HERE, "circuits_bulk.jsonl.gz"), "wt") as fb:
        for r in recs:
            r.pop("key", None)
            r.pop("_rstr", None)
            r["sources"] = r["sources"][:2]
            if r["tier"] == "core":
                nc += 1
                r["id"] = "c%06d" % nc
                fc.write(json.dumps(r, separators=(",", ":")) + "\n")
            else:
                nb += 1
                r["id"] = "b%06d" % nb
                fb.write(json.dumps(r, separators=(",", ":")) + "\n")
    report["n_core"] = nc
    report["n_bulk"] = nb
    report["seconds"] = round(time.time() - t0, 1)
    json.dump(report, open(os.path.join(HERE, "collect_report.json"), "w"), indent=1)
    print("core", nc, "bulk", nb, "non-C4-free skipped", report["non_c4free"],
          "dropped", sum(s["dropped"] for s in report["sources"].values()))


if __name__ == "__main__":
    main()
