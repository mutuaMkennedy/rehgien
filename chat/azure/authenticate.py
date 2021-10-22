from django.contrib.auth import get_user_model
from django.conf import settings
# Azure Communication Services import stuff for building chat service
from azure.identity import DefaultAzureCredential
from azure.communication.identity import CommunicationIdentityClient, CommunicationUserIdentifier
from azure.communication.chat import ChatClient, CommunicationTokenCredential

User = get_user_model()
credential = DefaultAzureCredential()
azure_connection_string = settings.COMMUNICATION_SERVICES_CONNECTION_STRING
resource_endpoint = settings.COMMUNICATION_SERVICES_ENDPOINT


# def create_identity_and_get_token():
#      client = CommunicationIdentityClient(resource_endpoint, credential)
#      user = client.create_user()
#      token_response = client.get_token(user, scopes=["voip"])
#
#      return token_response

def get_azure_token(user_id):
    user = User.objects.filter(pk=user_id)

    # Instantiate the identity client
    client = CommunicationIdentityClient.from_connection_string(azure_connection_string)

    if user.exists():
        if user.first().azure_identity:
            # Get user on azure
            identity = CommunicationUserIdentifier(user.first().azure_identity)
            # Refresh the access token
            token_result = client.get_token(identity, ["chat"])

            # Save the users azure identity and access tokens
            a = user.first()
            a.azure_identity = identity.properties['id']
            a.azure_access_token = token_result.token

            a.save()

            return token_result
        else:
            # Create user on azure
            identity = client.create_user()
            # Generate a acess token
            token_result = client.get_token(identity, ["chat"])

            # Save the users azure identity and access tokens
            a = user.first()
            a.azure_identity = identity.properties['id']
            a.azure_access_token = token_result.token

            a.save()

            return token_result
    else:
        return False
