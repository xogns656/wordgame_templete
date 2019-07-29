import random

from django.http import HttpResponse, JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from pydantic import ValidationError

from word_chain.models import Words
from word_chain.utils import check_match, check_reverse_match
from word_chain.consts import INITIAL_SOUND_SET
from word_chain.schemas import ContinueRequest, ContinueResponse, StartRequest, StartResponse, ReverseContinueRequest


def word_chain_start(request: WSGIRequest) -> JsonResponse:
    request_content = {
        'uid': request.GET.get('uid'),
        'level': request.GET.get('level')}
    try:
        request = StartRequest(**request_content)
    except ValidationError as error:
        return HttpResponse(error.json(), status=400, content_type='application/json')

    words = Words.objects.filter(word_length__gt=1, noun=True, very_simple=True)
    response_content = {
        'uid': request.uid,
        'text': random.choice(words).content
    }
    response = StartResponse(**response_content)
    return HttpResponse(response.json(), content_type='application/json')


def word_chain_continue(request):
    request_content = {
        'uid': request.GET.get('uid'),
        'q': request.GET.get('q'),
        'last_word': request.GET.get('last-word'),
        'duplications': request.GET.getlist('duplications'),
        'level': request.Get.get('level')
    }
    try:
        request = ContinueRequest(**request_content)
    except ValueError as error:
        return HttpResponse(error.json(), status=400, content_type='application/json')

    response_content = {'uid': request.uid}
    response = ContinueResponse(**response_content)
    if len(request.q) < 2:
        response.error = 'too_short_word'
        response.error_message = 'User sent too short word.'
        response = HttpResponse(response.json(), content_type='application/json')
        return response

    if not check_match(request.last_word, request.q):
        response.error = 'wrong_answer'
        response.error_message = 'User sent wrong answer.'
        response = HttpResponse(response.json(), content_type='application/json')
        return response

    if request.q in request.duplications:
        response.error = 'duplicated_answer'
        response.error_message = 'User sent duplicated answer.'
        response = HttpResponse(response.json(), content_type='application/json')
        return response
    #db에 해당하는 단어가 없는 경우
    if not len(Words.objects.filter(content=request.q)):
        response.error = 'not_found_word'
        response.error_message = 'Cannot find the word from dictionary.'
        return HttpResponse(response.json(), content_type='application/json')
    
    #sdk에서 저장해줘야 한다.
    response.duplications = request.duplications.append(request.q)
    # 플레이어가 말한 단어의 끝말로 시작하는 단어를 db에서 찾는 코드 시작
    if request.q[-1] in INITIAL_SOUND_SET:
        words = Words.objects.filter(word_length__gt=1, word_length__lt=5,
                                     first_sound=INITIAL_SOUND_SET[request.q[-1]], noun=True, very_simple=True) \
            .exclude(content__in=request.duplications)
        if not words:
            response.error = 'user_win'
            response.error_message = 'User won.'
            return HttpResponse(response.json(), content_type='application/json')
        else:
            response.text = random.choice(words).content
            response.is_game_over = False
            return HttpResponse(response.json(), content_type='application/json')

    else:
        words = Words.objects.filter(word_length__gt=1, word_length__lt=5, first_sound=request.q[-1],
                                     noun=True, very_simple=True) \
            .exclude(content__in=request.duplications)
        if not words:
            response.error = 'user_win'
            response.error_message = 'User won.'
            return HttpResponse(response.json(), content_type='application/json')
        else:
            response.text = random.choice(words).content
            response.is_game_over = False
            return HttpResponse(response.json(), content_type='application/json')

def reverse_mode_continue(request):
    request_content = {
        'uid': request.GET.get('uid'),
        'q': request.GET.get('q'),
        'first_word': request.GET.get('first_word'),
        'duplications': request.GET.getlist('duplications'),
        'level': request.Get.get('level')
    }
    try:
        request = ReverseContinueRequest(**request_content)
    except ValueError as error:
        return HttpResponse(error.json(), status=400, content_type='application/json')

    response_content = {'uid': request.uid}
    response = ContinueResponse(**response_content)
    if len(request.q) < 2:
        response.error = 'too_short_word'
        response.error_message = 'User sent too short word.'
        response = HttpResponse(response.json(), content_type='application/json')
        return response

    if not check_reverse_match(request.first_word, request.q):
        response.error = 'wrong_answer'
        response.error_message = 'User sent wrong answer.'
        response = HttpResponse(response.json(), content_type='application/json')
        return response

    if request.q in request.duplications:
        response.error = 'duplicated_answer'
        response.error_message = 'User sent duplicated answer.'
        response = HttpResponse(response.json(), content_type='application/json')
        return response
    #db에 해당하는 단어가 없는 경우
    if not len(Words.objects.filter(content=request.q)):
        response.error = 'not_found_word'
        response.error_message = 'Cannot find the word from dictionary.'
        return HttpResponse(response.json(), content_type='application/json')
    
    #sdk에서 저장해줘야 한다.
    response.duplications = request.duplications.append(request.q)
    # 플레이어가 말한 단어의 끝말로 시작하는 단어를 db에서 찾는 코드 시작
    if request.q[0] in INITIAL_SOUND_SET:
        words = Words.objects.filter(word_length__gt=1, word_length__lt=5,
                                     last_sound=INITIAL_SOUND_SET[request.q[0]], noun=True, very_simple=True) \
            .exclude(content__in=request.duplications)
        if not words:
            response.error = 'user_win'
            response.error_message = 'User won.'
            return HttpResponse(response.json(), content_type='application/json')
        else:
            response.text = random.choice(words).content
            response.is_game_over = False
            return HttpResponse(response.json(), content_type='application/json')

    else:
        words = Words.objects.filter(word_length__gt=1, word_length__lt=5, last_sound=request.q[0],
                                     noun=True, very_simple=True) \
            .exclude(content__in=request.duplications)
        if not words:
            response.error = 'user_win'
            response.error_message = 'User won.'
            return HttpResponse(response.json(), content_type='application/json')
        else:
            response.text = random.choice(words).content
            response.is_game_over = False
            return HttpResponse(response.json(), content_type='application/json')