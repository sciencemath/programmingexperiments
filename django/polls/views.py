from django.http import HttpResponse

def index(request):
    return HttpResponse('Hello, the answer to everything is 42')