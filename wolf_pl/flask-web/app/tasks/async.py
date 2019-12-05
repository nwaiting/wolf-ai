# coding=utf-8


@celery.task
def my_background_task(arg1, arg2):
    return "Hello"
