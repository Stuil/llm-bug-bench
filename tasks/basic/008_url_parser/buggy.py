def parse_query_string(query):
    params = {}
    for pair in query.split("&"):
        if not pair:
            continue
        key, value = pair.split("=")
        params[key] = value
    return params
