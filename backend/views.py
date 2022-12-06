from copyreg import constructor
from re import search
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication
from crypt import crypt
from .serializers import *
from .models import *
import json
from django.contrib.auth import login
import requests
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAdminUser,IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import viewsets,status
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

class CarouselVS(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    queryset = Carousel.objects.all()
    serializer_class = CarouselSerializer

@api_view(["GET"])
@csrf_exempt
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def get_carousel(request):
    carousel = Carousel.objects.filter(is_visible=True)
    serializer = CarouselSerializer(carousel, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

class ArtistVS(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

@api_view(["GET"])
@csrf_exempt
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def get_artists(request):
    artists = Artist.objects.filter(is_visible=True)
    serializer = ArtistSerializer(artists, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(["POST"])
@csrf_exempt
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def get_artist(request):
    data = request.data
    artists = Artist.objects.filter(is_visible=True, id=data['id'])
    print(artists)
    serializer = ArtistSerializer(artists, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

class HomeVS(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    queryset = Home.objects.all()
    serializer_class = HomeSerializer

@api_view(["GET"])
@csrf_exempt
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def get_artists_home(request):
    home = Home.objects.all()
    artists = HomeSerializer(home, many=True).data
    data = []
    for artist in artists:
        item = Artist.objects.get(id=artist['artist'])
        if item.is_visible:
            serializer = ArtistSerializer(item).data
            data.append(serializer)
    return Response(data,status=status.HTTP_200_OK)

class NewsVS(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    queryset = News.objects.all()
    serializer_class = NewsSerializer

@api_view(["GET"])
@csrf_exempt
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def get_news(request):
    news = News.objects.filter(is_visible=True)
    serializer = NewsSerializer(news, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

class PerfilVS(viewsets.ModelViewSet):
    permission_classes=[AllowAny]
    #authentication_classes=[BasicAuthentication]
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('wallet', 'username')

    def create(self,request):  
        data = request.data
        data.address = json.loads(data['address'])
   
        try:
            if data.address['country'] and data.address['street_address'] and data.address['street_address2'] and data.address['city'] and data.address['state'] and data.address['postal']:
                serializer = self.get_serializer(data=data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                perfil = Perfil.objects.get(wallet=data['wallet'])
                address = Address.objects.create(perfil=perfil,country=data.address['country'],street_address=data.address['street_address'],street_address2=data.address['street_address2'],city=data.address['city'],state=data.address['state'],postal=data.address['postal'])
                data_address = AddressSerializer(address).data
                headers = self.get_success_headers(serializer.data)
                datos = serializer.data
                datos.address = data_address
                return Response(datos, status=status.HTTP_201_CREATED, headers=headers)
            else:
                serializer = self.get_serializer(data=data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                perfil = Perfil.objects.get(wallet=data['wallet'])
                address = Address.objects.create(perfil=perfil)
                data_address = AddressSerializer(address).data
                headers = self.get_success_headers(serializer.data)
                datos = serializer.data
                datos.address = data_address
                return Response(datos, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            print(e)
            return Response("%s"%(e),status=status.HTTP_400_BAD_REQUEST)
    
    def update(self,request,*args,**kwargs):
        data = request.data
        data.address = json.loads(data['address'])
        try:
            if data.address['country'] and data.address['street_address'] and data.address['street_address2'] and data.address['city'] and data.address['state'] and data.address['postal']:
                partial = kwargs.pop('partial', False)
                instance = self.get_object()
                serializer = self.get_serializer(instance, data=request.data, partial=partial)
             
                perfil = Perfil.objects.get(wallet=data['wallet'])
                address = Address.objects.get(perfil=perfil)
             
                address.country = data.address['country']
                address.street_address = data.address['street_address']
                address.street_address2 = data.address['street_address2']
                address.city = data.address['city']
                address.state = data.address['state']
                address.postal = data.address['postal']
                address.save()

                data_address = AddressSerializer(address).data
        
                serializer.is_valid(raise_exception=True)                
                self.perform_update(serializer)

                datos = serializer.data
                datos.address = data_address
                return Response(datos,status=status.HTTP_200_OK)
            else:
                partial = kwargs.pop('partial', False)
                instance = self.get_object()
                serializer = self.get_serializer(instance, data=request.data, partial=partial)
                perfil = Perfil.objects.get(wallet=data['wallet'])
                address = Address.objects.get(perfil=perfil)
                data_address = AddressSerializer(address).data
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                datos = serializer.data
                datos.address = data_address
                return Response(datos,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response("%s"%(e),status=status.HTTP_400_BAD_REQUEST)
    def list(self, request, *args, **kwargs):
       return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def retrieve(self, request, *args, **kwargs):
       return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class AddressVS(viewsets.ModelViewSet):
    permission_classes=[AllowAny]
    authentication_classes=[BasicAuthentication]
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


@api_view(["POST"])
@csrf_exempt
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def get_perfil_data(request):
    data = request.data
    perfil = Perfil.objects.filter(wallet=data['wallet']).first()
    if (perfil):
        address = Address.objects.get(perfil=perfil)
        data_perfil = PerfilSerializer(perfil).data
        data_address = AddressSerializer(address).data
        datos = data_perfil
        datos['address'] = data_address
        return Response([datos],status=status.HTTP_200_OK)
    return Response([],status=status.HTTP_200_OK)

@api_view(["POST"])
@csrf_exempt
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def validate_perfil(request):
    data = request.data
    perfil = {
        "username": False,
        "email": False,
        "discord": False,
        "instagram": False,
        "twitter": False,
        "telegram": False
    }

    if data['username']:
        username = Perfil.objects.filter(username=data['username'].lower()).first()
        if (username and data['wallet'] != username.wallet and data['username'] != ""):
            perfil['username'] = True

    if data['email']:
        email = Perfil.objects.filter(email=data['email'].lower()).first()
        if (email and data['wallet'] != email.wallet):
            perfil['email'] = True

    if data['discord']:
        discord = Perfil.objects.filter(discord=data['discord'].lower()).first()
        if (discord and data['wallet'] != discord.wallet and data['discord'] != ""):
            perfil['discord'] = True

    if data['instagram']:
        instagram = Perfil.objects.filter(instagram=data['instagram'].lower()).first()
        if (instagram and data['wallet'] != instagram.wallet and data['instagram'] != ""):
            perfil['instagram'] = True

    if data['twitter']:
        twitter = Perfil.objects.filter(twitter=data['twitter'].lower()).first()
        if (twitter and data['wallet'] != twitter.wallet and data['twitter'] != ""):
            perfil['twitter'] = True

    if data['telegram']:
        telegram = Perfil.objects.filter(telegram=data['telegram'].lower()).first()
        if (telegram and data['wallet'] != telegram.wallet and data['telegram'] != ""):
            perfil['telegram'] = True
    return Response(perfil,status=status.HTTP_200_OK)

class AboutVS(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    queryset = About.objects.all()
    serializer_class = AboutSerializer

@api_view(["GET"])
@csrf_exempt
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def get_about(request):
    about = About.objects.filter(is_visible=True)
    serializer = AboutSerializer(about, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

class CoreTeamVS(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    queryset = CoreTeam.objects.all()
    serializer_class = CoreTeamSerializer

@api_view(["GET"])
@csrf_exempt
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def get_core_team(request):
    coreteam = CoreTeam.objects.filter(is_visible=True)
    items = CoreTeamSerializer(coreteam, many=True).data
    data = []
    for item in items:
        datos = {
            "img": item['img'],
            "name": item['name'],
            "position": item['position'],
            "description": item['description'],
            "social": []
        }
        social = []
        if (item['instagram'] != None):
            social.append({"name": "instagram", "user": item['instagram']})

        if (item['twitter'] != None):
            social.append({"name": "twitter", "user": item['twitter']})

        if (item['facebook'] != None):
            social.append({"name": "facebook", "user": item['facebook']})

        if (item['discord'] != None):
            social.append({"name": "discord", "user": item['discord']})

        datos['social'] = social

        data.append(datos)
    return Response(data,status=status.HTTP_200_OK)

@api_view(["POST"])
@csrf_exempt
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def get_avatars(request):
    datos = request.data
    data = []
    for id in datos['artists']:
        item = Artist.objects.get(id_collection=id)
        serializer = ArtistSerializer(item).data
        data.append(serializer)
    return Response(data,status=status.HTTP_200_OK)

class EventsVS(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    queryset = Events.objects.all()
    serializer_class = EventsSerializer

@api_view(["POST"])
@csrf_exempt
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def get_events(request):
    data = request.data
    artist = Artist.objects.get(id_collection=data['artist_id'])
    if artist:
        events = Events.objects.filter(artist=artist ,is_visible=True)
        serializer = EventsSerializer(events, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    return Response([],status=status.HTTP_200_OK)

class EventTicketVS(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    queryset = EventTicket.objects.all()
    serializer_class = EventTicketSerializer
    
@api_view(["POST"])
@csrf_exempt
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def get_event_tickets(request):
    data = request.data
    event = Events.objects.get(id=data['event_id'])
    if event:
        tickets = EventTicket.objects.filter(event=event)
        serializer = EventTicketSerializer(tickets, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    return Response([],status=status.HTTP_200_OK)

class NftMediaVS(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    queryset = NftMedia.objects.all()
    serializer_class = NftMediaSerializer
    
@api_view(["POST"])
@csrf_exempt
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def get_media(request):
    data = request.data
    media = NftMedia.objects.filter(tier=data['tier'], artist=data['artist'])
    serializer = NftMediaSerializer(media, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)