# Stock Data Visualization (Alpha Vantage)

A Python application that fetches historical stock data from the **Alpha Vantage** API and opens an interactive chart in your default browser.  
Users choose **symbol**, **time series**, **date range**, and **chart type**.

> Built for a 3‑week Scrum project: includes suggested backlog, a report template, and Jira/GitHub tips.

---

## Quick Start

### 1) Requirements
- Python 3.9+
- Alpha Vantage API key (free): https://www.alphavantage.co/support/#api-key
- Install dependencies:
```bash
pip install -r requirements.txt
```

### 2) Set your API key
Use either environment variable or enter when prompted:
```bash
# macOS/Linux
export ALPHAVANTAGE_API_KEY="YOUR_KEY"

# Windows (PowerShell)
setx ALPHAVANTAGE_API_KEY "YOUR_KEY"
```

### 3) Run
```bash
python main.py
```
Follow the prompts to pick:
- Stock symbol (e.g., AAPL, MSFT, TSLA)
- Time series (Daily, Daily Adjusted, Weekly, Monthly)
- Chart type (Line, Area, Candlestick)
- Begin date / End date (YYYY-MM-DD)

An HTML chart opens in your browser.

---

## Project Structure

```
.
├── main.py                  # Entry point (CLI prompts & orchestration)
├── av_client.py             # API client for Alpha Vantage
├── charting.py              # Plotly chart generation + browser open
├── utils.py                 # Validation and helpers
├── requirements.txt         # Dependencies
├── .gitignore
├── docs/
│   ├── use_cases.mmd        # Mermaid Use Case Diagram (render on GitHub or mermaid.live)
│   ├── use_case_descriptions.md
│   ├── communication_plan.md
│   ├── jira_backlog_sample.csv
│   └── submission_report_template.md
└── tests/
    └── test_utils.py
```

---

## Time Series Options (supported)
- `TIME_SERIES_DAILY` (compact/full auto-managed)
- `TIME_SERIES_DAILY_ADJUSTED`
- `TIME_SERIES_WEEKLY`
- `TIME_SERIES_MONTHLY`

> Free tier has rate limits (typically 5 calls/minute, 500/day). If you hit limits, wait and try again.

---

## Chart Types
- **Line**: closing price vs time
- **Area**: filled area under closing price vs time
- **Candlestick**: OHLC bars (if available in selected series)

---

## Tips for Jira & GitHub

### GitHub
- Protect `main` branch; merge via Pull Requests.
- Every teammate works off a feature branch (e.g., `feature/cli`, `feature/charting`).
- Commit early and often with clear messages:
  - `feat(cli): add prompts and validation`
  - `fix(utils): robust date parsing`
  - `docs: add use case descriptions`

### Jira
- Create Scrum project with **3 one‑week sprints**:
  - **Sprint 1**: Spike API, CLI skeleton, basic chart.
  - **Sprint 2**: Validation, candlestick, tests, error handling.
  - **Sprint 3**: Polish, docs, report, buffer for fixes.
- Use story points (1/2/3/5).
- Keep the board current and move tickets daily.
- Attach screenshots to issues during and at end of each sprint for your report.

---

## Packaging the Report
- Use `docs/submission_report_template.md` to assemble your PDF.
- Paste Jira board and burndown screenshots where indicated.
- Include your **GitHub repo link** in the final section.

Good luck!