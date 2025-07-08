from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'store/index.html')


def about(request):
    return render(request, 'store/about.html')


def contact(request):
    return render(request, 'store/contact.html')