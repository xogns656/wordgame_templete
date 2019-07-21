---
description: Initial sound quiz API
---

# Initial Sound Quiz

{% api-method method="get" host="http://0.0.0.0:923" path="/initial-sound-quiz/start" %}
{% api-method-summary %}
Start initial sound quiz
{% endapi-method-summary %}

{% api-method-description %}
This endpoint allows you to start initial sound quiz.
{% endapi-method-description %}

{% api-method-spec %}
{% api-method-request %}
{% api-method-query-parameters %}
{% api-method-parameter name="uid" type="string" required=true %}
User id
{% endapi-method-parameter %}
{% endapi-method-query-parameters %}
{% endapi-method-request %}

{% api-method-response %}
{% api-method-response-example httpCode=200 %}
{% api-method-response-example-description %}
Initial sound quiz successfully started. The `text` is more than a letter and less than five letters \(`2 <= len(text) <= 4`\).
{% endapi-method-response-example-description %}

```javascript
{
    "uid": "UID-you-sent",
    "text": "ㅌㅈ"
}
```
{% endapi-method-response-example %}

{% api-method-response-example httpCode=400 %}
{% api-method-response-example-description %}
`uid` is required
{% endapi-method-response-example-description %}

```javascript
[
    {
        "loc": [
            "uid"
        ],
        "msg": "none is not an allowed value",
        "type": "type_error.none.not_allowed"
    }
]
```
{% endapi-method-response-example %}
{% endapi-method-response %}
{% endapi-method-spec %}
{% endapi-method %}

{% api-method method="get" host="http://0.0.0.0:923" path="/initial-sound-quiz/continue" %}
{% api-method-summary %}
Get next word
{% endapi-method-summary %}

{% api-method-description %}
This endpoint determines whether the user hans sent the appropriate response.
{% endapi-method-description %}

{% api-method-spec %}
{% api-method-request %}
{% api-method-query-parameters %}
{% api-method-parameter name="uid" type="string" required=true %}
User id
{% endapi-method-parameter %}

{% api-method-parameter name="q" type="string" required=true %}
Query user sent
{% endapi-method-parameter %}

{% api-method-parameter name="quiz" type="string" required=true %}
Consonants for quiz
{% endapi-method-parameter %}

{% api-method-parameter name="duplications" type="array" required=false %}
History of initial sound quiz.  
e.g. \['통장', '투자', '토지'\]
{% endapi-method-parameter %}
{% endapi-method-query-parameters %}
{% endapi-method-request %}

{% api-method-response %}
{% api-method-response-example httpCode=200 %}
{% api-method-response-example-description %}

{% endapi-method-response-example-description %}

```javascript
{
    "uid": "test",
    "text": "특종",
    "is_game_over": false,
    "error": "not_found_word / wrong_answer / duplicated_answer / user_win",
    "error_message": ""
}
```
{% endapi-method-response-example %}

{% api-method-response-example httpCode=400 %}
{% api-method-response-example-description %}
`uid`, `q`, `quiz` is required
{% endapi-method-response-example-description %}

```javascript
[
    {
        "loc": [
            "uid"
        ],
        "msg": "UID cannot be an empty string.",
        "type": "value_error"
    }
]
```
{% endapi-method-response-example %}
{% endapi-method-response %}
{% endapi-method-spec %}
{% endapi-method %}

