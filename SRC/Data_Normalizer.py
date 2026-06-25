import re 
import unicodedata
def remove_accents(text):
    if not text:
        return ""
    text = unicodedata.normalize('NFKD', text)
    result=" "
    for char in text:
        if not unicodedata.combining(char):
            result+=char
    return result
def normalize_name(name):
    if not name:
        return " "
    name=remove_accents(name)
    name=name.lower()
    name=re.sub(r'[^a-z0-9\s]', " ", name)
    return name
def split_aliases(aliase_text):
    if not aliase_text:
        return []
    aliases=aliase_text.split("|")
    normalized_aliases=[]
    for alias in aliases:
        normalized_alias=normalize_name(alias)
        if normalized_alias:
            normalized_aliases.append(normalized_alias)
    return normalized_aliases