from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters

from rest_framework.decorators import action
from ...models.import_duty import ImportDuty
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class QuestionViewsetPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = "page_size"
    max_page_size = 10000
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = {'test': ['exact']}


class ImportHandlerViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = ImportDuty.objects.all().order_by('id')
    pagination_class = QuestionViewsetPagination

    @action(detail=False, methods=['get'])
    def import_bhavcopy(self, request, version=1):
        print(request)
        return Response(status=status.HTTP_200_OK)
