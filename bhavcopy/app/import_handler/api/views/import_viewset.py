from rest_framework import viewsets
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters

from ...models.import_duty import ImportDuty


class QuestionViewsetPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = "page_size"
    max_page_size = 10000
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = {'test': ['exact']}


class ImportHandlerViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = ImportDuty.objects.all().order_by('id')
    pagination_class = QuestionViewsetPagination
