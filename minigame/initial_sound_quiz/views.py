import random

from django.http import HttpResponse, JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from pydantic import ValidationError

from initial_sound_quiz.models import Words, Session
from initial_sound_quiz.schemas import ContinueRequest, ContinueResponse, InfiniteContinueResponse, StartRequest, StartResponse, InfiniteContinueRequest, NextStageRequest


# game over 후의 start와 continue start에 대한 구별 필요
def initial_sound_game_start(request: WSGIRequest) -> JsonResponse:
    #print("request",request)
    request_content = {
        'uid': request.GET.get('uid'),
        'level': request.GET.get('level')
    }
    # 모드, 난이도에 대한 정보를 받아서 분기 처리할 수 있게

    try:
        request = StartRequest(**request_content)
    except ValidationError as error:
        return HttpResponse(error.json(),
                            status=400,
                            content_type='application/json')

    if request.level == 'easy':
        words = Words.objects.filter(word_length__gt=1,
                                     word_length__lt=4,
                                     noun=True,
                                     very_simple=True)
        print(words)
        if not Session.objects.filter(uid=request.uid):
            Session.objects.create(uid=request.uid)
            userInfo = Session.objects.filter(uid=request.uid)
            print('new?')
            score = userInfo.values()[0]['init_easy']
        else:
            userInfo = Session.objects.filter(uid=request.uid)
            print('old?')
            score = userInfo.values()[0]['init_easy']
        print(Session.objects.all().values())
        response_content = {
            'uid': request.uid,
            'text': random.choice(words).consonants,
            'hint': 3,
            'hintGiven': 0,
            'score': score
        }
    else:
        words = Words.objects.filter(word_length__gt=2,
                                     word_length__lt=7,
                                     noun=True,
                                     very_simple=True)
        print(words)
        response_content = {
            'uid': request.uid,
            'text': random.choice(words).consonants,
            'hint': 3,
            'hintGiven': 0,
            'score': score
        }
    response = StartResponse(**response_content)
    print('------', response)
    return HttpResponse(response.json(), content_type='application/json')


def next_infinite_initial_sound_game(request: WSGIRequest) -> JsonResponse:
    #print("request",request)
    request_content = {
        'uid': request.GET.get('uid'),
        'level': request.GET.get('level'),
        'hint': request.GET.get('hint')
    }
    # 모드, 난이도에 대한 정보를 받아서 분기 처리할 수 있게
    try:
        request = NextStageRequest(**request_content)
    except ValidationError as error:
        return HttpResponse(error.json(),
                            status=400,
                            content_type='application/json')

    if request.level == 'easy':
        words = Words.objects.filter(word_length__gt=1,
                                     word_length__lt=4,
                                     noun=True,
                                     very_simple=True)
        print(words)
        response_content = {
            'uid': request.uid,
            'text': random.choice(words).consonants,
            'hint': request.hint,
            'hintGiven': 0
        }
    else:
        words = Words.objects.filter(word_length__gt=1,
                                     word_length__lt=7,
                                     noun=True,
                                     very_simple=True)
        print(words)
        response_content = {
            'uid': request.uid,
            'text': random.choice(words).consonants,
            'hint': request.hint,
            'hintGiven': 0
        }
    response = StartResponse(**response_content)
    return HttpResponse(response.json(), content_type='application/json')


# 초성퀴즈 모드
def initial_sound_game_continue(request: WSGIRequest) -> JsonResponse:
    request_content = {
        'uid': request.GET.get('uid'),
        'q': request.GET.get('q'),
        'quiz': request.GET.get('quiz'),
        'duplications': request.GET.getlist('duplications'),
        'level': request.GET.get('level')
    }
    #level은 각 게임의 난이도 정보
    #getlist list 형식의 querystring을 처리하기 위한 것
    '''
    def my_view(request):
    duplications = request.GET.getlist('duplications[]')
    '''
    #시도한 초성 답안의 저장소
    #sdk에서 저장하고 있다가, contiunue로 request 할 때 보내줘야 함
    try:
        request = ContinueRequest(**request_content)
    except ValidationError as error:
        return HttpResponse(error.json(),
                            status=400,
                            content_type='application/json')
    else:
        response_content = {'uid': request.uid}

        response = ContinueResponse(**response_content)

        answer_list = Words.objects.filter(content=request.q)

        if not len(answer_list):
            response.error = 'not_found_word'
            response.error_message = 'Cannot find the word from dictionary.'
            response = HttpResponse(response.json(),
                                    content_type='application/json')
            return response
        #request.quiz는 처음에 초성게임 start에서 text로 줬던 초성을 sdk에서 저장하고 있다가
        #request 시에  quiz로 담아 보내준다
        if request.quiz != answer_list[0].consonants:
            response.error = 'wrong_answer'
            response.error_message = 'User sent wrong answer.'
            return HttpResponse(response.json(),
                                content_type='application/json')

        if request.q in request.duplications:
            response.error = 'duplicated_answer'
            response.error_message = 'User sent duplicated answer.'
            return HttpResponse(response.json(),
                                content_type='application/json')

        response.duplications = request.duplications.append(request.q)
        words = Words.objects.filter(consonants=request.quiz, noun=True, very_simple=True) \
            .exclude(content__in=request.duplications)
        # 던져준 초성에 대하여 db 상에 존재하는 모든 단어를 주고 받은 경우 user win
        if not len(words):
            response.error = 'user_win'
            response.error_message = 'User won.'
            return HttpResponse(response.json(),
                                content_type='application/json')
        # db에 아직 답변할 단어가 남아있으면, 해당 단어를 AI가 답변한다
        else:
            response.text = random.choice(words).content
            response.is_game_over = False
            return HttpResponse(response.json(),
                                content_type='application/json')


