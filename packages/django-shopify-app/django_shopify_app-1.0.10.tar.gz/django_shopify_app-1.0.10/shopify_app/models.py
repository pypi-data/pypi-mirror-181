from functools import cached_property

from django.db import models
from django.apps import apps
from django.conf import settings

import shopify
from shopify import Session

from .services.webhooks import update_shop_webhooks


class ShopBase(models.Model):

    shopify_domain = models.CharField(max_length=50, default="")
    shopify_token = models.CharField(
        max_length=150, default="", blank=True, null=True
    )
    access_scopes = models.CharField(max_length=250, default="")

    @cached_property
    def shopify(self):
        return shopify

    @property
    def shopify_session(self):
        api_version = apps.get_app_config("shopify_app").SHOPIFY_API_VERSION
        shopify_domain = self.shopify_domain
        return Session.temp(shopify_domain, api_version, self.shopify_token)

    def installed(self):
        pass

    def update_webhooks(self):
        update_shop_webhooks(self)

    class Meta:
        abstract = True
