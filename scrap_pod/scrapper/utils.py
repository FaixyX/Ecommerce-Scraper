
from re import search as rsearch, sub as rsub

def extract_price(s: str):
    f = rsearch(r'\d', s)
    l = rsearch(r'\d(?=[^\d]*$)', s)
    if not f or not l:
        return ""
    parts = s[f.start():l.end()].split('.', 1)  # Split at the first dot
    return rsub(r'[^\d.]', '', '.'.join([parts[0], parts[1].replace('.', '') if len(parts)>1 else '00']))
