from rest_framework.exceptions import ValidationError

forbidden_word = "youtube"

def validate_forbidden_word(value):
    """Проверяет, содержит ли значение запрещенное слово"""
    if value and forbidden_word in value.lower():
        raise ValidationError(f"Слово '{forbidden_word}' запрещено")
    return value