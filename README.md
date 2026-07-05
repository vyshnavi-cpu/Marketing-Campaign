# 📊 Marketing Campaign Analysis

An end-to-end analytics solution that combines **Python**, **SQL**, and **Streamlit** to clean, analyze, segment, and visualize retail marketing campaign data — enabling stakeholders to identify high-value customer segments, understand spending patterns, and optimize future campaign targeting.

---

## 📑 Table of Contents

- [Problem Statement](#-problem-statement)
- [Business Use Cases](#-business-use-cases)
- [Skills & Learning Outcomes](#-skills--learning-outcomes)
- [Tech Stack](#-tech-stack)
- [Project Architecture](#-project-architecture)
- [Repository Structure](#-repository-structure)
- [Database Schema](#-database-schema)
- [Setup & Installation](#-setup--installation)
- [How to Run](#-how-to-run)
- [Approach & Methodology](#-approach--methodology)
- [Key Results & Insights](#-key-results--insights)
- [Recommendations](#-recommendations)
- [Screenshots](#-screenshots)
- [License](#-license)

---

## 🎯 Problem Statement

A retail company has run multiple marketing campaigns and recorded detailed information about customers — demographics, spending across product categories, channel-wise purchases, and campaign acceptance history (`AcceptedCmp1–5`, `Response`).

Management needs a **consolidated analytics solution** to:

- Identify who its best customers are.
- Understand what drives campaign acceptance.
- Discover how different customer segments behave across products and channels.

This project delivers that solution through a reproducible data pipeline: **raw CSV → cleaned data → SQL data warehouse → interactive Streamlit dashboard**.

---

## 💼 Business Use Cases

| # | Business Question |
|---|---|
| 1 | Which customer segments have the **highest campaign response rates** — overall and per campaign (Cmp1–5)? |
| 2 | How do **spending patterns** across products (wine, fruits, meat, fish, sweets, gold) vary by age, income, marital status, and country? |
| 3 | Which **purchase channels** (web, store, catalog, deals) are most used by high-value customers, and how often do they visit the website? |
| 4 | Are there **under-served segments** — high web visits but low spending and low campaign response? |
| 5 | What are the characteristics of **ideal target customers** for future campaigns? (age range, income band, family composition, country, etc.) |

---

## 🧠 Skills & Learning Outcomes

| Domain | Skills Demonstrated |
|--------|-------------------|
| **Python** | Data cleaning, EDA, feature engineering, outlier handling, CSV processing, rule-based segmentation |
| **SQL** | Normalized table design, DDL, data loading via SQLAlchemy, analytical queries, KPI extraction, `CASE` segmentation |
| **EDA & Visualization** | Univariate analysis (distributions), bivariate/multivariate analysis (response vs. demographics), segment profiling |
| **Dashboard** | Interactive Streamlit app with filters, tabs, metrics, bar charts, and data tables |
| **Domain** | Marketing Analytics, Customer Analytics, Campaign Performance |

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.x |
| Data Processing | Pandas, NumPy |
| Visualization (EDA) | Matplotlib, Seaborn |
| Dashboard | Streamlit |
| Database | PostgreSQL |
| ORM / Connector | SQLAlchemy, psycopg2-binary |
| Notebook | Jupyter Notebook |

---

## 🏗 Project Architecture

```
┌────────────────────┐
│  marketing_data.csv│  ← Raw dataset
└────────┬───────────┘
         │
         ▼
┌────────────────────────────────────────────┐
│  Jupyter Notebook (EDA & Segmentation)     │
│  ├─ Data Cleaning & Feature Engineering    │
│  ├─ Univariate & Bivariate Analysis        │
│  ├─ Rule-Based Customer Segmentation       │
│  └─ Load Cleaned Data → PostgreSQL         │
└────────┬───────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────────┐
│  PostgreSQL Database                       │
│  ├─ customers                              │
│  ├─ customer_spend                         │
│  ├─ customer_activity                      │
│  └─ campaign_responses                     │
└────────┬───────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────────┐
│  Streamlit Dashboard  (Marketing.py)       │
│  ├─ Tab 1: Campaign Conversion Performance │
│  ├─ Tab 2: Product Spending Dynamics       │
│  ├─ Tab 3: Channel & Web Traffic Analysis  │
│  └─ Tab 4: Under-Served & Target Profiles  │
└────────────────────────────────────────────┘
```

---

## 📁 Repository Structure

```
Marketing-Campaign-main/
│
├── Marketing_Campaign_EDA_and_Segmentation.ipynb   # Full EDA, cleaning, segmentation & DB loading
├── Marketing.py                                     # Streamlit dashboard application
├── Table_Creation.sql                               # DDL — normalized PostgreSQL schema
├── KPI_Extraction.sql                               # Baseline KPI analytical queries
├── Segmentation_Queries.sql                         # SQL segmentation & demographic analysis
└── README.md                                        # Project documentation (this file)
```

### File Descriptions

| File | Purpose |
|------|---------|
| `Marketing_Campaign_EDA_and_Segmentation.ipynb` | End-to-end notebook: loads raw CSV, cleans data (missing values, outliers, type conversions), engineers features (`Age`, `Total_Spend`, `Total_Purchases`, `Children`, `Customer_Tenure_Days`), performs univariate/bivariate EDA with Matplotlib & Seaborn, applies rule-based segmentation, and loads cleaned data into PostgreSQL via SQLAlchemy. |
| `Marketing.py` | Streamlit dashboard connecting to PostgreSQL. Provides 4 interactive tabs answering all 5 business use cases. Features global country filters, segment-level KPIs, dynamic bar charts, and data tables. |
| `Table_Creation.sql` | PostgreSQL DDL defining a normalized 4-table schema: `customers`, `customer_spend`, `customer_activity`, and `campaign_responses` — linked via foreign keys with cascade deletes. |
| `KPI_Extraction.sql` | Analytical SQL queries computing baseline KPIs: total customer count, overall response rate (%), average spend per customer, and average monthly web visits. |
| `Segmentation_Queries.sql` | SQL-based segmentation queries: segment by education + marital status, and by country + age band + income band. Uses `CASE` statements for banding and computes conversion rates per group. |

---

## 🗄 Database Schema

The PostgreSQL database uses a **normalized star-like schema** with four tables:

```
┌──────────────────────┐
│     customers        │  ← Dimension: Demographics
│ ─────────────────    │
│ customer_id (PK)     │
│ year_birth           │
│ education            │
│ marital_status       │
│ income               │
│ kidhome / teenhome   │
│ dt_customer          │
│ recency              │
│ complain             │
│ country              │
│ customer_tenure_days │
│ age                  │
│ children             │
└──────┬───────────────┘
       │ 1:1 FK
       ├──────────────────────────────────┐
       │                                  │
┌──────▼───────────────┐   ┌──────────────▼──────────────┐
│   customer_spend     │   │   customer_activity         │
│ ─────────────────    │   │ ─────────────────           │
│ customer_id (PK/FK)  │   │ customer_id (PK/FK)         │
│ mnt_wines            │   │ num_deals_purchases         │
│ mnt_fruits           │   │ num_web_purchases           │
│ mnt_meat_products    │   │ num_catalog_purchases       │
│ mnt_fish_products    │   │ num_store_purchases         │
│ mnt_sweet_products   │   │ num_web_visits_month        │
│ mnt_gold_prods       │   │ total_purchases             │
│ total_spend          │   └─────────────────────────────┘
└──────────────────────┘
       │
┌──────▼───────────────┐
│ campaign_responses   │
│ ─────────────────    │
│ customer_id (PK/FK)  │
│ accepted_cmp1–5      │
│ response             │
└──────────────────────┘
```

---

## ⚙️ Setup & Installation

### Prerequisites

- **Python 3.8+**
- **PostgreSQL** (running locally on port `5432`)
- **pip** (Python package manager)

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/Marketing-Campaign.git
cd Marketing-Campaign
```

### 2. Install Python Dependencies

```bash
pip install pandas numpy matplotlib seaborn streamlit sqlalchemy psycopg2-binary
```

### 3. Set Up the PostgreSQL Database

1. Create a PostgreSQL database (e.g., `demo`):

   ```sql
   CREATE DATABASE demo;
   ```

2. Run the table creation script to build the schema:

   ```bash
   psql -U postgres -d demo -f Table_Creation.sql
   ```

3. Open and run the Jupyter notebook (`Marketing_Campaign_EDA_and_Segmentation.ipynb`) end-to-end. The final cells will:
   - Clean the raw CSV data.
   - Engineer all derived features.
   - Load the processed data into the 4 PostgreSQL tables.

### 4. Configure Database Credentials

Update the connection settings in `Marketing.py` (lines 17–21) to match your local PostgreSQL setup:

```python
DB_USER = 'postgres'
DB_PASSWORD = 'YourPasswordHere'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'demo'
```

---

## 🚀 How to Run

### Run the Jupyter Notebook (EDA & Data Loading)

```bash
jupyter notebook Marketing_Campaign_EDA_and_Segmentation.ipynb
```

Execute all cells sequentially to perform data cleaning, EDA, segmentation, and database loading.

### Launch the Streamlit Dashboard

```bash
streamlit run Marketing.py
```

The dashboard will open at `http://localhost:8501` with four interactive tabs.

---

## 📐 Approach & Methodology

### Phase 1 — Data Understanding & Cleaning (Python)

- Loaded `marketing_data.csv` and inspected structure with `.info()` and `.isnull().sum()`.
- Converted `Dt_Customer` to datetime; derived `Customer_Tenure_Days`.
- Engineered features: `Age` (from `Year_Birth`), `Total_Spend`, `Total_Purchases`, `Children` (`Kidhome + Teenhome`).
- Removed unrealistic ages (> 100 years); filled missing `Income` with median.
- Capped income outliers using business-rule thresholds.

### Phase 2 — Exploratory Data Analysis (Python)

- **Univariate**: Distribution plots for Age, Income, Total Spend, and Recency.
- **Bivariate**: Campaign response vs. Income (boxplot), Response vs. Age, Spend vs. Education.
- **Multivariate**: Product spending breakdown across demographic cuts; channel usage patterns.
- Identified that campaign responders have significantly higher incomes and total spend.

### Phase 3 — Rule-Based Customer Segmentation

Applied business-driven segmentation rules:

| Segment | Rule |
|---------|------|
| **High Spender** | `Total_Spend ≥ $1,500` |
| **High Income Elite** | `Income ≥ $75,000` AND `Total_Spend < $1,500` |
| **Standard Retail Profile** | `Income $40k–$75k` AND `Total_Spend < $1,500` |
| **Family Shopper** | `Income < $40,000` |

Additional banding:
- **Age Bands**: Young (< 35), Middle-Aged (35–55), Senior (> 55)
- **Income Bands**: Low (< $40k), Moderate ($40k–$75k), Premium (> $75k)

### Phase 4 — SQL Data Modeling & Queries

- Designed a normalized 4-table schema in PostgreSQL.
- Loaded cleaned DataFrames via SQLAlchemy's `to_sql()`.
- Wrote analytical queries for:
  - Baseline KPIs (total customers, response rate, average spend, web visits).
  - Segment-level summaries by education × marital status.
  - Geographic + age band + income band cross-tabulations with conversion rates.

### Phase 5 — Interactive Dashboard (Streamlit)

Built a 4-tab Streamlit application:

| Tab | Content |
|-----|---------|
| **Campaign Conversion Performance** | Response rates per segment across Cmp1–5; bar chart of latest response rate |
| **Product Spending Dynamics** | Average spend per product category pivoted by age band, income band, marital status, or country |
| **Channel & Web Traffic** | Average purchases by channel (web, catalog, store, deals) per segment; monthly web visit frequency |
| **Under-Served & Target Profiles** | Identifies under-served customers (high visits, low spend); profiles ideal target customers based on converted users |

Global sidebar filter enables region-based slicing across all tabs.

---

## 📈 Key Results & Insights

1. **High Spenders drive campaign success** — the "High Spender" segment shows the highest response rates across all campaigns.
2. **Income is a strong predictor** — customers who accepted campaigns have notably higher median incomes than non-responders.
3. **Store and web channels dominate** — high-value customers prefer in-store and web purchases over catalog and deals.
4. **Under-served segment exists** — a measurable group of customers visits the website frequently (> 5 times/month) but spends under $500, indicating a conversion opportunity.
5. **Ideal target profile** — converted customers tend to be middle-aged to senior, with above-average income, fewer children, and are typically in a coupled marital status.

---

## 💡 Recommendations

1. **Target High-Income, Low-Response segments** with personalized offers to improve conversion among untapped premium customers.
2. **Invest in web-to-purchase conversion** for the under-served cohort — use retargeting, cart abandonment emails, and exclusive web discounts.
3. **Double down on store + catalog channels** for high-spender segments where conversion rates are already strongest.
4. **Tailor campaigns by family composition** — family shoppers (with children) respond differently; consider family-oriented bundles and promotions.
5. **Use age and income banding** in campaign targeting — focus future campaigns on the 35–55 age range with $40k+ income for best ROI.
6. **Expand geographic analysis** — certain countries show disproportionately high or low response rates, warranting region-specific campaign strategies.

---

## 📸 Screenshots

> *Launch the Streamlit app (`streamlit run Marketing.py`) to explore the interactive dashboard with campaign performance metrics, spending dynamics, channel analysis, and customer profiling.*

---

## 📄 License

This project is open-source and available for educational and analytical purposes.

---

<p align="center">
  Built with ❤️ using Python · SQL · Streamlit
</p>
