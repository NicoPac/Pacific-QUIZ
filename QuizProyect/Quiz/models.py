from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

import random


class QuizUsuario(models.Model):

    usuario = models.OneToOneField(User, on_delete = models.CASCADE)
    puntaje_total = models.DecimalField(verbose_name = 'Puntaje Total', default = 0, decimal_places = 1, max_digits = 10)

    def crearIntentos(self, pregunta):
        
        intento = PreguntasRespondidas(pregunta = pregunta, quiz_usuario = self)
        intento.save()

    def obtenerNuevasPreguntas(self):
        respondidas = PreguntasRespondidas.objects.filter(quiz_usuario = self).values_list('pregunta__pk', flat = True)
        preguntas_restantes = Pregunta.objects.exclude(pk__in = respondidas)

        if not preguntas_restantes.exists():
            return None
        return random.choice(preguntas_restantes)

    def validarIntentos(self, pregunta_respondida, respuesta_seleccionada):

        if pregunta_respondida.pregunta_id != respuesta_seleccionada.pregunta_id:
            return

        pregunta_respondida.respuesta_seleccionada = respuesta_seleccionada

        if respuesta_seleccionada.correcta is True:

            pregunta_respondida.correcta = True
            
            pregunta_respondida.puntaje_obtenido = respuesta_seleccionada.pregunta.max_puntaje

            pregunta_respondida.respuesta = respuesta_seleccionada

        else:
            pregunta_respondida.respuesta = respuesta_seleccionada

        pregunta_respondida.save()

        self.actualizarPuntaje()

    def actualizarPuntaje(self):

        puntaje_actualizado = self.intentos.filter(correcta = True).aggregate(
            models.Sum('puntaje_obtenido'))['puntaje_obtenido__sum']
        
        self.puntaje_total = puntaje_actualizado
        self.save()


class Pregunta(models.Model):

    respuestas_permitidas = 1

    texto = models.TextField(verbose_name= "Texto de la pregunta")
    max_puntaje = models.DecimalField(verbose_name = 'Máximo puntaje', default = 3, decimal_places = 2, max_digits = 6)
    
    def __str__(self):
        return self.texto


class ElegirRespuesta(models.Model):

    cantidad_respuestas = 4

    pregunta = models.ForeignKey(Pregunta, related_name='opciones', on_delete=models.CASCADE)
    correcta = models.BooleanField(default= False, null= False, verbose_name='¿Es ésta la pregunta correcta?')
    texto = models.TextField(verbose_name='Texto de la respuesta')

    def __str__(self):
        return self.texto


class PreguntasRespondidas(models.Model):
    
    quiz_usuario = models.ForeignKey(QuizUsuario, on_delete = models.CASCADE, related_name = 'intentos')

    pregunta = models.ForeignKey(Pregunta, on_delete = models.CASCADE)
    
    respuesta = models.ForeignKey(ElegirRespuesta, on_delete = models.CASCADE, null = True)
    
    correcta = models.BooleanField(verbose_name = '¿Es ésta la respuesta correcta?', default = False, null = False)
    
    puntaje_obtenido = models.DecimalField(verbose_name = 'Puntaje obtenido', default = 0, decimal_places = 1, max_digits = 6)
