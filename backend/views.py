from decouple import config
from copyreg import constructor
from re import search
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from crypt import crypt
from .serializers import *
from .models import *
import json
from django.contrib.auth import login
import requests
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


# Create your views here.


class CarouselVS(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Carousel.objects.all()
    serializer_class = CarouselSerializer


@api_view(["GET"])
@csrf_exempt
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def get_carousel(request):
    carousel = Carousel.objects.filter(is_visible=True)
    serializer = CarouselSerializer(carousel, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class ArtistVS(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class ArtistSubmissionVS(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    # authentication_classes=[BasicAuthentication]
    queryset = ArtistSubmission.objects.all()
    serializer_class = ArtistSubmissionSerializer

    def create(self, request):
        data = request.data
        try:
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            datos = serializer.data
            network = "TESTNET: "
            if config("NETWORK") == "mainnet":
                network = ""
            send_mail_mf(
                ["jburkholder1985@gmail.com", "blake_harden@yahoo.com"],
                'MusicFeast: You have a new artist submission',
                'artist_submission.html',
                {
                    "network": network,
                    "full_name": datos["full_name"],
                    "name_artist": datos["name_artist"],
                    "genere": datos["genere"],
                    "email": datos["email"],
                    "website": datos["website"] or "",
                    "twitter": datos["twitter"] or "",
                    "instagram": datos["instagram"] or "",
                    "facebook": datos["facebook"] or "",
                }
            )
            return Response(datos, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            print(e)
            return Response("%s" % (e), status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TiersComingSoonVS(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = TiersComingSoon.objects.all()
    serializer_class = TiersComingSoonSerializer


@api_view(["GET"])
@csrf_exempt
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def get_artists(request):
    artists = Artist.objects.filter(is_visible=True)
    serializer = ArtistSerializer(artists, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@csrf_exempt
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def get_artist(request):
    data = request.data
    artists = Artist.objects.filter(is_visible=True, id_collection=data['id'])
    serializer = ArtistSerializer(artists, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@csrf_exempt
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def get_tiers_coming(request):
    data = request.data
    try:
        artist = Artist.objects.get(id=data['id'])
    except:
        artist = None

    print(artist)
    if artist:
        tiersDatin = TiersComingSoon.objects.filter(artist=artist).first()
        if tiersDatin:
            tiersData = TiersComingSoonSerializer(tiersDatin)
            return Response(tiersData.data, status=status.HTTP_200_OK)
        else:
            tiersData = {
                "tierOne": False,
                "tierTwo": False,
                "tierThree": False,
                "tierFour": False,
                "tierFive": False,
                "tierSix": False,
            }
            return Response(tiersData, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


class HomeVS(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
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
    return Response(data, status=status.HTTP_200_OK)


class NewsVS(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = News.objects.all()
    serializer_class = NewsSerializer


@api_view(["GET"])
@csrf_exempt
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def get_news(request):
    news = News.objects.filter(is_visible=True)
    serializer = NewsSerializer(news, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class PerfilVS(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    # authentication_classes=[BasicAuthentication]
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('wallet', 'username')

    def create(self, request):
        data = request.data
        data.address = json.loads(data['address'])

        try:
            if data.address['country'] and data.address['street_address'] and data.address['street_address2'] and data.address['city'] and data.address['state'] and data.address['postal']:
                serializer = self.get_serializer(data=data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                perfil = Perfil.objects.get(wallet=data['wallet'])
                address = Address.objects.create(perfil=perfil, country=data.address['country'], street_address=data.address['street_address'],
                                                 street_address2=data.address['street_address2'], city=data.address['city'], state=data.address['state'], postal=data.address['postal'])
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
            return Response("%s" % (e), status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        data = request.data
        data.address = json.loads(data['address'])
        try:
            if data.address['country'] and data.address['street_address'] and data.address['street_address2'] and data.address['city'] and data.address['state'] and data.address['postal']:
                partial = kwargs.pop('partial', False)
                instance = self.get_object()
                serializer = self.get_serializer(
                    instance, data=request.data, partial=partial)

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
                return Response(datos, status=status.HTTP_200_OK)
            else:
                partial = kwargs.pop('partial', False)
                instance = self.get_object()
                serializer = self.get_serializer(
                    instance, data=request.data, partial=partial)
                perfil = Perfil.objects.get(wallet=data['wallet'])
                address = Address.objects.get(perfil=perfil)
                data_address = AddressSerializer(address).data
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                datos = serializer.data
                datos.address = data_address
                return Response(datos, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response("%s" % (e), status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class AddressVS(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    authentication_classes = [BasicAuthentication]
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
        return Response([datos], status=status.HTTP_200_OK)
    return Response([], status=status.HTTP_200_OK)


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
        username = Perfil.objects.filter(
            username=data['username'].lower()).first()
        if (username and data['wallet'] != username.wallet and data['username'] != ""):
            perfil['username'] = True

    if data['email']:
        email = Perfil.objects.filter(email=data['email'].lower()).first()
        if (email and data['wallet'] != email.wallet):
            perfil['email'] = True

    if data['discord']:
        discord = Perfil.objects.filter(
            discord=data['discord'].lower()).first()
        if (discord and data['wallet'] != discord.wallet and data['discord'] != ""):
            perfil['discord'] = True

    if data['instagram']:
        instagram = Perfil.objects.filter(
            instagram=data['instagram'].lower()).first()
        if (instagram and data['wallet'] != instagram.wallet and data['instagram'] != ""):
            perfil['instagram'] = True

    if data['twitter']:
        twitter = Perfil.objects.filter(
            twitter=data['twitter'].lower()).first()
        if (twitter and data['wallet'] != twitter.wallet and data['twitter'] != ""):
            perfil['twitter'] = True

    if data['telegram']:
        telegram = Perfil.objects.filter(
            telegram=data['telegram'].lower()).first()
        if (telegram and data['wallet'] != telegram.wallet and data['telegram'] != ""):
            perfil['telegram'] = True
    return Response(perfil, status=status.HTTP_200_OK)


class AboutVS(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = About.objects.all()
    serializer_class = AboutSerializer


@api_view(["GET"])
@csrf_exempt
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def get_about(request):
    about = About.objects.filter(is_visible=True)
    serializer = AboutSerializer(about, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class CoreTeamVS(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
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
    return Response(data, status=status.HTTP_200_OK)


@api_view(["POST"])
@csrf_exempt
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def get_avatars(request):
    datos = request.data
    data = []
    for id in datos['artists']:
        item = Artist.objects.filter(id_collection=id).first()
        if item:
            serializer = ArtistSerializer(item).data
            data.append(serializer)
    return Response(data, status=status.HTTP_200_OK)


class EventsVS(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
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
        events = Events.objects.filter(artist=artist, is_visible=True)
        serializer = EventsSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response([], status=status.HTTP_200_OK)


class EventTicketVS(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
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
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response([], status=status.HTTP_200_OK)


class NftMediaVS(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = NftMedia.objects.all()
    serializer_class = NftMediaSerializer


@api_view(["POST"])
@csrf_exempt
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def get_media(request):
    data = request.data
    artist = Artist.objects.get(id_collection=data['artist'])
    media = NftMedia.objects.get(artist=artist)
    serializer = NftMediaSerializer(media)
    if data['media'] == 'audio':
        return Response({"media": serializer.data['audio']}, status=status.HTTP_200_OK)
    elif data['media'] == 'video':
        return Response({"media": serializer.data['video']}, status=status.HTTP_200_OK)
    return Response([], status=status.HTTP_200_OK)


class InfoMFVS(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = InfoMF.objects.all()
    serializer_class = InfoMFSerializer


@api_view(["GET"])
@csrf_exempt
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def get_info_mf(request):
    info = InfoMF.objects.all()
    serializer = InfoMFSerializer(info, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class ArtistDiscordVS(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    authentication_classes = [BasicAuthentication]
    queryset = ArtistDiscord.objects.all()
    serializer_class = ArtistDiscordSerializer


class UserDiscordVS(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = UserDiscord.objects.all()
    serializer_class = UserDiscordSerializer


@api_view(["POST"])
@csrf_exempt
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def save_user_discord(request):
    data = request.data
    userdc = UserDiscord.objects.filter(wallet=data['wallet'])
    if userdc:
        return Response(status=status.HTTP_200_OK)
    user = UserDiscord.objects.create(
        wallet=data['wallet'], discord_id=data['discord_id'])
    data_user = UserDiscordSerializer(user).data
    return Response(data_user, status=status.HTTP_200_OK)


class UserRolesVS(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = UserRoles.objects.all()
    serializer_class = UserRolesSerializer


@api_view(["POST"])
@csrf_exempt
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def get_chats_enabled(request):
    data = request.data
    userDiscord = UserDiscord.objects.filter(wallet=data['wallet'])
    if userDiscord:
        user = UserDiscord.objects.get(wallet=data['wallet'])
        roles = UserRoles.objects.filter(user=user)
        serializer = UserRolesSerializer(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response([], status=status.HTTP_200_OK)


class SubscribeVS(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    authentication_classes = [BasicAuthentication]
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer


def send_mail_mf(users_mail, subject, template_name, context):
    template = get_template(template_name)
    content = template.render(context)

    message = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=users_mail,
        cc=[]
    )

    message.attach_alternative(content, 'text/html')
    message.send(fail_silently=False)
    return
