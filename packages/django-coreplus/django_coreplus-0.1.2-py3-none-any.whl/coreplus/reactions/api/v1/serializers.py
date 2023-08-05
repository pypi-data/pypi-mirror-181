from rest_framework import serializers

from ...models import Flag, Reaction


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = "__all__"


class ReactionableModelSerializer(serializers.ModelSerializer):
    user_reaction = serializers.SerializerMethodField(required=False)

    def get_user_reaction(self, obj) -> ReactionSerializer:
        user = self.context.get("request").user
        return ReactionSerializer(instance=obj.user_reaction(user)).data


class ReactionableModelAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ["value"]


class FlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flag
        fields = "__all__"


class FlaggableModelAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flag
        fields = ["value", "message"]
