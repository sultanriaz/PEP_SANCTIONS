import re 
import unicodedata
def remove_accents(text):
    if not text:
        return ""
    text = unicodedata.normalize('NFKD', text)
    