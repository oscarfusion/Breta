from django.utils import timezone
from rest_framework import viewsets

from .serializers import ActivitySerializer
from .permissions import ActivityPermission
from ..models import Activity


class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Activity.objects.select_related().all()
    serializer_class = ActivitySerializer
    permission_classes = (ActivityPermission,)

    def get_queryset(self):
        qs = self.queryset.order_by('-created_at')
        if 'project' in self.request.QUERY_PARAMS:
            qs = qs.filter(project=self.request.QUERY_PARAMS['project'])
        if 'type' in self.request.QUERY_PARAMS:
            act_type = self.request.QUERY_PARAMS['type']
            if act_type == 'last-week':
                qs = qs.filter(created_at__gte=timezone.now()-timezone.timedelta(days=7))
            elif act_type == 'last-month':
                qs = qs.filter(created_at__gte=timezone.now()-timezone.timedelta(days=31))
        return qs
