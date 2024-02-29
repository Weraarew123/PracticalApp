from django.db import models

class Product(models.Model):
          name = models.CharField(max_length=100)
          image = models.ImageField()
          price = models.IntegerField()

          created_at = models.DateTimeField(auto_now_add=True)
          updated_at = models.DateTimeField(auto_now=True)

          def __str__(self):
                  return self.name


class Session(models.Model):
          name = models.CharField(max_length=150)
          image = models.ImageField()
          film = models.URLField()
          file = models.FileField()
          product = models.ForeignKey(Product, on_delete=models.CASCADE)

          created_at = models.DateTimeField(auto_now_add=True)
          updated_at = models.DateTimeField(auto_now=True)

          def __str__(self):
                  return self.name