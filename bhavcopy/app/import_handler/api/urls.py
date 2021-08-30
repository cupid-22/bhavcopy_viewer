from rest_framework_extensions.routers import ExtendedSimpleRouter
from .views.import_viewset import ImportHandlerViewSet

router = ExtendedSimpleRouter()
questions_router = router.register(r'configuration/(?P<custom_date>([0-2][0-9]|(3)[0-1])(((0)[0-9])|((1)[0-2]))\d{2})', ImportHandlerViewSet, basename='importDuty')

urlpatterns = []

urlpatterns += router.urls
