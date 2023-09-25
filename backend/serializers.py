from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class CarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carousel
        fields = '__all__'


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'


class ArtistSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistSubmission
        fields = '__all__'


class TiersComingSoonSerializer(serializers.ModelSerializer):
    class Meta:
        model = TiersComingSoon
        fields = '__all__'


class HomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'


class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = '__all__'


class CoreTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoreTeam
        fields = '__all__'


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'


class EventTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTicket
        fields = '__all__'


class NftMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NftMedia
        fields = '__all__'


class InfoMFSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoMF
        fields = '__all__'


class UserDiscordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDiscord
        fields = '__all__'


class ArtistDiscordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistDiscord
        fields = '__all__'


class UserRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoles
        fields = '__all__'


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = '__all__'


class OrderRedeemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRedeem
        fields = '__all__'


class DriveNftSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriveNft
        fields = '__all__'


class ContestFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestForm
        fields = '__all__'


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'
