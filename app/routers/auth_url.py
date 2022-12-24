from fastapi import APIRouter
from ..pkce import code, auth_url_builder


router = APIRouter()


@router.get("/auth_url", status_code=200)
async def authorization_url():
    """
    Generate the authorization URL.
    This method needs the following data:
        - The Client ID as "client_id" ( available as an environment variable )
        - The response type as "response_type" ( it will be "code" )
        - The Authorization scope as "scope"
        - The PKCE code challenge from generate_code_verifier() as "code_challenge"
        - The code challenge method ( which is a constant "S256" ) as "code_challenge_method"
        - The PKCE state as "state"
    """

    # The code verifier must be stored along with the state.
    code_verifier: str = code.generate_code_verifier()
    
    param_dict: dict = {
        'client_id': '238N67',   # Needs to be sourced as an env var.
        'response_type': 'code', # A constant
        'scope': 'activity+cardio_fitness+electrocardiogram+heartrate+location+nutrition+oxygen_saturation+profile+respiratory_rate+settings+sleep+social+temperature+weight',
        'code_challenge': code.generate_code_challenge(code_verifier),
        'code_challenge_method': 'S256', # A constant
        'state': code.generate_code_verifier(), # The state and code_verifier can use the same method.
    }

    # Building the Authorization URL
    url_builder = auth_url_builder.URLBuilder('https://www.fitbit.com/oauth2/authorize')

    # Iterate through the dict and then load all the params.
    for param in param_dict:
        url_builder.add_query_param(param, param_dict[param])

    return { "URL": url_builder.create().strip() }
