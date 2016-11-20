def youtube_video_whitelist(iframe_tag):
    """
    Given an HTML iframe element, pass it through the filters we impose on
    embedded YouTube video.

    Returns the HTML iframe element as a string, which can be reinserted
    at the position of the element that was passed.
    """
    from bs4 import BeautifulSoup
    import re

    # Replace YouTube embed links with privacy-friendly alternative
    src = iframe_tag.get("src", "")
    iframe_tag['src'] = re.sub(r"(https?:)?//www\.youtube\.com/", "https://www.youtube-nocookie.com/", src)

    return iframe_tag

def umap_osm_whitelist(iframe_tag):
    """
    Given an HTML iframe element, pass it through the filters we impose on
    embedded OpenStreetMaps (umap.openstreetmap.fr).

    Returns the HTML iframe element as a string, which can be reinserted
    at the position of the element that was passed.
    """
    return iframe_tag

def filter_iframes(html, testing=False):
    """
    Given an HTML string, strips iframe tags that do not
    (just) contain an embedded video, OpenStreetMap or any
    other content we deem acceptable.

    In order to extend this list:
    1. Write a processing function that acceptably processes an iframe
       element of a given form.
    2. Add a matcher below that contains this function, as well as a
       regex that matches the desired src attribute as narrowly as
       possible.

    Returns the remaining HTML string.
    """
    from bs4 import BeautifulSoup
    import re
 
    # Tuple of tuples (regex, function) that define allowed URL patterns and their handling
    # functions. If an src tag of an iframe matches the regex, the iframe will be passed
    # to the function for further processing. Functions should allow one argument, the
    # iframe element to process.
    matchers = (("^(https?:)?//www\.youtube\.com/embed/[a-zA-Z0-9-_]{8,15}$", youtube_video_whitelist),
                ("^(https?:)?//umap\.openstreetmap\.fr/en/map/[a-zA-Z0-9-_]*\?", umap_osm_whitelist))
    # Tuple of allowed attributes in an iframe
    allowed_attributes = ('height', 'src', 'width', 'frameBorder')

    # Parse the input HTML into a DOM
    dom = BeautifulSoup(html, "html.parser")

    for iframe in dom.findAll("iframe"):
        src = iframe.get("src", "")
        matched = False
        # Check whether any one matcher matches
        for (expression, whitelist_function) in matchers:
            exp = re.compile(expression)
            if exp.match(src):
                iframe = whitelist_function(iframe)
                matched = True
                break
        # If no matcher matched, remove the iframe
        if not matched:
            iframe.extract()
            continue
        # If iframe tag contains something, remove the iframe
        if len(iframe.contents) > 0:
            iframe.extract()
            continue
        # Check for illegal iframe attributes
        for attr in iframe.attrs:
            # If iframe contains illegal attribute, remove the iframe
            if attr not in allowed_attributes:
                iframe.extract()
                break

    return str(dom)

def strip_scripts_not_in_whitelist(html):
    """
    Given an HTML string, will strip all script tags that do not conform to
    one of the whitelist patterns as defined in settings.py.
    """
    from bs4 import BeautifulSoup
    from mezzanine.conf import settings
    import logging
    logger = logging.getLogger(__name__)

    # Parse the whitelist into a list of tags (to make sure format matches exactly)
    allowed_tags = []
    for allowed_tag_str in settings.RICHTEXT_SCRIPT_TAG_WHITELIST:
        allowed_tags.append(str(BeautifulSoup(allowed_tag_str, "html.parser").find("script")))

    # Parse the input HTML into a DOM
    dom = BeautifulSoup(html, "html.parser")

    # Look for all script tags and match them to the whitelist
    for script_tag in dom.findAll("script"):
        if str(script_tag) not in allowed_tags:
            script_tag.extract()
            logger.debug("Found non-whitelisted script tag. Stripped.")
            logger.debug("CONF: stripped tag is "+str(script_tag))
        else:
            logger.debug("Found whitelisted script tag. Did not strip.")

    return str(dom)


def strip_illegal_objects(html):
    """
    Given an HTML string, will strip all object tags that do not embed
    a PDF that is locally stored on this server.
    
    Returns the remaining HTML string.
    """
    from bs4 import BeautifulSoup
    import re
    from mezzanine.conf import settings
    import logging
    logger = logging.getLogger(__name__)
 
    # Tuple of regexes that define allowed URL patterns
    matchers = ("^{0}".format(settings.MEDIA_URL),)
    # Tuple of allowed attributes in an object
    allowed_attributes = ('data', 'type', 'width', 'height')

    # Parse the input HTML into a DOM
    dom = BeautifulSoup(html, "html.parser")

    for object_tag in dom.findAll("object"):
        data = object_tag.get("data", "")
        filetype = object_tag.get("type", "")
        matched = False
        illegal_tag = False
        # Check whether any one matcher matches
        for matcher in matchers:
            exp = re.compile(matcher)
            if exp.match(data):
                matched = True
                break
        # If no matcher matched, remove the object
        if not matched:
            object_tag.extract()
            logger.debug("Stripped object - Could not match URL pattern.")
            continue
        # Check for illegal object attributes
        for attr in object_tag.attrs:
            # If object contains illegal attribute, remove the object
            if attr not in allowed_attributes:
                illegal_tag = True
                break
        if illegal_tag:
            object_tag.extract()
            logger.debug("Stripped object - Found illegal attribute.")
            continue
        # The value of the type attribute should be 'application/pdf'
        if filetype != "application/pdf":
            object_tag.extract()
            logger.debug("Stripped object - Found illegal filetype.")
            continue
    
    return str(dom)
