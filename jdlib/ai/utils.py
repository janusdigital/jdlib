import json
import re


def parse_json_response(response):
    """Parse a JSON response, handling markdown code blocks."""
    text = response.strip()
    match = re.search(r'```(?:json)?\s*(.*?)\s*```', text, re.DOTALL)
    if match:
        text = match.group(1)
    return json.loads(text)
