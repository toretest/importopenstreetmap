#!/usr/bin/env bash
set -e

# 1) Ensure osmium-tool is installed (provides osmium CLI)
echo "🔧 Installing osmium-tool (if needed)..."
brew install osmium-tool

# 2) Create a fresh venv if you don't already have one
if [ ! -d ".venv" ]; then
  echo "🐍 Creating Python virtualenv (.venv)..."
  python3 -m venv .venv
fi

# 3) Activate it and upgrade pip
echo "🚀 Activating virtualenv and upgrading pip..."
# shellcheck disable=SC1091
source .venv/bin/activate
pip install --upgrade pip setuptools wheel

# 4) (Optional) install any pure-Python deps you list
#    If you have nothing in requirements.txt, skip this
if [ -f requirements.txt ] && [ -s requirements.txt ]; then
  echo "📦 Installing Python dependencies from requirements.txt..."
  pip install -r requirements.txt
fi

echo
echo "✅ Setup complete!"
echo "Next, run the pipeline:"
echo "  osmium tags-filter data/norway-latest.osm.pbf w/addr:postcode -o data/out/filtered.osm.pbf"
echo "  osmium export    data/out/filtered.osm.pbf -f json -o data/out/addrs.json"
echo "  python main.py addrs.json"
