import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from whatapp.app.models import Message

__author__ = 'kenneth'


@csrf_exempt
def handle_rapidpro(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        fro = request.POST.get('to')
        id = request.POST.get("id")

        Message.objects.create(direction=Message.OUTGOING, text=text, urn=fro.strip('+'), rapidpro_id=id)
        return HttpResponse(status=200)
    return JsonResponse(json.dumps({'error': 'Bad Request', 'message': 'This activity has been reported'}), status=401)
