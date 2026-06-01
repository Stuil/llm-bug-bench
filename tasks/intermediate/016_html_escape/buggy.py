def escape_html(text):
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace("&", "&amp;")
    text = text.replace('"', "&quot;")
    return text
