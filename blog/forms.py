# blog/forms.py
from django import forms
from .models import Post, Comment, HashTag

# Form () : html 에 있는 form 태그
# Model Form [] : model을 사용하는 form
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment 
        fields = ['content']
        # form에 화면 출력과 관련된 부분
        widgets = {
            'content' : forms.Textarea(attrs={'rows' : '3', 'cols' : '35'})
        } # 여기서 어트리뷰트는 태그 속성


class HashTagForm(forms.ModelForm):

    class Meta:
        model = HashTag
        fields = ['name']


