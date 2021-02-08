"""Forms for Blog Posts"""

from django.forms import ModelForm

from .models import Post


class PostForm(ModelForm):
    """Model Form for Post model"""

    class Meta:
        model = Post
        fields = '__all__'
