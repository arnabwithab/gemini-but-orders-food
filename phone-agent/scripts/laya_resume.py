import json, time, sys, urllib.request, urllib.error

sys.path.insert(0, "/tmp/opencode")
from laya_cmp import BATTERY, MODELS, KEY, URL

WANT = [
    ("tap_target", "convaiinnovations/laya"),
    ("toggle_op", "convaiinnovations/laya-free"),
    ("toggle_op", "convaiinnovations/laya"),
    ("done_check", "convaiinnovations/laya-free"),
    ("done_check", "convaiinnovations/laya"),
]


def ask(model, state, questions):
    body = json.dumps({"state": state, "questions": questions}).encode()
    req = urllib.request.Request(
        URL,
        data=body,
        headers={
            "Authorization": f"Bearer {KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "ai-gateway-protocol-version": "0.0.1",
            "ai-evaluation-model-specification-version": "4",
            "ai-model-id": model,
        },
    )
    t = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return time.perf_counter() - t, json.load(r), None
    except urllib.error.HTTPError as e:
        return time.perf_counter() - t, None, f"HTTP {e.code}"
    except Exception as e:
        return time.perf_counter() - t, None, str(e)[:100]


for name, m in WANT:
    b = BATTERY[name]
    for attempt in range(6):
        dt, res, err = ask(m, b["state"], b["questions"])
        if err == "HTTP 429":
            time.sleep(45)
            continue
        break
    if err:
        print(f"{name} {m.split('/')[-1]}: ERROR {err}", flush=True)
    else:
        conf = (
            (res.get("providerMetadata") or {})
            .get("typesafe", {})
            .get("confidence", {})
        )
        out = []
        for qid, a in res.get("answers", {}).items():
            if a.get("type") == "boolean":
                out.append(f"{qid}={a.get('probability')}")
            else:
                probs = a.get("probabilities", {})
                top = sorted(probs.items(), key=lambda kv: -kv[1])[:2]
                out.append(
                    f"{qid}={a.get('choice')} conf={conf.get(qid,'n/a')} "
                    + str([(k, round(v, 2)) for k, v in top])
                )
        print(f"{name} {m.split('/')[-1]}: {dt:.2f}s | " + " ; ".join(out), flush=True)
    time.sleep(20)
