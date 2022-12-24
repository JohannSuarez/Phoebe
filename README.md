An implementation of OAuth 2.0 Authorization in the context of a Fitbit Application. This is both a practical use project as well as a study guide.

Following the OAuth 2.0 authorization code flow, this app serves as a client to access a user's Fitbit data.

# Workflow

There are currently two endpoints — /auth_url and /callback

The /auth_url endpoint generates an authorization URL to be used
by a user to grant this app access to their Fitbit data.
The authorization URL includes several parameters to specify the details
of the authorization request such as:

- client ID
- response_type
- scope
- code_challenge
- code_challenge_method
- state

