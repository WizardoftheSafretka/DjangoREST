from rest_framework.exceptions import ValidationError

forbidden_word = "youtube"

def validate_forbidden_word(value):
	if forbidden_word not in value.lower():
		raise ValidationError(value)