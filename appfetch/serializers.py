from rest_framework import serializers
from . import models

class OffChainDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OffChainData
        fields = ['timestamp','priceCoingecko']

class OnChainDataSerializer(serializers.ModelSerializer):
    timestamp = OffChainDataSerializer()
    class Meta:
        model = models.OnChainData
        fields = ['timestamp','priceUniswapV3','blockNo']
