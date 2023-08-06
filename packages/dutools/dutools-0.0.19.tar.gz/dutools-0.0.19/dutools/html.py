from lxml import html


def remove_span(data, span=None):
    """ 用于xpath 中删除某个标签 """
    if not data:
        return None
    doc = html.fromstring(data)
    if span:
        ele = doc.xpath(f'//{span}')
    else:
        ele = doc.xpath('//script | noscript')
    for e in ele:
        e.getparent().remove(e)
    new_html = html.tostring(doc).decode()
    return new_html
