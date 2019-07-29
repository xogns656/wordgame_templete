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

class NextStageRequest(BaseModel):
    uid: str
    level: str
    hint: int
    hintGiven: int

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
    hint: int 
    hintGiven: int

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

    @validator('hint')
    def hint_must_be_not_an_empty_string(cls, value):
        if not len(value):
            raise ValueError('The hint cannot be an empty Integer')
        return value

    @validator('hintGiven')
    def hintGiven_must_be_not_an_empty_boolean(cls, value):
        if not len(value):
            raise ValueError('The hintGiven cannot be an empty Integer')
        return value    


class ContinueRequest(BaseModel):
    uid: str
    q: str
    quiz: str
    duplications: list = []
    level: str

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

    @validator('level')
    def level_must_be_not_an_empty_string(cls, value):
        if not value:
            raise ValueError('The level cannot be an empty string.')
        return value

class InfiniteContinueRequest(BaseModel):
    uid: str
    q: str
    quiz: str
    hint: int
    level: str
    hintGiven : int

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

    @validator('hint')
    def hint_must_be_not_an_empty_number(cls, value):
        if not value:
            raise ValueError('The hint cannot be an empty number.')
        return value

    @validator('level')
    def level_must_be_not_an_empty_string(cls, value):
        if not value:
            raise ValueError('The level cannot be an empty string.')
        return value
        
    @validator('hintGiven')
    def hintGiven_be_not_an_empty_integer(cls, value):
        if not value:
            raise ValueError('The hintGiven cannot be an empty integer.')
        return value    
    


class ContinueResponse(BaseModel):
    uid: str
    text: str = ''
    is_game_over: bool = True 
    duplications: list = []
    error: str = ''
    error_message: str = ''

class InfiniteContinueResponse(BaseModel):
    uid: str
    text: str = ''
    hint: int 
    hintGiven : int
    error: str = ''
    error_message: str = ''
