from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, request, JsonResponse, Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views import generic
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os
import http.client
import urllib.parse
import json
from .models import (BioMarker,
                    Parameter,
                    Reading,
                    Disease,
                    Recommendation,
                    Practitioner,
                    Patient,
                    Diagnosis,
                    DiagnosisDoc
                    )
from .forms import (UserRegisterForm,
                    UserUpdateForm,
                    PractitionerUpdateForm,
                    PatientForm,
                    ProfileGrayedForm,
                    DiagnosisForm)
from .serializers import (BioMarkerSerializer,
                          ParameterSerializer,
                          ReadingSerializer,
                          DiseaseSerializer,
                          RecommendationSerializer)
from .utilities import ReadContents


# Create your views here.
class UserRegisterView(generic.CreateView):
    template_name = 'clinic/register.html'
    form_class = UserRegisterForm
    context_object_name = 'register'

    def signup(self):
        if self.request.method == 'POST':
            form = UserRegisterForm(self.request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(self.request, user)
                return HttpResponseRedirect('index')
            else:
                form = UserRegisterForm
                return render(self.request, 'register', {'form': form})


@login_required
def updateuser(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('../profile')
    else:
        form = UserUpdateForm(instance=request.user)
        return render(request, 'clinic/updateuser.html', {'form': form})


class BioMarkerList(APIView):
    def get(self, request):
        bio_markers = BioMarker.objects.all()
        serializer = BioMarkerSerializer(bio_markers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BioMarkerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ParameterList(APIView):
    def get(self, request):
        parameters = Parameter.objects.all()
        serializer = ParameterSerializer(parameters, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ParameterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReadingList(APIView):
    def get(self, request):
        readings = Reading.objects.all()
        serializer = ReadingSerializer(readings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReadingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DiseaseList(APIView):
    def get(self, request):
        diseases = Disease.objects.all()
        serializer = ParameterSerializer(diseases, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DiseaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecommendationList(APIView):
    def get(self, request):
        recommendations = Recommendation.objects.all()
        serializer = RecommendationSerializer(recommendations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RecommendationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required
def home(request):
    context = {}
    return render(request, 'clinic/home.html', context)


@login_required
def updatepractitioner(request):
    if request.method == 'POST':
        form = PractitionerUpdateForm(request.POST, request.FILES, instance=request.user.practitioner)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('../profile')
    else:
        form = PractitionerUpdateForm(instance=request.user.practitioner)
        return render(request, 'clinic/updatepractitioner.html', {'form': form})


class ProfileView(LoginRequiredMixin, generic.FormView):
    template_name = 'clinic/profile.html'
    form_class = ProfileGrayedForm
    context_object_name = 'profile'

    def profile(self):
        form = ProfileGrayedForm
        return render(self.request, 'profile', {'form': form})


class PatientListView(LoginRequiredMixin, generic.ListView):
    model = Patient
    template_name = 'clinic/patientlist.html'
    context_object_name = 'patientlist'
    paginate_by = 20

    def get_queryset(self):
        return Patient.objects.order_by('-date_created')


class PatientCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'clinic/patient_form.html'
    form_class = PatientForm
    context_object_name = 'createpatient'

    def createpatient(self):
        if self.request.method == 'POST':
            form = super(PatientCreateView, self).get_form(PatientForm)
            form.fields['date_field'].widget.attrs.update({'class': 'datepicker'})

    def form_valid(self, form):
        form.instance.created_by = self.request.user.practitioner
        return super().form_valid(form)


class PatientDetailView(LoginRequiredMixin, generic.DetailView):
    model = Patient
    template_name = 'clinic/patient_detail.html'


class PatientUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Patient
    template_name = 'clinic/patient_form.html'
    form_class = PatientForm
    context_object_name = 'updatepatient'

    def updatepatient(self):
        if self.request.method == 'POST':
            form = super(PatientUpdateView, self).get_form(PatientForm)
            form.fields['date_field'].widget.attrs.update({'class': 'datepicker'})

    def form_valid(self, form):
        form.instance.created_by = self.request.user.practitioner
        return super().form_valid(form)

    def test_func(self):
        patient = self.get_object()
        if self.request.user.practitioner == patient.created_by:
            return True
        else:
            return False


class PatientDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Patient
    template_name = 'clinic/patient_confirm_delete.html'
    success_url = '../../patientlist'

    def test_func(self):
        patient = self.get_object()
        if self.request.user.practitioner == patient.created_by:
            return True
        else:
            return False


class DiagnosisListView(LoginRequiredMixin, generic.ListView):
    model = Diagnosis
    template_name = 'clinic/diagnosislist.html'
    context_object_name = 'diagnosislist'
    paginate_by = 20

    def get_queryset(self):
        self.patient = get_object_or_404(Patient, national_id=self.kwargs['national_id'])
        patient = self.patient.id
        return Diagnosis.objects.filter(patient=patient).order_by('-date_created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.patient
        return context


class DiagnosisDetailView(LoginRequiredMixin, generic.DetailView):
    model = Diagnosis
    template_name = 'clinic/diagnosis_detail.html'


@login_required
def diagnosiscreate(request, national_id):
    if request.method == 'POST':
        form = DiagnosisForm(request.POST)
        if form.is_valid():
            patient = Patient.objects.get(national_id=national_id)
            diagnosis_id = patient.national_id
            patientinstance = form.save(commit=False)
            patientinstance.patient = patient
            patientinstance.practitioner = request.user.practitioner
            patientinstance.save()
            return HttpResponseRedirect('../diagnosislist/' + str(diagnosis_id))
        else:
            print(form.errors)
    else:
        form = DiagnosisForm()
        return render(request, 'clinic/diagnosis_form.html', {'form': form})


@login_required
def diagnosisuploadprep(request, national_id):
    diagnosis = national_id
    print(diagnosis)
    return render(request, 'clinic/diagnosisuploadprep.html', {'output': diagnosis})


@login_required
def diagnosisupload(request):
    if request.method == 'POST':
        myfile = request.FILES.get('file')
        diagnosis = request.POST.get('diagnosis')
        diagnosis = Diagnosis.objects.get(pk=diagnosis)
        DiagnosisDoc.objects.create(upload=myfile, diagnosis=diagnosis)
        records = DiagnosisDoc.objects.filter(content__isnull=True)
        for row in records:
            path = row.upload.path
            pre_purge = path.rfind('\\')
            filename = path[pre_purge + 1:]
            purge = filename.rfind('.')
            file_type = filename[purge + 1:]
            extension = file_type
            filename = 'media/documents/' + str(filename)

            if extension == 'jpg' or extension == 'png':
                file_object = ReadContents(filename)
                text = file_object.read_image()
                row.content = text
                row.save()
            elif extension == 'pdf':
                file_object = ReadContents(filename)
                text = file_object.read_pdf()
                row.content = text
                row.save()
            elif extension == 'docx':
                file_object = ReadContents(filename)
                text = file_object.read_docx()
                row.content = text
                row.save()

        return HttpResponse('')
    return JsonResponse({'post':'false'})


class DiagnosisDocListView(LoginRequiredMixin, generic.ListView):
    model = DiagnosisDoc
    template_name = 'clinic/diagnosisdoclist.html'
    context_object_name = 'diagnosisdoclist'
    paginate_by = 20

    def get_queryset(self):
        self.diagnosis = get_object_or_404(Diagnosis, pk=self.kwargs['id'])
        diagnosis = self.diagnosis.pk
        return DiagnosisDoc.objects.filter(diagnosis=diagnosis)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['diagnosis'] = self.diagnosis
        return context


@login_required
def diagnosisdownload(request, id):
    path_object = DiagnosisDoc.objects.get(id=id)
    path = path_object.upload
    file_path = os.path.join(settings.MEDIA_ROOT, str(path))
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
        raise Http404



class ConvertedTextDetailView(LoginRequiredMixin, generic.DetailView):
    model = DiagnosisDoc
    template_name = 'clinic/documentdetails.html'