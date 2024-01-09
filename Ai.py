from utils.auth import OPENAI_API_KEY
from utils.utils import parse_str
import requests


def extract_ads_features(base64_encoded_image: str) -> str:
    explain_image_prompt = """You are provided with a screenshot of a website. The screenshot may contain a main content part and ads. Detect and explain the ads as follows: 
        [{
            height: the height of the ad in pixels,
            width: the width of the ad in pixels,
            image_ratio: the approximate height/width ratio (e.g. for a banner of 300/200px the ratio is 1.5),
            text: the text of the ad,
            target: either the domain, brand, website, etc...,
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
                        "text": explain_image_prompt
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
    ads_features = parse_str(ret)

    return ads_features


def create_list_new_ads(ads_features: list[dict[str, str]], full_article_text: str) -> list[str]:
    create_list_new_ads = f"""
    You are provided with a full article text and a list of ads. The ads contain a text field and a target field. 
    Rewrite the ad copy, so that it's contextualized and related to the article context. 
    For example: If the article is funny and has jokes, make the ad copy a joke - write an actual joke! 
    Or if it's hacker content, make the ad talk to hackers. 
    Keep the new ad copy concise, of about 10-12 words, but most importantly amaze people by smartly relating the ad to the article. 
    Include a couple of emoticons to make it look even cooler. 
    Output as a JSON list ['ad copy 1', 'ad copy 2', ...]
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
                        "text": create_list_new_ads
                    }
                ] 
            }
        ],
        "max_tokens": 2056
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    print(response)
    ret = response.json().get('choices')[0].get('message').get('content')

    new_ads_list = parse_str(ret)
    return new_ads_list


def hack_add(ad_subject: str = 'alternative recyclable energy source', ad_goal: str = 'use the force as in Star Wars',
             ad_style:str = 'Funny standup punches, mention Vader', full_article_text: str = '') -> list[str]:
    ad_prompt = f"""
    You are provided with several ad properties and a full article text.  
    Write an ad copy, so that it's contextualized and related to the article context.
    Keep the new ad copy concise, of about 10-12 words, but most importantly amaze people by smartly relating the ad to the article. 
    Include a couple of emoticons to make it look even cooler. 
    Output just the plain ad copy without any explanatory text whatsoever!
    
    ad_subject: {ad_subject}
    ad_goal: {ad_goal}
    ad_style: {ad_style}
    full_article_text: {full_article_text}
"""

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    payload = {
        "model": "gpt-4-1106-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": ad_prompt
                    }
                ]
            }
        ],
        "max_tokens": 2056
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    # print(response)
    ret = response.json().get('choices')[0].get('message').get('content')

    return ret
