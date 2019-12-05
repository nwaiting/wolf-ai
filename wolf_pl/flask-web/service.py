# coding=utf8

from flask import Flask, jsonify
from celery import Celery
from time import sleep

app = Flask(__name__)
app.config['broker'] = "redis://localhost:6333/0"
# broker_url
app.config['result_backend'] = "redis://localhost:6333/0"

celery = Celery(app.name, broker=app.config['broker'], result_backend=app.config['result_backend'])
celery.conf.update(app.config)

"""
    定义实现任务逻辑
"""
@celery.task(bind=True)
def send_async_email(self):
    """do task"""
    return "task"


@celery.task(bind=True)
def long_task(self):
    for i in range(1000):
        sleep(1)
        self.update_state(state="progress")
    return {"status":'task completed'}


"""
    #调用任务
"""
@app.route('/', methods=['GET'])
def app_index():
    is_send_quick = 0
    if not is_send_quick:
        data = "send mail data"
        send_async_email.delay(data)
    else:
        data = "semd mail data"
        # send in one minute
        # 任务函数中有参数的，通过args参数传递
        send_async_email.apply_async(args=[data], countdown=60)


@app.route('/longtask', methods=["GET"])
def app_longtask():
    long_task.make_async()
    return jsonify({"msg":"success"}), 200


"""
    #查询任务
"""
@app.route("/status/<task_id>", methods=["GET"])
def taskstatus(task_id):
    task = long_task.AsyncResult(task_id)
    # task.state  PENDING、FAILURE
    print("{}".format(task))
    response = {'state': task.state}
    return jsonify(response)
    

if __name__ == "__main__":
    data = "send mail data"
    print("send_async_email send begin, data = ", data)
    send_async_email.delay(data)
    send_async_email.apply_async(args=[data], countdown=60)
    print("send_async_email send done")