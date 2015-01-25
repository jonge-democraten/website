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

def obfuscate_email_addresses(html):
    """
    Given an HTML string, will obfuscate e-mail addresses using HTML entities.
    Works on mailto links and plain e-mail addresses.

    Returns the HTML string with obfuscated e-mail addresses.
    """
    from bs4 import BeautifulSoup
    import re

    # Parse the input HTML into a DOM
    dom = BeautifulSoup(html, "html.parser")

    # First, look for mailto: links and obfuscate them
    for link in dom.findAll("a"):
        href = link.get("href", "")
        if href.startswith("mailto:"):
            link['href'] = "".join(['&#%i;' % ord(char) for char in href])

    # The intermediate HTML has all mailto: links obfuscated. Plaintext
    # e-mail addresses are next.
    intermediate_html = str(dom)

    email_seeker = re.compile("([\w._%+-]+@[\w.-]+\.[A-Za-z]{2,4})")

    resulting_html = ""
    for index, fragment in enumerate(email_seeker.split(intermediate_html)):
        if index % 2 != 0:
            resulting_html += "".join(['&#%i;' % ord(char) for char in fragment])
        else:
            resulting_html += fragment

    return resulting_html

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
