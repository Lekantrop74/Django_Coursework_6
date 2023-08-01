from django import forms

from blog.models import BlogPost


class BlogPostFilterForm(forms.Form):
    is_published = forms.BooleanField(label='Только опубликованные', required=False)


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'preview', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'preview': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
