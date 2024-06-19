import requests
from django.conf import settings
from celery import shared_task
from coinmarketcap.models import CoinProfile, CoinPriceHistorical, Crypto

@shared_task
def updateCoinInfo():
    headers = {'x-access-token': settings.COINRANKING_API_KEY}
    cryptos = Crypto.objects.all()

    for crypto in cryptos:
        # Fetch existing profile for historical data update
        # try:
        #     profile = CoinProfile.objects.get(coin_id=crypto.coin_id)
        #     # Update CoinHistorical from existing CoinProfile
        #     CoinHistorical.objects.update_or_create(
        #         coin_id=profile.coin_id,
        #         defaults={
        #             'price': profile.price,
        #             'twitter_followers': profile.twitter_followers,
        #             'tg_subscribers': profile.tg_subscribers
        #         }
        #     )
        #     print(f"Historical data updated for {crypto.coin_id}")
        # except CoinProfile.DoesNotExist:
        #     print(f"No existing profile found for {crypto.coin_id}, skipping historical update")

        # Fetch new data from API and update CoinProfile
        url = f"https://api.coinranking.com/v2/coin/{crypto.coin_id}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json().get('data', {})
            coin_data = data.get('coin', {})

            # Extract fields from response
            price = coin_data.get('price', '0')
            try:
                webUrl = [l for l in coin_data.get('links', '') if l.get('type', '') == 'website'][0].get('url', '')
            except:
                webUrl = ''

            try:
                twitter = [l for l in coin_data.get('links', '') if l.get('type', '') == 'twitter'][0].get('url', '')
            except:
                twitter = ''

            try:
                telegram = [l for l in coin_data.get('links', '') if l.get('type', '') == 'telegram'][0].get('url', '')
            except:
                telegram = ''

            twitter_followers = 0 # coin_data.get('twitter_followers', 0)
            tg_subscribers = 1 # coin_data.get('tg_subscribers', 0)

            # Update or create CoinProfile
            CoinProfile.objects.update_or_create(
                coin_id=crypto.coin_id,
                defaults={
                    'price': price,
                    'telegram': telegram,
                    'twitter': twitter,
                    'weburl': webUrl
                }
            )
            print(f"CoinProfile updated for {crypto.coin_id}")
        else:
            print(f"Failed to fetch data for {crypto.coin_id}: {response.status_code}")
@shared_task
def updateCoinPriceHistorical():
    headers = {'x-access-token': settings.COINRANKING_API_KEY}
    cryptos = Crypto.objects.all()
    for crypto in cryptos:
        url = f"https://api.coinranking.com/v2/coin/{crypto.coin_id}/history?timePeriod=all"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json().get('data', {})
            price_data = data.get('history', {})
            # Update CoinPriceHistorical from existing coin_id & timestamp
            for coin_price in price_data:
                CoinPriceHistorical.objects.update_or_create(
                    coin_id=crypto.coin_id,
                    timestamp=coin_price.get('timestamp', ''),
                    defaults={
                        'price': coin_price.get('price', '')
                    }
                )
            print(f"Historical data updated for {crypto.coin_id}")
        else:
            print(f"Failed to fetch price historical data for {crypto.coin_id}: {response.status_code}")