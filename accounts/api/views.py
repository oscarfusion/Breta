from rest_framework import viewsets

from .serializers import UserSerializer
from .permissions import UserPermissions
from ..models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermissions, )

    def perform_create(self, serializer):
        instance = serializer.save()
        password = self.request.DATA.get('password')
        if password:
            instance.is_active = True
            instance.set_password(password)
            instance.save()
        return instance
