"""Read MongoDB transactions, train a Spark MLlib model, and export results."""
import os
import json
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator

load_dotenv()
URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB = os.getenv("MONGODB_DB", "fintech_fraud")
COLLECTION = os.getenv("MONGODB_COLLECTION", "transactions")
NUMERIC = ["amount", "hour", "distance_km", "account_age_days", "device_change", "international"]

def main():
    client = MongoClient(URI, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    docs = list(client[DB][COLLECTION].find({}, {"_id": 0}))
    client.close()
    if len(docs) < 100:
        raise RuntimeError("Not enough records. Run generate_data.py and ingest_mongo.py first.")
    pdf = pd.DataFrame(docs)
    spark = (SparkSession.builder.appName("FintechFraudDetection")
             .master(os.getenv("SPARK_MASTER", "local[*]"))
             .config("spark.sql.shuffle.partitions", "8")
             .getOrCreate())
    sdf = spark.createDataFrame(pdf)
    sdf = sdf.withColumn("label", sdf["is_fraud"].cast("double"))
    sdf = sdf.dropna(subset=NUMERIC + ["merchant_category", "label"])
    indexer = StringIndexer(inputCol="merchant_category", outputCol="merchant_idx", handleInvalid="keep")
    assembler = VectorAssembler(inputCols=NUMERIC + ["merchant_idx"], outputCol="features")
    rf = RandomForestClassifier(
        labelCol="label", featuresCol="features", predictionCol="prediction",
        probabilityCol="probability", numTrees=80, maxDepth=8, seed=42
    )
    pipeline = Pipeline(stages=[indexer, assembler, rf])
    train, test = sdf.randomSplit([0.8, 0.2], seed=42)
    model = pipeline.fit(train)
    pred = model.transform(test).cache()

    auc = BinaryClassificationEvaluator(labelCol="label", rawPredictionCol="rawPrediction",
                                        metricName="areaUnderROC").evaluate(pred)
    accuracy = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction",
                                                  metricName="accuracy").evaluate(pred)
    precision = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction",
                                                    metricName="weightedPrecision").evaluate(pred)
    recall = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction",
                                                metricName="weightedRecall").evaluate(pred)
    f1 = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction",
                                            metricName="f1").evaluate(pred)
    metrics = {
        "records_loaded": len(docs), "train_rows": train.count(), "test_rows": test.count(),
        "roc_auc": auc, "accuracy": accuracy, "weighted_precision": precision,
        "weighted_recall": recall, "f1": f1,
        "note": "Synthetic rule-generated labels; metrics demonstrate pipeline behavior, not production fraud performance."
    }
    with open("metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    pred.select("transaction_id", "customer_id", "amount", "merchant_category",
                "is_fraud", "prediction", "probability", "latitude", "longitude") \
        .toPandas().assign(
            risk_score=lambda x: x["probability"].apply(lambda p: float(p[1]) if p is not None else 0.0)
        ).drop(columns=["probability"]).to_csv("predictions.csv", index=False)
    model.write().overwrite().save("spark_fraud_model")
    print(json.dumps(metrics, indent=2))
    print("Saved predictions.csv, metrics.json, and spark_fraud_model/")
    pred.unpersist()
    spark.stop()

if __name__ == "__main__":
    main()
