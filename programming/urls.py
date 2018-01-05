"""programming URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf.urls import url
from programming import views as programming_views
from rest_framework import serializers, permissions, viewsets
from .models import GameSolution

class GameSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameSolution
        fields = '__all__'


class GameSolutionViewSet(viewsets.ModelViewSet):
    queryset = GameSolution.objects.all()  # TODO: get help with this...
    serializer_class = GameSolutionSerializer
    permission_classes = (permissions.IsAuthenticated)

    def get_queryset(self):
        return GameSolution.objects.filter(creator=self.request.user.student).all()


urlpatterns = [
    path('game/', programming_views.GameSolutionCreateView.as_view(), name='programming game')
]
