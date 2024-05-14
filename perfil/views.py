from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants
from .models import Conta
from django.http import HttpResponse

def home(request):
    if request.method == 'GET':
        return render(request, 'home.html')

def gerenciar(request):
    if request.method == 'GET':
        contas = Conta.objects.all()
        total_contas = 0
        for conta in contas:
            total_contas += conta.valor
        return render(request, 'gerenciar.html', {'contas': contas, 'total_contas': total_contas})

def cadastrar_banco(request):
    if request.method == 'POST':
        apelido = request.POST.get('apelido')
        banco = request.POST.get('banco')
        tipo = request.POST.get('tipo')
        valor = request.POST.get('valor')
        icone = request.FILES.get('icone')
        if len(apelido.strip()) == 0 or len(valor.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Preencha o campo, apelido e valor')
            return redirect('/perfil/gerenciar/')
        try:
            conta = Conta(
                apelido=apelido,
                banco=banco,
                tipo=tipo,
                valor=valor,
                icone=icone
            )
            conta.save()
            messages.add_message(request, constants.SUCCESS, 'Cadastrado com sucesso')
            return redirect('/perfil/gerenciar/')
        except Exception:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('/perfil/gerenciar/')
