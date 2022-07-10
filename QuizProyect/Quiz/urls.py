from django.urls import path
from .views import (inicio, registro, 
                    loginUser, logoutUser,
                    homeUser, playGame,
                    resultadoPregunta, tablero)


urlpatterns = [

    path('', inicio, name='inicio'),
    path('home/', homeUser, name='home'),
    path('login/', loginUser, name='login'),
    path('registro/', registro, name='registro'),
    path('logout/', logoutUser, name='logout'),
    path('playGame/', playGame, name='playGame'),
    path('resultado/<int:pregunta_respondida_pk>', resultadoPregunta, name='resultado'),
    path('tablero/', tablero, name='tablero'),

]