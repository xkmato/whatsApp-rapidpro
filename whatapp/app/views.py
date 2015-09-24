from django.http import HttpResponse
from whatapp.app import tasks
from whatapp.app.models import Message

__author__ = 'kenneth'


def handle_rapidpro(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        fro = request.POST.get('from')
        id = request.POST.get("id")

        m = Message.objects.create(direction=Message.OUTGOING, text=text, urn=fro, rapidpro_id=id)
        tasks.push_out.delay([m.pk])
        return HttpResponse(status=200)
    return HttpResponse(status=401)