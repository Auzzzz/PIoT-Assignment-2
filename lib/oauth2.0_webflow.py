import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleads import adwords
from googleads import oauth2


# Initialize the flow using the client ID and secret downloaded earlier.
flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'client_secret.json',
    scopes=['https://www.googleapis.com/auth/calendar'])

# Indicate where the API server will redirect the user after the user completes
# the authorization flow. The redirect URI is required.

flow.redirect_uri = #WE NEED A PROPER URI TO REDIRECT TO

# Generate URL for request to Google's OAuth 2.0 server.
# Use kwargs to set optional request parameters.
# Enable offline access so that you can refresh an access token without re-prompting the user for permission. 
# Recommended for web server apps.
# Enable incremental authorization. Recommended as a best practice.
authorization_url, state = flow.authorization_url(access_type='offline',include_granted_scopes='true', prompt='consent')

print('Please go to this URL: {}'.format(authorization_url))
auth_code = input('\nEnter the authorization code: ')

flow.fetch_token(code=auth_code)
credentials = flow.credentials
print(str(credentials)) #for testing
#TODO: NEED TO STORE CREDENTIALS IN DATABASE

# Initialize the GoogleRefreshTokenClient using the credentials you received
# in the earlier steps.

#oauth2_client = oauth2.GoogleRefreshTokenClient(client_id, client_secret, refresh_token)

# Initialize the AdWords client.
# adwords_client = adwords.AdWordsClient(developer_token, oauth2_client, user_agent, client_customer_id=client_customer_id)

    