from celery import shared_task


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def health_task(self):
    return {"status": "ok"}
