import json, time, os, urllib.request

KEY = os.environ["VERCEL_AI_GATEWAY_KEY"]
URL = "https://ai-gateway.vercel.sh/v4/ai/evaluation-model"
MODELS = ["convaiinnovations/laya-free", "convaiinnovations/laya"]

# Probes shaped like jev-phone's real requests (goal + numbered screen menu).
BATTERY = {
    "app_select": {
        "state": "Goal: Open the Domino's app, open the menu, and navigate to the Chocolate Souffle item so it is visible on screen.\nScreen: Home screen.\napps: Settings, Contacts, Phone, Messages, Chrome, Calendar, Photos, Maps, YouTube, Play Store, Domino's",
        "questions": {
            "operation": {
                "type": "choice",
                "instructions": "Which operation moves the goal forward?",
                "criteria": {
                    "OPEN_APP Domino's": "open the Domino's app",
                    "OPEN_APP Calendar": "open the Calendar app",
                    "OPEN_APP Play Store": "open the Play Store app",
                    "OPEN_APP Phone": "open the Phone app",
                    "WAIT": "wait for the screen to settle",
                },
            },
        },
    },
    "in_app_op": {
        "state": "Goal: In the Domino's app, navigate to the Chocolate Souffle item so it is visible on screen.\nScreen: Domino's home.\ncontrols: [1] Button Search for [2] Cell Farmhouse pizza [3] Cell Margherita [4] Button Menu [5] Button Cart",
        "questions": {
            "operation": {
                "type": "choice",
                "instructions": "Which operation moves the goal forward?",
                "criteria": {
                    "TAP": "tap a control on screen",
                    "TYPE": "type into a field",
                    "SCROLL": "scroll the menu",
                    "BACK": "go back",
                    "WAIT": "wait",
                },
            },
        },
    },
    "tap_target": {
        "state": "Goal: In the Domino's app, navigate to the Chocolate Souffle item so it is visible on screen.\nScreen: Domino's menu, desserts section below.\ncontrols: [1] Cell Farmhouse pizza [2] Cell Peppy Paneer [3] Cell Choco Lava Cake [4] Button Desserts [5] Button Beverages",
        "questions": {
            "tap_target": {
                "type": "choice",
                "instructions": "Which control should be tapped to find Chocolate Souffle?",
                "criteria": {
                    "[1] Farmhouse pizza": "a pizza item",
                    "[2] Peppy Paneer": "a pizza item",
                    "[3] Choco Lava Cake": "a chocolate dessert item",
                    "[4] Desserts": "opens the desserts section",
                    "[5] Beverages": "opens the drinks section",
                },
            },
        },
    },
    "toggle_op": {
        "state": "Goal: In Settings, turn on Airplane mode.\nScreen: Settings main.\ncontrols: [1] Cell Airplane mode, switch OFF [2] Cell Wi-Fi [3] Cell Bluetooth [4] SearchField Search",
        "questions": {
            "operation": {
                "type": "choice",
                "instructions": "Which operation moves the goal forward?",
                "criteria": {
                    "TOGGLE": "flip a switch",
                    "TAP": "tap a control",
                    "TYPE": "type into search",
                    "SCROLL": "scroll down",
                    "DONE": "goal already achieved",
                },
            },
        },
    },
    "done_check": {
        "state": "Goal: In the Domino's app, navigate to the Chocolate Souffle item so it is visible on screen.\nScreen: item page.\nvisible_text: ['Chocolate Souffle', 'Molten choco delight', 'Add to cart']",
        "questions": {
            "goal_done": {
                "type": "boolean",
                "instructions": "Is the Chocolate Souffle item visible on screen?",
            },
        },
    },
}


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
            dt = time.perf_counter() - t
            return dt, json.load(r), None
    except Exception as e:
        return time.perf_counter() - t, None, str(e)[:150]


for name, b in BATTERY.items():
    print(f"### {name}")
    for m in MODELS:
        dt, res, err = ask(m, b["state"], b["questions"])
        if err:
            print(f"  {m}: ERROR {err}")
            continue
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
                c = conf.get(qid, "n/a")
                out.append(
                    f"{qid}={a.get('choice')} conf={c} "
                    + str([(k, round(v, 2)) for k, v in top])
                )
        print(f"  {m.split('/')[-1]}: {dt:.2f}s | " + " ; ".join(out))
