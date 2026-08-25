#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

PORT="${1:-8501}"
PID="$(lsof -ti tcp:"${PORT}" || true)"

if [[ -n "${PID}" ]]; then
  echo "Stopping existing process on port ${PORT}: ${PID}"
  kill ${PID}
  sleep 1
fi

exec bash scripts/demo_launch.sh "${PORT}"
