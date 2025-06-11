from django.core.exceptions import ValidationError


def validate_file_size(file):
    if file.size > (100 * 1024):
        raise ValidationError('The file size must not exceed 100 KB')
