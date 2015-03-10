from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.conf import settings
from rest_framework import filters
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .serializers import (
    UserSerializer, DeveloperSerializer, PortfolioProjectSerializer,
    PortfolioProjectAttachmentSerializer, WebsiteSerializer,
)

from .permissions import (
    UserPermissions, DeveloperPermissions, WebsitePermission, PortfolioProjectPermission,
    PortfolioProjectAttachmentPermission
)
from ..models import User, Developer, PortfolioProject, PortfolioProjectAttachment, Website
from .. import email
from .. import mailchimp_api
from .forms import ResetPasswordConfirmForm


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
            # if 'HTTP_REFERER' in self.request.stream.META:
            #     if 'project-owner' in self.request.stream.META['HTTP_REFERER']:
            #         instance.is_active = True
            instance.is_active = False
            instance.set_password(password)
            instance.save()
        email.send_welcome_email(instance)
        email.notify_admins_about_registration(instance)
        if not settings.TESTING:
            mailchimp_api.subscribe_user(instance)
        return instance

    def create(self, request, *args, **kwargs):
        resp = super(UserViewSet, self).create(request, args, kwargs)
        if resp.status_code != 201:
            return resp
        user_id = resp.data['id']
        token, created = Token.objects.get_or_create(user=user_id)
        resp.data['token'] = token.key
        return resp

    def retrieve(self, request, pk=None):
        """
        If provided 'pk' is "me" then return the current user.
        """
        if pk == 'me':
            return Response(UserSerializer(request.user).data)
        return super(UserViewSet, self).retrieve(request, pk)


class DeveloperViewSet(viewsets.ModelViewSet):
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer
    permission_classes = (DeveloperPermissions,)


class PortfolioProjectViewSet(viewsets.ModelViewSet):
    queryset = PortfolioProject.objects.all()
    serializer_class = PortfolioProjectSerializer
    permission_classes = (WebsitePermission,)


class PortfolioProjectAttachmentViewSet(viewsets.ModelViewSet):
    queryset = PortfolioProjectAttachment.objects.all()
    serializer_class = PortfolioProjectAttachmentSerializer
    permission_classes = (PortfolioProjectPermission,)


class WebsiteViewSet(viewsets.ModelViewSet):
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer
    permission_classes = (PortfolioProjectAttachmentPermission,)


class ChangePasswordView(generics.CreateAPIView):
    serializer_class = None
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)

    def create(self, request, *args, **kwargs):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if not form.is_valid():
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        form.save()
        email.send_password_changed_email(request.user)
        return Response({
            'message': 'Password updated.'
        }, status=status.HTTP_200_OK)


class ResetPasswordView(generics.CreateAPIView):
    serializer_class = None
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)

    def create(self, request, *args, **kwargs):
        form = PasswordResetForm(request.POST)
        if not form.is_valid():
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        form.save(
            request=request,
            email_template_name='emails/accounts/reset_password.html',
            domain_override=settings.DOMAIN
        )
        return Response({
            'success': True
        }, status=status.HTTP_200_OK)


class ResetPasswordConfirmView(generics.CreateAPIView):
    serializer_class = None
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)

    def create(self, request, *args, **kwargs):
        form = ResetPasswordConfirmForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return Response({
                'success': True
            }, status=status.HTTP_200_OK)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
