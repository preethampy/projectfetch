from datetime import date
from django.db.models import Q
from . import models
from . import db_operations
from . import utils

'''
db_operations.py
This module contains all the necessary functions that handles database-related operations

'''

def get_offchain_data_filtered_past():
    '''
    Gets all the objects from OffChainData model where last_update key is less than todays date
    and returns it
    Raises exception if any error occurs
    '''
    try:
        # Using 'Q' Object to apply query for __lt lookup
        data = models.OffChainData.objects.filter(Q(last_updated__lt=date.today()))
        return data
    except:
        raise "Failed filtering offchain data"

def get_onchain_data_filtered_current():
    '''
    Gets all the objects from OnChainData model where last_update key is equal to todays date
    and returns that list
    Raises exception if any error occurs
    '''
    try:
        data = models.OnChainData.objects.filter(last_updated=date.today())
        return data
    except:
        raise "Failed filtering onchain data"

def create_offchain_bulk(data):
    '''
    This is an internal function which takes offchain api's data as parameter.
    Then it loops and creates a list of OffChainData model instances
    Then we pass that list to bulk_create() OffChainData model's function to create/insert 
    all the latest data in one go instead of looping db queries.
    last_updated field is automatically set to current date when data is inserted
    Returns True on success
    Raises exception on any errors
    '''
    try:
        # preparing list of OffChainData model instances for each item in list of data
        offchain_data_list = [models.OffChainData(timestamp = item["timestamp"], priceCoingecko = item["priceCoingecko"]) for item in data]
        # using the list prepared above, to create objects in bulk at once using .bulk_create()
        models.OffChainData.objects.bulk_create(offchain_data_list)
        return True
    except:
        raise "Failed creating bulk data"

def create_onchain_bulk(data):
    '''
    This is an internal function which takes onchain api's data as parameter.
    Then it loops and creates a list of OnChainData model instances
    Then we pass that list to bulk_create()  OnChainData model's function to create/insert 
    all the latest data in one go instead of looping db queries.
    last_updated field is automatically set to current date when data is inserted
    timestamp field of OnChainData model is a ForeignKey to OffChainData with on_delete=models.CASCADE,
    so onchain data will gets deleted if the related data in OffChainData model gets deleted
    Returns True on success
    Raises exception on any errors
    '''
    try:
        # preparing list of OnChainData model instances for each item in list of data
        onchain_data_list = [models.OnChainData(timestamp_id = item["timestamp"], priceUniswapV3 = item["priceUniswapV3"],blockNo=item["blockNo"]) for item in data]
        # using the list prepared above, to create objects in bulk at once using .bulk_create()
        models.OnChainData.objects.bulk_create(onchain_data_list)
        return True
    except:
        raise "Failed creating bulk data"

def get_and_create_latest():
    '''
    This function will fetch latest offchain and onchain historical data from get_offchain_data() & get_onchain_data() utility functions
    And pass that data to create_offchain_bulk() & create_onchain_bulk() functions
    which responds with a boolean on successfully inserting data into database
    Then we call prepare_and_respond() utility function which fetches data from database and structures it and we will return it as response
    Else we will respond will Boolean false
    Raises exception on any errors
    '''
    try:
        # stores the coingecko data returned from get_offchain_data() in offchain_data
        offchain_data = utils.get_offchain_data()
        # stores the geckoterminal data returned from get_onchain_data() in onchain_data
        onchain_data = utils.get_onchain_data()
        # stores the boolean value returned from create_offchain_bulk() which insert data into database
        bulkdata_offchain_inserted = db_operations.create_offchain_bulk(offchain_data)
        # stores the boolean value returned from create_onchain_bulk() which insert data into database
        bulkdata_onchain_inserted = db_operations.create_onchain_bulk(onchain_data)
        if bulkdata_offchain_inserted == True and bulkdata_onchain_inserted == True:
            # responds with properly structured data / expected structure of data returned from prepare_and_respond()
            return utils.prepare_and_respond()
        else:
            return False
    except:
        raise "Failed to fetch and create in bulk"