from rest_framework import viewsets

from .serializers import UserSerializer
from .permissions import UserPermissions
from ..models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermissions, )
