from django.contrib import admin
from Profile import models

# Register your models here.
admin.site.register(models.School)
admin.site.register(models.Course)
admin.site.register(models.Module)
admin.site.register(models.CourseModules)
admin.site.register(models.UserModules)
admin.site.register(models.LikedVideos)
admin.site.register(models.DislikedVideos)
admin.site.register(models.ReportedVideos)
admin.site.register(models.SavedVideos)
admin.site.register(models.LikedComments)
admin.site.register(models.DislikedComments)
admin.site.register(models.ReportedComments)