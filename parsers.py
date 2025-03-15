import re

def parser(original_text: str) -> dict:
    """
    Convert an original text containing numbered sections into a dictionary with keys:
    'user_query', 'complete_user_query', and 'thoughts'.
    Raises a ValueError if any required section is missing.
    
    Parameters:
        original_text (str): The input string containing the sections.
        
    Returns:
        dict: A dictionary with the extracted sections.
    """
    # Regular expression pattern to capture the section header and its content.
    pattern = r'\d+\.\s*([^:]+):\s*(.*?)(?=\n\d+\.|$)'
    matches = re.findall(pattern, original_text, re.DOTALL)
    
    # Create a dictionary to map expected keys based on section titles.
    key_map = {
        "user query": "user_query",
        "complete user query": "complete_user_query",
        "thoughts": "thought"
    }
    
    result = {}
    for title, content in matches:
        key = key_map.get(title.strip().lower())
        if key:
            result[key] = content.strip()
    
    # Check if all required sections are present
    missing_keys = [key for key in key_map.values() if key not in result]
    if missing_keys:
        raise ValueError(f"Missing required section(s): {', '.join(missing_keys)}")
    
    return result
