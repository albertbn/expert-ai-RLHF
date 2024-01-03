from utils.auth import OPENAI_API_KEY
import requests


def explain_image(base64_encoded_image: str) -> str:
    EXPLAIN_IMAGE_PROMPT = """
        You are provided with a screenshot of a website. The screenshot may contain a main content part and ads. Detect and explain the ads as follows:
        ```javascript
        [{
            height: the height of the ad in pixels,
            width: the width of the ad in pixels,
            text: the text of the ad,
            text_color: the color of the text,
            background_color: the background color of the ad,
            emotions: [a list of emotions the ad conveys] (TODO specify),
            target: the target of the ad (TODO specify that),
            close_content_text: if there is close text from the main content to any of the ads - write it here
            ...      
        }, {...}]
        ```
    """

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": EXPLAIN_IMAGE_PROMPT
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_encoded_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 2056
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    ret = response.json().get('choices')[0].get('message').get('content')
    return ret

def create_list_new_ads(ads_features: str) -> str:
    CREATE_LIST_NEW_ADS = """
        Given the full article text and the list of ad features, create a list of new ads, combining the article text and subject and the target idea of each ad. 
        If the ad has `close_content_text`, prefer it, to enhance the effect of an even stronger contextual ad. Relate the new ad copy text as much as possible to the page content. 
        If it's funny - make a joke, if it's for hackers - come up with a hacky copy, etc... Last but not least, you are provided with a list of markup elements recorded at the time 
        the screenshot was taken. Use the width and height of the detected images to build a relation of which ad is related to which detected markup."""
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": CREATE_LIST_NEW_ADS
                    }
                ] 
            }
        ],
        "max_tokens": 2056
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    ret = response.json().get('choices')[0].get('message').get('content')
    return ret
