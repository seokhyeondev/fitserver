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
        hotKeywords = HotKeyword.objects.all().order_by('-nowCount')
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
        
        email = request.GET.get('email', None)
        if email is not None:
            seachlogs = seachlogs.filter(email=email)
        else:
            return JsonResponse({'message': 'Email required'}, status=status.HTTP_404_NOT_FOUND)
        
        searchlogs_list = []
        for searchlog in searchlogs:
            searchlogs_list.append(seachlog.word)
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

