# 💳 Expense Tracker & Financial Intelligence App (Data Science Project)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458.svg?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Seaborn](https://img.shields.io/badge/Seaborn-0.12%2B-4c72b0.svg)](https://seaborn.pydata.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An industry-oriented, end-to-end data science and financial analytics platform designed to track, categorize, audit, and visualize multi-channel financial cash flows. Built with **Python, Pandas, Seaborn, and Streamlit**, this project mirrors the core analytical engines powering FinTech platforms such as **CRED, Mint, Google Pay, RazorpayX, and Splitwise**.

---

## 📌 Executive Summary & Industry Relevance

In personal and corporate finance, unorganized transaction data leads to budget leaks, lack of emergency cushion, and sub-optimal capital allocation. 
This project bridges raw transactional data and strategic decision-making by:
1. Transforming raw, heterogeneous payment records into normalized financial datasets.
2. Automating cash flow trend identification, month-over-month (MoM) burn rates, and discretionary expense concentration.
3. Auditing spending against the industry-standard **50/30/20 Budgeting Rule** (Needs vs. Wants vs. Savings).
4. Flagging statistical outliers using **Interquartile Range (IQR)** anomaly detection.
5. Delivering both an automated **CLI Executive Report** and an **Interactive Web Dashboard**.

---

## 🏗️ System Architecture

```
[ Data Ingestion Layer ]
  - Synthetic Financial Engine (750+ multi-month realistic transactions)
  - Interactive Manual Expense Logging (Streamlit Form)
  - External CSV / Excel Ingestion
            │
            ▼
[ Preprocessing & Feature Engineering Layer ]
  - Deduplication & Null Imputation
  - String Normalization & Text Sanitization
  - Chronological Sorting & Temporal Feature Engineering (Year, Month, Weekday, Quarter)
  - Financial Classification (50/30/20 Rule: Needs, Wants, Savings)
            │
            ▼
[ Analytics & Intelligence Layer ]
  - Executive Financial KPIs (Inflow, Outflow, Net Savings, Burn Rate)
  - Category Concentration & Ticket Size Variance
  - Month-over-Month (MoM) Growth & Deficit Month Identification
  - 1.5 * IQR Statistical Expense Outlier Detection
            │
            ▼
[ Presentation & Visualization Layer ]
  - Interactive Streamlit Dashboard (Real-time Filtering, Metric Cards, Charts)
  - High-Resolution Chart Export (DPI 300 Matplotlib/Seaborn Plots)
  - Natural Language Executive Report Generation (`financial_summary_report.txt`)
```

---

## 🛠️ Tech Stack

| Domain | Technology / Library | Role in Project |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ | Core scripting, pipeline orchestration, logic execution |
| **Data Manipulation** | Pandas, NumPy | Data cleaning, type conversion, aggregation, IQR math |
| **Data Visualization** | Matplotlib, Seaborn | Publication-grade charts (bar, donut, dual-axis line) |
| **Interactive UI** | Streamlit | Web dashboard with dynamic sidebar filters and data explorer |
| **Environment** | Virtual Environment (`venv`) | Dependency isolation and reproducible environments |

---

## 📂 Repository Structure

```
Expense-Tracker-App/
│
├── data/
│   ├── raw_expenses.csv              # Synthetic raw transaction dataset
│   └── cleaned_expenses.csv          # Preprocessed and feature-engineered dataset
│
├── notebooks/
│   └── expense_analysis_eda.ipynb    # Interactive Jupyter Notebook for exploratory analysis
│
├── src/
│   ├── __init__.py                   # Package initialiser
│   ├── generate_data.py              # Realistic multi-month synthetic transaction generator
│   ├── data_preprocessing.py         # Data cleaning, deduplication, and 50/30/20 classifier
│   ├── analytics.py                  # Financial KPI engine, anomaly detection, report builder
│   └── visualizations.py             # Matplotlib & Seaborn chart rendering pipeline
│
├── outputs/
│   ├── category_distribution.png     # Category spend & donut chart
│   ├── monthly_trend.png             # Inflow vs Outflow monthly trajectory
│   ├── weekday_spending.png          # Weekday velocity and transaction frequency
│   ├── payment_method_breakdown.png  # UPI / Card / Net Banking share
│   ├── budget_vs_actual.png          # 50/30/20 Rule audit chart
│   └── financial_summary_report.txt  # Auto-generated executive report
│
├── images/                           # README image assets and screenshots
├── app.py                            # Interactive Streamlit dashboard application
├── main.py                           # Master CLI pipeline execution script
├── requirements.txt                  # Python dependency specifications
├── .gitignore                        # Git exclusions for python bytecode and cache
└── README.md                         # Detailed project documentation
```

---

## 🚀 Quick Start Guide

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/Expense-Tracker-App.git
cd Expense-Tracker-App
```

### 2. Set Up Virtual Environment

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Master CLI Pipeline
```bash
python main.py
```
*This command generates synthetic data, executes data cleaning, computes KPIs, renders all charts into `outputs/`, and generates `financial_summary_report.txt`.*

### 5. Launch the Interactive Streamlit Dashboard
```bash
streamlit run app.py
```
*Opens automatically at `http://localhost:8501` in your default browser.*

