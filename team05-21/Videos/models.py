from django.db import models


MODEL_ACCOUNTS_USER = 'Accounts.MyUser'


# Create your models here.
class Video(models.Model):
    link = models.CharField(max_length=120)
    user_id = models.ForeignKey(MODEL_ACCOUNTS_USER, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=512)
    description = models.CharField(max_length=2048, null=True)
    has_captions = models.BooleanField(null=True)
    when_posted = models.DateTimeField()

    def __str__(self):
        return self.title


class VideoModules(models.Model):
    # The relation between the modules that a video is categorised by
    video_id = models.ForeignKey(Video, on_delete=models.CASCADE)
    module_id = models.ForeignKey('Profile.Module', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['video_id', 'module_id'], name='unique_video_modules'),
        ]


class VideoNote(models.Model):
    video_id = models.ForeignKey(Video, on_delete=models.CASCADE)
    user_id = models.ForeignKey(MODEL_ACCOUNTS_USER, on_delete=models.CASCADE)
    time_start = models.PositiveIntegerField();
    time_end = models.PositiveIntegerField();
    note = models.CharField(max_length=1024)


class Comment(models.Model):
    video_id = models.ForeignKey(Video, on_delete=models.CASCADE)
    user_id = models.ForeignKey(MODEL_ACCOUNTS_USER, on_delete=models.CASCADE)
    parent_id = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)  # on_delete behaviour may not be right
    content = models.CharField(max_length=1024)
    when_posted = models.DateTimeField()

    def __str__(self):
        return self.content
