# !/bin/bash
echo "start scraping naver top500 list"
uv run python -m google_sheets.naver_data_lab

echo "start scraping temu data list"
uv run python -m google_sheets.temu_data