---

## 📊 Analytical Highlights & Visual Proofs

### 1. Category-Wise Financial Outflow
Evaluates largest capital drains, transaction volume, and percentage exposure across lifestyle categories.
![Category Distribution](outputs/category_distribution.png)

### 2. Monthly Cash Flow Trajectory (Inflow vs. Outflow)
Compares monthly income deposits against total debits, highlighting cash flow margins and deficit months.
![Monthly Trajectory](outputs/monthly_trend.png)

### 3. Financial Health Audit: 50/30/20 Rule
Audits actual spending behavior against the benchmark budgeting standard (50% Needs, 30% Wants, 20% Savings).
![Budget Rule](outputs/budget_vs_actual.png)

### 4. Weekly Spending Velocity
Identifies transaction clustering and peak spending days to prevent weekend discretionary spending spikes.
![Weekday Velocity](outputs/weekday_spending.png)

### 5. Payment Channel Utilization
Analyzes reliance on digital rails (UPI, Credit Cards, Net Banking, Cash).
![Payment Methods](outputs/payment_method_breakdown.png)

---

## 📑 Automated Executive Report Sample

```text
=======================================================
        EXECUTIVE FINANCIAL HEALTH REPORT             
=======================================================

📌 1. MACRO SUMMARY & SAVINGS PERFORMANCE:
  • Cumulative Cash Inflow:  ₹1,270,123.31
  • Cumulative Cash Outflow: ₹1,368,200.02
  • Net Savings Accumulated: ₹-98,076.71
  • Overall Savings Rate:    -7.72%
  • Status: 🔴 VULNERABLE - High burn rate; vulnerable to liquidity shocks.

📌 2. CATEGORY CONCENTRATION:
  • Largest Outflow Driver:  'Groceries' accounting for ₹353,156.91 (25.81% of total expenses).
  • Secondary Cost Driver:   'Shopping' with ₹296,491.82 (21.67%).

📌 3. BUDGET ADHERENCE (50/30/20 RULE):
  • Needs Allocation:   54.44% (Benchmark: ≤ 50%) -> ⚠️ Over budget
  • Wants Allocation:   44.07% (Benchmark: ≤ 30%) -> ⚠️ Discretionary lifestyle creep detected
  • Savings Allocation: -7.72% (Benchmark: ≥ 20%) -> ⚠️ Below savings target

📌 4. ACTIONABLE FINANCIAL RECOMMENDATIONS:
  1. Cap 'Groceries' spending using predefined monthly threshold limits.
  2. Trim dining and entertainment subscriptions to bring 'Wants' down to the 30% benchmark.
  3. Automate recurring transfers to an investment/emergency fund on the 1st of every month.
=======================================================
```

---

## 🎯 5-Day Proof-Building Strategy for Placements

| Day | Task Focus | Key Deliverable | Recommended Git Commit |
| :--- | :--- | :--- | :--- |
| **Day 1** | Project Setup & Scope | Repo setup, virtual environment, directory architecture | `feat: initialize project structure and dependencies` |
| **Day 2** | Synthetic Data & Pipeline | Multi-channel data synthesizer & pandas cleaning pipeline | `feat: implement synthetic data generator and cleaning pipeline` |
| **Day 3** | Financial Analytics Engine | 50/30/20 rule logic, KPI metrics, IQR anomaly detection | `feat: add financial analytics engine and budget audit logic` |
| **Day 4** | Visualization Suite | Publication-grade Matplotlib/Seaborn chart generation | `feat: build automated visualization suite and export charts` |
| **Day 5** | Interactive UI & Documentation | Streamlit app, master `main.py`, comprehensive `README.md` | `docs: complete README and finalize interactive Streamlit dashboard` |

---

## 💼 Placement & Interview Readiness

### Top 3 Core Concepts Demonstrated:
1. **Financial Domain Literacy:** Applied understanding of cash flow velocity, burn rate, 50/30/20 budget framework, and deficit cycles.
2. **Robust Data Engineering:** Defensive data cleaning, handling messy strings, handling categorical normalization, and preventing data leakage.
3. **Product-Thinking & Stakeholder Presentation:** Bridged statistical calculations with actionable natural language recommendations and an executive-facing dashboard.

---

## 🔮 Future Roadmap

- [ ] **Predictive Cash Flow Forecasting:** Implement Facebook Prophet / ARIMA time-series models to predict month-end expense totals.
- [ ] **OCR Receipt Extraction:** Integrate Tesseract / EasyOCR to scan paper bills directly into the transaction database.
- [ ] **Automated Budget Alerts:** Webhook integration with WhatsApp or Telegram for instant threshold breach notifications.
- [ ] **Open Banking / Account Aggregator API:** Connect live bank feeds using Plaid or Setu Account Aggregator.

---

## AUTHOR 
- **Project Lead**: **Abhishek Basu**
- **GitHub**: [DevAbhay2003](https://github.com/DevAbhay2003?tab=repositories)
- **LinkedIn**: [https://linkedin.com/in/your-profile](https://www.linkedin.com/in/abhishek-basu-68b1b1342/)
- **Email**: devabhishekbasu03@gmail.com

---

## 📄 License
This project is open-source under the [MIT License](LICENSE).
