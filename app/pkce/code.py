"""
The application needs to generate two values to keep 
the Oauth 2 protocol and the Fitbit user data secure:

- A cryptographically random value between 43-128 characters long 
    called a code verifier.

- A SHA-256 hash of the code verifier, base64url encoded with 
    padding omitted, called the code challenge.

For more information, refer to Step 1 of:
https://dev.fitbit.com/build/reference/web-api/developer-guide/authorization/
"""

import base64
import hashlib
import os

def generate_code_verifier() -> str:
    """
    Generate a 32-byte random string
    The optional Base64Url padding characters (=) is omitted.
    """

    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8')

    # Trim the padding '=' characters
    code_verifier = code_verifier.rstrip('=')

    return code_verifier

def generate_code_challenge(code_verifier: str) -> str:
    """
    Transforming the code verifier into the code challenge
    requires the use of libraries that implement the SHA-256 
    hash and Base64Url encoding specifications.
    """
    # Calculate the SHA-256 hash of the code verifier
    hash = hashlib.sha256(code_verifier.encode("utf-8")).digest()

    # Encode the hash in base64
    encoded_hash = base64.urlsafe_b64encode(hash).decode("utf-8")

    # Print the result
    return encoded_hash[:-1]
