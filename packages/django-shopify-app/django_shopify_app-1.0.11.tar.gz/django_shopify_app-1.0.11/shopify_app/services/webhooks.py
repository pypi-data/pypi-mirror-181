from django.conf import settings


def update_shop_webhooks(shop):
    with shop.shopify_session:

        pubsub_address = "pubsub://{}:{}".format(
            settings.SHOPIFY_GOOGLE_PUBSUB_PROJECT_ID,
            settings.SHOPIFY_GOOGLE_PUBSUB_TOPIC_ID,
        )

        for topic in settings.SHOPIFY_WEBHOOK_TOPICS:
            webhooks = shop.shopify.Webhook.find(topic=topic)
            if len(webhooks):
                webhook = webhooks[0]
                webhook.address = pubsub_address
                webhook.save()

            else:
                webhook = shop.shopify.Webhook.create({
                    "topic": topic,
                    "address": pubsub_address,
                    "format": "json"
                })
                print(webhook)

        print(shop.shopify.Webhook.find())
        for created_webhook in shop.shopify.Webhook.find():
            if created_webhook.topic not in settings.SHOPIFY_WEBHOOK_TOPICS:
                created_webhook.destroy()
