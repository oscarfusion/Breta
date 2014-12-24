from rest_framework import viewsets
from rest_framework.permissions import BasePermission

from cities_light.models import Region, City

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

