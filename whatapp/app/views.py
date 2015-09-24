from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from whatapp.app import tasks
from whatapp.app.models import Message

__author__ = 'kenneth'


@csrf_exempt
def handle_rapidpro(request):
    # if request.method == 'POST':
    text = request.GET.get('text')
    fro = request.GET.get('to')
    id = request.GET.get("id")

    m = Message.objects.create(direction=Message.OUTGOING, text=text, urn=fro.strip('+'), rapidpro_id=id)
    tasks.push_out([m.pk])
    return HttpResponse(status=200)
    # return HttpResponse(status=401)
