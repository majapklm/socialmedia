from django.shortcuts import render

from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import JsonResponse

from . models import Post, UserIdentifier, UserPostAction

from itertools import chain
from django.core.paginator import Paginator
import json


class PostListViewSet(generics.ListCreateAPIView):
    paginate_by = 2
    def get(self, request):

        if 'user_id' in self.request.GET and self.request.GET['user_id']:
            user_id = self.request.GET['user_id']
            try:
                user_identifier = UserIdentifier.objects.get(id=user_id)
            except:
                pass
            try:
                user_action = UserPostAction.objects.get(user_identifier=user_identifier)
            except:
                pass

            liked_categories = []
            disliked_categories = []
            if user_action:
                for post in user_action.liked_posts.all().values('category__category_name').distinct():
                    liked_categories.append(post['category__category_name'])

                for post in user_action.disliked_posts.all().values('category__category_name').distinct():
                    disliked_categories.append(post['category__category_name'])
           
                favourite_posts = Post.objects.filter(category__category_name__in=liked_categories, user_identifier=user_identifier)
                unfavourite_posts = Post.objects.filter(category__category_name__in=disliked_categories, user_identifier=user_identifier)
                ordinary_posts = Post.objects.all().exclude(category__category_name__in=liked_categories+disliked_categories)
                posts = list(chain(favourite_posts,ordinary_posts,unfavourite_posts))
            else:
                posts = Post.objects.all()
        else:
            posts = Post.objects.all()
        
        data=[]

        if 'page' in self.request.GET and self.request.GET['page']:
            page = self.request.GET['page']
            paginator = Paginator(posts, 3)
            pages = paginator.page(page)

            posts = pages.object_list

        for post in posts:
            images = []
            for image in post.postimage_set.all():

                images.append(json.dumps(str(image.image)))

            data.append({'post_name':post.post_name,
                         'category':post.category.category_name,
                         'description':post.description,
                         'like':post.like,
                         'dislike':post.dislike,
                         'images':images,
                         'id':post.id,
                         'status':post.status,
                         'date':post.updated_at
                         })

        return JsonResponse(data, safe=False)


class PostActionViewSet(generics.RetrieveUpdateAPIView):

    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({'error':'Invalid Post'}, status=status.HTTP_404_NOT_FOUND)
        images = []
        for image in post.postimage_set.all():
            images.append(json.dumps(str(image.image)))
        
        data = {'post_name':post.post_name,
                         'category':post.category.category_name,
                         'description':post.description,
                         'like':post.like,
                         'dislike':post.dislike,
                         'images':images,
                         'id':post.id,
                         'status':post.status,
                         'date':post.updated_at
                         }
        return JsonResponse(data, safe=False)

    def patch(self,  request, post_id):

        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({'error':'Invalid Post'}, status=status.HTTP_404_NOT_FOUND)

        if 'user_id' in self.request.GET and self.request.GET['user_id']:
            user_id = self.request.GET['user_id']
        else:
            return Response({'error':'User id Not Found'}, status=status.HTTP_404_NOT_FOUND)

        if not UserIdentifier.objects.filter(id=user_id).exists():
            user_identifier = UserIdentifier()
            user_identifier.save()
        else:
            user_identifier = UserIdentifier.objects.get(id=user_id)

        if not UserPostAction.objects.filter(user_identifier=user_identifier).exists():
            user_action = UserPostAction.objects.create(user_identifier=user_identifier)
            
        else:
            user_action = UserPostAction.objects.get(user_identifier=user_identifier)

        if 'like' in self.request.data and self.request.data['like'] == True:
            
            if post not in user_action.liked_posts.all():
                post.like += 1
                post.status = 'Liked'
                post.user_identifier = user_identifier
                post.save()
                print("looooooo")
                if post in user_action.disliked_posts.all():
                    print("koooooo")
                    user_action.disliked_posts.remove(post)
                    post.dislike -= 1
                    post.save()
                user_action.liked_posts.add(post)

        if 'dislike' in self.request.data and self.request.data['dislike'] == True:
            if post not in user_action.disliked_posts.all():
                post.dislike += 1
                post.status = 'Disliked'
                post.user_identifier = user_identifier
                post.save()
                if post in user_action.liked_posts.all():
                    user_action.liked_posts.remove(post)
                    post.like -= 1
                    post.save()
                user_action.disliked_posts.add(post)

        
        data = {'post_name':post.post_name,
                'category':post.category.category_name,
                'description':post.description,
                'like':post.like,
                'dislike':post.dislike,
                'status':post.status,
                'date':post.updated_at
                }

        return JsonResponse(data, safe=False)