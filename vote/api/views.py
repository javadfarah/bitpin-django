from api.serializers import PostSerializer,VoteSerializer
from api.models import Post, Votes
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class PostList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        posts = Post.objects.all()
        "sending context to serializer for access the user"
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Vote_Add(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        post_id = request.data.get('post_id', None)
        vote = request.data.get('vote', None)
        if  not (post_id and vote):
            return Response({'status': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)
        post = Post.objects.filter(id=post_id)
        if post.exists():
            
            obj,created = Votes.objects.get_or_create(user=request.user,post_id=post.first())
            obj.vote = vote
            obj.save()
            serializer = VoteSerializer(obj)
            return Response(serializer.data)
        else:
            return Response({'status': 'invalid post_id'}, status=status.HTTP_400_BAD_REQUEST)
