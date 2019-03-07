#author:Haoqiu Wu Time 19.2.25
from django import forms
from .models import Comment
from .models import Article

from haystack.forms import SearchForm

class ShareEmailForm(forms.Form):
    # ref django/2/ref/forms/fields
    # charfiled redered as <input type='text'> in html
    name=forms.CharField(max_length=30)
    email=forms.EmailField()
    to = forms.EmailField()
    # use widget to override default input type, here, input type
    # in replaced from text to textarea
    email_content=forms.CharField(required=False,widget=forms.Textarea)

# create froms dynamically according to the model
class CommentForm(forms.ModelForm):
    # use class Meta to tell django form framwork you want
    # to built which model from nad user fields to explicitly
    # tell which filed you want to buil.
    # The form html input type of those fields are determined by how you define those fields in the model
    # each file in the model has a default corresponding input type
    class Meta:
        model=Comment
        fields=('comment_content',)


class ArticleForm(forms.ModelForm):
    class Meta:
        model=Article
        fields=('title','article_content','label_in_url','tags')

class SearchForm(SearchForm):
    def no_query_found(self):
        return self.searchqueryset.all()
