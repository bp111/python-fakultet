from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome at the Home Page.")

def about(request):
    return HttpResponse("The About Page.")