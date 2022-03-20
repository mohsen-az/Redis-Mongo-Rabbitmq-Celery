from time import sleep

from billiard.exceptions import SoftTimeLimitExceeded
from celery import Celery

from celery.schedules import crontab

"""
    Redis broker url: "redis://localhost:6379/0"
    Rabbit broker url: "amqp://guest@localhost:5672/"
"""
broker_url = "amqp://guest@localhost:5672/"
app = Celery(main="tasks", broker=broker_url)

"""
    beat_schedule is a module
    that control run any task 
    in self specific time 
    manage.
    
    app.conf.beat_schedule = {
        "task-name": {
            "task": "the-name-of-task-execute",
            "schedule": "the-frequency-of-execution",
            "args": list[] or tuple() | positional-args
        }
    }
"""
app.conf.beat_schedule = {
    'run-every-5-seconds': {
        'task': 'tasks.run_every_5_seconds',
        'schedule': 5.0,
    },
    'run-every-7-seconds': {
        'task': 'tasks.run_every_7_seconds',
        'schedule': 7.0,
    },
    'run-every-monday-morning': {
        'task': 'tasks.run_every_monday_morning',
        'schedule': crontab(hour=7, minute=30, day_of_week=1, day_of_month="*"),
    },
}
app.conf.timezone = 'Asia/Tehran'


@app.task()
def wait_required_seconds(n):
    try:
        sleep(n)
        return f"Sleep for {n} seconds"
    except SoftTimeLimitExceeded:
        return "Cannot finish task, soft time limit exceeded."


@app.task()
def run_every_5_seconds():
    return f"Run Every 5 Seconds!!!"


@app.task()
def run_every_7_seconds():
    return f"Run Every 7 Seconds!!!"


@app.task()
def run_every_monday_morning():
    return f"Run Every Monday Morning."
