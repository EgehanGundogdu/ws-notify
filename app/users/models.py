from django.contrib.auth.models import AbstractUser
# Create your models here.



class User(AbstractUser):
    pass


    @property
    def full_name(self):
        return self.get_full_name()