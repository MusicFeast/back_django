from django.urls import path, include
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register(r'carousel', CarouselVS,basename='carousel')
router.register(r'artist', ArtistVS,basename='artist')
router.register(r'home', HomeVS,basename='home')
router.register(r'news', NewsVS,basename='news')
router.register(r'perfil', PerfilVS,basename='perfil')
router.register(r'about', AboutVS,basename='about')
router.register(r'coreteam', CoreTeamVS,basename='coreteam')
#router.register(r'address', AddressVS,basename='address')

urlpatterns = [
    path('', include(router.urls)),
    path('get-carousel', get_carousel),
    path('get-artists', get_artists),
    path('get-artists-home', get_artists_home),
    path('get-news', get_news),
    path('get-perfil-data/', get_perfil_data),
    path('validate-perfil/', validate_perfil),
    path('get-about', get_about),
    path('get-core-team', get_core_team),
]