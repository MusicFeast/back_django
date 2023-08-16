from email.mime import image
from email.policy import default
from django.db import models
from django.contrib.auth.models import *
from tinymce.models import HTMLField

# Create your models here.


class Carousel(models.Model):
    name = models.CharField(max_length=255, null=False,
                            blank=False, default="")
    image = models.ImageField(null=True, blank=True)
    image_mobile = models.ImageField(null=True, blank=True)
    is_visible = models.BooleanField(default=False)


class Artist(models.Model):
    id_collection = models.PositiveBigIntegerField(
        null=False, blank=False, default=0)
    name = models.CharField(max_length=255, null=False,
                            blank=False, default="")
    description = HTMLField()
    about = HTMLField()
    order_list = models.PositiveIntegerField(
        null=False, blank=False, default=1)
    image = models.ImageField(null=True, blank=True)
    banner = models.ImageField(null=True, blank=True)
    banner_mobile = models.ImageField(null=True, blank=True)
    is_visible = models.BooleanField(default=False)
    comming = models.BooleanField(default=False)
    instagram = models.CharField(max_length=255, null=True, blank=True)
    twitter = models.CharField(max_length=255, null=True, blank=True)
    facebook = models.CharField(max_length=255, null=True, blank=True)
    discord = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.name)


class ArtistSubmission(models.Model):
    full_name = models.CharField(max_length=255, null=False,
                                 blank=False, default="")
    name_artist = models.CharField(max_length=255, null=False,
                                   blank=False, default="")
    genere = models.CharField(max_length=255, null=False,
                              blank=False, default="")
    email = models.EmailField(
        max_length=255, null=True, blank=True, unique=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    twitter = models.CharField(max_length=255, null=True, blank=True)
    facebook = models.CharField(max_length=255, null=True, blank=True)
    instagram = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.name_artist)


class TiersComingSoon(models.Model):
    artist = models.OneToOneField(Artist, on_delete=models.CASCADE)
    tierOne = models.BooleanField(default=False)
    tierTwo = models.BooleanField(default=False)
    tierThree = models.BooleanField(default=False)
    tierFour = models.BooleanField(default=False)
    tierFive = models.BooleanField(default=False)
    tierSix = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % (self.artist.name)


class Home(models.Model):
    artist = models.OneToOneField(Artist, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % (self.artist.name)


class News(models.Model):
    image = models.ImageField(null=True, blank=True)
    title = models.CharField(
        max_length=255, null=False, blank=False, default="")
    title2 = models.CharField(
        max_length=255, null=False, blank=False, default="")
    description = HTMLField()
    desc_long = HTMLField()
    is_visible = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.title)


class Perfil(models.Model):
    wallet = models.CharField(
        max_length=255, unique=True, null=False, blank=False)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(
        max_length=255, null=True, blank=True, unique=True)
    email = models.EmailField(
        max_length=255, null=True, blank=True, unique=True)
    avatar = models.ImageField(null=True, blank=True)
    banner = models.ImageField(null=True, blank=True)
    instagram = models.CharField(max_length=255, null=True, blank=True)
    twitter = models.CharField(max_length=255, null=True, blank=True)
    telegram = models.CharField(max_length=255, null=True, blank=True)
    discord = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.wallet)


class Address(models.Model):
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE)
    country = models.CharField(max_length=255, null=True, blank=True)
    street_address = models.CharField(max_length=255, null=True, blank=True)
    street_address2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    postal = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.perfil.wallet)


class About(models.Model):
    title = models.CharField(
        max_length=255, null=False, blank=False, default="")
    description = HTMLField()
    is_visible = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % (self.title)


class CoreTeam(models.Model):
    img = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=255, null=False,
                            blank=False, default="")
    position = models.CharField(
        max_length=255, null=False, blank=False, default="")
    description = HTMLField()
    is_visible = models.BooleanField(default=False)
    instagram = models.CharField(max_length=255, null=True, blank=True)
    twitter = models.CharField(max_length=255, null=True, blank=True)
    facebook = models.CharField(max_length=255, null=True, blank=True)
    discord = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.name)


class Events(models.Model):
    name = models.CharField(max_length=255, null=False,
                            blank=False, default="")
    serie_ticket = models.CharField(max_length=255, null=True, blank=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    img = models.ImageField(null=True, blank=True)
    description = HTMLField()
    coordinates = models.CharField(max_length=255, null=True, blank=True)
    date_event = models.DateTimeField()
    location_event = models.CharField(max_length=255, null=True, blank=True)
    location_name = models.CharField(max_length=255, null=True, blank=True)
    location_desc = models.TextField(max_length=255, null=True, blank=True)
    is_visible = models.BooleanField(default=False)
    link_instagram = models.CharField(max_length=255, null=True, blank=True)
    link_twitter = models.CharField(max_length=255, null=True, blank=True)
    link_facebook = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.name)


class EventTicket(models.Model):
    serie_id = models.CharField(max_length=255, null=True, blank=True)
    event = models.ForeignKey(
        Events, null=True, blank=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.serie_id)


class NftMedia(models.Model):
    artist = models.OneToOneField(
        Artist, on_delete=models.CASCADE, null=True, blank=True)
    audio = models.FileField(null=True, blank=True)
    video = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.artist)


class InfoMF(models.Model):
    join_community = models.TextField(null=True, blank=True)
    instagram_icon = models.CharField(
        max_length=255, null=True, blank=True, default="mdi-instagram")
    instagram_link = models.CharField(max_length=255, null=True, blank=True)
    twitter_icon = models.CharField(
        max_length=255, null=True, blank=True, default="mdi-twitter")
    twitter_link = models.CharField(max_length=255, null=True, blank=True)
    facebook_icon = models.CharField(
        max_length=255, null=True, blank=True, default="mdi-facebook")
    facebook_link = models.CharField(max_length=255, null=True, blank=True)
    discord_icon = models.CharField(
        max_length=255, null=True, blank=True, default="discord")
    discord_link = models.CharField(max_length=255, null=True, blank=True)


class UserDiscord(models.Model):
    wallet = models.CharField(
        max_length=255, null=True, blank=True)
    discord_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return '%s' % (self.wallet)


class ArtistDiscord(models.Model):
    artist = models.OneToOneField(
        Artist, on_delete=models.CASCADE, null=True, blank=True)
    role_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return '%s' % (self.artist.name)


class UserRoles(models.Model):
    user = models.ForeignKey(UserDiscord, null=True,
                             blank=True, on_delete=models.CASCADE)
    role = models.ForeignKey(ArtistDiscord, null=True,
                             blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % (self.user.wallet)


class Subscribe(models.Model):
    email = models.EmailField(
        max_length=255, null=True, blank=True, unique=True)

    def __str__(self):
        return '%s' % (self.email)


class OrderRedeem(models.Model):
    wallet_burn = models.CharField(max_length=255)
    token_id = models.CharField(max_length=255)
    hash_burn = models.CharField(max_length=255)
    country = models.CharField(max_length=255, null=True, blank=True)
    street_address = models.CharField(max_length=255, null=True, blank=True)
    street_address2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    postal = models.CharField(max_length=255, null=True, blank=True)
    sku = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(
        max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    approved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class DriveNft(models.Model):
    wallet = models.CharField(
        max_length=255, null=False, blank=False, default="")
    token_id = models.CharField(
        max_length=255, null=False, blank=False, default="")
    email = models.EmailField(
        max_length=255, null=True, blank=True)

    def __str__(self):
        return '%s - %s' % (self.wallet, self.token_id)
