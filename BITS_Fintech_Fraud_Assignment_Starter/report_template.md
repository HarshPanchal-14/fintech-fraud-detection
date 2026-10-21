# Big Data Systems Assignment 2
## Big Data Analytics for Financial Fraud Detection Using MongoDB, PySpark and Machine Learning

**Course:** CC ZG522 — Big Data Systems  
**Assignment:** 2 — Big Data Systems Implementation & Analytics  
**Student name / ID:** [Fill in]  
**Date:** [Fill in]

## 1. Abstract
This project implements a hybrid big-data workflow for financial transaction risk analysis. MongoDB stores transaction documents and indexes frequently queried fields. Python retrieves the documents and passes them to Apache Spark, where data preparation and a Random Forest classification pipeline are executed using Spark MLlib. A Streamlit dashboard presents transaction summaries, risk scores, and evaluation metrics. The dataset in this prototype is synthetic; therefore, findings demonstrate implementation behavior and must not be interpreted as real-world fraud-detection performance.

## 2. Problem statement
Payment systems process transactions with different amounts, locations, merchant categories, devices, and customer histories. Reviewing every transaction manually is costly. The objective is to build a prototype that identifies transactions with patterns associated with a synthetic fraud label and summarizes risk for analyst review.

## 3. Objectives
- Store semi-structured transaction records in MongoDB.
- Apply indexes to transaction, customer, and label fields.
- Read records into PySpark for feature preparation and distributed model training.
- Train and evaluate a Random Forest classifier with Spark MLlib.
- Persist predictions as an output artifact and visualize findings in a dashboard.
- Discuss architecture trade-offs, limitations, and future improvements.

## 4. Dataset and schema
The included generator creates 20,000 synthetic records with transaction ID, customer ID, amount, hour, distance, account age, device-change flag, international flag, merchant category, latitude, longitude, and a binary synthetic label. The generator uses a fixed random seed for repeatability. The labels are rule-generated and are not verified fraud incidents.

**Actual dataset row count:** [Fill in after execution]  
**Synthetic positive-label rate:** [Copy from generator output]  
**Missing/duplicate checks:** [Record actual results]

## 5. Architecture and technology
Describe MongoDB as the document store; PyMongo as the Python integration layer; PySpark DataFrames for preparation; Spark MLlib for Random Forest training; and Streamlit/Plotly for reporting. Include your architecture diagram and screenshots. Note that this implementation uses PyMongo to bridge MongoDB and Spark rather than the Mongo-Spark Connector.

## 6. Implementation methodology
1. Generate repeatable synthetic data.
2. Insert documents into MongoDB and create indexes.
3. Read transaction documents from MongoDB.
4. Cast the label, remove incomplete rows, index merchant category, and assemble feature vectors.
5. Split the data into 80% training and 20% testing using a fixed seed.
6. Train a Random Forest classifier.
7. Evaluate with ROC AUC, accuracy, weighted precision, weighted recall, and F1.
8. Export test predictions and render the dashboard.

## 7. Results
Paste the real output from `metrics.json` here. Do not invent metrics.

| Metric | Actual result |
|---|---|
| Records loaded | [Fill in] |
| Training rows | [Fill in] |
| Test rows | [Fill in] |
| ROC AUC | [Fill in] |
| Accuracy | [Fill in] |
| Weighted precision | [Fill in] |
| Weighted recall | [Fill in] |
| F1 | [Fill in] |

Discuss the class balance and why precision/recall for the fraud class and a confusion matrix should be examined before any operational use. Add observations from your own dashboard.

## 8. Screenshots / evidence
Insert genuine screenshots captured from your own environment:
1. MongoDB database and transaction collection count.
2. MongoDB indexes.
3. Terminal output from synthetic data generation.
4. Successful MongoDB ingestion.
5. Spark model training and actual evaluation metrics.
6. Streamlit dashboard overview.
7. Highest-risk transactions table.
8. Optional cluster / Spark UI evidence if you ran a multi-node setup.

Caption every screenshot with the tool, action, and observation. Remove connection strings, passwords, tokens, and personal information.

## 9. Discussion: compute placement
MongoDB is appropriate for document storage, indexing, and operational retrieval. Spark is appropriate for feature processing and model training over larger datasets. Transferring all records from MongoDB to the driver through PyMongo is convenient for a coursework-sized dataset, but it is not ideal for very large datasets because it centralizes the read in one Python process. For larger deployments, evaluate the Mongo-Spark Connector or a partitioned extraction strategy, and test performance rather than assuming Spark is automatically faster.

## 10. Limitations and future work
- Synthetic labels do not represent confirmed fraud.
- Random train/test split is not a time-based evaluation.
- Geographic coordinates are random synthetic points and do not imply real locations.
- Add class-specific precision, recall, PR-AUC, and a confusion matrix.
- Use temporal validation, leakage checks, explainability, threshold tuning, and a real permitted dataset before any real-world use.
- For the required two-node lab outcome, document an actual two-node cluster run if available; local[*] is local parallel execution, not proof of a two-node cluster.

## 11. Conclusion
Summarize only the implementation and measured results you actually obtained. Explain what MongoDB contributed, what Spark contributed, and how the dashboard supports analyst review.

## References
- BITS Pilani, Big Data Systems Assignment 2, CC ZG522, First Semester 2026–2027.
- Apache Spark MLlib documentation: https://spark.apache.org/docs/latest/ml-guide.html
- MongoDB Python driver documentation: https://www.mongodb.com/docs/languages/python/pymongo-driver/current/
- Streamlit documentation: https://docs.streamlit.io/
