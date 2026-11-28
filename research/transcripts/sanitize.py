"""Export sanitized agent transcripts for reproducibility.

Keeps only the research-relevant content of Claude Code session logs:
user / assistant text, tool calls (name + input) and tool results (truncated),
with timestamps and model ids. Drops system prompts, hook output, attachments,
images, internal bookkeeping records and hidden reasoning blocks. Redacts
personal data (email addresses) and anything that looks like a credential.

Usage: python3 sanitize.py <projects_dir> <out_dir>
Writes one gzipped JSONL per session / subagent and an index.json.
"""
import gzip
import json
import os
import re
import sys

MAX_RESULT = 4000
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
SECRET = re.compile(r"\b(?:ghp_|gho_|github_pat_|sk-ant-)[A-Za-z0-9_-]{8,}|\bsk-[A-Za-z0-9]{24,}|Bearer\s+[A-Za-z0-9._-]{16,}")
# keep the public GitHub noreply commit address used as the contributor identity
# private account identifiers (local part of the private email), never the public handle
PRIV = re.compile(r"lenguyen\d{7,}")
KEEP = {"120765515+lenguyen259@users.noreply.github.com", "noreply@anthropic.com"}


def clean(s):
    if not isinstance(s, str):
        s = json.dumps(s, ensure_ascii=False)
    s = SECRET.sub("<redacted-secret>", s)
    s = PRIV.sub("<redacted-id>", s)
    return EMAIL.sub(lambda m: m.group(0) if m.group(0) in KEEP else "<redacted-email>", s)


def deep(x):
    if isinstance(x, str):
        return clean(x)
    if isinstance(x, list):
        return [deep(v) for v in x]
    if isinstance(x, dict):
        return {k: deep(v) for k, v in x.items()}
    return x


def blocks(content, role):
    out = []
    if isinstance(content, str):
        return [{"type": "text", "text": clean(content)}]
    for c in content or []:
        t = c.get("type")
        if t == "text":
            txt = c.get("text", "")
            if role == "user" and ("<system-reminder>" in txt and len(txt) > 20000):
                txt = txt[:2000] + " ...[long system reminder truncated]"
            out.append({"type": "text", "text": clean(txt)})
        elif t == "tool_use":
            out.append({"type": "tool_use", "name": c.get("name"), "input": deep(c.get("input", {}))})
        elif t == "tool_result":
            r = c.get("content")
            if isinstance(r, list):
                r = "\n".join(x.get("text", "[non-text content omitted]") for x in r if isinstance(x, dict))
            r = clean(r if r is not None else "")
            if len(r) > MAX_RESULT:
                r = r[:MAX_RESULT] + f" ...[truncated {len(r) - MAX_RESULT} chars]"
            out.append({"type": "tool_result", "is_error": c.get("is_error", False), "content": r})
        # thinking, redacted_thinking, image, document: dropped
    return out


def export(src, dst):
    n = 0
    with open(src) as f, gzip.open(dst, "wt", encoding="utf-8") as g:
        for line in f:
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if d.get("type") not in ("user", "assistant"):
                continue
            m = d.get("message") or {}
            b = blocks(m.get("content"), m.get("role"))
            if not b:
                continue
            rec = {"t": d.get("timestamp"), "role": m.get("role"), "model": m.get("model"), "content": b}
            g.write(json.dumps(rec, ensure_ascii=False) + "\n")
            n += 1
    return n


def main(root, out):
    os.makedirs(out, exist_ok=True)
    index = []
    for proj in sorted(os.listdir(root)):
        pdir = os.path.join(root, proj)
        if not os.path.isdir(pdir):
            continue
        for name in sorted(os.listdir(pdir)):
            if name.endswith(".jsonl"):
                sid = name[:-6]
                n = export(os.path.join(pdir, name), os.path.join(out, f"session-{sid[:8]}-{proj.strip('-')}.jsonl.gz"))
                index.append({"kind": "session", "project": proj, "file": f"session-{sid[:8]}-{proj.strip('-')}.jsonl.gz", "records": n})
                sub = os.path.join(pdir, sid, "subagents")
                if os.path.isdir(sub):
                    for a in sorted(os.listdir(sub)):
                        if not a.endswith(".jsonl"):
                            continue
                        aid = a[:-6]
                        meta = {}
                        mp = os.path.join(sub, aid + ".meta.json")
                        if os.path.exists(mp):
                            meta = json.load(open(mp))
                        fn = f"{aid}.jsonl.gz"
                        n = export(os.path.join(sub, a), os.path.join(out, fn))
                        index.append({"kind": "subagent", "file": fn, "records": n,
                                      "description": clean(meta.get("description", "")),
                                      "model": meta.get("pickedEffortModel") or meta.get("model"),
                                      "effort": meta.get("effort")})
    json.dump(index, open(os.path.join(out, "index.json"), "w"), indent=1, ensure_ascii=False)
    print(len(index), "transcripts exported")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
