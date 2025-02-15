from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def forbidden_words(value):
	forbidden_words = ['хуй', 'пизда', 'fuck']
	if forbidden_word := _find_forbidden_word(value, forbidden_words):
		raise ValidationError(
			_(f'A forbidden word has been found: {forbidden_word}'),
			code='invalid',
			params={
				'value': value,
				'forbidden_word': forbidden_word
			}
		)

def _find_forbidden_word(text, forbidden_words):
	text = text.lower()
	for forbidden_word in forbidden_words:
		if forbidden_word in text:
			return forbidden_word
