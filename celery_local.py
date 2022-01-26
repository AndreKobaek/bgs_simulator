from celery import Celery
from celery.result import AsyncResult

backend_URL = "redis://localhost"

app = Celery(
    "bgs_simulator",
    broker="pyamqp://",
    backend=backend_URL,
    include=["tasks"],
    accept_content=["pickle"],
    task_serializer="pickle",
)


app.conf.update(
    result_expires=3600,
)


def get_results(id):
    A = AsyncResult(id)
    print(A.failed())
    print(A.get())


if __name__ == "__main__":
    app.start()
