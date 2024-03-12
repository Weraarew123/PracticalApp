from django.db import models
from django.core.validators import FileExtensionValidator

def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # pobierz rozszerzenie pliku
    valid_extensions = ['.pdf', '.doc', '.docx']  # lista dozwolonych rozszerzeń
    if not ext.lower() in valid_extensions:
       raise ValidationError('Nieprawidłowe rozszerzenie pliku. Dozwolone są jedynie pliki typu PDF, DOC i DOCX. (dla pliku tekstowego)')


class Product(models.Model):
       name = models.CharField(max_length=100, verbose_name='Nazwa')
       image = models.ImageField(upload_to='media/photos/', verbose_name='Zdjęcie')
       description = models.TextField(blank=True, verbose_name='Opis')
       price = models.FloatField(verbose_name='Cena')
       is_published = models.BooleanField(default=False, verbose_name='Opublikowany')

       created_at = models.DateTimeField(auto_now_add=True)
       updated_at = models.DateTimeField(auto_now=True)

       class Meta:
              verbose_name_plural = 'Produkt'

       def __str__(self):
              return self.name


class Session(models.Model):
          name = models.CharField(max_length=150, verbose_name='Nazwa')
          image = models.ImageField(upload_to='media/photos/', verbose_name='Zdjęcie')
          film = models.FileField(verbose_name='Film', upload_to='videos_uploaded', null=True, validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
          file = models.FileField(validators=[validate_file_extension], verbose_name='Plik tekstowy')
          product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Produkt')

          created_at = models.DateTimeField(auto_now_add=True)
          updated_at = models.DateTimeField(auto_now=True)


          class Meta:
                 verbose_name_plural = 'Sesja'

          def __str__(self):
                  return self.name