import requests
from dotenv import load_dotenv
import os
import time

load_dotenv()

def get_person_urn(auth_token):
    """
    Retrieves the unique identifier (URN) of a person from LinkedIn using the provided authentication token.

    Parameters:
        auth_token (str): The authentication token required to access the LinkedIn API.

    Returns:
        str or None: The unique identifier (URN) of the person if found, None otherwise.
    """
    userinfo_url = "https://api.linkedin.com/v2/userinfo"
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    
    response = requests.get(userinfo_url, headers=headers)
    response_data = response.json()
    
    if "sub" in response_data:
        return response_data["sub"]
    else:
        return None

def create_linkedin_image_share(image_path, text_to_post):
    """
    Creates a LinkedIn image share using the provided image path and text to post.
    
    Args:
        image_path (str): The path to the image file to be shared.
        text_to_post (str): The text to include in the share commentary.
    
    Returns:
        bool: True if the image share was successfully created, False otherwise.
    """
    auth_token = os.getenv("LINKEDIN_API_KEY")
    # Step 0: Get the Person URN
    person_urn = get_person_urn(auth_token)
    if person_urn is None:
        raise Exception("Failed to retrieve person URN")
    
    print('Registering image...')
    # Step 1: Register the Image
    register_upload_url = "https://api.linkedin.com/v2/assets?action=registerUpload"
    
    register_upload_payload = {
        "registerUploadRequest": {
            "recipes": [
                "urn:li:digitalmediaRecipe:feedshare-image"
            ],
            "owner": "urn:li:person:{}".format(person_urn),
            "serviceRelationships": [
                {
                    "relationshipType": "OWNER",
                    "identifier": "urn:li:userGeneratedContent"
                }
            ]
        }
    }
    
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    headers_for_upload = {
        "Authorization": f"Bearer {auth_token}"
    }
    
    try:
        response = requests.post(register_upload_url, json=register_upload_payload, headers=headers)
        response_data = response.json()
    except Exception as e:
        raise Exception("Error occurred while making api request to register upload: {}".format(e))

    if "value" in response_data and "uploadMechanism" in response_data["value"]:
        upload_url = response_data["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
        asset_id = response_data["value"]["asset"]
        
        # Step 2: Upload Image Binary File
        with open(image_path, "rb") as image_file:
            try:
                upload_response = requests.post(upload_url, data=image_file, headers=headers_for_upload)
            except Exception as e:
                raise Exception("Error occurred while making api request to upload image: {}".format(e))
        
        if upload_response.status_code != 201:
            return False
        
        # wait before continuing
        print('Uploading image...')
        time.sleep(7)

        # Step 3: Create the Image Share
        share_url = "https://api.linkedin.com/v2/ugcPosts"
        
        share_payload = {
            "author": "urn:li:person:{}".format(person_urn),
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text_to_post
                    },
                    "shareMediaCategory": "IMAGE",
                    "media": [
                        {
                            "status": "READY",
                            "media": asset_id,
                        }
                    ]
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        try:
            share_response = requests.post(share_url, json=share_payload, headers=headers)
        except Exception as e:
            raise Exception("Error occurred while making api request to share image: {}".format(e))

        if share_response.status_code == 201:
            return "https://www.linkedin.com/feed/update/{}".format(share_response.json()["id"])
        
    raise Exception("Registering upload did not contain valid keys.")

def create_text_share(text_to_post):
    """
    Creates a LinkedIn text share using the provided text to post.
    
    Args:
        text_to_post (str): The text to include in the share commentary.
    
    Returns:
        bool: True if the text share was successfully created, False otherwise.
    """
    auth_token = os.getenv("LINKEDIN_API_KEY")
    # Step 0: Get the Person URN
    person_urn = get_person_urn(auth_token)
    if person_urn is None:
        raise Exception("Failed to retrieve person URN")
    
    # Step 3: Create the Image Share
    share_url = "https://api.linkedin.com/v2/ugcPosts"
    
    share_payload = {
        "author": "urn:li:person:{}".format(person_urn),
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": text_to_post
                },
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }

    try:
        share_response = requests.post(share_url, json=share_payload, headers=headers)
    except Exception as e:
        raise Exception("Error occurred while making api request to share image: {}".format(e))

    if share_response.status_code == 201:
        return "https://www.linkedin.com/feed/update/{}".format(share_response.json()["id"])
    
import openai

def getAiRespose(context, mt=1000, t=1, f=0):
    """
    Generate a chat response using the OpenAI ChatCompletion API.

    Args:
        context (str): The conversation context to generate a response for.
        mt (int, optional): The maximum number of tokens allowed in the response. Defaults to 1000.
        t (float, optional): The temperature parameter for response generation. Defaults to 1.
        f (float, optional): The frequency penalty parameter for response generation. Defaults to 0.

    Returns:
        str: The generated chat response.
    """
    # create a chat completion using the OpenAI ChatCompletion API
    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[{"role": "user", "content": context}],
        max_tokens=mt,
        temperature=t,
        frequency_penalty=f
    )

    # return the content of the first choice in the chat completion response
    return chat_completion.choices[0].message.content
    
    