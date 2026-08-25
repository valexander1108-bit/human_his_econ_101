#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

PORT="${1:-8501}"

python -m pip install -r requirements.txt
python -m py_compile streamlit_app.py pages/*.py apps/*.py modules_data.py
python scripts/check_app.py

echo "Launching ECON 101 demo at http://localhost:${PORT}"
exec streamlit run streamlit_app.py --server.port "${PORT}"
