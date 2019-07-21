from pydantic import BaseModel, validator


class StartRequest(BaseModel):
    uid: str

    @validator('uid')
    def uid_must_be_not_an_empty_string(cls, value):
        if not len(value):
            raise ValueError('UID cannot be an empty string.')
        return value


class StartResponse(BaseModel):
    uid: str
    text: str

    @validator('uid')
    def uid_must_be_not_an_empty_string(cls, value):
        if not len(value):
            raise ValueError('The uid cannot be an empty string.')
        return value

    @validator('text')
    def text_must_be_not_an_empty_string(cls, value):
        if not len(value):
            raise ValueError('The text cannot be an empty string.')
        return value


class ContinueRequest(BaseModel):
    uid: str
    q: str
    quiz: str
    duplications: list = []

    @validator('uid')
    def uid_must_be_not_an_empty_string(cls, value):
        if not value:
            raise ValueError('UID cannot be an empty string.')
        return value

    @validator('q')
    def query_must_be_not_an_empty_string(cls, value):
        if not value:
            raise ValueError('The query cannot be an empty string.')
        return value

    @validator('quiz')
    def quiz_must_be_not_an_empty_string(cls, value):
        if not value:
            raise ValueError('The quiz cannot be an empty string.')
        return value


class ContinueResponse(BaseModel):
    uid: str
    text: str = ''
    is_game_over: bool = True
    error: str = ''
    error_message: str = ''
