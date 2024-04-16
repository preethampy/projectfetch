from rest_framework import serializers
from . import models

'''
We will use Serializers for converting complex data types such as querysets that django models usually returns 
and their instances to native Python datatypes that can then be rendered into JSON.
We have OffChainDataSerializer and OnChainDataSerializer with several fields defined,
These fields will be used to convert their instances into JSON data which makes it
very convenient for us to process or destruct or create new structured data
'''

class OffChainDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OffChainData
        fields = ['timestamp','priceCoingecko']

class OnChainDataSerializer(serializers.ModelSerializer):

    # We have timestamp field in OnChainData as ForeignKey to OffChainData
    # Including OffChainDataSerializer instance to the fields will populate
    # the values based on the ForeignKey when we try to get the data using serializers
    timestamp = OffChainDataSerializer()
    class Meta:
        model = models.OnChainData
        fields = ['timestamp','priceUniswapV3','blockNo']
