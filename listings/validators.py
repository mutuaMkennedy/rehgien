import os
from django.core.exceptions import ValidationError
#custom validator to restrict file types uploaded for model filefields

def validate_video_extension(value):
    ext = os.path.splitext(value.name)[1] #[0] returns path+filename
    valid_extensions = ['.mp4','.mkv']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsurported video format.')
