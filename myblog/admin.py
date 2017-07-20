from django.contrib import admin
from django import forms
from myblog.models import Post, Comment, Blog

# Register your models here.

class PostCreationForm(forms.ModelForm):

    title = forms.CharField(error_messages = {'required': 'title needed'})
    summery = forms.CharField(widget=forms.Textarea, error_messages = {'required': 'summery needed'})
    text = forms.CharField(widget=forms.Textarea, error_messages = {'required': 'text needed'})

    class Meta:
        model = Post
        fields = ('title', 'summery', 'text',)

    def save(self, commit=True):
        post = super(PostCreationForm, self).save(commit=False)
        if commit:
            post.save()
        return post


class PostGetForm(forms.ModelForm):
    id = forms.IntegerField(error_messages={'required': 'id needed'})

    class Meta:
        model = Post
        fields = ('id', )



class BlogGetForm(forms.Form):
    count = forms.IntegerField(required=False)
    offset = forms.IntegerField(required=False)





class CommentCreationForm(forms.ModelForm):
    post_id = forms.IntegerField(error_messages = {'required': 'post id needed'})
    text = forms.CharField(widget=forms.Textarea, error_messages = {'required': 'text needed'})

    class Meta:
        model = Comment
        fields = ['text', 'post_id']


    def save(self, commit=True):
        comment = super(CommentCreationForm, self).save(commit=False)
        if commit:
            comment.save()
        return comment



class CommentGetForm(forms.Form):
    post_id = forms.IntegerField(error_messages={'required': 'post id needed'})
    count = forms.IntegerField(required=False)
    offset = forms.IntegerField(required=False)




class BlogAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'id', 'posts_words']
    list_filter = ['name', 'author']
    search_fields = ['name']

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'blog', 'id']
    list_filter = ['blog__name', 'blog__author']
    search_fields = ['title', 'blog__name']

class CommentAdmin(admin.ModelAdmin):
    list_display = [ 'text', 'post','date']
    list_filter = ['post__title', 'post__blog__name']
    search_fields = ['text', 'post__title','post__blog__name']

admin.site.register(Blog, BlogAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)