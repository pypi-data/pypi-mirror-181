from django.apps import apps as django_apps
from django.conf import settings

from rest_framework import serializers

from coreplus.reactions.api.v1.serializers import ReactionableModelSerializer

from ...models import DirectMessage, DirectMessageAttachment


class FilerImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = django_apps.get_model(settings.FILER_IMAGE_MODEL, require_ready=False)
        fields = ["id", "file", "name", "_height", "_width"]


class AttachmentSerializer(serializers.ModelSerializer):
    attachment = FilerImageSerializer(many=False)

    class Meta:
        model = DirectMessageAttachment
        fields = ["attachment"]


class DirectMessageSerializer(ReactionableModelSerializer, serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = DirectMessage
        fields = "__all__"


class DirectMessageCreateSerializer(serializers.ModelSerializer):
    attachment_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False
    )

    class Meta:
        model = DirectMessage
        fields = ["content", "recipient", "attachment_ids"]
