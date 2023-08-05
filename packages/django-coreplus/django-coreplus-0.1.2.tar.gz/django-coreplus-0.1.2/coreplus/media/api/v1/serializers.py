import logging

from django.apps import apps as django_apps
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from filer.models import File
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ...models import MediaSetting

logger = logging.getLogger(__name__)


class FilerBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer for filer related serializers
    """

    def validate(self, data):
        """
        Ensure that the file is smaller than the max file size
        """
        media_settings = MediaSetting.for_request(self.context.get("request"))
        if data["file"]:
            if data["file"].size > media_settings.max_file_size * 1000000:
                raise ValidationError(
                    _(
                        "File size must be smaller than %s MB"
                        % (media_settings.max_file_size)
                    )
                )
        else:
            logger.error(_("File field is required"))
            raise ValidationError(_("File field is required"))
        return data


class FilerImageSerializer(FilerBaseSerializer):
    class Meta:
        model = django_apps.get_model(settings.FILER_IMAGE_MODEL, require_ready=False)
        fields = [
            "id",
            "file",
            "_file_size",
            "name",
            "description",
            "is_public",
            "author",
            "folder",
            "owner",
        ]


class FilerImageCreateSerializer(FilerBaseSerializer):
    class Meta:
        model = django_apps.get_model(settings.FILER_IMAGE_MODEL, require_ready=False)
        fields = ["file"]


class FilerFileSerializer(FilerBaseSerializer):
    class Meta:
        model = File
        fields = [
            "id",
            "file",
            "_file_size",
            "name",
            "description",
            "is_public",
            "folder",
            "owner",
        ]


class FilerFileCreateSerializer(FilerBaseSerializer):
    class Meta:
        model = File
        fields = ["file"]


class FilerAudioVisualSerializer(FilerBaseSerializer):
    class Meta:
        model = django_apps.get_model(settings.FILER_IMAGE_MODEL, require_ready=False)
        fields = "__all__"


class FilerAudioVisualCreateSerializer(FilerBaseSerializer):
    class Meta:
        model = django_apps.get_model(settings.FILER_IMAGE_MODEL, require_ready=False)
        fields = ["file"]
