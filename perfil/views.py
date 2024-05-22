from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.messages import constants
from .models import Conta, Categoria
from .utils import calcula_total


def home(request):
    if request.method == 'GET':
        contas = Conta.objects.all()
        total_contas = calcula_total(contas, 'valor')
        return render(request, 'home.html', {'contas': contas, 'total_contas': total_contas})

def gerenciar(request):
    if request.method == 'GET':
        contas = Conta.objects.all()
        categorias = Categoria.objects.all()
        total_contas = calcula_total(contas, 'valor')
        return render(request, 'gerenciar.html', {'contas': contas, 'total_contas': total_contas, 'categorias': categorias})

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

def deletar_banco(request, id):
    conta = get_object_or_404(Conta, id=id)
    conta.delete()

    messages.add_message(request, constants.SUCCESS, 'Conta removida com sucesso')
    return redirect('/perfil/gerenciar/')


def cadastrar_categoria(request):
    nome = request.POST.get('categoria')
    essencial = bool(request.POST.get('essencial'))

    try:
        categoria = Categoria(
            categoria=nome,
            essencial=essencial,
        )
        categoria.save()
        messages.add_message(request, constants.SUCCESS, 'Categoria cadastrada com sucesso')
        return redirect('/perfil/gerenciar/')
    except Exception as e:
        print(e)
        messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
        return redirect('/perfil/gerenciar/')

def update_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    categoria.essencial = not categoria.essencial

    categoria.save()
    return redirect('/perfil/gerenciar/')
