import base64
import hashlib
import hmac
from django.views import View
from django.urls import reverse
from django.conf import settings
from django.shortcuts import redirect, render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException

import shopify

from shopify_app.utils import get_function_from_string, get_shop_model
from shopify_app.decorators import shopify_embed


class ShopAPIView(APIView):
    pass


class InitTokenRequestView(View):

    redirect_path_name = ''

    @method_decorator(xframe_options_exempt)
    @method_decorator(shopify_embed)
    def get(self, request, *args, **kwargs):

        shopify.Session.setup(
            api_key=settings.SHOPIFY_API_KEY,
            secret=settings.SHOPIFY_API_SECRET
        )

        shop_url = request.GET.get('shop')
        api_version = '2022-07'
        state = ''
        path = reverse(self.redirect_path_name)
        redirect_uri = f"{settings.SHOPIFY_APP_HOST}{path}"
        scopes = settings.SHOPIFY_APP_SCOPES

        newSession = shopify.Session(shop_url, api_version)
        auth_url = newSession.create_permission_url(
            scopes, redirect_uri, state
        )

        if request.GET.get('embedded'):
            context = {
                'api_key': settings.SHOPIFY_API_KEY,
                'host': request.GET.get('host'),
                'redirect': auth_url
            }
            return render(request, 'shopify_app/index.html', context=context)
        else:
            return redirect(auth_url)


class EndTokenRequestView(View):
    redirect_path_name = ''

    def get(self, request, *args, **kwargs):

        shop_url = request.GET.get('shop')

        shopify.Session.setup(
            api_key=settings.SHOPIFY_API_KEY,
            secret=settings.SHOPIFY_API_SECRET
        )

        session = shopify.Session(shop_url, '2022-07')

        access_token = session.request_token(request.GET.dict())

        Shop = get_shop_model()
        shop_record = Shop.objects.get_or_create(shopify_domain=session.url)[0]

        installed = bool(not shop_record.shopify_token and access_token)

        shop_record.shopify_token = access_token
        shop_record.access_scopes = session.access_scopes

        shop_record.save()

        if installed:
            shop_record.installed()

        host = settings.SHOPIFY_APP_HOST
        path = reverse(self.redirect_path_name)
        query = request.META['QUERY_STRING']

        return redirect(f"{host}{path}?{query}")


class WebhookAuthenticationFailed(APIException):
    status_code = 401
    default_detail = 'authentication failed'


class WebhookMixin:

    def webhook_request_is_valid(self, secret):
        hmac_header = self.request.META.get('HTTP_X_SHOPIFY_HMAC_SHA256')
        if not hmac_header:
            raise WebhookAuthenticationFailed()

        secret = secret.encode('utf-8')
        digest = hmac.new(secret, self.request.body, hashlib.sha256).digest()
        computed_hmac = base64.b64encode(digest)
        received_hmac = hmac_header.encode('utf-8')
        is_valid = hmac.compare_digest(computed_hmac, received_hmac)
        return is_valid


class MandatoryWebhooksView(WebhookMixin, APIView):

    topic = None

    def post(self, request, *args, **kwargs):

        try:
            domain = request.META['HTTP_X_SHOPIFY_SHOP_DOMAIN']
            Shop = get_shop_model()
            shop = Shop.objects.get(shopify_domain=domain)
        except (KeyError, Shop.DoesNotExist):
            return Response(status=404)

        if not self.webhook_request_is_valid(shop.shopify_app_api_secret):
            raise WebhookAuthenticationFailed()

        func = get_function_from_string(
            settings.SHOPIFY_GDPR_WEBHOOK_CALLBACK
        )
        func(self.topic, request.data)

        return Response(status=200)
