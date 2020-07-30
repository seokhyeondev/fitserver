from rest_framework import serializers
from fitzme.models import HotKeyword
from fitzme.models import UserSearchLog
from fitzme.models import Feed
from fitzme.models import UserOutfit
from fitzme.models import Garment

import pprint

class HotKeywordSerializer(serializers.ModelSerializer):
   class Meta:
       model = HotKeyword
       fields = ('word',)

        
class SearchLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSearchLog
        fields = ('word',
                  'email')

              
class GarmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Garment
        fields = '__all__'

class UserOutfitSerializer(serializers.ModelSerializer):
    top = GarmentSerializer(allow_null=True, required=False)
    bottom = GarmentSerializer(allow_null=True, required=False)
    dress = GarmentSerializer(allow_null=True, required=False)
    shoes = GarmentSerializer(allow_null=True, required=False)
    outer = GarmentSerializer(allow_null=True, required=False)
    
    class Meta:
        model = UserOutfit
        fields = '__all__'

class FeedSerializer(serializers.ModelSerializer):
    user_outfit = UserOutfitSerializer()
    class Meta:
        model = Feed
        fields = '__all__'

    def create(self, validated_data):
        outfit_data = validated_data.pop('user_outfit')
        top = None
        if 'top' in outfit_data:
            top_data = outfit_data.pop('top')
            try:
                top = Garment.objects.get(uuid=top_data["uuid"])
            except Garment.DoesNotExist:
                top = Garment.objects.create(**top_data)
                top.save()
                    
        bottom = None
        if 'bottom' in outfit_data:
            bottom_data = outfit_data.pop('bottom')
            try:
                bottom = Garment.objects.get(uuid=bottom_data["uuid"])
            except Garment.DoesNotExist:
                bottom = Garment.objects.create(**bottom_data)
                bottom.save()
                    
        dress = None
        if 'dress' in outfit_data:
            dress_data = outfit_data.pop('dress')
            try:
                dress = Garment.objects.get(uuid=dress_data["uuid"])
            except Garment.DoesNotExist:
                dress = Garment.objects.create(**dress_data)
                dress.save()
                    
        shoes = None
        if 'shoes' in outfit_data:
            shoes_data = outfit_data.pop('shoes')
            try:
                shoes = Garment.objects.get(uuid=shoes_data["uuid"])
            except Garment.DoesNotExist:
                shoes = Garment.objects.create(**shoes_data)
                shoes.save()
                    
        outer = None
        if 'outer' in outfit_data:
            outer_data = outfit_data.pop('shoes')
            try:
                outer = Garment.objects.get(uuid=outer_data["uuid"])
            except Garment.DoesNotExist:
                outer = Garment.objects.create(**outfit_data.pop('outer'))
                outer.save()
        outfit = UserOutfit.objects.create(top=top,bottom=bottom,dress=dress,shoes=shoes,outer=outer, **outfit_data)
        outfit.save()
        feed = Feed.objects.create(user_outfit=outfit, **validated_data)
        return feed
        
    def update(self, instance, validated_data):
        outfit_data = validated_data.pop('user_outfit')
        outfit = instance.user_outfit
        if 'hash_tag' in outfit_data:
            outfit.hash_tag = outfit_data["hash_tag"]
        if 'comment' in outfit_data:
            outfit.comment = outfit_data["comment"]
        outfit.save()
        instance.isShow = validated_data["isShow"]
        instance.email = validated_data["email"]
        instance.nickname = validated_data["nickname"]
        

        return super(FeedSerializer, self).update(instance, validated_data)
