from django import forms
from .models import Article, Book


class ArticleForm(forms.ModelForm):

    subject = forms.TextInput()
    sub_text = forms.TextInput
    description = forms.CharField(widget=forms.Textarea)
    available = forms.BooleanField()

    class Meta:
        model = Article
        fields = "__all__"


class bookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"


# class ArticleForm(forms.Form):

#     subject = forms.CharField()
#     sub_text = forms.CharField()
#     description = forms.CharField(widget=forms.Textarea)
#     available = forms.BooleanField()

#     class Meta:
#         model = Article
#         fields = {
#             "subject",
#             "sub_text",
#             "description",
#             "available",
#         }
