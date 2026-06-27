#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
#  RxClear – Start script
#  Runs FastAPI backend (port 8000) + Vite frontend (port 3000)
# ─────────────────────────────────────────────────────────────

set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  RxClear – AI Prescription Analyzer"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Install Python deps if needed
if ! python -c "import fastapi" 2>/dev/null; then
  echo "▸ Installing Python dependencies…"
  pip install -r "$ROOT/requirements.txt" --break-system-packages -q
fi

# Train model if missing
if [ ! -f "$ROOT/models/disease_model.pkl" ]; then
  echo "▸ Training disease prediction model…"
  python "$ROOT/models/train_model.py"
fi

# Create dirs
mkdir -p "$ROOT/uploads" "$ROOT/reports"

# Start FastAPI backend in background
echo "▸ Starting FastAPI backend on http://localhost:8000"
cd "$ROOT/backend"
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Start Vite frontend
echo "▸ Starting React frontend on http://localhost:3000"
cd "$ROOT/frontend"
npm run dev &
FRONTEND_PID=$!

echo ""
echo "  Backend  → http://localhost:8000"
echo "  Frontend → http://localhost:3000"
echo "  API docs → http://localhost:8000/docs"
echo ""
echo "  Press Ctrl+C to stop both servers."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo 'Stopped.'" EXIT
wait
