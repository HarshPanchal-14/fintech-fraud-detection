# BITS Pilani Big Data Systems Assignment 2 — Fintech Fraud Analytics

## Scope
This prototype demonstrates a hybrid MongoDB + PySpark workflow: synthetic transaction generation, MongoDB storage and indexing, Spark MLlib model training, evaluation, exported predictions, and a Streamlit dashboard.

**Academic honesty / limitations:** labels are generated synthetically from a rule-based probability. The model learns patterns related to those synthetic labels. Do not describe the data as real banking data or the metrics as evidence of production fraud-detection performance. Run the code yourself and report the actual values it produces.

## Requirements
- Python 3.10 or 3.11 recommended
- Java compatible with your PySpark release (Java 17 is a common choice for Spark 3.5)
- MongoDB Community Server running locally, or a MongoDB Atlas connection string
- At least 8 GB RAM recommended for a comfortable local run; reduce N in `generate_data.py` if needed

## Setup (Windows)
1. Install Python and Java, then install/start MongoDB Community Server or create an Atlas cluster.
2. Extract this folder and open a terminal in it.
3. Create a virtual environment:
   - Windows: `py -m venv .venv` then `.venv\\Scripts\\activate`
   - Linux/WSL: `python3 -m venv .venv` then `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and edit `MONGODB_URI` if needed. Never submit your real credentials.
6. Generate sample data: `python generate_data.py`
7. Load MongoDB: `python ingest_mongo.py`
8. Train and evaluate with Spark: `python train_model.py`
9. Launch dashboard: `streamlit run dashboard.py`

If using Atlas, allow your current IP address in Atlas Network Access and use a database user. Avoid exposing credentials in screenshots or your report.

## Files
- `generate_data.py`: deterministic synthetic dataset generator (20,000 rows)
- `ingest_mongo.py`: loads records and creates indexes
- `train_model.py`: reads from MongoDB via PyMongo, trains a Spark MLlib Random Forest pipeline, exports test predictions and metrics
- `dashboard.py`: interactive Streamlit analytics dashboard
- `metrics.json`, `predictions.csv`, `spark_fraud_model/`: generated after running the model script
- `report_template.md`: report structure to complete with actual outputs

## Architecture note
This implementation integrates MongoDB and Spark through Python/PyMongo. It is a hybrid architecture, but it does **not** use the Mongo-Spark Connector. If your instructor explicitly expects that connector, the data-ingestion stage must be adapted and the connector version matched to your Spark and Scala versions.

## Suggested validation
- Check the MongoDB document count equals 20,000 (or the configured N).
- Check the split sizes sum to the number of valid rows.
- Record the metrics printed by `train_model.py`.
- Compare confusion matrix and fraud-class precision/recall if you add class-specific metrics; weighted metrics alone can hide minority-class errors.
- Capture screenshots of successful runs and your own dashboard.
