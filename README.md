# Gemini but orders me food

an Android agent loop (adb) driven by a System One decision
model, because Gemini & Siri couldn't order me a pizza

## Setup

```bash
git clone https://github.com/arnabwithab/gemini-but-orders-food.git
cd gnani-multilingual-phone-use
uv sync
```

Needs: Python 3.12, an NVIDIA GPU (8GB is enough), `adb` on PATH, a phone
with USB debugging.

## Weights

Finetuned checkpoint (Laya-english + AndroidControl, full RLCD):

```bash
hf download arnabwithab/laya-android-control --local-dir phone-agent/checkpoints/ac-full
```

## Serve

```bash
LAYA_DEVICE=cuda LAYA_PRELOAD=1 LAYA_MODELS=phone-agent/checkpoints/ac-full \
  .venv/bin/laya-serve  # :8000, POST /v1/systemone
```

Point any System One client at it (`TYPESAFE_BASE_URL=http://127.0.0.1:8000`).
