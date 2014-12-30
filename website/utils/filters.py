def filter_non_video_iframes(html, testing = False):
    """
    Given an HTML string, strips iframe tags that do not
    (just) contain an embedded video. 

    Returns the remaining HTML string.
    """
    from bs4 import BeautifulSoup
    import re   
 
    # Tuple of regexes that define allowed URL patterns
    matchers = ("^(https?:)?//www\.youtube\.com/embed/[a-zA-Z0-9-_]{8,15}$",)
    # Tuple of allowed attributes in an iframe
    allowed_attributes = ('height', 'src', 'width')

    # Parse the input HTML into a DOM
    dom = BeautifulSoup(html, "html.parser")

    for iframe in dom.findAll("iframe"):
        src = iframe.get("src", "")
        matched = False
        # Check whether any one matcher matches
        for matcher in matchers:
            exp = re.compile(matcher)
            if exp.match(src):
                matched = True
                break
        # If no matcher matched, remove the iframe
        if not matched:
            iframe.extract()
            break
        # If iframe tag contains something, remove the iframe
        if len(iframe.contents) > 0:
            iframe.extract()
            break
        # Check for illegal iframe attributes
        for attr in iframe.attrs:
            # If iframe contains illegal attribute, remove the iframe
            if attr not in allowed_attributes:
                iframe.extract()
                break
    
    return str(dom)
