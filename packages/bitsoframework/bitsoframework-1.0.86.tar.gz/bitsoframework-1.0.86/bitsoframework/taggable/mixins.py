from .serializers import TaggitSerializer, TagListSerializerField


class TaggableSerializer(TaggitSerializer):
    tags = TagListSerializerField(required=False)
