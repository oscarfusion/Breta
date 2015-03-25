from django.contrib.auth.forms import PasswordChangeForm
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
    PortfolioProjectAttachmentSerializer, WebsiteSerializer, EmailSerializer
)

from .permissions import (
    UserPermissions, DeveloperPermissions, WebsitePermission, PortfolioProjectPermission,
    PortfolioProjectAttachmentPermission, EmailPermissions
)
from ..models import User, Developer, PortfolioProject, PortfolioProjectAttachment, Website, Email
from .. import email
from .. import mailchimp_api
from ..utils import get_client_ip
from .forms import ResetPasswordConfirmForm, EmailForm, InviteUserForm, ResetPasswordForm


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermissions, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('first_name', 'last_name')

    def perform_create(self, serializer):
        # referral_code = serializer.initial_data['referral_code']
        referral_code = serializer.initial_data.get('referral_code', None)
        if referral_code:
            try:
                referrer = User.objects.get(referral_code=referral_code)
            except User.DoesNotExist:
                referrer = None

            try:
                email_obj = Email.objects.get(referral_code=referral_code)
            except:
                email_obj = None
            referrer_email = email_obj.email if email_obj else None
            instance = serializer.save(referrer=referrer, referral_code=None, referrer_email=referrer_email)
        else:
            instance = serializer.save()
        password = self.request.DATA.get('password')
        if password:
            # if 'HTTP_REFERER' in self.request.stream.META:
            #     if 'project-owner' in self.request.stream.META['HTTP_REFERER']:
            #         instance.is_active = True
            instance.is_active = False
            instance.set_password(password)
        try:
            email_obj = Email.objects.get(email=instance.email)
        except Email.DoesNotExist:
            email_obj = None
        if email_obj:
            instance.referral_code = email_obj.referral_code
        instance.ip_address = get_client_ip(self.request)
        instance.save()
        User.objects.filter(referrer_email=instance.email).update(referrer=instance)
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
        form = ResetPasswordForm(request.POST)
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


class EmailViewSet(viewsets.ModelViewSet):
    serializer_class = EmailSerializer
    permission_classes = (EmailPermissions,)
    queryset = Email.objects.all()

    def create(self, request, *args, **kwargs):
        form = EmailForm(request.data)
        instance = None
        if form.is_valid():
            instance = form.save()
            instance.ip_address = get_client_ip(request)
            instance.save()
        else:
            try:
                instance = Email.objects.get(email=form.data['email'])
            except Email.DoesNotExist:
                instance = None
        if instance:
            return Response(EmailSerializer(instance).data, status=status.HTTP_200_OK)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class InvityByEmailView(generics.CreateAPIView):
    serializer_class = None
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)

    def create(self, request, *args, **kwargs):
        form = InviteUserForm(request.POST)
        if form.is_valid():
            form.save()
            return Response({
                'success': True
            }, status=status.HTTP_200_OK)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
