from dotenv import load_dotenv
from moralis import evm_api
from . import db_operations,serializers
import requests
import os
load_dotenv()

'''
utils.py
This module contains utility related or helper functions that perform some common or specific tasks
that can be reused. Also to keep the code more organized.
'''

# API keys from .env file
coingecko_key = os.getenv("coingecko_key")
api_key = os.getenv("api_key")

# API endpoints
onchain_data_endpoint = "https://api.geckoterminal.com/api/v2/networks/eth/pools/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640/ohlcv/day?limit=30&currency=usd"
offchain_data_endpoint = "https://api.coingecko.com/api/v3/coins/weth/market_chart?vs_currency=usd&days=30&interval=daily&precision=18"

def make_request(url,headers):
    '''
    Makes HTTP requests using the url & headers passed and returns the response in JSON
    Raises exception when error occurs
    '''
    try:
        response = requests.get(url=url,headers=headers)
        return response.json()
    except:
        raise "Failed"

def get_onchain_data():
    '''
    Makes a call to a geckoterminal API endpoint which responds with 30 days ETH/USD UniswapV3 pool historical data
    Then get the values of 'ohlcv_list' key, which is a list and reverse it so it will be in DESC order
    Loop and construct an object with only the values we need (timestamp, price) attached to related key names
    We pass timestamp we got to unixToBlock() function which returns the closest block possible
    Raises exception when error occurs
    '''
    try:
        response = make_request(url=onchain_data_endpoint,headers={})['data']['attributes']['ohlcv_list'][::-1]
        # Looping through list of lists and extracting the values we need and constructing a new list of dict and returning it
        onchain_data_list = [{"timestamp":item[0],"priceUniswapV3":item[1],"blockNo":unixToBlock(item[0])} for item in response]
        return onchain_data_list
    except:
        raise "Failed to get data from geckoterminal api"

def unixToBlock(unixTime):
    '''
    We use Moralis(node) Python SDK to query blockchain data
    We use .get_date_to_block function of moralis to get closest block, given the api key, date in unix & chain id as params
    Returns the block number
    Raises exception when error occurs
    '''
    try:
        params = {
        "date": str(unixTime),
        "chain": "eth"
        }
        # Calls the function .get_date_to_block() on moralis block module with necessary params and stores the data returned 
        response = evm_api.block.get_date_to_block(api_key=api_key,params=params)
        # Return only the block number
        return response["block"]
    except:
        raise "Failed"

def get_offchain_data():
    '''
    Makes a call to a coingecko API endpoint which responds with 30 days historical data
    Then get the values of 'prices' key, which is a list of lists that comes in DESC order by default
    We exclude the last item from list as it has data of time we called the API
    We do loop and destruct the data first and also convert unix timestamp to length 10 from 13 (just removing milliseconds)
    to match data coming from geckoterminal
    Loop and construct an object with only the values we need (timestamp, price) attached to related key names
    and return that list
    Raises exception when error occurs
    '''
    try:
        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": coingecko_key}
        response = make_request(url=offchain_data_endpoint,headers=headers)['prices']
        # Excluding the last item from list of lists in response variable because the data it has is not useful for us
        preprocess_data = response[:len(response)-1]
        # Looping and converting unix timestamp by removing milliseconds from each timestamp using divmod
        processed_data = [[divmod(x[0],1000)[0],x[1]] for x in preprocess_data]
        # Looping through list of lists and extracting the values we need and constructing a new list of dict and returning it
        offchain_data_list = [{"timestamp":x[0],"priceCoingecko":x[1]} for x in processed_data]
        return offchain_data_list
    except Exception as e:
        raise "Failed to get data from coingecko api"
    
def prepare_and_respond():
    '''
    This function will fetch data from database, prepare the data structure required as final output to respond
    Raises exception if any error occurs
    '''
    try:
        # Gets the latest updated data from db and stores it in variable
        filtered_onchain_data = db_operations.get_onchain_data_filtered_current()
        # Used serializers to convert complex django datatype QuerySet to JSON format
        serialized_data = serializers.OnChainDataSerializer(filtered_onchain_data,many=True).data
        # Utilizing serialized data to construct a new structure that resembles the expected output of this assignment
        structured_data = [
            {"priceUniswapV3" : item["priceUniswapV3"],
             "priceCoingecko" : item["timestamp"]["priceCoingecko"],
             "timestamp": item['timestamp']['timestamp'],
             "blockNo" : item['blockNo']
              } for item in serialized_data]
        return structured_data
    except:
        raise "Failed to structure the data"