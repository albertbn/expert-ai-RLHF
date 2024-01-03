import ast
import re
from typing import Optional


def parse_to_dict(input_string: str) -> Optional[list[dict[str, str]]]:
    cleaned_str = input_string.strip('()[]"')
    cleaned_str = cleaned_str.replace(':', '=').replace(',', '')
    cleaned_str = '\n'.join(line for line in cleaned_str.split('\n') if not line.strip().startswith('#'))

    cleaned_str = re.sub(r'(\b\w+)\s*=', r"'\1':", cleaned_str)

    try:
        data = ast.literal_eval(f'[{cleaned_str}]')
        return data
    except (SyntaxError, ValueError) as e:
        print(f"Error parsing string: {e}")
        return None

def parse_to_list(input_string: str) -> Optional[list[str]]:
    cleaned_str = input_string.strip('()[]"')
    cleaned_str = cleaned_str.replace(':', '=').replace(',', '')
    cleaned_str = '\n'.join(line for line in cleaned_str.split('\n') if not line.strip().startswith('#'))

    cleaned_str = re.sub(r'(\b\w+)\s*=', r"'\1':", cleaned_str)

    try:
        data = ast.literal_eval(f'[{cleaned_str}]')
        return data
    except (SyntaxError, ValueError) as e:
        print(f"Error parsing string: {e}")
        return None
