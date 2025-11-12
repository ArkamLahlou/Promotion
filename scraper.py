# .github/workflows/run_scraper.yml
name: AliExpress Scraper

on:
  # التشغيل التلقائي كل 24 ساعة (عند الساعة 00:00 بتوقيت UTC)
  schedule:
    - cron: '0 0 * * *'
  # يدوياً عند الحاجة
  workflow_dispatch:

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests beautifulsoup4 pyyaml

      - name: Run Scraper Script
        run: python scraper.py
        
      # هذه الخطوة الحيوية لنجاح الأتمتة: حفظ التغييرات على المستودع
      - name: Commit and Push Changes
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: '🤖 Automated: Update AliExpress deals via Scraper'
          files: _data/deals.yml
