from celery.utils.log import get_task_logger
from djcelery_transactions import task
from django_redis import get_redis_connection
import time
from whatapp.app.models import Message
from whatapp.app.send_stack import YowsupSendStack

__author__ = 'kenneth'

logger = get_task_logger(__name__)


@task
def push_out(limit=30):
    r = get_redis_connection()
    key = 'sending_message_task_on'
    if not r.get(key):
        with r.lock(key, timeout=60*4):
            messages = Message.objects.filter(status=Message.QUEUED, direction=Message.OUTGOING).order_by('created_on')[
                           :limit]
            msg = list(messages.values_list('urn', 'text'))
            y = YowsupSendStack(msg)
            y.start()
            messages.update(status=Message.SENT)


@task
def push_to_rapidpro(messages=None):
    if not messages:
        messages = Message.objects.filter(direction=Message.INCOMING, status=Message.QUEUED).order_by('created_on')
    for message in messages:
        message.notify_rapidpro_received()
