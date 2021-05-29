"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, re_path, path

base_app_folder = 'bhavcopy.app'
common_url_file = 'api.urls'

browser_base_url = 'bhavcopy_viewer_api/(?P<version>[v1|v2]+)/'

urlpatterns = [
    path('admin/', admin.site.urls),

    # App based URLs
    re_path(fr'{browser_base_url}', include(f'{base_app_folder}.import_handler.{common_url_file}')),

]
