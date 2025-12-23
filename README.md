# ml_retrain_pipeline (Airflow DAG)

Учебный проект: DAG в Apache Airflow для переобучения ML-модели с проверкой метрики, условным деплоем и уведомлением в Telegram.

## Состав проекта

- `dags/ml_retrain_pipeline.py` — DAG `ml_retrain_pipeline`
- `docker-compose.yml` — запуск Airflow + Postgres в Docker
- `plugins/` — папка под плагины (если понадобится)
- `logs/` — логи Airflow (в репозиторий не коммитятся)

## Логика DAG

DAG состоит из задач:

1. `train_model` — имитация обучения модели  
2. `evaluate_model` — оценка качества и сохранение метрик, запись в XCom  
3. `branch_on_metrics` — ветвление:
   - если метрика >= порога → `deploy_model`
   - иначе → `skip_deploy`
4. `deploy_model` — имитация деплоя новой версии
5. `notify_success` — уведомление в Telegram (после успешного деплоя)
6. `end` — финальная задача

### Условие деплоя
Деплой выполняется **только если** `NEW_MODEL_METRIC >= METRIC_THRESHOLD`.

## Переменные окружения

Переменные задаются в `docker-compose.yml`:

- `MODEL_VERSION` — версия модели (показывается в логах/уведомлении)
- `NEW_MODEL_METRIC` — метрика новой модели (float)
- `METRIC_THRESHOLD` — порог для деплоя (float)
- `TELEGRAM_BOT_TOKEN` — токен бота Telegram
- `TELEGRAM_CHAT_ID` — id чата/пользователя для отправки сообщения


Запуск
Поднять сервисы:
```bash
docker compose up -d
```
Открыть Airflow UI:

http://localhost:8080

логин/пароль: admin / admin 

Включить DAG ml_retrain_pipeline и запустить вручную (Trigger DAG).

Уведомление в Telegram
Задача notify_success отправляет сообщение вида:

✅ Новая модель в продакшене: <MODEL_VERSION>
<img width="974" height="582" alt="image" src="https://github.com/user-attachments/assets/cd51a29e-32d9-4def-bffb-35bdde855174" />
<img width="974" height="582" alt="image" src="https://github.com/user-attachments/assets/a23a17dc-4869-40d9-b37a-806337ac3ec9" />
<img width="974" height="582" alt="image" src="https://github.com/user-attachments/assets/69227003-9c11-4c1d-aed1-b517b1bbbc76" />
<img width="590" height="1280" alt="image" src="https://github.com/user-attachments/assets/f81d3049-b2a7-46fa-b3d9-92c81c632fd8" />





