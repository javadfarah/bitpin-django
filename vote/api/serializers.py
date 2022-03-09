from api.models import Post, Votes
from rest_framework import serializers
from django.db.models import Avg
from django.shortcuts import get_object_or_404

class VoteSerializer(serializers.ModelSerializer):

     class Meta:
        model = Votes
        fields = "__all__"   

class PostSerializer(serializers.ModelSerializer):
    "add new field for check user votes and calculate average votes"
    vote = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "__all__"

    def get_vote(self,object):
        query = Votes.objects.filter(post_id=object)
        average_vote = query.aggregate(Avg('vote'))
        user = self.context['request'].user
        user_vote =  Votes.objects.filter(post_id=object,user=user).exists()
        if user_vote:
            user_vote = Votes.objects.get(post_id=object,user=user).vote
            return {"user_vote": user_vote,"total_vots":query.count(),**average_vote}
        else:
            return {"user_vote": None,"total_vots":query.count(),**average_vote}