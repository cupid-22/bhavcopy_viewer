from rest_framework_extensions.routers import ExtendedSimpleRouter
from .views.import_viewset import ImportHandlerViewSet

router = ExtendedSimpleRouter()
questions_router = router.register(r'configuration/(?P<date>\d+)', ImportHandlerViewSet, basename='importDuty')

urlpatterns = []

urlpatterns += router.urls
