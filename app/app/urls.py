"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include

from rest_framework_swagger.views import get_swagger_view


# We exclude user_url_pattern from swagger UI so we add it in urlpatterns at last
user_url_pattern = path('api/user/', include('user.urls', namespace='user_apis'))

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('meme.urls')),
    path('api/', include('product.urls')),
]

schema_view = get_swagger_view(title='x-memes', patterns=urlpatterns.copy())

# At last we add user_url_pattern and swagger-ui url
urlpatterns += [
    user_url_pattern,
    path('swagger-ui/', schema_view)
]