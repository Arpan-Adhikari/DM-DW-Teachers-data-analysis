# 📊 Teacher Distribution Analysis & Dashboard (Nepal, 2074 BS)

This project analyzes the distribution of approved teacher positions in community schools across districts of Nepal for the year **2074 BS**, and visualizes insights through an **interactive dashboard**.

The dashboard helps explore:
- Number of approved and Rahat teachers by district
- Top & bottom districts
- Distribution and boxplot of teacher counts
- Share of teachers by province
- Clusters of districts with similar teacher allocations

---

## 🧰 **Dataset**
- File: `data.csv`
- Contains:
  - District & province info
  - Approved teacher posts (Primary, Lower Secondary, Secondary)
  - Rahat teacher posts (Primary, Lower Secondary, Secondary)

This dataset was cleaned to remove aggregate "ALL" rows and handle missing values.

---

## ⚙ **Technologies & Libraries**
- Python 3
- [Streamlit](https://streamlit.io/) (for dashboard)
- pandas (data handling)
- seaborn & matplotlib (visualizations)
- scikit-learn (clustering)

---

## 🚀 **How to run**
1. Clone/download this repository
2. Install required libraries:
```bash
pip install streamlit pandas seaborn matplotlib scikit-learn


**Project Structure**
student-performance-analysis/
├── data/
│   └── data.csv
├── dashboard/
│   └── app.py             # Streamlit dashboard
├── notebooks/
│   └── education_analysis.ipynb  # Exploratory data analysis
└── README.md
