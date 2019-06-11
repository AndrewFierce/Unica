from .models import Post
from rest_framework import serializers

class PostSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Post
		fields = ('title', 'summary', 'slug', 'created_at', 'modified_at')