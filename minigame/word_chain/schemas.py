from pydantic import BaseModel, validator


class StartRequest(BaseModel):
    uid: str
    level: str

    @validator('uid')
    def uid_must_be_not_an_empty_string(cls, value):
        if not len(value):
            raise ValueError('UID cannot be an empty string.')
        return value

    @validator('level')
    def level_must_be_not_an_empty_string(cls, value):
        if not len(value):
            raise ValueError('level cannot be an empty string.')
        return value


class StartResponse(BaseModel):
    uid: str
    text: str
    score: int

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
    last_word: str
    level: str
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

    @validator('last_word')
    def last_word_must_be_not_an_empty_string(cls, value):
        if not value:
            raise ValueError('The last word cannot be an empty string.')
        return value

    @validator('level')
    def level_must_be_not_an_empty_string(cls, value):
        if not value:
            raise ValueError('The level cannot be an empty string.')
        return value


class ReverseContinueRequest(BaseModel):
    uid: str
    q: str
    first_word: str
    level: str
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

    @validator('level')
    def level_must_be_not_an_empty_string(cls, value):
        if not value:
            raise ValueError('The level cannot be an empty string.')
        return value

    @validator('first_word')
    def first_word_must_be_not_an_empty_string(cls, value):
        if not value:
            raise ValueError('The first word cannot be an empty string.')
        return value


class ContinueResponse(BaseModel):
    uid: str
    text: str = ''
    is_game_over: bool = True
    error: str = ''
    error_message: str = ''
