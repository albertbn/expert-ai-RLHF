from utils.auth import OPENAI_API_KEY
from utils.utils import parse_to_dict, parse_to_list
import requests


def extract_ads_features(base64_encoded_image: str) -> str:
    EXPLAIN_IMAGE_PROMPT = """You are provided with a screenshot of a website. The screenshot may contain a main content part and ads. Detect and explain the ads as follows: 
        [{
            height: the height of the ad in pixels,
            width: the width of the ad in pixels,
            text: the text of the ad,
            target: the target of the ad,
            ...
        }, {...}]
        Your answer should only contain the list of JSON objects, and nothing more. """

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
    ads_features = parse_to_dict(ret)

    return ads_features

def create_list_new_ads(ads_features: list[dict[str, str]], full_article_text: str) -> list[str]:
    CREATE_LIST_NEW_ADS = f"""
        Given the full article text, encapsulated in <full_article_text></full_article_text> tags below, and the list of ad features, enclosed in <ads_features></ads_features> tags below, 
        create a list of new ads, combining the article text and each of the ads features, in the provided list in <ads_features></ads_features>. You should use the 'text' field in each
        entry of the ads features. Relate the new ad copy text as much as possible to the page content. 
        If it's funny - make a joke, if it's for hackers - come up with a hacky copy, etc... Last but not least, you are provided with a list of markup elements recorded at the time 
        the screenshot was taken. Use the width and height of the detected images to build a relation of which ad is related to which detected markup.
        Your answer should be given in a list format, containing each new ad text for each ad feature, in order. \n\n
        <full_article_text>{full_article_text}</full_article_text>
        <ads_features>{ads_features}</ads_features>
        """
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    payload = {
        "model": "gpt-4",
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
    print(response)
    ret = response.json().get('choices')[0].get('message').get('content')

    new_ads_list = parse_to_list(ret)
    return new_ads_list
