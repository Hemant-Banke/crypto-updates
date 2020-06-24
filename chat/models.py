from django.db import models
from jsonfield import JSONField


class Room(models.Model):
    """
    A room for people to chat in.
    """

    # Room title
    title = models.CharField(max_length=255)

    # If only "staff" users are allowed (is_staff on django's User)
    staff_only = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def group_name(self):
        """
        Returns the Channels Group name that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return "room-%s" % self.id



class Exchanges(models.Model):
    """
    Defines the exchanges to be used
    """

    # Room title
    exchange_name = models.CharField(max_length=255)

    price_endpoint = models.CharField(max_length=1000, blank=True)
    is_all_coins = models.BooleanField(default=True)
    has_usdt = models.BooleanField(default=True)
    price_datatype = JSONField(null=True)

    symbol_format = models.CharField(max_length=360, default="{symbol}")
    bookTicker_endpoint = models.CharField(max_length=1000, blank=True)

    symbols_endpoint = models.CharField(max_length=1000, blank=True)

    exchange_img_url = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.exchange_name