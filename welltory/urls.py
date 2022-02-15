from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'welltory'
urlpatterns = [
   path('register/', views.UserRegisterView.as_view(success_url='../'), name='register'),
   path('', auth_views.LoginView.as_view(template_name='clinic/index.html'), name='index'),
   path('logout/', auth_views.LogoutView.as_view(template_name='clinic/logout.html'), name='logout'),
   path('home', views.home, name='home'),
   path('profile/', views.ProfileView.as_view(), name='profile'),
   path('updateuser/', views.updateuser, name='updateuser'),
   path('updatepractitioner/', views.updatepractitioner, name='updatepractitioner'),
   path('patientlist/', views.PatientListView.as_view(), name='patientlist'),
   path('patientdetails/<int:pk>', views.PatientDetailView.as_view(), name='patientdetails'),
   path('createpatient/', views.PatientCreateView.as_view(), name='createpatient'),
   path('updatepatient/<int:pk>/update', views.PatientUpdateView.as_view(), name='updatepatient'),
   path('deletepatient/<int:pk>/delete', views.PatientDeleteView.as_view(), name='deletepatient'),
   path('diagnosislist/<national_id>', views.DiagnosisListView.as_view(), name='diagnosislist'),
   path('diagnosisdetails/<int:pk>', views.DiagnosisDetailView.as_view(), name='diagnosisdetails'),
   path('creatediagnosis/<national_id>', views.diagnosiscreate, name='creatediagnosis'),
   path('diagnosisuploadprep/<national_id>', views.diagnosisuploadprep, name='diagnosisuploadprep'),
   path('diagnosisupload', views.diagnosisupload, name='diagnosisupload'),
   path('diagnosisdoclist/<id>/', views.DiagnosisDocListView.as_view(), name='diagnosisdoclist'),
   path('diagnosisdownload/<id>/', views.diagnosisdownload, name='diagnosisdownload'),
]
