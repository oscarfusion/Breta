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
            return qs.filter(project=self.request.QUERY_PARAMS['project'])
        return qs
