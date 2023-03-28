from django.urls import path, include
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register(r'carousel', CarouselVS, basename='carousel')
router.register(r'artist', ArtistVS, basename='artist')
router.register(r'artist-submission', ArtistSubmissionVS,
                basename='artistsubmission')
router.register(r'tiers-coming-soon', TiersComingSoonVS,
                basename='tiers-available')
router.register(r'home', HomeVS, basename='home')
router.register(r'news', NewsVS, basename='news')
router.register(r'perfil', PerfilVS, basename='perfil')
router.register(r'about', AboutVS, basename='about')
router.register(r'coreteam', CoreTeamVS, basename='coreteam')
router.register(r'events', EventsVS, basename='events')
router.register(r'eventticket', EventTicketVS, basename='eventticket')
router.register(r'nftmedia', NftMediaVS, basename='nftmedia')
router.register(r'infomf', InfoMFVS, basename='infomf')
router.register(r'userdiscord', UserDiscordVS, basename='userdiscord')
router.register(r'artistdiscord', ArtistDiscordVS, basename='artistdiscord')
router.register(r'userroles', UserRolesVS, basename='userroles')
router.register(r'suscribe', SubscribeVS, basename='suscribe')
# router.register(r'address', AddressVS,basename='address')

urlpatterns = [
    path('', include(router.urls)),
    path('get-carousel', get_carousel),
    path('get-artists', get_artists),
    path('get-artist/', get_artist),
    path('get-tiers-coming/', get_tiers_coming),
    path('get-artists-home', get_artists_home),
    path('get-news', get_news),
    path('get-perfil-data/', get_perfil_data),
    path('validate-perfil/', validate_perfil),
    path('get-about', get_about),
    path('get-core-team', get_core_team),
    path('get-avatars/', get_avatars),
    path('get-events/', get_events),
    path('get-event-tickets/', get_event_tickets),
    path('get-media/', get_media),
    path('get-info-mf', get_info_mf),
    path('save-user-discord/', save_user_discord),
    path('get-chats-enabled/', get_chats_enabled),
]
