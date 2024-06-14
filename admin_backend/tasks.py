import requests
from django.conf import settings
from celery import shared_task
from coinmarketcap.models import CoinProfile, CoinHistorical, Crypto

@shared_task
def updateCoinInfo():
    headers = {'x-access-token': settings.COINRANKING_API_KEY}
    cryptos = Crypto.objects.all()

    for crypto in cryptos:
        # Fetch existing profile for historical data update
        try:
            profile = CoinProfile.objects.get(coin_id=crypto.coin_id)
            # Update CoinHistorical from existing CoinProfile
            CoinHistorical.objects.update_or_create(
                coin_id=profile.coin_id,
                defaults={
                    'balance': profile.balance,
                    'twitter_followers': profile.twitter_followers,
                    'tg_subscribers': profile.tg_subscribers
                }
            )
            print(f"Historical data updated for {crypto.coin_id}")
        except CoinProfile.DoesNotExist:
            print(f"No existing profile found for {crypto.coin_id}, skipping historical update")

        # Fetch new data from API and update CoinProfile
        url = f"https://api.coinranking.com/v2/coin/{crypto.coin_id}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json().get('data', {})
            coin_data = data.get('coin', {})

            # Extract fields from response
            balance = coin_data.get('marketCap', '0')

            twitter_followers = 0 # coin_data.get('twitter_followers', 0)
            tg_subscribers = 1 # coin_data.get('tg_subscribers', 0)

            # Update or create CoinProfile
            CoinProfile.objects.update_or_create(
                coin_id=crypto.coin_id,
                defaults={
                    'balance': balance,
                    'twitter_followers': twitter_followers,
                    'tg_subscribers': tg_subscribers
                }
            )
            print(f"CoinProfile updated for {crypto.coin_id}")
        else:
            print(f"Failed to fetch data for {crypto.coin_id}: {response.status_code}")