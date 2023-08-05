from rest_framework import serializers

from coreplus.reactions.api.v1.serializers import ReactionableModelSerializer

from ...models import Discuss


class DiscussSerializerRelation(serializers.ModelSerializer):
    class Meta:
        model = Discuss
        fields = "__all__"


class DiscussSerializer(ReactionableModelSerializer, serializers.ModelSerializer):
    parent = DiscussSerializerRelation(many=False)
    children = DiscussSerializerRelation(many=True)

    class Meta:
        model = Discuss
        fields = "__all__"


class DiscussCreateSerializer(serializers.ModelSerializer):
    """
    serializer to create a new discuss
    """

    class Meta:
        model = Discuss
        fields = ["content"]
