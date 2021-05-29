from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ...models.import_duty import CacheRouter


class ImportHandlerViewSet(viewsets.ViewSet):
    queryset = '',
    permission_classes = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dbOperation = CacheRouter()

    def handle_bhavcopy_download(self, date):
        pass

    @action(detail=False, methods=['get'], description="Importing Latest Bhavcopy", name="Importing Bhavcopy")
    def import_bhavcopy(self, request, version=1, date='today'):
        self.dbOperation.create_many({date: 'not_today', 'today': date})
        resultant = self.dbOperation.find_many(['today', date])

        return Response(status=status.HTTP_200_OK, data=resultant)

    def import_bhavcopy_with_cron(self, request, version=1, date='today'):
        self.dbOperation.create_many({date: 'not_today', 'today': date})
        resultant = self.dbOperation.find_many(['today', date])

        return Response(status=status.HTTP_200_OK, data=resultant)
