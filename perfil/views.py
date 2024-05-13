from django.shortcuts import render

def home(request):
    if request.method == 'GET':
        return render(request, 'home.html')
    
def gerenciar(request):
    if request.method == 'GET':
        return render(request, 'gerenciar.html')
