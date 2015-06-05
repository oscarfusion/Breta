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

from projects.utils import create_demo_project_for_po, create_demo_project_for_developer

from .serializers import (
    UserSerializer, DeveloperSerializer, PortfolioProjectSerializer,
    PortfolioProjectAttachmentSerializer, WebsiteSerializer, UserSearchSerializer
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
            instance.set_password(password)
        try:
            email_obj = Email.objects.get(email=instance.email)
        except Email.DoesNotExist:
            email_obj = None
        if email_obj:
            instance.referral_code = email_obj.referral_code
            email_obj.delete()
        instance.is_active = True
        instance.ip_address = get_client_ip(self.request)
        instance.save()
        User.objects.filter(referrer_email=instance.email).update(referrer=instance)
        email.send_welcome_email(instance)
        email.notify_admins_about_registration(instance)
        if not settings.TESTING:
            mailchimp_api.subscribe_user(instance)
        create_demo_project_for_po(instance)
        return instance

    def perform_update(self, serializer):
        was_subscribed_to_newsletters = serializer.instance.settings.get('receive_newsletters', True)
        instance = serializer.save()
        subscribe_to_newsletters = instance.settings.get('receive_newsletters', True)
        if not was_subscribed_to_newsletters and subscribe_to_newsletters:
            mailchimp_api.subscribe_user(instance)
        elif was_subscribed_to_newsletters and not subscribe_to_newsletters:
            mailchimp_api.unsubscribe_user(instance)

    def check_email(self, email):
        try:
            user = User.objects.get(email=email)
            if user and not user.has_usable_password():
                return user
            else:
                return None
        except User.DoesNotExist:
            return None

    def create(self, request, *args, **kwargs):
        if 'email' in request.data:
            user = self.check_email(request.data['email'])
        else:
            user = None
        if user:
            serializer = self.get_serializer(data=request.data, instance=user)
        else:
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        resp = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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
            return Response(UserSerializer(request.user, context={
                'request': request
            }).data)
        return super(UserViewSet, self).retrieve(request, pk)


class DeveloperViewSet(viewsets.ModelViewSet):
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer
    permission_classes = (DeveloperPermissions,)

    def perform_create(self, serializer):
        instance = serializer.save()
        from projects.models import Project
        # remove project owner's demo project if user is registered as developer
        Project.objects.filter(user=instance.user, is_demo=True).delete()
        # and create demo project for developers
        create_demo_project_for_developer(instance.user)


class PortfolioProjectViewSet(viewsets.ModelViewSet):
    queryset = PortfolioProject.objects.all()
    serializer_class = PortfolioProjectSerializer
    permission_classes = (PortfolioProjectPermission,)


class PortfolioProjectAttachmentViewSet(viewsets.ModelViewSet):
    queryset = PortfolioProjectAttachment.objects.all()
    serializer_class = PortfolioProjectAttachmentSerializer
    permission_classes = (PortfolioProjectAttachmentPermission,)


class WebsiteViewSet(viewsets.ModelViewSet):
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer
    permission_classes = (WebsitePermission,)


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
            email.send_password_reset_confirmation_email(form.get_user())
            return Response({
                'success': True
            }, status=status.HTTP_200_OK)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (EmailPermissions,)
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        form = EmailForm(request.POST)
        instance = None
        if form.is_valid():
            instance = form.save()
            instance.ip_address = get_client_ip(request)
            instance.save()
            mailchimp_api.subscribe_by_email(instance.email)
            email.send_user_subscribed_email(instance.email)
            email.notify_admins_about_newsletter_signup(instance.email)
        else:
            if 'email' in request.POST:
                try:
                    instance = User.objects.get(email=request.POST['email'])
                except User.DoesNotExist:
                    instance = None
            else:
                instance = None
        if instance:
            return Response({'referralLink': instance.referral_code}, status=status.HTTP_200_OK)
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


class UsersSearchViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSearchSerializer
    permission_classes = (UserPermissions, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('first_name', 'last_name')

    def get_queryset(self):
        user = self.request.user
        users_ids = []

        # if user is project owner
        for project in user.own_projects.select_related('manager', 'members').all():
            if project.manager:
                users_ids.append(project.manager.id)
            users_ids.extend(list(project.members.values_list('id', flat=True)))

        # if user is project manager
        for project in user.manager_projects.select_related('member', 'project', 'project__members', 'project__user').all():
            users_ids.append(project.user.id)
            users_ids.extend(list(project.members.values_list('id', flat=True)))

        # if user is developer
        for proj_member in user.project_memberships.select_related('member', 'project', 'project__members', 'project__manager', 'project__user').all():
            users_ids.append(proj_member.project.user.id)
            if proj_member.project.manager:
                users_ids.append(proj_member.project.manager.id)
            users_ids.extend(list(proj_member.project.members.values_list('id', flat=True)))

        users_ids = list(set(users_ids))  # remove duplicates

        # remove own id
        if user.id in users_ids:
            users_ids.remove(user.id)

        return User.objects.filter(id__in=users_ids)
