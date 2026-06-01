from urllib.parse import unquote_plus

def parse_query_string(query):
    params = {}
    for pair in query.split("&"):
        if not pair:
            continue
        if "=" in pair:
            key, value = pair.split("=", 1)
            params[key] = unquote_plus(value)
        else:
            params[pair] = ""
    return params