# 제시어 모드
# 종료 조건 - 틀린 경우, 힌트 갯수 초기화하고 새로운 초성 줘야함
# 맞힌 경우 - 힌트 갯수 유지 후 새로운 초성 줘야한다
def infinite_initial_sound_game_continue(request: WSGIRequest) -> JsonResponse:
    request_content = {
        'uid': request.GET.get('uid'),
        'q': request.GET.get('q'),
        'quiz': request.GET.get('quiz'),
        'hint': request.GET.get('hint'),
        'level': request.GET.get('level'),
        'hintGiven': request.GET.get('hintGiven')
    }
    #level은 각 게임의 난이도 정보
    #getlist는 시도한 초성 답안의 저장소
    #sdk에서 저장하고 있다가, contiunue로 request 할 때 보내줘야 함
    try:
        request = InfiniteContinueRequest(**request_content)
    except ValidationError as error:
        return HttpResponse(error.json(),
                            status=400,
                            content_type='application/json')
    else:
        response_content = {'uid': request.uid}

        response = InfiniteContinueResponse(**response_content)
        if request.hintGiven == 0:
            answer_list = Words.objects.filter(content=request.q)
        else:
            if len(request.quiz) == 2:
                answer_list = Words.objects.filter(word_length=len(
                    request.quiz),
                                                   first_sound=request.quiz[0])
            else:
                answer_list = Words.objects.filter(word_length=len(
                    request.quiz),
                                                   first_sound=request.quiz[0],
                                                   last_sound=request.quiz[-1])
        #힌트를 준 뒤라면,
        if not len(answer_list):
            #틀린 경우
            #게임 종료, 랭킹 창으로 이동하여 답안 보여주기
            words = Words.objects.filter(consonants=request.quiz,
                                         noun=True,
                                         very_simple=True)
            response.text = random.choice(words).content
            return HttpResponse(response.json(),
                                content_type='application/json')
        #request.quiz는 처음에 초성게임 start에서 text로 줬던 초성을 sdk에서 저장하고 있다가
        #request 시에  quiz로 담아 보내준다
        if request.quiz != answer_list[0].consonants:
            words = Words.objects.filter(consonants=request.quiz,
                                         noun=True,
                                         very_simple=True)
            response.text = random.choice(words).content
            return HttpResponse(response.json(),
                                content_type='application/json')

        # 힌트를 준 적 있다면, 앞뒤의 글자로 좁혀진 db 내 단어 중에서 말했을 경우에 user win
        # 힌트를 준 적 없다면, 해당하는 초성의 단어가 db에 있을 경우 user win
        if not len(words):
            response.error = 'user_win'
            response.error_message = 'User won.'
            return HttpResponse(response.json(),
                                content_type='application/json')
        # db에 아직 답변할 단어가 남아있으면, 해당 단어를 AI가 답변한다
        else:
            response.text = random.choice(words).content
            response.is_game_over = False
            return HttpResponse(response.json(),
                                content_type='application/json')


def give_hint(request: WSGIRequest) -> JsonResponse:
    request_content = {
        'uid': request.GET.get('uid'),  #사용자 id
        'q': request.GET.get('q'),  #사용자 입력 단어
        'quiz': request.GET.get('quiz'),  #제시해준 초성
        'hint': request.GET.get('hint'),
        'level': request.GET.get('level'),
        'hintGiven': request.GET.get('hintGiven')
    }
    #level은 각 게임의 난이도 정보
    #getlist는 시도한 초성 답안의 저장소
    #sdk에서 저장하고 있다가, contiunue로 request 할 때 보내줘야 함
    #hintGiven은 0, 1로 구분해야 js, python 모두 인식 가능
    try:
        request = InfiniteContinueRequest(**request_content)
    except ValidationError as error:
        return HttpResponse(error.json(),
                            status=400,
                            content_type='application/json')
    else:
        response_content = {'uid': request.uid}
    if request.hintGiven == 1:
        response.error = 'already_used'
        response.error_message = "you already use hint in this round"
        return HttpResponse(response.json(), content_type='application/json')

    response = InfiniteContinueResponse(**response_content)
    #초성과 일치하는 단어들의 목록을 가져와, 랜덤한 index의 초성, 종성을 준다. 단, 초성이 2글자라면 초성만 준다.
    answer_list = Words.objects.filter(consonants=request.quiz)
    if len(request.quiz) == 2:
        send = request.quiz
        send[0] = random.choice(answer_list).first_sound
        response.text = send
        response.hint = request.hint - 1
        response.hintGiven = 1
        return HttpResponse(response.json(), content_type='application/json')
    else:
        send = request.quiz
        chosenWord = random.choice(answer_list)
        send[0] = chosenWord.first_sound
        send[-1] = chosenWord.last_sound
        response.text = send
        response.hint = request.hint - 1
        response.hintGiven = 1
        return HttpResponse(response.json(), content_type='application/json')
