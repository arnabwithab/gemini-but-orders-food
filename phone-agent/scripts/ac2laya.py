"""xwm/AndroidControl (per-step rows) -> Laya laya-train JSONL.

Row -> up to 2 decision rows:
  operation: choice over TAP/TYPE/SCROLL/BACK/WAIT/DONE; state = goal + prior instructions
  done: noul "is the phone task complete?"
Maps: click/longpress->TAP, input->TYPE, scroll->SCROLL, press[back]->BACK,
      wait->WAIT, finished->DONE. Other press keys are skipped and counted.
"""

import json, sys, hashlib
from collections import Counter
from datasets import load_dataset

OP_DESC = {
    "TAP": "tap a control on screen",
    "TYPE": "type text into a field",
    "SCROLL": "scroll the screen",
    "BACK": "go back to the previous screen",
    "WAIT": "wait for the screen to settle",
    "DONE": "the goal is already achieved, do nothing",
}


def op_of(action):
    name = action.get("action_name")
    if name in ("click", "longpress"):
        return "TAP"
    if name == "input":
        return "TYPE"
    if name == "scroll":
        return "SCROLL"
    if name == "wait":
        return "WAIT"
    if name == "finished":
        return "DONE"
    if name == "press":
        return "BACK" if (action.get("keys") or []) == ["back"] else None
    return None


def hist_text(history):
    out = []
    for h in (history or [])[-3:]:
        if isinstance(h, dict):
            ins = h.get("instruction", "")
            an = (h.get("action") or {}).get("action_name", "")
            out.append(f"{ins} [{an}]" if ins else f"[{an}]")
        else:
            out.append(str(h))
    return out


def convert(row):
    goal = row["goal"]
    prev = "\n".join(f"- done: {t}" for t in hist_text(row.get("history_list")))
    state = f"Goal: {goal}\nPrevious steps:{chr(10) + prev if prev else ' none yet'}"
    state = state[:1500]
    op = op_of(row["action"])
    fin = row["action"].get("action_name") == "finished"
    rows = []
    if op:
        rows.append(
            {
                "state": state,
                "questions": {
                    "operation": {
                        "type": "choice",
                        "instructions": "Which operation moves this phone task forward?",
                        "criteria": OP_DESC,
                    }
                },
                "expected": {"operation": op},
            }
        )
    cur = row.get("instruction", "")
    rows.append(
        {
            "state": (state + f"\nNow: {cur}")[:1500],
            "questions": {
                "done": {"type": "noul", "instructions": "Is the phone task complete?"}
            },
            "expected": {"done": bool(fin)},
        }
    )
    return rows


if __name__ == "__main__":
    cols = [
        "goal",
        "action",
        "step_id",
        "episode_length",
        "instruction",
        "history_list",
    ]
    ds = load_dataset(
        "xwm/AndroidControl", split="train", streaming=True
    ).select_columns(cols)
    if "--hist" in sys.argv:
        c, sk, n = Counter(), Counter(), 0
        for r in ds:
            op = op_of(r["action"])
            c[r["action"].get("action_name")] += 1
            if not op:
                sk[str(r["action"].get("keys"))] += 1
            n += 1
        print("rows:", n, "\nactions:", dict(c), "\nskipped press keys:", dict(sk))
    else:
        out_t = open("phone-agent/data/train.jsonl", "w")
        out_e = open("phone-agent/data/eval.jsonl", "w")
        nt = ne = skip = 0
        for r in ds:
            is_eval = int(hashlib.md5(r["goal"].encode()).hexdigest(), 16) % 10 == 0
            for row in convert(r):
                (out_e if is_eval else out_t).write(json.dumps(row) + "\n")
                if is_eval:
                    ne += 1
                else:
                    nt += 1
        print(f"train rows: {nt}, eval rows: {ne}")
