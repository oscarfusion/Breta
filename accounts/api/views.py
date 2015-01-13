from rest_framework import filters
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import UserSerializer
from .permissions import UserPermissions
from ..models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermissions, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('first_name', 'last_name')

    def perform_create(self, serializer):
        instance = serializer.save()
        password = self.request.DATA.get('password')
        if password:
            instance.is_active = True
            instance.set_password(password)
            instance.save()
        return instance

    def retrieve(self, request, pk=None):
        """
        If provided 'pk' is "me" then return the current user.
        """
        if pk == 'me':
            return Response(UserSerializer(request.user).data)
        return super(UserViewSet, self).retrieve(request, pk)
