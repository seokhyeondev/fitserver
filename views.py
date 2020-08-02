from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
 

from fitzme.models import HotKeyword
from fitzme.serializers import HotKeywordSerializer

from fitzme.models import UserSearchLog
from fitzme.serializers import SearchLogSerializer

from fitzme.models import Feed
from fitzme.serializers import FeedSerializer

from fitzme.models import UserOutfit
from fitzme.serializers import UserOutfitSerializer

from fitzme.models import Garment
from fitzme.serializers import GarmentSerializer

from rest_framework.decorators import api_view

@api_view(['GET'])
def hotkeyword_list(request):
    if request.method == 'GET':
        hotKeywords = HotKeyword.objects.all().order_by('-nowCount')[:10:1]
        hotKeywords_list = []
        for keyword in hotKeywords:
            hotKeywords_list.append(keyword.word)
        return JsonResponse({
            'result' : hotKeywords_list
        }, json_dumps_params = {'ensure_ascii': True})

@api_view(['GET', 'POST'])
def searchlog_list(request):
    if request.method == 'GET':
        searchlogs = UserSearchLog.objects.all()
        
        word = request.GET.get('word')
        if word is not None:
            if word:
                searchlogs = searchlogs.filter(word__icontains=word)
            else:
                searchlogs = []
        searchlogs_list = []
        for searchlog in searchlogs:
            searchlogs_list.append(searchlog.word)
        return JsonResponse({
            'result' : searchlogs_list
        }, json_dumps_params = {'ensure_ascii': True})
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        searchlog_data = JSONParser().parse(request)
        searchlog_serializer = SearchLogSerializer(data=searchlog_data)

        try:
            hotkeyword = HotKeyword.objects.get(word=searchlog_data["word"])
            hotkeyword.nowCount = hotkeyword.nowCount + 1
            hotkeyword.save()
        except HotKeyword.DoesNotExist:
            hotkeyword_serializer = HotKeywordSerializer(data=searchlog_data)
            if hotkeyword_serializer.is_valid():
                hotkeyword_serializer.save()
        searchlogs = UserSearchLog.objects.filter(email=searchlog_data["email"],word=searchlog_data["word"])
        searchlogs.delete()
            
        if searchlog_serializer.is_valid():
            searchlog_serializer.save()
            return JsonResponse(searchlog_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(searchlog_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
def searchlog_list_detail(request, email):
    try:
        searchlogs = UserSearchLog.objects.filter(email=email)
    except UserSearchLog.DoesNotExist:
        return JsonResponse({'message': 'The Searchlog does not exist'}, status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        searchlogs_list = []
        for searchlog in searchlogs:
            searchlogs_list.append(searchlog.word)
        return JsonResponse({
            'result' : searchlogs_list
        }, json_dumps_params = {'ensure_ascii': True})

    elif request.method == 'DELETE':
        searchlogs.delete()
        return JsonResponse({'message': 'Searchlog was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def feed_list(request):
    if request.method == 'GET':
        feeds = Feed.objects.all().order_by('-id')
        isFilter = False
        like_log_id = request.GET.get('like_log_id', None)
        if like_log_id is not None:
            feeds = feeds.filter(like_log_id=like_log_id)
            isFilter = True
        email = request.GET.get('email', None)
        if email is not None:
            feeds = feeds.filter(email=email)
            isFilter = True

        if isFilter is False:
            feeds = feeds.filter(isShow=True)

        tag_search = request.GET.get('tags', None)
        if tag_search is not None:
            tempfeeds = []
            for feed in feeds :
                if tag_search in feed.user_outfit.hash_tag  :
                    tempfeeds.append(feed)
            feeds = tempfeeds

        colors_search = request.GET.getlist('color', None)
        tempfeeds = []
        if colors_search:
            feeds.filter(user_outfit__top__color__in=colors_search)
            for feed in feeds :
                if feed.user_outfit.top is not None:
                    if feed.user_outfit.top.color in colors_search:
                        tempfeeds.append(feed)
                        continue
                if feed.user_outfit.bottom is not None:
                    if feed.user_outfit.bottom.color in colors_search:
                        tempfeeds.append(feed)
                        continue
                if feed.user_outfit.outer is not None:
                    if feed.user_outfit.outer.color in colors_search:
                        tempfeeds.append(feed)
                        continue
                if feed.user_outfit.dress is not None:
                    if feed.user_outfit.dress.color in colors_search:
                        tempfeeds.append(feed)
                        continue
                if feed.user_outfit.shoes is not None:
                    if feed.user_outfit.shoes.color in colors_search:
                        tempfeeds.append(feed)
                        continue
            feeds = tempfeeds
            
        styletags = request.GET.getlist('styletag', None)
        if styletags:
            for feed in feeds:
                for styletag in styletags:
                    if feed.style_tag:
                        if styletag in feed.style_tag:
                            tempfeeds.append(feed)
                            continue
            feeds = tempfeeds           
            
        feeds_serializer = FeedSerializer(feeds, many=True)
        return JsonResponse(feeds_serializer.data, safe=False)
        # 'safe=False' for objects serialization 
    elif request.method == 'POST':
        feed_data = JSONParser().parse(request)
        feeds_serializer = FeedSerializer(data=feed_data)

            
        if feeds_serializer.is_valid():
            feeds_serializer.save()
            return JsonResponse(feeds_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(feeds_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE', 'PATCH'])
def feed_list_detail(request, pk):
    try:
        feed = Feed.objects.get(pk=pk)
        print(feed)
    except Feed.DoesNotExist:
        return JsonResponse({'message': 'The Feed does not exist'}, status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        feeds_serializer = FeedSerializer(feed)
        return JsonResponse(feeds_serializer.data, safe=False)
 
    elif request.method == 'DELETE':
        feed.delete()
        return JsonResponse({'message': 'Searchlog Feed deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PATCH':
        feed_data = JSONParser().parse(request)
        feeds_serializer = FeedSerializer(feed, data=feed_data)
        if feeds_serializer.is_valid():
            feeds_serializer.save()
            return JsonResponse(feeds_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse({'message': 'Searchlog Feed fatched successfully!'}, status=status.HTTP_204_NO_CONTENT)

