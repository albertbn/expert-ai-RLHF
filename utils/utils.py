import ast
import re
from typing import Optional, Union


r_list = re.compile(r'\[[\s\S]+]')


def parse_str(input_string: str) -> Optional[Union[list[dict[str, str]], list[str]]]:
    print(f"input_string = {input_string}")
    cleaned_str = r_list.search(input_string).group(0)

    try:
        data = ast.literal_eval(cleaned_str)
        return data
    except (SyntaxError, ValueError) as e:
        print(f"Error parsing string: {e}")
        return None
