#!/bin/bash
python3 -m venv venv_specs
source venv_specs/bin/activate
pip install playwright
playwright install-deps chromium
playwright install chromium

python3 src/apps/products/management/commands/scrape_specs.py

rm -rf ~/.cache/ms-playwright/
deactivate
rm -rf venv_specs