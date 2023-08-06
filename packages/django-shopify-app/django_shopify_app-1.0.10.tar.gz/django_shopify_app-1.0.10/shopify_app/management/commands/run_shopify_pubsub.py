import json
import importlib

from google.auth import jwt
from google.cloud import pubsub_v1

from django.apps import AppConfig
from django.conf import settings
from django.core.management import BaseCommand, CommandError
from django.utils import autoreload


def pubsub_callback(message):
    callback_path = settings.SHOPIFY_WEBHOOK_CALLBACK
    func_name = callback_path.rsplit('.')[-1]
    location = callback_path.replace(f'.{func_name}', "")
    module = importlib.import_module(location)
    if hasattr(module, func_name):
        func = getattr(module, func_name)
        func(message)
    message.ack()


def subscribe_to_pubsub():
    subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
        project_id=settings.SHOPIFY_GOOGLE_PUBSUB_PROJECT_ID,
        sub=settings.SHOPIFY_GOOGLE_PUBSUB_SUB_NAME,
    )
    service_account_info = json.loads(
        settings.SHOPIFY_GOOGLE_PUBSUB_SERVICE_ACCOUNT_STRING,
    )

    audience = "https://pubsub.googleapis.com/google.pubsub.v1.Subscriber"

    credentials = jwt.Credentials.from_service_account_info(
        service_account_info, audience=audience
    )

    with pubsub_v1.SubscriberClient(credentials=credentials) as subscriber:
        future = subscriber.subscribe(subscription_name, pubsub_callback)
        try:
            print('pubsub running')
            future.result()
        except KeyboardInterrupt:
            future.cancel()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--autoreload', action='store_true',
            help='Auto reload after code update'
        )

    def execute(self, *args, **options):

        if options['autoreload']:
            autoreload.run_with_reloader(
                subscribe_to_pubsub
            )
        else:
            subscribe_to_pubsub()
