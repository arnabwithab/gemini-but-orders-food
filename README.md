<div align="center">

# Gemini but orders me food

an Android agent loop (adb) driven by a System One decision model, because Gemini & Siri couldn't order me a pizza.

[![Black](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black) [![HF Model](https://img.shields.io/badge/🤗-laya--android--control-059669)](https://huggingface.co/arnabwithab/laya-android-control) [![Base: Laya](https://img.shields.io/badge/🤗%20Base-Laya--421M-yellow)](https://huggingface.co/convaiinnovations/laya) [![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org) [![CUDA](https://img.shields.io/badge/CUDA-12.0-76b900?logo=nvidia&logoColor=white)](https://developer.nvidia.com/cuda-toolkit)

</div>

## Setup

```bash
git clone https://github.com/arnabwithab/gemini-but-orders-food.git
cd gnani-multilingual-phone-use
uv sync
```

Needs: Python 3.12, an NVIDIA GPU (8GB is enough), `adb` on PATH, a phone with USB debugging.

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
