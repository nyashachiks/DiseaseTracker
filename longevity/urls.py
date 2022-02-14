"""longevity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from rest_framework.urlpatterns import format_suffix_patterns
from welltory import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('welltory/passwordreset/', auth_views.PasswordResetView.as_view(template_name='clinic/password_reset.html'),
          name='password_reset'),
    path('welltory/passwordreset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='clinic/password_reset_done.html'),
         name='password_reset_done'),
    path('welltory/passwordresetconfirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='clinic/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('welltory/passwordresetcomplete/', auth_views.PasswordResetCompleteView.as_view(
         template_name='clinic/password_reset_complete.html'), name='password_reset_complete'),
    path('welltory/', include('welltory.urls')),
    path('welltory/biomarker', views.BioMarkerList.as_view()),
    path('welltory/parameter', views.ParameterList.as_view()),
    path('welltory/reading', views.ReadingList.as_view()),
    path('welltory/disease', views.DiseaseList.as_view()),
    path('welltory/recommendation', views.RecommendationList.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
