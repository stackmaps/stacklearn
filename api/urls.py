from django.conf.urls import url, include
from django.contrib.auth.models import User
from django.urls import path
from rest_framework import routers, serializers, viewsets

from programming.urls import GameSolutionViewSet

class UserSerializer(serializers.ModelSerializer):
	class Meta:
			model = User
			exclude = ('password')

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

	# overwrite the get_object method so that `@me` returns the currently
	# logged in user.
	def get_object(self):
		pk = self.kwargs.get('pk')

		if pk == "@me":
			return self.request.user

		return super(UserViewSet, self).get_object()

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('programming/solutions', GameSolutionViewSet)

urlpatterns = router.urls
