from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from .serializers import UserSerializer, GroupSerializer
from rest_framework_swagger.views import get_swagger_view
from django.conf.urls import url
import os

from .models import Article, Commentary, ConnectedUsers
from .serializers import ArticleSerializer, CommentarySerializers
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from web_app.tasks import send_email, long_work


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = ArticleSerializer


class CommentaryViewSet(viewsets.ModelViewSet):
    queryset = Commentary.objects.all()
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = CommentarySerializers


def index(request):
    articles = [user for user in Article.objects.all()]
    return render(request, 'index.html', {
        'articles': articles
    })


def room(request, article_id):
    # Send article by id to user
    article = Article.objects.get(id=article_id)
    comments = [c for c in Commentary.objects.filter(article_id=article_id)]
    if article:
        return render(request, 'room.html', {
            'article_id': article_id,
            'comments': comments,
            'article': article
        })
    else:
        return HttpResponse('Wrong Article id')


def users_online(request):
    if request.user.is_authenticated:
        connected_users = [user for user in ConnectedUsers.objects.all()]
        return render(request, 'online.html', {
            'connected_users': connected_users
        })


def send_email_task(request):
    email_task_id = send_email.apply_async(queue='email', args=([os.environ.get('EMAIL_USER')],))
    return HttpResponse(f'The jobs for sending email in progress. Wait for finish. Task id {email_task_id}')


def run_long_task(request):
    ml_task_id = long_work.apply_async(queue='long_task', args=(5,))
    return HttpResponse(f'job id are:  {ml_task_id}')


def list_finished_tasks(request):
    return render(request, 'list.html')
