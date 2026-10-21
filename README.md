# Real-Time Fintech Fraud Detection and Geospatial Risk Analysis

An AI-powered financial transaction analysis project using MongoDB, PySpark MLlib, Random Forest, and Streamlit to identify potentially fraudulent transactions and visualize financial risk.

## 🚀 Live Demo

**[Launch the Fintech Fraud Detection Dashboard](https://fintech-fraud-detection-9vww35fuciybvqfux2pehc.streamlit.app/)**

Explore interactive dashboards for transaction analysis, model performance, and fraud-risk investigation.

## 📌 Project Overview

Financial fraud is a significant challenge for digital payment systems and financial institutions. This project demonstrates how big data technologies and machine learning can help analyze transaction data and classify potentially suspicious activity.

The system uses MongoDB to store transaction records, PySpark MLlib to build a Random Forest classification pipeline, and Streamlit to present results through an interactive dashboard.

The project uses **20,000 synthetic financial transaction records** for educational and demonstration purposes.

## ✨ Key Features

- **MongoDB Integration:** Store transaction records and use database indexes for efficient querying.
- **Big Data Processing:** Process and prepare transaction data using PySpark.
- **Machine Learning:** Train a Random Forest classification model using PySpark MLlib.
- **Model Evaluation:** Review accuracy, precision, recall, F1-score, and ROC-AUC.
- **Interactive Dashboard:** Explore transaction summaries and model performance.
- **Transaction Explorer:** Filter, search, and inspect transaction records.
- **Risk Analysis:** Visualize flagged transactions and potential financial exposure.
- **Data Export:** Export selected transaction results to CSV.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development and data processing |
| MongoDB | Transaction storage and indexing |
| PySpark | Distributed-data processing framework and ML pipeline |
| Spark MLlib | Machine-learning model training and evaluation |
| Random Forest | Transaction classification |
| Streamlit | Interactive web dashboard |
| Pandas | Data manipulation |
| Plotly | Interactive visualizations |

## 📊 Recorded Model Performance

The recorded evaluation metrics are:

| Metric | Result |
|---|---:|
| Accuracy | 93.14% |
| ROC-AUC | 0.739 |
| Weighted Precision | 90.72% |
| Weighted Recall | 93.14% |
| Weighted F1-score | 90.00% |

**Note:** These results are based on synthetic data. Accuracy alone does not establish fraud-detection effectiveness. Results can vary with the classification threshold, and the dashboard's flagged-transaction statistics may differ from the saved evaluation metrics.

## 📈 Dashboard Sections

1. **Overview** — Summary of transaction records and risk indicators.
2. **Model Performance** — Evaluation metrics and model results.
3. **Transaction Explorer** — Search and filter transaction records.
4. **Risk Analysis** — Examine flagged transactions and risk patterns.

## ⚙️ Run Locally

### Prerequisites

- Python installed
- Git installed
- Access to a configured MongoDB database if required by the application
- The project's required data and model files

### 1. Clone the repository

Replace `YOUR-USERNAME` with your GitHub username.

```bash
git clone https://github.com/YOUR-USERNAME/fintech-fraud-detection.git
cd fintech-fraud-detection
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MongoDB

Set up the MongoDB connection required by the application. Store connection credentials securely in environment variables or an appropriate secrets configuration. Never commit passwords or private credentials to GitHub.

### 5. Start the Streamlit dashboard

If the main application file is named `app.py`, run:

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal.

## 📁 Project Components

The project includes components for transaction data preparation, MongoDB integration, PySpark model training, model evaluation, and the Streamlit dashboard. Refer to the repository files for the exact filenames and execution order.

## ⚠️ Limitations

- The dataset contains synthetic transactions and does not represent verified real-world financial activity.
- Performance on real-world or previously unseen transactions may differ.
- Fraud detection involves a trade-off between identifying fraudulent activity and incorrectly flagging legitimate transactions.
- This project is intended for academic and demonstration purposes, not as a production financial security system.

## 🔮 Future Improvements

- Evaluate the model on independently sourced and appropriately authorized datasets.
- Compare classification models and investigate precision-recall trade-offs.
- Improve geospatial risk features and transaction anomaly analysis.
- Optimize MongoDB queries and evaluate processing performance at larger data volumes.
- Add secure, production-ready monitoring and alerting.

## 👨‍💻 Author

Developed as a Big Data Systems project demonstrating financial transaction analytics using MongoDB, PySpark MLlib, machine learning, and Streamlit.

## 📄 License

Add a license file if you intend to distribute this project for reuse. Until a license is specified, reuse is subject to applicable copyright restrictions.
