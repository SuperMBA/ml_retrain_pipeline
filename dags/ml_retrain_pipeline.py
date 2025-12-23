from __future__ import annotations

import os
import json
import requests
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.trigger_rule import TriggerRule

MODEL_VERSION = os.getenv("MODEL_VERSION", "v1.0.0")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

METRIC_THRESHOLD = float(os.getenv("METRIC_THRESHOLD", "0.80"))
METRICS_PATH = os.getenv("METRICS_PATH", "/opt/airflow/metrics.json")


def train_model():
    print("Обучение модели завершено.")
    print(f"MODEL_VERSION = {MODEL_VERSION}")


def evaluate_model(**context):
    metric = float(os.getenv("NEW_MODEL_METRIC", "0.85"))

    payload = {
        "model_version": MODEL_VERSION,
        "metric_name": "quality_score",
        "metric_value": metric,
        "threshold": METRIC_THRESHOLD,
        "passed": metric >= METRIC_THRESHOLD,
    }

    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print("Оценка модели завершена:")
    print(json.dumps(payload, ensure_ascii=False, indent=2))

    context["ti"].xcom_push(key="metric_payload", value=payload)


def branch_on_metrics(**context) -> str:
    ti = context["ti"]
    payload = ti.xcom_pull(task_ids="evaluate_model", key="metric_payload")

    passed = bool(payload.get("passed"))
    return "deploy_model" if passed else "skip_deploy"


def deploy_model():
    print(f"Деплой модели {MODEL_VERSION} выполнен успешно.")


def notify_success():
    # Если Telegram не настроен — просто пишем в лог, чтобы DAG не падал.
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print(f"[NOTIFY] Новая модель в продакшене: {MODEL_VERSION} (Telegram не настроен)")
        return

    text = f"✅ Новая модель в продакшене: {MODEL_VERSION}"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    resp = requests.get(url, params={"chat_id": TELEGRAM_CHAT_ID, "text": text}, timeout=20)
    resp.raise_for_status()
    print("Уведомление в Telegram отправлено.")


with DAG(
    dag_id="ml_retrain_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["mlops", "retraining"],
) as dag:

    train = PythonOperator(task_id="train_model", python_callable=train_model)
    evaluate = PythonOperator(task_id="evaluate_model", python_callable=evaluate_model)

    branch = BranchPythonOperator(task_id="branch_on_metrics", python_callable=branch_on_metrics)

    deploy = PythonOperator(task_id="deploy_model", python_callable=deploy_model)
    skip = EmptyOperator(task_id="skip_deploy")

    notify = PythonOperator(
        task_id="notify_success",
        python_callable=notify_success,
        trigger_rule=TriggerRule.ALL_SUCCESS,
    )

    end = EmptyOperator(
        task_id="end",
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS,
    )

    train >> evaluate >> branch
    branch >> deploy >> notify >> end
    branch >> skip >> end
