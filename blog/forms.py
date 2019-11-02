from .models import Comment
from django.forms import ModelForm

#form to add new comment
class CommentForm(ModelForm):
    class Meta:
        model=Comment
        fields=('text',)