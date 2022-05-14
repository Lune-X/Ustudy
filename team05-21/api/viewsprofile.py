from django.shortcuts import get_list_or_404, get_object_or_404

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.permissions import IsAdminOrSelf

from api import serializerprofile
from api import serializeraccounts
from Profile import models
from Videos.models import Video
from Accounts.models import MyUser

import datetime


class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Course.objects.all()  # Likely not used
    serializer_class = serializerprofile.CourseSerializer

    user_queryset = MyUser.objects.all()
    school_queryset = models.School.objects.all()
    course_queryset = models.Course.objects.all()
    module_queryset = models.Module.objects.all()
    course_modules_queryset = models.CourseModules.objects.all()
    user_modules_queryset = models.UserModules.objects.all()

    def _get_my_account(self, request):
        return get_object_or_404(self.user_queryset, id=request.user.id)

    def _get_my_course(self, request):
        my_account = self._get_my_account(request)
        return get_object_or_404(self.course_queryset, id=my_account.course_id.id)

    def _get_my_modules(self, request):
        # Returns list

        my_user_modules = list(self.user_modules_queryset.filter(user_id=request.user.id))
        my_modules = []

        for my_user_module in my_user_modules:
            my_modules.append(my_user_module.module_id)

        return my_modules

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def get_all_schools(self, request):
        # Usage: GET to /api/profile/get_all_schools/
        # Front-end sends: Nothing
        # Back-end sends: List of Schools (id: Int, name: String)

        schools_serialized = serializerprofile.SchoolSerializer(self.school_queryset, many=True)
        return Response(schools_serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def get_my_school(self, request):
        # Usage: GET to /api/profile/get_my_school/
        # Front-end sends: Nothing
        # Back-end sends: id: Int, name: String

        my_course = self._get_my_course(request)
        my_school = get_object_or_404(self.school_queryset, id=my_course.school_id.id)

        my_school_serialized = serializerprofile.SchoolSerializer(my_school)
        return Response(my_school_serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def get_courses_in_school(self, request):
        # Usage: GET to /api/profile/get_courses_in_school/?id=<id of school>
        # Front-end sends: ID of school in URL
        # Back-end sends: List of Courses (id: Int, name: String, school_id: Int)

        school_id = request.query_params.get('id')

        courses_in_school = get_list_or_404(self.course_queryset, school_id=school_id)
        courses_in_school_serialized = serializerprofile.CourseSerializer(courses_in_school, many=True)
        return Response(courses_in_school_serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def get_my_course(self, request):
        # Usage: GET to /api/profile/get_my_course/
        # Front-end sends: Nothing
        # Back-end sends: id: Int, school_id: Int, name: String

        my_course = self._get_my_course(request)

        my_course_serialized = serializerprofile.CourseSerializer(my_course)
        return Response(my_course_serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def set_my_course(self, request):
        # Usage: POST to /api/profile/set_my_course/
        # Front-end sends: id: Int
        # Back-end sends: Success (HTTP 200) or error

        course_id = request.data['id']
        course = get_object_or_404(self.course_queryset, id=course_id)
        my_account = self._get_my_account(request)
        my_account.course_id = course
        my_account.save()

        return Response({'Success': 'You have set your course'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def set_my_year(self, request):
        # Usage: POST to /api/set_my_year/
        # Front-end sends: JSON object: { year: Int }
        # Back-end sends: HTTP 200 if success, else error (404 or 500)

        year = request.data['year']
        me = self._get_my_account(request)

        me.year_of_study = year
        me.save()

        return Response({'message': 'Successfully set your year of study!'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def set_my_user_modules(self, request):
        # Usage: POST to /api/profile/set_my_user_modules/
        # Front-end sends: Nothing
        # Back-end sends: Success (HTTP 200) or error

        my_account = self._get_my_account(request)
        course = self._get_my_course(request)

        course_modules = get_list_or_404(self.course_modules_queryset, course_id=course.id)

        my_existing_modules = self._get_my_modules(request);
        if len(list(my_existing_modules)) == len(course_modules):
            # TODO: this may prevent you from switching courses in the future
            return Response({'Success': 'You have already set your course modules. No need to redo it.'}, status=status.HTTP_100_CONTINUE)

        for course_module in course_modules:
            module = course_module.module_id
            user_module = models.UserModules(user_id=my_account, module_id=module)
            user_module.save()

        return Response({'Success': 'You have set all your enrolled modules'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def set_my_saved_video(self, request):
        # Usage: POST to /api/profile/set_my_saved_video/
        # Front-end sends: JSON object: { id: int ID of video }
        # Back-end sends: Success (HTTP 200) or error
        my_account = self._get_my_account(request)
        
        video_id = request.data['id']
        
        video = get_object_or_404(Video.objects.all(), id=video_id)
        
        try:
            saved_video = models.SavedVideos.objects.create(video_id = video, user_id = my_account, when = datetime.datetime.now())
        except Exception as e:
            return Response({'message': 'failed to save video', 'exception': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({'success':'Saved video'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def get_all_my_modules(self, request):
        # Usage: GET to /api/profile/get_all_my_modules/
        # Front-end sends: Nothing
        # Back-end sends: List of Modules (id: Int, name: String)

        my_modules = self._get_my_modules(request)

        my_modules_serialized = serializerprofile.ModuleSerializer(my_modules, many=True)
        return Response(my_modules_serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def get_my_modules_this_year(self, request):
        # Usage: GET to /api/profile/get_my_modules_this_year/
        # Front-end sends: Nothing
        # Back-end sends: List of Modules (id: Int, name: String)

        my_course = self._get_my_course(request)
        my_year_of_study = self._get_my_account(request).year_of_study
        my_modules = self._get_my_modules(request)
        course_modules_my_year = get_list_or_404(self.course_modules_queryset, year_of_study=my_year_of_study)
        my_modules_this_year = []

        # god this is a taxing function
        for course_module_my_year in course_modules_my_year:
            if course_module_my_year.module_id in my_modules:
                my_modules_this_year.append(course_module_my_year.module_id)

        my_modules_this_year_serialized = serializerprofile.ModuleSerializer(my_modules_this_year, many=True)
        return Response(my_modules_this_year_serialized.data, status=status.HTTP_200_OK)
        

    @action(detail=False, methods=['get'])
    def get_module(self, request):
        # Usage: GET to /api/profile/get_module/?id=<id of module>
        # Front-end sends: ID of module in URL
        # Back-end sends: id: Int, name: String

        module_id = request.query_params.get('id')
        module = get_object_or_404(self.module_queryset, id=module_id)
        module_serialized = serializerprofile.ModuleSerializer(module)
        return Response(module_serialized.data, status=status.HTTP_200_OK)
