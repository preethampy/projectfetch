from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from . import utils
from . import db_operations

@api_view(['GET'])
def fetch_past_data(request):
    '''
    This function will run on a get call to /fetch API and
    Responds with available data in database based on some conditions mentioned below
    Returns exception raised if any
    '''
    try:
        # filtered_offchain_data - It has result of filtered data from database where last_updated key is less than today's date, it is a list
        filtered_offchain_data = db_operations.get_offchain_data_filtered_past()

        # filtered_onchain_data - It has result of filtered data from database where last_updated key is today's date, it is a list
        filtered_onchain_data = db_operations.get_onchain_data_filtered_current()

        # If length of filtered_offchain_data is greater than 0, it means we have old data but not latest
        # So we delete them and use get_and_create_latest() function to fetch latest data, insert into database and return the latest added data from database
        if(len(filtered_offchain_data) > 0):
            filtered_offchain_data.delete()
            return Response(db_operations.get_and_create_latest())
        
        # If length of filtered_offchain_data is 0, length of filtered_onchain_data is > 0 it means we have latest data
        # So we use prepare_and_respond() function to get the latest data from database and return it as response 
        elif (len(filtered_offchain_data) == 0 and len(filtered_onchain_data) > 0):
            return Response(utils.prepare_and_respond())
        
        # In any other cases like when the database is empty,
        # we use get_and_create_latest() function to function to fetch latest data and insert into database and return the latest added data from database
        else:
            return Response(db_operations.get_and_create_latest())
        
    except Exception as e:
        return HttpResponse(e)
