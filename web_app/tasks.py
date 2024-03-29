import datetime
from time import sleep
from celery import shared_task, Task
from django.core.mail import EmailMessage
from web_app.models import Article, Commentary
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import os


class CallbackTask(Task):
    def on_success(self, retval, task_id, *args, **kwargs):
        channel_layer = get_channel_layer()
        if not channel_layer:
            print("Not found")
            return

        async_to_sync(channel_layer.group_send)(
            "finished_tasks",
            {
                'type': 'task_message',
                'message': f'Finished Task {task_id}.  Result is {retval}, Args is {args} Current time is {datetime.datetime.now()}'
            }
        )
        print(
            f'Finished Task {task_id}.  Result is {retval}, Args is {args} Current time is {datetime.datetime.now()}')


@shared_task(name="send_email_tasks")
def send_email(emails: list):
    message_content = "hello! its working"
    # print('dorova')
    msg = EmailMessage("lab3", message_content,
                       os.environ.get('EMAIL_USER'), emails)
    msg.send()
    return "successful"


@shared_task(name="some_long_work", base=CallbackTask)
def long_work(time):
    sleep(time)
    count_entity = Article.objects.count()
    return count_entity
