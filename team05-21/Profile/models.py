from django.db import models
NAME_MAX_LENGTH = 240


# Create your models here.
MODEL_ACCOUNTS_USER = 'Accounts.MyUser'
MODEL_VIDEOS_VIDEO = 'Videos.Video'
MODEL_VIDEOS_COMMENT = 'Videos.Comment'


class School(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    school_id = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)

    def __str__(self):
        return self.name


class Module(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)

    def __str__(self):
        return self.name


class CourseModules(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    module_id = models.ForeignKey(Module, on_delete=models.CASCADE)
    year_of_study = models.PositiveIntegerField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course_id', 'module_id'], name='unique_course_modules'),
        ]


class UserModules(models.Model):
    # The relation between the modules that users are a part of
    user_id = models.ForeignKey(MODEL_ACCOUNTS_USER, on_delete=models.CASCADE)
    module_id = models.ForeignKey(Module, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'module_id'], name='unique_user_modules'),
        ]


# Video related user-specific relations
class LikedVideos(models.Model):
    video_id = models.ForeignKey(MODEL_VIDEOS_VIDEO, on_delete=models.CASCADE)
    user_id = models.ForeignKey(MODEL_ACCOUNTS_USER, on_delete=models.CASCADE)
    when = models.DateTimeField()


class DislikedVideos(models.Model):
    video_id = models.ForeignKey(MODEL_VIDEOS_VIDEO, on_delete=models.CASCADE)
    user_id = models.ForeignKey(MODEL_ACCOUNTS_USER, on_delete=models.CASCADE)
    when = models.DateTimeField()


class ReportedVideos(models.Model):
    video_id = models.ForeignKey(MODEL_VIDEOS_VIDEO, on_delete=models.CASCADE)
    user_id = models.ForeignKey(MODEL_ACCOUNTS_USER, on_delete=models.CASCADE)
    when = models.DateTimeField()


class SavedVideos(models.Model):
    video_id = models.ForeignKey(MODEL_VIDEOS_VIDEO, on_delete=models.CASCADE)
    user_id = models.ForeignKey(MODEL_ACCOUNTS_USER, on_delete=models.CASCADE)
    when = models.DateTimeField()


# Comment related user-specific relations
class LikedComments(models.Model):
    comment_id = models.ForeignKey(MODEL_VIDEOS_COMMENT, on_delete=models.CASCADE)
    user_id = models.ForeignKey(MODEL_ACCOUNTS_USER, on_delete=models.CASCADE)
    when = models.DateTimeField()


class DislikedComments(models.Model):
    comment_id = models.ForeignKey(MODEL_VIDEOS_COMMENT, on_delete=models.CASCADE)
    user_id = models.ForeignKey(MODEL_ACCOUNTS_USER, on_delete=models.CASCADE)
    when = models.DateTimeField()


class ReportedComments(models.Model):
    comment_id = models.ForeignKey(MODEL_VIDEOS_COMMENT, on_delete=models.CASCADE)
    user_id = models.ForeignKey(MODEL_ACCOUNTS_USER, on_delete=models.CASCADE)
    when = models.DateTimeField()
