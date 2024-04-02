from django.test import TestCase
from django.contrib.auth.models import User

class MultiRegisterTestCase(TestCase):
          def test_create_users(self):
                  for i in range(1000):
                          User.objects.create(username="i"+str(i), password="p"+str(i))
          
          def test_delete_users(self):
                  for i in range(1000):
                          User.objects.filter(username="i"+str(i), password="p"+str(i)).delete()