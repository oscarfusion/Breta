from annoying.decorators import ajax_request
from rest_framework import parsers
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from cities_light.models import Region, City
from constance import config

from .serializers import AuthTokenSerializer
from .serializers import RegionSerializer, CitySerializer


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = (BasePermission,)
    filter_fields = ('country__code3',)


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (BasePermission,)
    filter_fields = ('region',)


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


obtain_auth_token = ObtainAuthToken.as_view()


@ajax_request
def breta_config(request):
    return {
        'config': {
            'bretaFee': config.BRETA_FEE
        }
    }
