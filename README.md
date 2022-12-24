# Phoebe

An implementation of OAuth 2.0 Authorization in the context of a Fitbit Application.  Following the OAuth 2.0 authorization code flow, this app serves as a client to access a user's Fitbit data. This is both a practical use project as well as a study guide.

## Preparation

Create an .env file at the root of the repository and create values for
CLIENT_ID and CLIENT_SECRET.

## Workflow

There are currently two endpoints — **/auth_url** and **/callback**

The **/auth_url** endpoint generates an authorization URL to be used by a user to grant this app access to their Fitbit data. The authorization URL includes several parameters to specify the details of the authorization request such as:

- client ID
- response_type
- scope
- code_challenge
- code_challenge_method
- state

The **/callback** endpoint ( also known as the redirect URI ) receives the authorization code once the user has authenticated with Fitbit's authentication server. This app will then use the authentication code to receive both an access token and a refresh token. Finally, the access token is forwarded to the user, which is needed to query [Fitbit's web API](https://dev.fitbit.com/build/reference/web-api/).



## Live Use

Phoebe is being actively used for a React app to update a webpage element with my sleep score. You may see it [here](https://johanns.xyz).
