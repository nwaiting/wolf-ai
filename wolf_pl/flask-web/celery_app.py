from time import sleep
from celery import Celery

celery = Celery("service", broker="redis://localhost:6333/0")


@celery.task
def reverse(s):
    sleep(100)
    return s[::-1]


if __name__ == "__main__":
    data = "send mail data"
    print("send_async_email send begin, data = ", data)
    # celery -A celery_app.celery worker -c 1 -l debug
    # celery -A file.obj worker -l info
    reverse.delay("10086")
    print("send_async_email send done")