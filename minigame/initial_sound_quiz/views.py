import random

from django.http import HttpResponse, JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from pydantic import ValidationError

from initial_sound_quiz.models import Words
from initial_sound_quiz.schemas import ContinueRequest, ContinueResponse, StartRequest, StartResponse


def initial_sound_game_start(request: WSGIRequest) -> JsonResponse:
    request_content = {'uid': request.GET.get('uid')}
    try:
        request = StartRequest(**request_content)
    except ValidationError as error:
        return HttpResponse(error.json(), status=400, content_type='application/json')

    words = Words.objects.filter(word_length__gt=1, word_length__lt=5,
                                 noun=True, very_simple=True)
    response_content = {
        'uid': request.uid,
        'text': random.choice(words).consonants
    }
    response = StartResponse(**response_content)
    return HttpResponse(response.json(), content_type='application/json')


def initial_sound_game_continue(request: WSGIRequest) -> JsonResponse:
    request_content = {
        'uid': request.GET.get('uid'),
        'q': request.GET.get('q'),
        'quiz': request.GET.get('quiz'),
        'duplications': request.GET.getlist('duplications')
    }
    try:
        request = ContinueRequest(**request_content)
    except ValidationError as error:
        return HttpResponse(error.json(), status=400, content_type='application/json')
    else:
        response_content = {
            'uid': request.uid
        }

        response = ContinueResponse(**response_content)

        answer_list = Words.objects.filter(content=request.q)

        if not len(answer_list):
            response.error = 'not_found_word'
            response.error_message = 'Cannot find the word from dictionary.'
            response = HttpResponse(response.json(), content_type='application/json')
            response = HttpResponse(response.json(), content_type='application/json')
            return response

        if request.quiz != answer_list[0].consonants:
            response.error = 'wrong_answer'
            response.error_message = 'User sent wrong answer.'
            return HttpResponse(response.json(), content_type='application/json')

        if request.q in request.duplications:
            response.error = 'duplicated_answer'
            response.error_message = 'User sent duplicated answer.'
            return HttpResponse(response.json(), content_type='application/json')

        request.duplications.append(request.q)
        words = Words.objects.filter(consonants=request.quiz, noun=True, very_simple=True) \
            .exclude(content__in=request.duplications)

        if not len(words):
            response.error = 'user_win'
            response.error_message = 'User won.'
            return HttpResponse(response.json(), content_type='application/json')
        else:
            response.text = random.choice(words).content
            response.is_game_over = False
            return HttpResponse(response.json(), content_type='application/json')
