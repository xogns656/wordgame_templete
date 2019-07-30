"""minigame URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from initial_sound_quiz import views as initial_sound_game_view
from word_chain import views as word_chain_view

urlpatterns = [
    path(r'word-chain/start',
         word_chain_view.word_chain_start,
         name="word_chain_start"),
    path(r'word-chain/continue',
         word_chain_view.word_chain_continue,
         name="word_chain_continue"),
    path(r'word-chain/reverse-continue',
         word_chain_view.reverse_mode_continue,
         name="reverse_mode_continue"),
    path(r'initial-sound-quiz/start',
         initial_sound_game_view.initial_sound_game_start,
         name="initial_sound_game_start"),
    path(r'initial-sound-quiz/infinite-next',
         initial_sound_game_view.next_infinite_initial_sound_game,
         name="next_infinite_initial_sound_game"),
    path(r'initial-sound-quiz/infinite-continue',
         initial_sound_game_view.infinite_initial_sound_game_continue,
         name="infinite_initial_sound_game_continue"),
    path(r'initial-sound-quiz/give-hint',
         initial_sound_game_view.give_hint,
         name="give_hint"),
    path(r'initial-sound-quiz/continue',
         initial_sound_game_view.initial_sound_game_continue,
         name="initial_sound_game_continue"),
]
