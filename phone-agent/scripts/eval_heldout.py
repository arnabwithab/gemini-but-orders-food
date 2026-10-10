import json, sys
import laya

agent = laya.load("phone-agent/checkpoints/ac-v1-head", device="cuda")
tot = right = 0
by_q = {}
for line in open("phone-agent/data/eval.jsonl"):
    row = json.loads(line)
    ans = agent.predict(row["state"], row["questions"])["answers"]
    for qid, exp in row["expected"].items():
        a = ans[qid]
        got = a.get("choice") if a["type"] == "choice" else (a.get("noul", 0) >= 0.5)
        ok = (got == exp)
        tot += 1; right += ok
        k = f"{qid}:{a['type']}"
        s = by_q.setdefault(k, [0, 0]); s[1] += 1; s[0] += ok
print(f"OVERALL {right}/{tot} = {right/tot:.3f}")
for k, (r, t) in sorted(by_q.items()):
    print(f"{k}: {r}/{t} = {r/t:.3f}")
