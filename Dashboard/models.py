from django.contrib.auth.models import User
from django.db import models


def get_upload_path(instance, filename):
    return "%s/%s" % (instance.user.id, filename)

class Picture(models.Model):
         # upload_to: The directory to be generated in the root directory (MEDIA_ROOT).
         # MEDIA_ROOT: As long as the image is uploaded, it must be set to specify the root directory of the image upload. Can be set under static (the search path of the static directory, has been configured through STATICFILES_DIRS), or you can customize the root directory (MEDIA_URL).
    #pic_url = models.ImageField(upload_to='%Y/%m')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    pic_url = models.ImageField(upload_to=get_upload_path)