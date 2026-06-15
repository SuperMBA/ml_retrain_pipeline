# ML Retraining Pipeline with Apache Airflow

## Project Overview

This project demonstrates an automated ML retraining workflow using Apache Airflow.

The pipeline simulates a typical machine learning lifecycle scenario: a new model is trained, evaluated against a predefined metric threshold, conditionally deployed and followed by a Telegram notification if deployment succeeds.

The project focuses on practical MLOps concepts such as workflow orchestration, metric-based branching, conditional deployment logic and notification integration.

## Key Features

* Apache Airflow DAG for ML retraining orchestration
* Docker Compose setup with Airflow and PostgreSQL
* Simulated model training step
* Model evaluation with metric tracking
* Conditional deployment based on a metric threshold
* Branching logic using Airflow
* Telegram notification after successful deployment
* Environment-based configuration

## Repository Structure

```text
ml_retrain_pipeline/
├── dags/
│   └── ml_retrain_pipeline.py     # Airflow DAG definition
├── docker-compose.yml             # Airflow + PostgreSQL local setup
├── plugins/                       # Optional Airflow plugins
├── logs/                          # Airflow logs, not committed to Git
└── README.md                      # Project documentation
```

## DAG Logic

The Airflow DAG is named:

```text
ml_retrain_pipeline
```

The workflow consists of the following tasks:

1. `train_model`
   Simulates training of a new ML model.

2. `evaluate_model`
   Evaluates the new model, saves the metric and passes the result through XCom.

3. `branch_on_metrics`
   Checks whether the new model metric reaches the required threshold.

4. `deploy_model`
   Simulates deployment of the new model version if the metric condition is satisfied.

5. `skip_deploy`
   Skips deployment if the new model does not meet the required quality threshold.

6. `notify_success`
   Sends a Telegram notification after successful deployment.

7. `end`
   Final task of the DAG.

## Deployment Condition

The deployment step is executed only if the new model reaches or exceeds the predefined metric threshold:

```text
NEW_MODEL_METRIC >= METRIC_THRESHOLD
```

If the metric is lower than the threshold, the DAG follows the `skip_deploy` branch and the new model is not deployed.

This logic reflects a common MLOps pattern: a model should only be promoted if it satisfies a predefined quality criterion.

## Environment Variables

The pipeline is configured through environment variables defined in `docker-compose.yml`.

| Variable             | Description                                             |
| -------------------- | ------------------------------------------------------- |
| `MODEL_VERSION`      | Version of the new model shown in logs and notification |
| `NEW_MODEL_METRIC`   | Metric value of the new model                           |
| `METRIC_THRESHOLD`   | Minimum metric value required for deployment            |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token                                      |
| `TELEGRAM_CHAT_ID`   | Telegram chat or user ID for notifications              |

Sensitive values such as Telegram tokens should not be committed to a public repository. In production-like projects, they should be managed through environment variables, secrets or a secure configuration system.

## Local Run

Start the services:

```bash
docker compose up -d
```

Open the Airflow UI:

```text
http://localhost:8080
```

Default credentials:

```text
admin / admin
```

Then enable the DAG `ml_retrain_pipeline` and trigger it manually through the Airflow UI.

## Expected Workflow

After triggering the DAG:

1. A new model version is simulated.
2. The model metric is evaluated.
3. The metric is compared with the threshold.
4. If the metric is high enough, deployment is executed.
5. A Telegram notification is sent after successful deployment.
6. If the metric is below the threshold, deployment is skipped.

## Telegram Notification

After successful deployment, the `notify_success` task sends a message in the following format:

```text
✅ New model deployed to production: <MODEL_VERSION>
```

This step demonstrates how Airflow can be integrated with external notification systems for monitoring and operational awareness.

## Screenshots

The screenshots below show the Airflow DAG, task execution and Telegram notification flow.

<img width="974" height="582" alt="Airflow DAG screenshot" src="https://github.com/user-attachments/assets/cd51a29e-32d9-4def-bffb-35bdde855174" />

<img width="974" height="582" alt="Airflow task execution screenshot" src="https://github.com/user-attachments/assets/a23a17dc-4869-40d9-b37a-806337ac3ec9" />

<img width="974" height="582" alt="Airflow pipeline screenshot" src="https://github.com/user-attachments/assets/69227003-9c11-4c1d-aed1-b517b1bbbc76" />

<img width="590" height="1280" alt="Telegram notification screenshot" src="https://github.com/user-attachments/assets/f81d3049-b2a7-46fa-b3d9-92c81c632fd8" />

## Tech Stack

* Apache Airflow
* Python
* Docker
* Docker Compose
* PostgreSQL
* Telegram Bot API
* MLOps workflow orchestration

## MLOps Concepts Demonstrated

This project demonstrates several practical MLOps concepts:

* workflow orchestration with Airflow;
* automated model retraining logic;
* metric-based model promotion;
* conditional deployment;
* branching in DAGs;
* operational notifications;
* environment-based configuration;
* reproducible local infrastructure with Docker Compose.

## Relevance

This project is relevant for ML engineering and MLOps workflows where model retraining, evaluation and deployment decisions need to be automated.

The same logic can be extended to real-world machine learning systems, including healthcare analytics and Medical AI pipelines, where a new model should only be promoted after meeting predefined quality and safety criteria.

## Author

**Margarita Balandina**
Medical Data Scientist | Dentist with German Approbation | MSc Data Science

Focus areas: Medical AI, Healthcare Analytics, Clinical Data, Machine Learning, MedTech and MLOps.
