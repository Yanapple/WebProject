from django.shortcuts import render
from application.models import Profession

# Create your views here.
def index_page(request):
    data = {'profession' : Profession.objects.get(id=1)}
    return render(request, 'index.html', data)

def main_page(request):
    return render(request, 'main_page.html')