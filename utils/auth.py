from os import getenv

# the caller should provide credentials in a .env file


def load_env_var(var_key: str) -> str:
    if not (value := getenv(var_key)):
        from dotenv import load_dotenv
        load_dotenv()
        value = getenv(var_key)
    return value


GPT_VERSION = 'gpt-4'
OPENAI_API_KEY = load_env_var('OPENAI_API_KEY')
