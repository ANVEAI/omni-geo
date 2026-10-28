#!/usr/bin/env bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "=========================================================="
echo "  OmniGEO: Generative Engine Optimization Platform"
echo "  AI Search Audit & Revenue Machine"
echo "=========================================================="

if [ ! -d ".venv" ]; then
    echo "[+] Initializing Python virtual environment..."
    uv venv
    source .venv/bin/activate
    uv pip install fastapi uvicorn pydantic requests beautifulsoup4 aiohttp jinja2 python-multipart
else
    source .venv/bin/activate
fi

# Initialize sample data if missing
if [ ! -f "data/sample_audits.json" ]; then
    echo "[+] Initializing benchmark sample audits..."
    python3 core/sample_generator.py
fi

echo ""
echo "🚀 Starting OmniGEO Server on http://127.0.0.1:8000"
echo "👉 Interactive Dashboard: http://127.0.0.1:8000"
echo "👉 Executive Benchmark:  http://127.0.0.1:8000/report/audit_linear_sample"
echo "👉 Turnkey GTM Kit:       http://127.0.0.1:8000/gtm-kit"
echo ""
echo "Press Ctrl+C to stop the server."
echo "=========================================================="

exec uvicorn app:app --host 127.0.0.1 --port 8000 --reload
