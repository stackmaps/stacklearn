from django.conf import settings
from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
			model = settings.AUTH_USER_MODEL
			fields = ('url', 'username', 'email', 'is_staff')

class UserViewSet(viewsets.ModelViewSet):
	queryset = settings.AUTH_USER_MODEL.objects.all()
	serializer_class = UserSerializer

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
	url(r'^api/', include(router.urls))
]
