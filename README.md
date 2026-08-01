# 🌍 Decarbonizing Corporate Travel — Capstone Project

**Summer Analytics 2026 | IIT Guwahati**

A data-driven approach to identifying and reducing carbon emissions from corporate business travel. This project analyzes 65,000+ trip records across multiple transport modes, regions, and business units to uncover emission hotspots and recommend actionable decarbonization strategies.

---

## 📌 Problem Statement

Corporate travel is a significant contributor to an organization's carbon footprint. This project tackles the challenge in two parts:

- **Part 1 — Exploratory Analysis & Strategy**: Profile emissions by transport mode, benchmark regions, identify high-emission routes, and quantify the impact of policy changes (flight class downgrades, modal shifts to trains, EV adoption).
- **Part 2 — Predictive Modeling**: Build a binary classifier to predict whether a trip will be **HighCarbon** based on trip attributes (route, transport mode, business unit, cost, etc.) — enabling proactive intervention before travel occurs.

---

## 🏗️ Project Structure

```
├── Capstone_part_2.ipynb                    # ML notebook — LightGBM classifier for HighCarbon prediction
├── submission.csv                           # Final prediction output
├── .gitignore
├── Part 1/
│   ├── detailed_analysis.py                 # Emissions profiling, regional benchmarking, hotspot analysis
│   ├── Sustainability Data Dictionary.xlsx  # Data dictionary for all datasets
│   ├── _Soumadipta_Konar__Capstone.pptx     # Final presentation
│   ├── README_ Sustainability...pdf         # Project brief
│   └── Sustainability Capstone Outline...pdf# Capstone outline
└── Part 2/
    ├── Part2.pdf                            # Part 2 problem statement
    └── sample_submission.csv                # Expected submission format
```

---

## 📊 Part 1 — Analysis Highlights

The analysis script (`Part 1/detailed_analysis.py`) covers:

| Analysis Area | Key Insight |
|---|---|
| **Emissions Profile** | Breakdown by Departure, Return, Hotel, and Spend CO₂e |
| **Transport Mode Comparison** | Economy vs Business vs First Class flight emissions |
| **Regional Benchmarking** | CO₂ and cost comparison across global regions |
| **Hotspot Identification** | Top 10 high-emission routes and business units |
| **Process Inefficiencies** | Out-of-policy travel impact, transportation change reasons |
| **Policy Recommendations** | Flight class downgrades, flight-to-train shifts, EV rental car adoption |

---

## 🤖 Part 2 — ML Model

**Objective**: Predict `HighCarbon` (binary) for each trip in the private test set.

| Component | Detail |
|---|---|
| **Model** | LightGBM Classifier |
| **Features** | Route info, transport mode, business unit, hotel nights, net costs, policy compliance |
| **Target** | `HighCarbon` (0 or 1) |
| **Leakage Handling** | Dropped `Departure_CO2e`, `Return_CO2e`, `Hotel_CO2e`, `Spend_CO2e`, `TotalCO2e` |
| **Class Imbalance** | Handled via `class_weight='balanced'` |

### Validation Results

| Metric | Score |
|---|---|
| **ROC-AUC** | 0.9994 |
| **F1 Score** | 0.9873 |
| **Precision** | 0.9898 |
| **Recall** | 0.9847 |

---

## 🛠️ Tech Stack

- **Python 3.13**
- **Pandas** — Data manipulation
- **NumPy** — Numerical operations
- **LightGBM** — Gradient boosting classifier
- **scikit-learn** — Model evaluation and train/test split

---

## 📂 Data

The datasets are **not included** in this repository due to their size (~65 MB). They were provided as part of the Summer Analytics 2026 capstone by IIT Guwahati.

**Datasets used:**
- `public_trip_data.csv` — 65,289 trip records with emissions and cost data
- `public_trip_event_attributes.csv` — Trip modification attributes
- `public_trip_event_log.csv` — Process event logs per trip
- `private_trip_data.csv` — Test set for HighCarbon prediction

---

## 🚀 How to Run

1. Clone the repo:
   ```bash
   git clone https://github.com/Soumadipta-Konar/decarbonizing-travel-capstone.git
   cd decarbonizing-travel-capstone
   ```

2. Install dependencies:
   ```bash
   pip install pandas numpy lightgbm scikit-learn
   ```

3. Place the dataset CSVs in `Public Dataset/` and `Private dataset/` folders.

4. Run the analysis:
   ```bash
   python "Part 1/detailed_analysis.py"
   ```

5. Run the notebook:
   ```
   jupyter notebook Capstone_part_2.ipynb
   ```

---

## 👤 Author

**Soumadipta Konar**

---

## 📄 License

This project was developed as part of the **Summer Analytics 2026** program conducted by the **Consulting & Analytics Club, IIT Guwahati**.
