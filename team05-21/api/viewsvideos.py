from urllib import response
from django.shortcuts import get_list_or_404, get_object_or_404

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.permissions import IsAdminOrSelf

from api import serializervideos
from api import serializerprofile
from api import serializeraccounts

from Accounts.models import MyUser
from Profile.models import SavedVideos, Module
from Videos import models

import datetime


class VideoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Video.objects.all()
    serializer_class = serializervideos.VideoSerializer

    user_queryset = MyUser.objects.all()
    video_modules_queryset = models.VideoModules.objects.all()
    saved_videos_queryset = SavedVideos.objects.all()

    def _get_my_account(self, request):
        return get_object_or_404(self.user_queryset, id=request.user.id)

    @action(detail=False, methods=['get'])
    def get_module_videos(self, request):
        # Usage: GET to /api/video/get_module_videos/?id=<id of module>
        # Front-end sends: ID of module in URL
        # Back-end sends: List of Videos (Refer to Videos/models.py)

        module_id = request.query_params.get('id')
        video_modules = get_list_or_404(self.video_modules_queryset, module_id=module_id)

        videos = []
        for video_module in video_modules:
            videos.append(video_module.video_id)

        videos_serialized = self.serializer_class(videos, many=True)
        return Response(videos_serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def get_my_saved_videos(self, request):
        # Usage: GET to /api/video/get_my_saved_videos/
        # Front-end sends: Nothing
        # Back-end sends: List of Videos (Refer to Videos/models.py)

        my_saved_videos = get_list_or_404(self.saved_videos_queryset, user_id=request.user.id)

        videos = []
        for saved_video in my_saved_videos:
            videos.append(saved_video.video_id)

        videos_serialized = self.serializer_class(videos, many=True)
        return Response(videos_serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def get_my_posted_videos(self, request):
        # Usage: GET to /api/video/get_my_posted_videos/
        # Front-end sends: Nothing
        # Back-end sends: List of Videos (Refer to Videos/models.py)

        videos = get_list_or_404(self.queryset, user_id=request.user.id)
        videos_serialized = self.serializer_class(videos, many=True)
        return Response(videos_serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def get_video(self, request):
        # Usage: GET to /api/video/get_video/?id=<id of video>
        # Front-end sends: ID of video in URL
        # Back-end sends: id: Int, link: String, user_id: Int, title: String, description: String, has_captions: Bool, when_posted: String (date format)
        
        video_id = request.query_params.get('id')
        video = get_object_or_404(self.queryset, id=video_id)
        video_serialized = self.serializer_class(video)
        return Response(video_serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def get_video_modules(self, request):
        # Usage: GET to /api/video/get_video_modules/?id=<id of video>
        # Front-end sends: ID of video in URL
        # Back-end sends: List of modules (id: Int, name: String)

        video_id = request.query_params.get('id')

        video_modules = list(self.video_modules_queryset.filter(video_id=video_id))
        modules = []

        for video_module in video_modules:
            modules.append(video_module.module_id)

        modules_serialized = serializerprofile.ModuleSerializer(modules, many=True)
        return Response(modules_serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def post_video(self, request):
        # Usage: POST to /api/video/post_video/
        # Front-end sends: JSON object: { title: String, link: String, description: String, module_ids: List of Int (currently would just be an array of 1 as only 1 module is selectable at a time) }
        # Back-end sends: Video ID (if HTTP 200 successful), else error status

        title = request.data['title']
        link = request.data['link']
        description = request.data['description']
        module_ids = request.data['module_ids']
        has_captions = getattr(request.data, 'has_captions', False)

        video = None

        try:
            video = models.Video.objects.create(link=link, user_id=self._get_my_account(request), title=title, description=description, has_captions=has_captions, when_posted=datetime.datetime.now())
        except Exception as e:
            return Response({'message': 'error trying to post a new video!', 'exception': str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        for module_id in module_ids: 
            try:
                video_module = models.VideoModules.objects.create(video_id=video, module_id=get_object_or_404(Module.objects.all(), id=module_id))
            except Exception as e:
                return Response({'message': 'error trying to post a new video - video module creation had an error!', 'exception': str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        video_serialized = serializervideos.VideoSerializer(video)
        return Response(video_serialized.data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrSelf]
    queryset = models.Comment.objects.all()
    serializer_class = serializervideos.CommentSerializer
