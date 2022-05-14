from django.contrib import admin
from Videos import models

# Register your models here.
admin.site.register(models.Video)
admin.site.register(models.VideoModules)
admin.site.register(models.VideoNote)
admin.site.register(models.Comment)