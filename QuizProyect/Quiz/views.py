from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from .forms import FormularioRegistro, FormularioLogin

from .models import PreguntasRespondidas, QuizUsuario, Pregunta


def inicio(request):
    
    context = {
        'bienvenido': 'Bienvenido'
    }

    return render(request, 'inicio.html', context)


def homeUser(request):
    return render(request, 'Usuario/home.html')


def loginUser(request):
    
    titulo = 'Login'
    form = FormularioLogin(request.POST or None)

    if form.is_valid():
    
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        usuario = authenticate(username = username, password = password)
        login(request, usuario)
        return redirect('home')
    
    context = {
        'form': form,
        'titulo': titulo,
    }

    return render(request, 'Usuario/login.html', context)


def registro(request):

    head = 'Crear una cuenta'

    if request.method == 'POST':
        form = FormularioRegistro(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    
    else:
        form = FormularioRegistro()
    
    context = {
        'form': form,
        'head': head
    }

    return render(request, 'Usuario/registro.html', context)


def logoutUser(request):
    logout(request)
    return redirect('/')


def playGame(request):

    try:
        QuizUser, created = QuizUsuario.objects.get_or_create(usuario = request.user)
    except :
        return redirect('/login')

    if request.method == 'POST':
        
        pregunta_pk = request.POST.get('pregunta_pk')
        pregunta_respondida = QuizUser.intentos.select_related('pregunta').get(pregunta__pk = pregunta_pk)
        respuesta_pk = request.POST.get('respuesta_pk')

        try:
            opcion_seleccionada = pregunta_respondida.pregunta.opciones.get(pk = respuesta_pk)
        
        except ObjectDoesNotExist:
            raise Http404

        QuizUser.validarIntentos(pregunta_respondida, opcion_seleccionada)

        return redirect('resultado', pregunta_respondida.pk)

    else:

        pregunta = QuizUser.obtenerNuevasPreguntas()

        if pregunta is not None:
            QuizUser.crearIntentos(pregunta)

        context = {
            'pregunta': pregunta

        }
    

    return render(request, 'Play/jugar.html', context)


def resultadoPregunta(request, pregunta_respondida_pk):
    
    respondida = get_object_or_404(PreguntasRespondidas, pk = pregunta_respondida_pk)

    context = {
        'respondida': respondida
    }
    
    return render(request, 'Play/resultados.html', context)


def tablero(request):

    top_usuarios = QuizUsuario.objects.order_by('-puntaje_total')[:10]
    contador = top_usuarios.count()

    context = {
        'usuario_quiz': top_usuarios,
        'contar_user': contador
    }

    return render(request, 'Play/tablero.html', context)