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
import boto3
from django.http import JsonResponse


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


@api_view(["GET"])
@csrf_exempt
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def get_contest(request):
    contest = ContestForm.objects.filter()
    serializer = ContestFormSerializer(contest, many=True)
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
        artist = Artist.objects.get(id_collection=data['id'])
    except:
        artist = None

    if artist:
        tiersDatin = TiersComingSoon.objects.filter(artist=artist)
        if tiersDatin:
            tiersData = TiersComingSoonSerializer(tiersDatin, many=True)
            return Response(tiersData.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
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
    title = request.GET.get('title', '')
    news = News.objects.filter(is_visible=True, title__icontains=title)
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
            if data.address['country'] and data.address['phone_number'] and data.address['street_address'] and data.address['street_address2'] and data.address['city'] and data.address['state'] and data.address['postal']:
                serializer = self.get_serializer(data=data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                perfil = Perfil.objects.get(wallet=data['wallet'])
                address = Address.objects.create(perfil=perfil, country=data.address['country'], phone_number=data.address['phone_number'], street_address=data.address['street_address'],
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
            if data.address['country'] and data.address['phone_number'] and data.address['street_address'] and data.address['street_address2'] and data.address['city'] and data.address['state'] and data.address['postal']:
                partial = kwargs.pop('partial', False)
                instance = self.get_object()
                serializer = self.get_serializer(
                    instance, data=request.data, partial=partial)

                perfil = Perfil.objects.get(wallet=data['wallet'])
                address = Address.objects.get(perfil=perfil)

                address.country = data.address['country']
                address.phone_number = data.address['phone_number']
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

    # if data['discord']:
    #     discord = Perfil.objects.filter(
    #         discord=data['discord'].lower()).first()
    #     if (discord and data['wallet'] != discord.wallet and data['discord'] != ""):
    #         perfil['discord'] = True

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

        # if (item['discord'] != None):
        #     social.append({"name": "discord", "user": item['discord']})

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


@api_view(["POST"])
@csrf_exempt
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def get_avatar(request):
    datos = request.data
    item = Artist.objects.filter(id_collection=datos['artist']).first()
    if item:
        serializer = ArtistSerializer(item).data
        data = serializer
        return Response(data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_204_NO_CONTENT)


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
    media = NftMedia.objects.filter(
        artist=artist, number_collection=data['number_collection']).first()
    serializer = NftMediaSerializer(media)
    if data['media'] == 'audio':
        return Response({"media": serializer.data['audio']}, status=status.HTTP_200_OK)
    elif data['media'] == 'video':
        session = boto3.session.Session()
                
        client = session.client('s3',       
            region_name='us-east-1',
            endpoint_url='https://nyc3.digitaloceanspaces.com',
            aws_access_key_id='DO00L3WLA2MPXWDB28EG',
            aws_secret_access_key='Fyslwpr8HJe3+pNz8EiuCBABA1uwgA0aG5KaJanmjyw'
        )

        # file = s3.get_object(
        #     Bucket='tier2',
        #     Key=serializer.data['video']
        # )
        
        url = client.generate_presigned_url('get_object',
            Params={'Bucket': 'tier2',
            'Key': serializer.data['video']},
            ExpiresIn=3600
        )
        
        return Response({"media": url}, status=status.HTTP_200_OK)
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


class OrderRedeemVS(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    # authentication_classes = [TokenAuthentication]
    queryset = OrderRedeem.objects.all()
    serializer_class = OrderRedeemSerializer

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class DriveNftVS(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    authentication_classes = [BasicAuthentication]
    queryset = DriveNft.objects.all()
    serializer_class = DriveNftSerializer


class ContestFormVS(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    authentication_classes = [BasicAuthentication]
    queryset = ContestForm.objects.all()
    serializer_class = ContestFormSerializer

    def create(self, request):
        data = request.data

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        datos = serializer.data

        url = config('AWARD_NFT_API')
        response = requests.post(
            url, json={'wallet': data["wallet"], 'email': data["email"]})
        print(response.content)
        # datares = response.content

        return Response(datos, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class AdminVS(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    authentication_classes = [BasicAuthentication]
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

    def create(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["POST"])
@csrf_exempt
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def is_admin(request):
    data = request.data
    admin = Admin.objects.filter(wallet=data['admin'])
    artist = Artist.objects.filter(creator_id=data['admin']).first()
    if admin:
        if artist:
            # serializer = ArtistSerializer(artist)
            return Response({"admin": True, "artist": artist.id_collection}, status=status.HTTP_200_OK)
        else:
            return Response({"admin": True, "artist": None}, status=status.HTTP_200_OK)
    else:
        if artist:
            # serializer = ArtistSerializer(artist)
            return Response({"admin": False, "artist": artist.id_collection}, status=status.HTTP_200_OK)
        else:
            return Response({"admin": False, "artist": None}, status=status.HTTP_200_OK)


class ArtistProposalVS(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    authentication_classes = [BasicAuthentication]
    queryset = ArtistProposal.objects.all()
    serializer_class = ArtistProposalSerializer

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["POST"])
@csrf_exempt
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def get_artist_proposal(request):
    data = request.data
    artist = ArtistProposal.objects.filter(wallet=data['wallet'])
    serializer = ArtistProposalSerializer(artist, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
@csrf_exempt
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def get_artist_by_wallet(request):
    data = request.data
    artist = Artist.objects.filter(creator_id=data['wallet']).first()
    
    if artist:
        serializer = ArtistSerializer(artist)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(False, status=status.HTTP_200_OK)


@api_view(["POST"])
@csrf_exempt
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def get_artist_proposals(request):
    data = request.data
    admin = Admin.objects.filter(wallet=data['wallet'])
    if admin:
        artistProposals = ArtistProposal.objects.all()
        datos = []
        for artistProposal in artistProposals:
            serialized_data = ArtistProposalSerializer(artistProposal).data
            serialized_data['tiers'] = TierProposalSerializer(
                TierProposal.objects.filter(artist_proposal=artistProposal.id, status=3), many=True
            ).data
            datos.append(serialized_data)

        return Response(datos, status=status.HTTP_200_OK)
    else:
        artistProposals = ArtistProposal.objects.filter(wallet=data['wallet'])
        datos = []
        for artistProposal in artistProposals:
            serialized_data = ArtistProposalSerializer(artistProposal).data
            serialized_data['tiers'] = TierProposalSerializer(
                TierProposal.objects.filter(artist_proposal=artistProposal.id), many=True
            ).data
            datos.append(serialized_data)

        return Response(datos, status=status.HTTP_200_OK)


@api_view(["POST"])
@csrf_exempt
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def new_collection(request):
    data = request.data
    artist = Artist.objects.filter(
        creator_id=data["wallet"], id_collection=data["id_collection"]).first()
    if artist:
        responseTier = requests.post(
            config('NODE_URL_API') + "new-collection/", json={'idCollection': data["id_collection"], 'title': data["nft_name"], 'description': data["description"], 'price': data["price"], 'media': data["image"], 'royalty': data["royalties"], 'royaltyBuy': data["royalties_split"]})

        if responseTier:
            return Response({"hash": "hash"}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@ api_view(["POST"])
@ csrf_exempt
@ authentication_classes([BasicAuthentication])
@ permission_classes([AllowAny])
def response_proposal(request):
    data = request.data
    admin = Admin.objects.filter(wallet=data['wallet']).first()
    if admin:
        tierProposal = TierProposal.objects.filter(id=data['tier_id']).first()
        artistProposal = ArtistProposal.objects.filter(
            id=data['artist_id']).first()
        if data['status'] == 1 and tierProposal and artistProposal:
            id_collection = None
            artist = None
            if (tierProposal.tierNumber == 1):
                response = requests.post(
                    config('NODE_URL_API') + "create-artist/", json={'walletArtist': artistProposal.wallet_artist, 'artistName': artistProposal.name})
                dataJson = response.json()
                id_collection = dataJson.get('id_collection')

                if id_collection:
                    # Crear un objeto Artist con los datos de ArtistProposal
                    all_artists = Artist.objects.all()
    
                    # Encuentra la longitud de la lista de orden
                    order_list_length = len(all_artists)
    
                    artist = Artist(
                        id_collection=id_collection,
                        creator_id=artistProposal.wallet,
                        name=artistProposal.name,
                        description=artistProposal.description,
                        about=artistProposal.about,
                        image=artistProposal.image,
                        banner=artistProposal.banner,
                        banner_mobile=artistProposal.banner_mobile,
                        instagram=artistProposal.instagram,
                        twitter=artistProposal.twitter,
                        facebook=artistProposal.facebook,
                        is_visible=True,  # Puedes establecer el valor deseado
                        comming=False,  # Puedes establecer el valor deseado
                        order_list=order_list_length + 1
                    )
                    artist.save()

                    # Actualiza el estado de artistProposal y guarda
                    artistProposal.id_collection = id_collection
                    artistProposal.status = 1
                    artistProposal.save()
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            id_collection = id_collection if id_collection is not None else artistProposal.id_collection

            price = float(tierProposal.price)

            responseTier = requests.post(
                config('NODE_URL_API') + "create-tiers/", json={'idCollection': id_collection, 'title': tierProposal.nft_name, 'description': tierProposal.description, 'price': price, 'media': tierProposal.image, 'royalty': tierProposal.royalties, 'royaltyBuy': tierProposal.royalties_split, 'email': artistProposal.email})

            if responseTier:
                tierJson = responseTier.json()
                hash = tierJson
                artist = Artist.objects.get(id_collection=id_collection)
                if artist and (tierProposal.tierNumber == 1 or tierProposal.tierNumber == 2):
                    tiersComingSoon = TiersComingSoon(
                        artist=artist,
                        tierOne=False,
                        tierTwo=True,
                        tierThree=True,
                        tierFour=True,
                        tierFive=True,
                        tierSix=True
                    )
                    tiersComingSoon.save()
                    nftMedia = NftMedia.objects.get_or_create(artist=artist)
                    if nftMedia:
                        if tierProposal.tierNumber == 1:
                            nftMedia[0].audio = tierProposal.audio
                        else:
                            nftMedia[0].video = tierProposal.video
                        nftMedia[0].save()
                tierProposal.status = 1
                tierProposal.save()
                return Response({"hash": hash}, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        elif data['status'] == 2 and tierProposal:
            tierProposal.status = 2
            tierProposal.save()
            return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@ api_view(["POST"])
@ csrf_exempt
@ authentication_classes([BasicAuthentication])
@ permission_classes([AllowAny])
def save_form(request):
    data = request.data
    perfil = Perfil.objects.filter(wallet=data['wallet']).first()

    if perfil:
        # Si el perfil ya existe, actualiza los campos necesarios
        perfil.username = data['username']
        perfil.email = data['email']
        perfil.description = data['description']
        perfil.about = data['description']
        perfil.instagram = data['instagram']
        perfil.twitter = data['twitter']
        perfil.facebook = data['facebook']
        
        perfil.save()
    else:
        # Si el perfil no existe, crea uno nuevo
        perfil = Perfil(
            wallet=data['wallet'],
            username=data['username'],
            email=data['email'],
            description=data['description'],
            about=data['description'],
            instagram=data['instagram'],
            twitter=data['twitter'],
            facebook=data['facebook']
        )
        perfil.save()
        
        address = Address(perfil=perfil)
        address.save()
    
    artist = Artist.objects.filter(creator_id=data['wallet']).first()
    
    newArtist = False
    
    if not artist:    
        newArtist = True    
        response = requests.post(
            config('NODE_URL_API') + "create-artist/", json={'walletArtist': data['wallet'], 'artistName': data['username']})
        dataJson = response.json()
        id_collection = dataJson.get('id_collection')

        if id_collection:
            # Crear un objeto Artist con los datos de ArtistProposal
            all_artists = Artist.objects.all()

            # Encuentra la longitud de la lista de orden
            order_list_length = len(all_artists)

            artist = Artist(
                id_collection=id_collection,
                creator_id=data['wallet'],
                name=data['username'],
                description=data['description'],
                about=data['description'],
                image=perfil.avatar,
                banner=perfil.banner,
                banner_mobile=perfil.banner_mobile,
                instagram=data['instagram'],
                twitter=data['twitter'],
                facebook=data['facebook'],
                is_visible=True,  # Puedes establecer el valor deseado
                comming=False,  # Puedes establecer el valor deseado
                order_list=order_list_length + 1
            )
            artist.save()
    else:
        artist.name=data['username']
        artist.description=data['description']
        artist.about=data['description']
        artist.image=perfil.avatar
        artist.banner=perfil.banner
        artist.banner_mobile=perfil.banner_mobile
        artist.instagram=data['instagram']
        artist.twitter=data['twitter']
        artist.facebook=data['facebook']
        artist.save()
        
    id_collection = artist.id_collection

    price = float(data["price"])
    
    if newArtist:
        responseTier = requests.post(
            config('NODE_URL_API') + "create-tiers/", json={'idCollection': id_collection, 'title': data["nft_name"], 'description': data["description"], 'price': price, 'media': data["image"], 'royalty': data["royalties"], 'royaltyBuy': data["royalties_split"], 'email': data["email"]})

        if responseTier:
            tierJson = responseTier.json()
            hash = tierJson
            
            all_comings = TiersComingSoon.objects.filter(artist=artist)
            comings_length = len(all_comings)
            
            tiersComingSoon = TiersComingSoon(
                artist=artist,
                number_collection=comings_length + 1,
                tierOne=False,
                tierTwo=True,
                tierThree=True,
                tierFour=True,
                tierFive=True,
                tierSix=True
            )
            tiersComingSoon.save()
            
            all_medias = NftMedia.objects.filter(artist=artist)
            medias_length = len(all_medias)
            
            nftMedia = NftMedia(
                artist=artist,
                number_collection=medias_length + 1,
                audio=data["audio"]
            )
            nftMedia.save()
            return Response({"hash": hash, "id_collection": id_collection}, status=status.HTTP_200_OK)
            # nftMedia = NftMedia.objects.get_or_create(artist=artist)
            # if nftMedia:
            #     nftMedia[0].audio = data["audio"]
            #     nftMedia[0].number_collection = medias_length + 1
            #     nftMedia[0].save()
            
            #     return Response({"hash": hash}, status=status.HTTP_200_OK)
            # else:
            #     return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        responseTier = requests.post(
            config('NODE_URL_API') + "new-collection/", json={'idCollection': id_collection, 'title': data["nft_name"], 'description': data["description"], 'price': price, 'media': data["image"], 'royalty': data["royalties"], 'royaltyBuy': data["royalties_split"]})

        tierJson = responseTier.json()
        hash = tierJson
        
        all_comings = TiersComingSoon.objects.filter(artist=artist)
        comings_length = len(all_comings)
            
        tiersComingSoon = TiersComingSoon(
            artist=artist,
            number_collection=comings_length + 1,
            tierOne=False,
            tierTwo=True,
            tierThree=True,
            tierFour=True,
            tierFive=True,
            tierSix=True
        )
        tiersComingSoon.save()
        
        all_medias = NftMedia.objects.filter(artist=artist)
        medias_length = len(all_medias)
        
        nftMedia = NftMedia(
            artist=artist,
            number_collection=medias_length + 1,
            audio=data["audio"]
        )
        nftMedia.save()
        
        return Response({"hash": hash, "id_collection": id_collection}, status=status.HTTP_200_OK)
        
        # nftMedia = NftMedia.objects.get_or_create(artist=artist, number_collection=medias_length + 1)
        # if nftMedia:
        #     nftMedia[0].audio = data["audio"]
        #     nftMedia[0].number_collection = medias_length + 1
        #     nftMedia[0].save()
        
        #     return Response({"hash": hash}, status=status.HTTP_200_OK)
        # else:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)
        

# @ api_view(["POST"])
# @ csrf_exempt
# @ authentication_classes([BasicAuthentication])
# @ permission_classes([AllowAny])
# def save_form(request):
#     data = request.data
#     perfil = Perfil.objects.filter(wallet=data['wallet']).first()
    
#     if perfil:
#         perfil.
        
#         if data['status'] == 1 and tierProposal and artistProposal:
#             id_collection = None
#             artist = None
#             if (tierProposal.tierNumber == 1):
#                 response = requests.post(
#                     config('NODE_URL_API') + "create-artist/", json={'walletArtist': artistProposal.wallet_artist, 'artistName': artistProposal.name})
#                 dataJson = response.json()
#                 id_collection = dataJson.get('id_collection')

#                 if id_collection:
#                     # Crear un objeto Artist con los datos de ArtistProposal
#                     all_artists = Artist.objects.all()
    
#                     # Encuentra la longitud de la lista de orden
#                     order_list_length = len(all_artists)
    
#                     artist = Artist(
#                         id_collection=id_collection,
#                         creator_id=artistProposal.wallet,
#                         name=artistProposal.name,
#                         description=artistProposal.description,
#                         about=artistProposal.about,
#                         image=artistProposal.image,
#                         banner=artistProposal.banner,
#                         banner_mobile=artistProposal.banner_mobile,
#                         instagram=artistProposal.instagram,
#                         twitter=artistProposal.twitter,
#                         facebook=artistProposal.facebook,
#                         discord=artistProposal.discord,
#                         is_visible=True,  # Puedes establecer el valor deseado
#                         comming=False,  # Puedes establecer el valor deseado
#                         order_list=order_list_length + 1
#                     )
#                     artist.save()

#                     # Actualiza el estado de artistProposal y guarda
#                     artistProposal.id_collection = id_collection
#                     artistProposal.status = 1
#                     artistProposal.save()
#                 else:
#                     return Response(status=status.HTTP_400_BAD_REQUEST)
#             id_collection = id_collection if id_collection is not None else artistProposal.id_collection

#             price = float(tierProposal.price)

#             responseTier = requests.post(
#                 config('NODE_URL_API') + "create-tiers/", json={'idCollection': id_collection, 'title': tierProposal.nft_name, 'description': tierProposal.description, 'price': price, 'media': tierProposal.image, 'royalty': tierProposal.royalties, 'royaltyBuy': tierProposal.royalties_split, 'email': artistProposal.email})

#             if responseTier:
#                 tierJson = responseTier.json()
#                 hash = tierJson
#                 artist = Artist.objects.get(id_collection=id_collection)
#                 if artist and (tierProposal.tierNumber == 1 or tierProposal.tierNumber == 2):
#                     tiersComingSoon = TiersComingSoon(
#                         artist=artist,
#                         tierOne=False,
#                         tierTwo=True,
#                         tierThree=True,
#                         tierFour=True,
#                         tierFive=True,
#                         tierSix=True
#                     )
#                     tiersComingSoon.save()
#                     nftMedia = NftMedia.objects.get_or_create(artist=artist)
#                     if nftMedia:
#                         if tierProposal.tierNumber == 1:
#                             nftMedia[0].audio = tierProposal.audio
#                         else:
#                             nftMedia[0].video = tierProposal.video
#                         nftMedia[0].save()
#                 tierProposal.status = 1
#                 tierProposal.save()
#                 return Response({"hash": hash}, status=status.HTTP_200_OK)
#             else:
#                 return Response(status=status.HTTP_400_BAD_REQUEST)
#         elif data['status'] == 2 and tierProposal:
#             tierProposal.status = 2
#             tierProposal.save()
#             return Response(status=status.HTTP_200_OK)
#     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TierProposalVS(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    authentication_classes = [BasicAuthentication]
    queryset = TierProposal.objects.all()
    serializer_class = TierProposalSerializer


@ api_view(["POST"])
@ csrf_exempt
@ authentication_classes([BasicAuthentication])
@ permission_classes([AllowAny])
def update_tier_coming_soong(request):
    data = request.data
    artist = Artist.objects.filter(
        creator_id=data["wallet"], id_collection=data["id_collection"]).first()
    if artist:
        tiersComingSoon = TiersComingSoon.objects.get(artist=artist, number_collection=data["number_collection"])
        if (data["tier"]) == "1":
            tiersComingSoon.tierOne = False
            nftMedia = NftMedia.objects.get(artist=artist, number_collection=data["number_collection"])
            
            dataSeria = NftMediaSerializer(nftMedia).data
            
            if dataSeria["audio"]:
                session = boto3.session.Session()
                
                client = session.client('s3',       
                    region_name='us-east-1',
                    endpoint_url='https://nyc3.digitaloceanspaces.com',
                    aws_access_key_id= config('AWS_ACCESS_KEY_ID'),
                    aws_secret_access_key= config('AWS_SECRET_ACCESS_KEY')
                )
                
                wallets_administradores = ['andresdom.near', '5fda13fec977d4588daf6cd1fa941362e8d335d700fd7070868ba5f87edd0d54'] 
                
                if data['wallet'] not in wallets_administradores:
                    client.delete_object(
                        Bucket='tier2',
                        Key=dataSeria["audio"]
                    )
                
            nftMedia.audio = data["media_id"]
            nftMedia.save()
        elif (data["tier"] == "2"):
            tiersComingSoon.tierTwo = False
            nftMedia = NftMedia.objects.get(artist=artist, number_collection=data["number_collection"])
            dataSeria = NftMediaSerializer(nftMedia).data
            
            if dataSeria["video"]:
                session = boto3.session.Session()
                
                client = session.client('s3',       
                    region_name='us-east-1',
                    endpoint_url='https://nyc3.digitaloceanspaces.com',
                    aws_access_key_id= config('AWS_ACCESS_KEY_ID'),
                    aws_secret_access_key= config('AWS_SECRET_ACCESS_KEY')
                )
                
                wallets_administradores = ['andresdom.near', '5fda13fec977d4588daf6cd1fa941362e8d335d700fd7070868ba5f87edd0d54'] 
                
                if data['wallet'] not in wallets_administradores:
                    client.delete_object(
                        Bucket='tier2',
                        Key=dataSeria["video"]
                    ) 
    
            nftMedia.video = data["media_id"]
            nftMedia.save()
        elif (data["tier"] == "3"):
            tiersComingSoon.tierThree = False
        elif (data["tier"] == "4"):
            tiersComingSoon.tierFour = False
        elif (data["tier"] == "5"):
            tiersComingSoon.tierFive = False
        elif (data["tier"] == "6"):
            tiersComingSoon.tierSix = False
        tiersComingSoon.save()
        print(tiersComingSoon)
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
