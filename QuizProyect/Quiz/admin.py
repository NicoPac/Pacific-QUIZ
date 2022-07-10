from django.contrib import admin

from .forms import ElegirInlineFormset

from .models import PreguntasRespondidas, Pregunta, ElegirRespuesta, QuizUsuario 

class ElegirRespuestaInline(admin.TabularInline):
    can_delete: False
    model = ElegirRespuesta
    max_num = ElegirRespuesta.cantidad_respuestas
    min_num = ElegirRespuesta.cantidad_respuestas
    formset = ElegirInlineFormset


class PreguntaAdmin(admin.ModelAdmin):
    model = Pregunta
    inlines = (ElegirRespuestaInline, )
    list_display = ['texto',]
    search_fields = ['texto','pregunta__texto']


class PreguntasRespondidasAdmin(admin.ModelAdmin):
    list_display = ['pregunta', 'respuesta', 'correcta', 'puntaje']

    class Meta:
        model = PreguntasRespondidas


admin.site.register(PreguntasRespondidas)
admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(ElegirRespuesta)
admin.site.register(QuizUsuario)
