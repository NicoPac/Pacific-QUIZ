from django import forms

from .models import Pregunta, ElegirRespuesta, PreguntasRespondidas

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import get_user_model, authenticate


User = get_user_model()



class ElegirInlineFormset(forms.BaseInlineFormSet):
    def clean(self):
        super(ElegirInlineFormset, self).clean()

        respuesta_correcta = 0
        for formulario in self.forms:
            if not formulario.is_valid():
                return
            
            if formulario.cleaned_data and formulario.cleaned_data.get('correcta') is True:
                respuesta_correcta += 1
        
        try:
            assert respuesta_correcta == Pregunta.respuestas_permitidas
        except AssertionError:
            raise forms.ValidationError('Solo se permite UNA respuesta correcta')



class FormularioLogin(forms.Form):

    username = forms.CharField(required = True)
    password = forms.CharField(widget = forms.PasswordInput, required = True)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username = username, password = password)

            if not user:
                raise forms.ValidationError('Usuario inexistente')
            
            if not user.check_password(password):
                raise forms.ValidationError('Contraseña incorrecta')
            
            if not user.is_active:
                raise forms.ValidationError('Usuario inactivo, contacte con el administrador')
        
        return super(FormularioLogin, self).clean(*args, **kwargs)



class FormularioRegistro(UserCreationForm):
    email = forms.EmailField(required = True)
    first_name = forms.CharField(required = True)
    last_name = forms.CharField(required = True)

    class Meta:
        model = User

        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
        ]