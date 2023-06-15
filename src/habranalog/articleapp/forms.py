from articleapp.models import * 
from django.forms import ModelForm

class CreateArticleForm(ModelForm):
    class Meta:
        model=Article
        fields=['title','prememo','image']