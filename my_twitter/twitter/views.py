from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, request
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views.generic import CreateView, FormView

from .models import Tweet
from .forms import AddPostForm, SignUpForm


class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
        else:
            return HttpResponse(str(form.errors))


class ShowAllPostsView(View):
    def get(self, request):
        posts = Tweet.objects.all()
        return render(request, "base.html", {'posts': posts})


class AddPostView(FormView, View):
    template_name = 'twitter/add_post.html'
    form_class = AddPostForm
    success_url = '/'
    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        object.save()
        return super(AddPostView, self).form_valid(form)

class DeletePost(View):
    def get(self, request, post_id):
        tweet = Tweet.objects.get(pk=post_id)
        tweet.delete()
        return redirect('/')
