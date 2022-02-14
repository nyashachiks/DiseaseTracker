from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField, Country
from django.utils import timezone
from PIL import Image
from django.urls import reverse


# Create your models here.
class BioMarker(models.Model):
    bio_marker = models.CharField(max_length=200)

    def __str__(self):
        return self.bio_marker


class Parameter(models.Model):
    bio_marker = models.ForeignKey(BioMarker, on_delete=models.CASCADE)
    min_reading = models.CharField(max_length=20)
    max_reading = models.CharField(max_length=20)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.bio_marker

    @property
    def raise_alarm(self):
        list_all = Parameter.objects.all().prefetch_related('reading_set')
        out_of_sync = []
        for check in list_all:
            if check.reading.reading.isnumeric:
                if check.reading.reading > check.max_reading:
                    out_of_sync.append(check.biomarker)
                elif check.reading.reading < check.min_reading:
                    out_of_sync.append(check.biomarker)
            elif check.reading == 'M':
                out_of_sync.append(check.reading.reading)
            elif check.reading == 'F':
                out_of_sync.append(check.reading.reading)
            elif check.reading == 'Black':
                out_of_sync.append(check.reading.reading)
            elif check.reading == 'White':
                out_of_sync.append(check.reading.reading)
            elif check.reading == 'Hispanic':
                out_of_sync.append(check.reading.reading)
            elif check.reading == 'Asian':
                out_of_sync.append(check.reading.reading)
            return out_of_sync


class Reading(models.Model):
    parameter_baseline = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    reading = models.CharField(max_length=100)


class Disease(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    critical_bio_markers = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Recommendation(models.Model):
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.description


class Practitioner(models.Model):
    MALE = 'Male'
    FEMALE = 'Female'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]
    WELLTORY_CLINIC = 'Welltory Clinic'
    BMI_CLINIC = 'BMI Clinic'
    CLINIC_CHOICES = [
        (BMI_CLINIC, 'Welltory Clinic'),
        (BMI_CLINIC, 'BMI Clinic')
    ]
    practitioner = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    national_id = models.CharField(max_length=12)
    dateOfBirth = models.DateField(null=True)
    street1 = models.CharField(max_length=100)
    street2 = models.CharField(max_length=100)
    city = models.CharField(max_length=40)
    country = CountryField()
    mobile = models.CharField(max_length=20)
    email = models.EmailField()
    employer = models.CharField(max_length=50, choices=CLINIC_CHOICES)
    date_created = models.DateTimeField(default=timezone.now)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return str(self.practitioner)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Patient(models.Model):
    GENDER_MALE = 'Male'
    GENDER_FEMALE = 'Female'
    GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female')]
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20)
    email = models.EmailField()
    street1 = models.CharField(max_length=100)
    street2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100, null=True)
    country = CountryField()
    dateOfBirth = models.DateField(null=True)
    national_id = models.CharField(max_length=20)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES,)
    created_by = models.ForeignKey(Practitioner, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.national_id})'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('welltory:patientdetails', kwargs={'pk': self.pk})





