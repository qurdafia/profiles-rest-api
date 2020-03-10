from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
import datetime

from io import BytesIO
from PIL import Image
from django.core.files import File

from django_resized import ResizedImageField


# Create your models here.
class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, nric_number, name, password=None):
        """Craete a new user profile"""
        if not nric_number:
            raise ValueError('User must have an nric number')

        nric_number = self.normalize_email(nric_number)
        user = self.model(nric_number=nric_number, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, nric_number, name, password):
        """Create a new superuser"""
        user = self.create_user(nric_number, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


#image compression method
def compress(image):
    im = Image.open(image).convert('RGB')
    im_io = BytesIO()
    im.save(im_io, 'JPEG', quality=70)
    new_image = File(im_io, name=image.name)
    return new_image


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """DB model for the users"""
    date_format = '%d-%m-%Y %H:%M:%S'

    nric_number = models.CharField(max_length=255, default='', unique=True)
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255, default='')
    # photo = models.FileField(upload_to='photos/', default='', null=True)
    photo = ResizedImageField(size=[640, 480], upload_to='photos/', blank=True, null=True, default='')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_pdpa_checked = models.BooleanField(default=False)
    reg_date = models.DateField(default=timezone.now)
    last_access_date = models.DateField(default=timezone.now)

    objects = UserProfileManager()

    USERNAME_FIELD = 'nric_number'
    REQUIRED_FIELDS = ['name']

    #calling image compression function before saving the data
    def save(self, *args, **kwargs):
                new_image = compress(self.photo)
                self.photo = new_image
                super().save(*args, **kwargs)

    def get_full_name(self):
        """Get full name of the user"""
        return self.name

    def get_short_name(self):
        """Get short name of the user"""
        return self.name

    def __str__(self):
        """Render string in the admin"""
        return self.name + ' - ' + self.nric_number
