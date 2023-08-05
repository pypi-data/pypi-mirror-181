import logging

from django.apps import apps as django_apps
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from filer.models import File, Folder
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from coreplus.configs import coreplus_configs

from ...helpers import validate_file_type_api
from ...models import MediaSetting
from .serializers import (
    FilerAudioVisualCreateSerializer,
    FilerAudioVisualSerializer,
    FilerFileCreateSerializer,
    FilerFileSerializer,
    FilerImageCreateSerializer,
    FilerImageSerializer,
)

logger = logging.getLogger(__name__)


class FilerImageViewSet(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = django_apps.get_model(settings.FILER_IMAGE_MODEL).objects.all()
    serializer_class = FilerImageSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return FilerImageCreateSerializer
        return super().get_serializer_class()

    @extend_schema(
        request=FilerImageCreateSerializer,
        responses=FilerImageSerializer,
    )
    def create(self, request, *args, **kwargs):
        """
        Upload image to file folder
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = self.perform_create(serializer)

        resp_serializers = FilerImageSerializer(
            instance=obj, context=self.get_serializer_context()
        )
        headers = self.get_success_headers(serializer.data)
        return Response(
            resp_serializers.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        media_settings = MediaSetting.for_request(self.request)
        if media_settings.image_extensions:
            exts = media_settings.image_extensions.replace(" ", "").split(",")
        else:
            exts = coreplus_configs.IMAGE_FILE_EXTENSIONS
        validate_file_type_api(self.request.data["file"], exts)
        folder = Folder.objects.get_or_create(name="images")[0]
        obj = serializer.save(author=self.request.user, folder=folder)
        logger.info(_("Image successfully uploaded"))
        return obj


class FilerAudioVisualViewSet(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = django_apps.get_model(settings.FILER_IMAGE_MODEL).objects.all()
    serializer_class = FilerAudioVisualSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return FilerAudioVisualCreateSerializer
        return super().get_serializer_class()

    @extend_schema(
        request=FilerAudioVisualCreateSerializer,
        responses=FilerAudioVisualSerializer,
    )
    def create(self, request, *args, **kwargs):
        """
        Upload audio visual (audio, video, and image) to file folder
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = self.perform_create(serializer)

        resp_serializers = FilerAudioVisualSerializer(
            instance=obj, context=self.get_serializer_context()
        )
        headers = self.get_success_headers(serializer.data)
        return Response(
            resp_serializers.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        media_settings = MediaSetting.for_request(self.request)
        if media_settings.image_extensions:
            exts = media_settings.image_extensions.replace(" ", "").split(",")
        else:
            exts = coreplus_configs.IMAGE_FILE_EXTENSIONS
        if media_settings.audio_extensions:
            exts += media_settings.audio_extensions.replace(" ", "").split(",")
        else:
            exts += coreplus_configs.AUDIO_FILE_EXTENSIONS
        if media_settings.video_extensions:
            exts += media_settings.video_extensions.replace(" ", "").split(",")
        else:
            exts += coreplus_configs.VIDEO_FILE_EXTENSIONS
        validate_file_type_api(self.request.data["file"], exts)
        folder = Folder.objects.get_or_create(name="audio_visuals")[0]
        obj = serializer.save(author=self.request.user, folder=folder)
        logger.info(_("Audio Visual successfully uploaded"))
        return obj


class FilerFileViewSet(ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FilerFileSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return FilerFileCreateSerializer
        return super().get_serializer_class()

    @extend_schema(
        request=FilerFileCreateSerializer,
        responses=FilerFileSerializer,
    )
    def create(self, request, *args, **kwargs):
        """
        Upload file (all types) to file folder
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = self.perform_create(serializer)

        resp_serializers = FilerFileSerializer(
            instance=obj, context=self.get_serializer_context()
        )
        headers = self.get_success_headers(serializer.data)
        return Response(
            resp_serializers.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        folder = Folder.objects.get_or_create(name="files")[0]
        obj = serializer.save(folder=folder)
        logger.info(_("File successfully uploaded"))
        return obj
