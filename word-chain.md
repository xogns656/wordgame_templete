---
description: Word chain game API
---

# Word Chain

{% api-method method="get" host="http://0.0.0.0:923" path="/word-chain/start" %}
{% api-method-summary %}
Start word chain
{% endapi-method-summary %}

{% api-method-description %}
This endpoint allows you to start word chain game.
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
Game successfully started.
{% endapi-method-response-example-description %}

```javascript
{
    "uid": "uid-you-sent",
    "text": "글리세린"
}
```
{% endapi-method-response-example %}

{% api-method-response-example httpCode=400 %}
{% api-method-response-example-description %}
`uid` is required.
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

{% api-method method="get" host="http://0.0.0.0:923" path="/word-chain/continue" %}
{% api-method-summary %}
Get next word
{% endapi-method-summary %}

{% api-method-description %}
This endpoint determines whether the user has sent the appropriate response.
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

{% api-method-parameter name="last-word" type="string" required=true %}
Last word that agent sent
{% endapi-method-parameter %}

{% api-method-parameter name="duplications" type="array" required=false %}
History of word chain gam
{% endapi-method-parameter %}
{% endapi-method-query-parameters %}
{% endapi-method-request %}

{% api-method-response %}
{% api-method-response-example httpCode=200 %}
{% api-method-response-example-description %}
User sent appropriate word.
{% endapi-method-response-example-description %}

```javascript
{
    "uid": "UID-you-sent",
    "text": "산탄",
    "is_game_over": false,
    "error": "too_short_word / wrong_answer / duplicated_answer / not_found_word / user_win",
    "error_message": ""
}
```
{% endapi-method-response-example %}

{% api-method-response-example httpCode=400 %}
{% api-method-response-example-description %}
`uid`, `q`, `last-word` is required
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



