from utils.auth import OPENAI_API_KEY
import requests


def explain_image(base64_encoded_image: str) -> str:

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
                        "text": "What’s in this image?"
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
