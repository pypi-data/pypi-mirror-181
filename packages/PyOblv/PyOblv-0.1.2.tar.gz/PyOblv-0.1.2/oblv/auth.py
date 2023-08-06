from oblv.exceptions import BadRequestError
from .oblv_client import OblvClient
from .api.auth import authenticate_key_authenticate_apikey_post
from .api.auth import logout_session_logout_delete
from .models import APIKey
from .client import Client,AuthenticatedClient

def authenticate(apikey: str):
    client = Client()
    input = APIKey(apikey)
    response = authenticate_key_authenticate_apikey_post.sync(client=client, json_body=input)
    return OblvClient(response.token,response.user_id)
