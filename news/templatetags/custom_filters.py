from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='censor', is_safe=True)
@stringfilter
def censor(value):
    CENSORED_WORDS = [
        'fuck',
        'редиска',
        'черт',
        'дурак',
    ]

    for word in CENSORED_WORDS:
        censored_word = word[0] + '*' * (len(word) - 1)
        value = value.replace(word, censored_word)
        value = value.replace(word.capitalize(), censored_word.capitalize())

    return value
