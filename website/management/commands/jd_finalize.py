import os
import pymysql
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from mezzanine.conf.models import Setting
from mezzanine.blog.models import BlogCategory
from mezzanine.forms.models import Form, Field
from mezzanine.forms import fields
from mezzanine.pages.models import Page, Link, RichTextPage
from mezzanine.utils.sites import current_site_id
from mezzanine.conf import settings
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import Site
from django.utils.text import slugify
from janeus import Janeus
from janeus.models import JaneusRole
from optparse import make_option
from website.jdpages.models import * 
from hemres.models import NewsletterTemplate, MailingList, NewsletterToList, Newsletter, EmailSubscriber, JaneusSubscriber
from filebrowser_safe import settings as fb_settings
from shutil import copy

def save_setting(name, value, domain):
    s = Setting()
    site = Site.objects.get(domain = domain)
    s.name = name
    s.value = value
    s.site = site
    s.save()

def save_group(name):
    g = Group()
    g.name = name
    g.save()

def save_group_permissions(groupname, permissionCodenames):
    g = Group.objects.get(name = groupname)
    for permCodename in permissionCodenames:
        p = Permission.objects.get(codename = permCodename)
        g.permissions.add(p)
    g.save()

def save_janeus_role(role, groupnames, sites):
    j = JaneusRole()
    j.role = role
    j.save()
    for groupname in groupnames:
        g = Group.objects.get(name = groupname)
        j.groups.add(g)
    for site in sites:
        s = Site.objects.get(domain = site)
        j.sites.add(s)
    j.save()

def activate_twitter_widget():
    s = Sidebar.objects.all()[0]
    widget, created = SidebarTwitterWidget.objects.get_or_create(sidebar = s)
    widget.active = True
    widget.save()

def force_create_uploads_directory():
    uploadDir = os.path.join(settings.MEDIA_ROOT,
                             fb_settings.DIRECTORY,
                             'site-{0}'.format(current_site_id()))
    os.makedirs(uploadDir, exist_ok = True)
    os.chmod(uploadDir, 0o755)
    os.makedirs(os.path.join(uploadDir, 'headers'), exist_ok = True)
    os.chmod(os.path.join(uploadDir, 'headers'), 0o755)
    os.makedirs(os.path.join(uploadDir, 'blogs-pages'), exist_ok = True)
    os.chmod(os.path.join(uploadDir, 'blogs-pages'), 0o755)
    os.makedirs(os.path.join(uploadDir, 'documents'), exist_ok = True)
    os.chmod(os.path.join(uploadDir, 'documents'), 0o755)

def set_header_image(slug, image_url):
    pages = Page.objects.filter(slug = slug)
    if len(pages) == 0:
        print ("Page not found with slug {0}".format(slug))
    elif len(pages) > 1:
        print ("Several pages found with slug {0}".format(slug))
    else:
        p = pages[0]
        w = PageHeaderImageWidget(name = p.site.name+"-"+slug, page = p, image = image_url)
        w.save()

def set_headers():
    prefix = Site.objects.get(id = current_site_id()).domain.split('.')[0]
    headerDir = os.path.join(settings.PROJECT_ROOT, '..', '..', 'new-headers')
    dirList = os.listdir(headerDir)
    uploadDirRel = os.path.join(settings.MEDIA_URL,
                             fb_settings.DIRECTORY,
                             'site-{0}'.format(current_site_id()))
    uploadDirAbs = os.path.join(settings.PROJECT_ROOT, uploadDirRel.lstrip('/'))
    for headerSubDir in dirList:
        if headerSubDir.startswith(prefix + '-'):
            slug = headerSubDir.split('-', 1)[1]
            if slug == '*':
                slug = '/'
            for image in os.listdir(os.path.join(headerDir, headerSubDir)):
                copy(os.path.join(headerDir, headerSubDir, image),
                     os.path.join(uploadDirAbs, 'headers'))
                os.chmod(os.path.join(uploadDirAbs, 'headers', image), 0o644)
                print("Setting header {0} for {1} - {2}".format(image, prefix, slug))
                set_header_image(slug, os.path.join(uploadDirRel, 'headers', image))

def create_column_element_widget(slug, hp, title, columnElement, numItems):
    """
    Function to create column elements. Should only be called through create_*_column_element_widget functions.
    """
    if hp == 'l':
        hp = HorizontalPosition.LEFT
    else:
        hp = HorizontalPosition.RIGHT
    p = Page.objects.get(slug = slug)
    cew = ColumnElementWidget(column_element = columnElement, page = p)
    cew.title = title
    cew.horizontal_position = hp
    cew.max_items = numItems
    cew.save()
    print("Imported column element {0} on {1} ({2}).".format(title, slug, current_site_id()))

def create_events_column_element_widget(slug, calendars, hp, title, numItems = 5):
    """
    Add a ColumnElementWidget to a Page with slug 'slug' for Events calendar calendars (one of
    EventColumnElement.EVENT_CHOICES), horizontal position hp (one of 'l' or 'r') with title 'title'
    and number of items numItems (default 5).

    (str, str, str, str, str, int) -> None
    """
    ece = EventColumnElement.objects.get(type = calendars)
    ce = ColumnElement.objects.get(object_id = ece.id, content_type = ContentType.objects.get_for_model(ece))
    create_column_element_widget(slug, hp, title, ce, numItems)

def create_blog_category_column_element_widget(slug, category, hp, title = None, st = "", numItems = 3):
    """
    Add a ColumnElementWidget to a Page with slug 'slug' for BlogCategory with name category at
    horizontal position hp (one of 'l' or 'r') with title 'title', subtype st (default "")
    and number of items numItems (default 3).

    (str, str, HorizontalPosition, str, str, int) -> None
    """
    cat = BlogCategory.objects.get(title = category)
    if title is None:
        title = category
    ce = ColumnElement.objects.get(object_id = cat.id, content_type = ContentType.objects.get_for_model(cat), subtype = st)
    create_column_element_widget(slug, hp, title, ce, numItems)

def create_column_element_widgets(domain):
    if (domain == 'website.jongedemocraten.nl'):
        create_blog_category_column_element_widget('/', "Politieke opinie", 'l', "Politiek")
        create_blog_category_column_element_widget('/', "Mededelingen", 'r', 'Mededelingen')
        create_blog_category_column_element_widget('media', "Persberichten", 'l', numItems = 5)
        create_blog_category_column_element_widget('media', "JD in de Media", 'r', 'JD in de media', numItems = 5)
    if (domain == 'amsterdam.jongedemocraten.nl'):
        create_events_column_element_widget('/', 'SI', 'l', "Geplande activiteiten Amsterdam")
        create_events_column_element_widget('/', 'MA', 'l', "Geplande activiteiten landelijk")
        create_blog_category_column_element_widget('/', "Nieuws", 'r', "Laatste nieuws Amsterdam", st = 'CP', numItems = 5)
    if (domain == 'rotterdam.jongedemocraten.nl'):
        create_events_column_element_widget('/', 'SM', 'l', "Geplande activiteiten Rotterdam")
        create_blog_category_column_element_widget('/', "Nieuws", 'r', "Laatste nieuws Rotterdam", st = 'CP', numItems = 5)
        create_blog_category_column_element_widget('oh-ja-joh', "Oh ja joh?", 'l', "Meest recente artikelen", numItems = 5)
    if (domain == 'arnhemnijmegen.jongedemocraten.nl'):
        pass
    if (domain == 'brabant.jongedemocraten.nl'):
        create_events_column_element_widget('/', 'SI', 'l', "Geplande activiteiten Brabant")
        create_blog_category_column_element_widget('/', "Nieuws", 'r', "Laatste nieuws Brabant", st = 'CP', numItems = 5)
    if (domain == 'groningen.jongedemocraten.nl'):
        create_events_column_element_widget('/', 'SI', 'l', "Geplande activiteiten Groningen")
        create_events_column_element_widget('/', 'MA', 'l', "Geplande activiteiten landelijk")
        create_blog_category_column_element_widget('/', "Nieuws", 'r', "Laatste nieuws Groningen", st = 'CP', numItems = 5)
        create_blog_category_column_element_widget('/', "Weblog", 'r', "Weblogs", st = 'CP', numItems = 5)
    if (domain == 'leidenhaaglanden.jongedemocraten.nl'):
        create_events_column_element_widget('/', 'SI', 'l', "Activiteiten Leiden-Haaglanden")
        create_events_column_element_widget('/', 'MA', 'l', "Geplande activiteiten landelijk")
        create_blog_category_column_element_widget('/', "Nieuws", 'r', "Laatste nieuws", st = 'CP', numItems = 5)
        create_blog_category_column_element_widget('/', "Weblog", 'r', "Weblogs", st = 'CP', numItems = 5)
    if (domain == 'twente.jongedemocraten.nl'):
        create_events_column_element_widget('/', 'SI', 'l', "Geplande activiteiten Twente")
        create_blog_category_column_element_widget('/', "Nieuws", 'r', 'Laatste nieuws Twente', st = 'CP', numItems = 5)
    if (domain == 'friesland.jongedemocraten.nl'):
        pass
    if (domain == 'fryslan.jongedemocraten.nl'):
        pass
    if (domain == 'internationaal.jongedemocraten.nl'):
        pass
    if (domain == 'limburg.jongedemocraten.nl'):
        create_events_column_element_widget('/', 'SI', 'l', "Geplande activiteiten Limburg")
        create_events_column_element_widget('/', 'MA', 'l', "Geplande activiteiten landelijk")
        create_blog_category_column_element_widget('/', "Nieuws", 'r', "Laatste nieuws Limburg", st = 'CP', numItems = 5)
    if (domain == 'utrecht.jongedemocraten.nl'):
        create_events_column_element_widget('/', 'SI', 'l', "Geplande activiteiten Utrecht")
        create_events_column_element_widget('/', 'MA', 'l', "Geplande activiteiten landelijk")
        create_blog_category_column_element_widget('/', "Nieuws", 'r', "Laatste nieuws", st = 'CP', numItems = 5)
        create_blog_category_column_element_widget('/', "Weblog", 'r', "Weblogs", st = 'CP', numItems = 5)

def create_page_for_each_blog_category():
    categories = BlogCategory.objects.all()
    for c in categories:
        try:
            p = Page.objects.get(slug = c.slug)
            return
        except Page.DoesNotExist:
            pass
        b, created = BlogCategoryPage.objects.get_or_create(slug = c.slug, blog_category = c)
        if created:
            b.title = c.title
            b.save()

def set_sidebar_blog(category, title = None):
    if title is None:
        title = category
    sb = Sidebar.objects.get()
    cat = BlogCategory.objects.get(title = category)
    w = SidebarBlogCategoryWidget(title = title, sidebar = sb, blog_category = cat)
    w.save()

def set_sidebar_blogs_for_domain(domain):
    if (domain == 'website.jongedemocraten.nl'):
        set_sidebar_blog("Weblog", "JD Blog")
    if (domain == 'amsterdam.jongedemocraten.nl'):
        set_sidebar_blog("Nieuws")
    if (domain == 'arnhemnijmegen.jongedemocraten.nl'):
        set_sidebar_blog("Nieuws")
        set_sidebar_blog("Weblog")
    if (domain == 'brabant.jongedemocraten.nl'):
        set_sidebar_blog("Nieuws")
        set_sidebar_blog("Weblog")
    if (domain == 'groningen.jongedemocraten.nl'):
        set_sidebar_blog("Nieuws")
        set_sidebar_blog("Weblog")
    if (domain == 'leidenhaaglanden.jongedemocraten.nl'):
        set_sidebar_blog("Nieuws")
        set_sidebar_blog("Weblog")
    if (domain == 'rotterdam.jongedemocraten.nl'):
        set_sidebar_blog("Nieuws")
        set_sidebar_blog("Oh ja joh?")
    if (domain == 'twente.jongedemocraten.nl'):
        set_sidebar_blog("Nieuws")
    if (domain == 'friesland.jongedemocraten.nl'):
        set_sidebar_blog("Nieuws")
    if (domain == 'internationaal.jongedemocraten.nl'):
        set_sidebar_blog("Weblog", "Weblog Internationaal")
    if (domain == 'limburg.jongedemocraten.nl'):
        set_sidebar_blog("Nieuws")
    if (domain == 'utrecht.jongedemocraten.nl'):
        set_sidebar_blog("Nieuws")
        set_sidebar_blog("Weblog")

def create_mailinglist(label, name):
    m = MailingList()
    m.label = label
    m.name = name
    m.save()
    return m

def create_newsletter_template(title, template):
    n = NewsletterTemplate()
    n.title = title
    n.template = template
    n.save()
    return n

def create_mailinglists_and_templates(domain, host, user, password, database, prefix):
    try:
        db = pymysql.connect(host=host, user=user, password=password, database=database)
    except pymysql.err.OperationalError as e:
        raise CommandError(e)
    cur = db.cursor()
    lists = []
    if (domain == 'website.jongedemocraten.nl'):
        l = create_mailinglist(slugify('Digizine'), 'Digizine')
        lists.append((1, l, ['[JD Digizine]', '[JD Landelijk]']))
        l = create_mailinglist(slugify('Jonge Democraten Kadernieuwsbrief'), 'Jonge Democraten Kadernieuwsbrief')
        lists.append((14,l, ['[JD Kader]']))
        l = create_mailinglist(slugify('Digizine via Mailman'), 'Digizine via Mailman')
        lists.append((18,l, []))
        l = create_mailinglist(slugify('Nieuwsbrief INCO'), 'Nieuwsbrief INCO')
        lists.append((19,l, ['[JD Inco]', '[JD Internationaal]']))
        l = create_mailinglist(slugify('Digitale Demo'), 'Digitale Demo')
        lists.append((22,l, []))
        l = create_mailinglist(slugify('Nieuwsbrief Buitenland'), 'Nieuwsbrief Buitenland')
        lists.append((23,l, []))
    if (domain == 'amsterdam.jongedemocraten.nl'):
        l = create_mailinglist(slugify('Nieuwsbrief Amsterdam'), 'Nieuwsbrief Amsterdam')
        lists.append((3,l, ['[JD Amsterdam]']))
    if (domain == 'arnhemnijmegen.jongedemocraten.nl'):
        l = create_mailinglist(slugify('Nieuwsbrief Arnhem-Nijmegen'), 'Nieuwsbrief Arnhem-Nijmegen')
        lists.append((4,l, ['[JD Arnhem-Nijmegen]']))
    if (domain == 'brabant.jongedemocraten.nl'):
        l = create_mailinglist(slugify('Nieuwsbrief Brabant'), 'Nieuwsbrief Brabant')
        lists.append((5,l, ['[JD Brabant]']))
    if (domain == 'groningen.jongedemocraten.nl'):
        l = create_mailinglist(slugify('Nieuwsbrief Groningen'), 'Nieuwsbrief Groningen')
        lists.append((7,l, ['[JD Groningen]']))
    if (domain == 'leidenhaaglanden.jongedemocraten.nl'):
        l = create_mailinglist(slugify('Nieuwsbrief Leiden-Haaglanden'), 'Nieuwsbrief Leiden-Haaglanden')
        lists.append((8,l, ['[JD Leiden-Haaglanden]']))
    if (domain == 'rotterdam.jongedemocraten.nl'):
        l = create_mailinglist(slugify('Nieuwsbrief Rotterdam'), 'Nieuwsbrief Rotterdam')
        lists.append((10,l, ['[JD Rotterdam]']))
    if (domain == 'twente.jongedemocraten.nl'):
        l = create_mailinglist(slugify('Nieuwsbrief Twente'), 'Nieuwsbrief Twente')
        lists.append((11,l, ['[JD Twente]']))
    if (domain == 'friesland.jongedemocraten.nl'):
        l = create_mailinglist(slugify('Nieuwsbrief Friesland'), 'Nieuwsbrief Friesland')
        lists.append((6,l, ['[JD Friesland]']))
    if (domain == 'internationaal.jongedemocraten.nl'):
        pass
    if (domain == 'limburg.jongedemocraten.nl'):
        l = create_mailinglist(slugify('Nieuwsbrief Limburg'), 'Nieuwsbrief Limburg')
        lists.append((9,l, ['[JD Limburg]', '[JD Maastricht]']))
    if (domain == 'utrecht.jongedemocraten.nl'):
        l = create_mailinglist(slugify('Nieuwsbrief Utrecht'), 'Nieuwsbrief Utrecht')
        lists.append((2,l, ['[JD Utrecht]']))
    if (domain == 'zwolle.jongedemocraten.nl'):
        l = create_mailinglist(slugify('Nieuwsbrief Zwolle'), 'Nieuwsbrief Zwolle')
        lists.append((12,l, []))
    for l_id, l, l_search in lists:
        appendQuery = ""
        for extraQuery in l_search:
            appendQuery += " OR (list_id = 0 AND subject LIKE '{0}%')".format(extraQuery)
        query = "SELECT * FROM "+prefix+"_jnews_mailings WHERE list_id = {0}".format(l_id) + appendQuery + ";"
        cur.execute(query)
        for mailing in cur.fetchall():
            nl = Newsletter(
                subject = mailing[5],
                content = mailing[9],
                template = "{{ content }}",
                public = True if l_id != 14 else False, # Public, behalve bij kader
                date = datetime.fromtimestamp(max(int(mailing[18]),int(mailing[13])))
            )
            nl.save()
            nltl = NewsletterToList(
                newsletter = nl,
                target_list = l,
                subscriptions_url = '',
                sent = True,
                date = datetime.fromtimestamp(max(int(mailing[18]),int(mailing[13])))
            )
            nltl.save()
        # Migreer subscribers
        cur.execute('SELECT * FROM '+prefix+'_jnews_subscribers AS sub ' \
                    'LEFT JOIN '+prefix+'_jnews_listssubscribers AS lsub ' \
                    'ON sub.id = lsub.subscriber_id WHERE sub.confirmed=1 ' \
                    'AND lsub.unsubscribe=0 AND lsub.list_id=%s;', (l_id, ))
        for sub in cur.fetchall():
            in_ldap = False
            for lidnummer, naam in Janeus().lidnummers(sub[3]):
                in_ldap = True
                s, created = JaneusSubscriber.objects.get_or_create(member_id=lidnummer)
                if created:
                    s.name = naam
                s.subscriptions.add(l)
                s.save()
            if not in_ldap:
                s, created = EmailSubscriber.objects.get_or_create(name=sub[2], email=sub[3])
                s.subscriptions.add(l)
                s.save()


def create_newsletter_templates():
    templateDir = os.path.join(settings.PROJECT_ROOT, '..', '..', 'newsletter-templates')
    dirList = os.listdir(templateDir)
    for templateName in dirList:
        with open(os.path.join(templateDir, templateName), "r") as templateFile:
            create_newsletter_template(templateName, templateFile.read())

def create_link(title, link, parentSlug = ''):
    l = Link()
    l.title = title
    l.slug = link
    try:
        p = Page.objects.get(slug = parentSlug)
        l.parent = p
    except Page.DoesNotExist:
        pass
    l.save()

def create_extra_content(domain):
    if (domain == "website.jongedemocraten.nl"):
        create_link("Amsterdam", "//amsterdam.jongedemocraten.nl", "afdelingen")
        create_link("Arnhem-Nijmegen", "//arnhemnijmegen.jongedemocraten.nl", "afdelingen")
        create_link("Brabant", "//brabant.jongedemocraten.nl", "afdelingen")
        create_link("Friesland / Fryslân", "//friesland.jongedemocraten.nl", "afdelingen")
        create_link("Groningen", "//groningen.jongedemocraten.nl", "afdelingen")
        create_link("Leiden-Haaglanden", "//.jongedemocraten.nl", "afdelingen")
        create_link("Limburg", "//limburg.jongedemocraten.nl", "afdelingen")
        create_link("Rotterdam", "//Rotterdam.jongedemocraten.nl", "afdelingen")
        create_link("Twente", "//twente.jongedemocraten.nl", "afdelingen")
        create_link("Utrecht", "//utrecht.jongedemocraten.nl", "afdelingen")
        create_link("Internationaal", "//internationaal.jongedemocraten.nl")
        create_link("Nieuwsbrieven", "/nieuwsbrief/list", "media")
        ## Set afdelingen page
        p = RichTextPage.objects.get(slug = 'afdelingen')
        p.content = """
<p>Naast een landelijke organisatie heeft de Jonge Democraten ook lokale afdelingen. Deze afdelingen vormen in feite het hart van de vereniging en organiseren iedere maand talloze activiteiten in een stad of regio. De activiteiten vari&euml;ren van inhoudelijke avonden met sprekers, debatten en trainingen tot gezellige borrels. Op de websites van de afdelingen vind je meer informatie over activiteiten die de afdeling bij jou in de omgeving organiseert.</p>
<h2>Overzichtskaart afdelingsgrenzen 2014</h2>
<div id="afdelingskaart">
<div class="infobox">
<h2>Afdeling</h2>
<h3>Gemeente</h3>
</div>
</div>
<script src="/static/website/js/d3.v3.min.js" type="text/javascript"></script>
<script src="/static/website/js/queue.v1.min.js" type="text/javascript"></script>
<script src="/static/website/js/d3.geo.projection.v0.min.js" type="text/javascript"></script>
<script src="/static/website/js/topojson.v0.min.js" type="text/javascript"></script>
<script src="/static/website/js/render.js" type="text/javascript"></script>
<p><em>Op basis van de afdelingsgrenzen en gemeentelijke indeling van januari 2013.</em></p>
<h1>De JD in jouw regio</h1>
<p>Op dit moment zijn er tien afdelingen van de Jonge Democraten door het gehele land. Kijk hierboven bij het overzicht tot welke afdeling de regio behoort waar jij woont. Kijk vervolgens op de afdelingspaginas om te zien wat die afdeling in jouw regio doet, bijvoorbeeld onder het kopje activiteiten of commissies.</p>
<p>Doet de afdeling op dit moment nog niets met jouw regio? Dan kun jij daar verandering in brengen! De JD heeft namelijk verschillende regiocommissies die onder de afdelingen vallen. Wellicht kun jij een regiocommissie opstarten bij jou in de buurt! Neem contact op met de landelijk secretaris op <a href="mailto:info@jongedemocraten.nl">info@jongedemocraten.nl</a>. Hij zal je in contact brengen met de betreffende afdeling en de mogelijkheden tot het oprichten van een regiocommissie samen met je onderzoeken.</p>"""
        p.save()
        ## Set trainers page
        p = RichTextPage.objects.get(slug = 'trainers')
        p.content = """<p>
<script src="/static/website/js/jdshowhide.js" type="text/javascript"></script>
</p>
<p>De trainingen van de Jonge Democraten kunnen niet worden aangeboden zonder de trainers die hele hele land doorreizen om hun trainingen te geven. Op deze pagina stellen de trainers zich voor en vertellen ze wat hun specialiteiten zijn.</p>
<h3 style="background-color: #578439; background-image: url('https://jongedemocraten.nl/templates/jd/images/TitleBackground.png'); background-repeat: repeat-x; color: white; font-size: 14px; line-height: 20px; font-weight: bold; padding: 2px 0px 2px 10px; margin: 0; vertical-align: middle;">Annelieke Bergink (Maastricht)</h3>
<p><img style="float: left;" src="https://jongedemocraten.nl/images/landelijk/Schermafbeelding%202014-09-29%20om%2023.50.12.png" alt="" width="80" height="108" border="0" />Ik ben sinds 2012 trainer bij de JD en heb daarnaast ervaring als trainer bij IFLRY, afdelingsbestuurder en congresvoorzitter. Ik geef graag bestuurstrainingen, waarbij ik het van belang vindt om de training in overleg met het bestuur vorm te geven. De training moet immers het bestuur in staat stellen het nog beter te doen! Hierbij kunnen onderdelen als vergadertraining, gedragsstijlen, communicatie en feedback, opstellen van een beleidsplan en teambuilding aan bod komen.</p>
<p><a id="jdtoggle-1" href="#"><strong>Leer meer/minder</strong></a></p>
<div id="A1" style="padding-left: 0px; display: none;"><br />Daarnaast vind ik het erg leuk om leden in staat te stellen nog beter mee te doen aan het politiek debat; dat kan via het formatiespel, een congressimulatie of debattrainingen. Ik ben flexibel in het opzetten van trainingen, dus neem vooral contact met me op zodat we samen kunnen kijken welke training het beste bij jouw ontwikkelbehoefte past. Ik werk fulltime in Maastricht, en op doordeweekse dagen reis ik max. 2 uur voor een training. In het weekend, indien tijdig aangegeven, kom ik overal!
<p><strong>Trainingen</strong></p>
<ul>
<li>Bestuurstraining</li>
<li>Organisatorische trainingen (congressimulatie, organiseren)</li>
<li>Politieke vaardigheden (presentatietraining, debattraining, formatiespel)</li>
</ul>
</div>
<h3 style="background-color: #578439; background-image: url('https://jongedemocraten.nl/templates/jd/images/TitleBackground.png'); background-repeat: repeat-x; color: white; font-size: 14px; line-height: 20px; font-weight: bold; padding: 2px 0px 2px 10px; margin: 0; vertical-align: middle;">Arend Meijer (Breda)</h3>
<p><img style="float: left;" src="https://jongedemocraten.nl/images/landelijk/Schermafbeelding%202014-09-29%20om%2023.58.09.png" alt="" width="82" height="93" border="0" /> Ik ben al een langere tijd binnen de vereniging actief, ben zowel lokaal bestuur, portefeuillehouder en Landelijk Bestuur geweest. Kortom, I know my way around de JD. Mijn kick is om met besturen aan de slag te gaan om een succes van hun periode te maken. Je steekt er veel tijd in, dus het moet ook iets opleveren. Zowel voor jezelf als voor de vereniging. Daarnaast vind ik het leuk om met de inhoudelijke vorming van leden aan de gang te zijn. Dus wil je de beginselen van de JD doorgronden, dan help ik je graag!</p>
<p><strong><a id="jdtoggle-2" href="#">Lees meer/minder</a></strong></p>
<div id="A2" style="padding-left: 0px; display: none;">
<p>Ik combineer trainingen met mijn fulltime baan, dus hoop dat jullie me tijdig een seintje geven als je een training van mij willen.</p>
<p><strong> Trainingen</strong></p>
<ul>
<li>Filosofie / Grondslagen</li>
<li>Bestuur</li>
</ul>
</div>
<h3 style="background-color: #578439; background-image: url('https://jongedemocraten.nl/templates/jd/images/TitleBackground.png'); background-repeat: repeat-x; color: white; font-size: 14px; line-height: 20px; font-weight: bold; padding: 2px 0px 2px 10px; margin: 0; vertical-align: middle;">Ayla Schneiders (Utrecht)</h3>
<p><img style="float: left;" src="https://jongedemocraten.nl/images/landelijk/Schermafbeelding%202014-09-29%20om%2023.57.43.png" alt="" width="80" height="122" border="0" />Mijn naam is Ayla Schneiders en tussen 2011 en 2014 ben ik actief geweest als bestuurslid bij de afdeling Utrecht. Als bestuurslid pers &amp; promotie en daarna als voorzitter van de afdeling heb ik vooral ervaring binnen de JD opgedaan in samenwerking, leiderschap en het stellen en behalen van doelen. Daarnaast zijn er een aantal thema's waar ik me in heb verdiept en waar ik graag met JD-ers de komende jaren ervaringen en kennis deel en zo eventueel discussies meer verdieping kan geven bijvoorbeeld over onderwijs, cultuur &amp; bestuur. Sinds maart 2015 ben ik Statenlid in de Provincie Utrecht.</p>
<p><strong><a id="jdtoggle-3" href="#">Lees meer/minder</a></strong></p>
<div id="A3" style="padding-left: 0px; display: none;">
<p>Als trainer bij de JD wil ik vooral ook gebruik maken van mijn trainingsvaardigheden buiten de JD en deze toepassen op de ervaring die ik heb binnen de JD. In 2011 ben ik afgestudeerd als toneelschrijver en voor en na die tijd heb ik veel workshops, trainingen en lessen gegeven die vooral te maken hebben met het juist vormgeven van een boodschap. Om me te ontwikkelen in talentontwikkeling en kennisoverdracht ben ik vorig jaar begonnen met de academische lerarenopleiding primair onderwijs.</p>
<p>Centraal bij de trainingen die ik geef, zal in eerste instantie het verzoek staan. Wat is de behoefte voor deze training en hoe kunnen we die het beste vormgeven? Met ook atypische werkvormen komen we uiteindelijk in overleg tot een mooie trainingsprogramma.</p>
<p>Ik verwacht van de deelnemers een actieve en open houding en in sommige gevallen voorbereiding. Wat je daarvoor terug krijgt is een trainingservaring, waar aandacht is voor jou als persoon binnen en buiten je functie bij de Jonge Democraten.</p>
<p>Het allerleukste is natuurlijk dat iedereen wat kan leren van zon training, ik misschien soms nog wel meer dan de deelnemers aan de training. Ik hoop dat ik velen van jullie kan voorzien van een leerzame en leuke trainingservaring!</p>
<p><strong>Trainingen</strong></p>
<ul>
<li>Bestuur &amp; Team</li>
<li>Promotie</li>
<li>Organisatie</li>
<li>Visie &amp; Doel</li>
<li>Project (organisatie &amp; ontwikkeling)</li>
<li>Leiderschap</li>
<li>Kennisthema's: o.a. Onderwijs, cultuur &amp; bestuur (Provinciale Staten)</li>
</ul>
</div>
<h3 style="background-color: #578439; background-image: url('https://jongedemocraten.nl/templates/jd/images/TitleBackground.png'); background-repeat: repeat-x; color: white; font-size: 14px; line-height: 20px; font-weight: bold; padding: 2px 0px 2px 10px; margin: 0; vertical-align: middle;">David Gitard (Antwerpen)</h3>
<p><img style="float: left;" src="https://jongedemocraten.nl/images/10481879_1511370872448842_2457126653942474303_n.jpg" alt="" width="118" height="92" border="0" />Eerst maar een korte introductie. Ik ben David, ik kom uit Arnhem en heb in Nijmegen de lerarenopleiding Frans gevolgd. Daar heb ik al enige ervaring met het geven van lessen opgedaan. Tevens geef ik al enkele jaren priv&eacute;lessen, Nederlands en Frans. Dat heb ik altijd met veel plezier gedaan, ik vind het heel leuk en waardevol om mensen dingen te leren en te zien hoe ze groeien. Bij de JD heb ik een paar keer geassisteerd met trainingen in Tunis, door die te tolken.</p>
<p><strong><a id="jdtoggle-4" href="#">Lees meer/minder</a></strong></p>
<div id="A4" style="padding-left: 0px; display: none;">Momenteel woon ik in Antwerpen, daar studeer ik Toegepaste Taalkunde. Ondanks de afstand wil ik graag actief blijven bij de JD. Dit door het geven van activerende, leuke trainingen waar mensen wat bij leren.&lt;/p&gt; &lt;p&gt;Ik hou ervan op een interactieve en actieve manier te werken, het liefst zo persoonlijk mogelijk. Ik maak graag gebruik van visueel materiaal en bouw het liefst voort op voorkennis die deelnemers al hebben.
<p><strong>Trainingen</strong></p>
<ul>
<ul>
<li>In overleg</li>
</ul>
</ul>
</div>
<h3 style="background-color: #578439; background-image: url('https://jongedemocraten.nl/templates/jd/images/TitleBackground.png'); background-repeat: repeat-x; color: white; font-size: 14px; line-height: 20px; font-weight: bold; padding: 2px 0px 2px 10px; margin: 0; vertical-align: middle;">Eva van Sloten (Amsterdam en Utrecht)</h3>
<p><img style="float: left;" src="https://jongedemocraten.nl/images/landelijk/Schermafbeelding%202014-09-29%20om%2023.57.20.png" alt="" width="90" height="91" border="0" />Samenwerken gaat niet vanzelf, dat leer ik bij mijn studie politicologie (richting organisatiewetenschappen), vrijwilligerswerk en natuurlijk ook bij de JD.&lt;/p&gt; &lt;p&gt;Het is erg handig om een training in samenwerking te krijgen omdat je zaken dan bespreekbaar maakt, en allemaal gaat werken vanuit hetzelfde kader. Daarbij zijn er gewoon een aantal handige tips en truuks die je gewoon een keer geleerd moet hebben. Ik vind het erg leuk om trainingen te geven dus bel of mail me gerust.</p>
<p><strong><a id="jdtoggle-5" href="#">Lees meer/minder</a></strong></p>
<div id="A5" style="padding-left: 0px; display: none;">Trainingen&lt;/p&gt; &lt;ul&gt; &lt;li&gt;Organisatorisch (time management, samenwerken, motivatie, bestuurstraining)
<p>&nbsp;</p>
</div>
<h3 style="background-color: #578439; background-image: url('https://jongedemocraten.nl/templates/jd/images/TitleBackground.png'); background-repeat: repeat-x; color: white; font-size: 14px; line-height: 20px; font-weight: bold; padding: 2px 0px 2px 10px; margin: 0; vertical-align: middle;">Erik Vandewall (Tilburg)</h3>
<p><img style="float: left;" src="https://jongedemocraten.nl/images/landelijk/Schermafbeelding%202014-09-29%20om%2023.46.30.png" alt="" width="127" height="90" border="0" />Ik ben Erik en ik kom graag een training geven. Binnen de vereniging heb ik nu redelijk wat functietjes bekleed en ik mag dan ook graag vanaf het pluche roepen wat er moet gebeuren, maar eigenlijk wil ik u leren om met uw eigen mening naar voren te komen.De scholingstak van de JD vind ik persoonlijk erg waardevol en ik heb dan ook veel geleerd van alle activiteiten die via dit kanaal worden aangeboden. Vandaar dat ik er best trots op ben om nu trainingen te geven aan u!</p>
<p><strong><a id="jdtoggle-6" href="#">Lees meer/minder</a></strong></p>
<div id="A6" style="padding-left: 0px; display: none;">Mijn sterkte ligt bij het trainen van uw overtuigingskracht en meningsvorming. Marketing en communicatie in een politiek jasje zeg maar.
<p><strong>Trainingen</strong></p>
<ul>
<li>Meningsvorming</li>
<li>Overtuigingstechnieken</li>
<li>Manipulatie / Framing</li>
</ul>
</div>
<h3 style="background-color: #578439; background-image: url('https://jongedemocraten.nl/templates/jd/images/TitleBackground.png'); background-repeat: repeat-x; color: white; font-size: 14px; line-height: 20px; font-weight: bold; padding: 2px 0px 2px 10px; margin: 0; vertical-align: middle;">Ivanka Bloom (Utrecht)</h3>
<p><img style="float: left;" src="https://jongedemocraten.nl/images/landelijk/Schermafbeelding%202014-09-29%20om%2023.57.02.png" alt="" width="85" height="81" border="0" />Als trainer bij de JD vind ik het mooi dat leden de kans krijgen om in een hele veilige omgeving kunnen experimenteren met het actief ontwikkelen van hun vaardigheden, en trainers een platform krijgen om vol creativiteit deze ontwikkeling te faciliteren.</p>
<p><strong><a id="jdtoggle-7" href="#">Lees meer/minder</a></strong></p>
<div id="A7" style="padding-left: 0px; display: none;">Zelf heb ik binnen en buiten de JD veel ervaring met het werken in teams en het organiseren van evenementen (JD afdelingsbestuur als secretaris scholing en internationaal, advieswerk in teams en nu werkzaam binnen HR). Ik specialiseer me daarom in bestuurstrainingen, organisatorische trainingen en trainingen over de JD Internationaal. Andere onderwerpen aanpakken met een andere ervaren trainer vind ik echter ook erg leuk!&lt;/p&gt; &lt;p&gt;Ik mik erop om mijn trainingen zo interactief mogelijk te laten zijn, zodat de deelnemers zelf kunnen oefenen met de theorie, actief kijken naar zichzelf en anderen en feedback op hun input krijgen. Soms mag daar ook zelfs een beetje huiswerk bij komen. Maar bovenal vind ik het belangrijk dat de training aansluit op de behoefte van de afdeling / het bestuur, dus daar zoek ik graag vooraf goed contact over!
<p><strong>Trainingen</strong></p>
<ul>
<li>Bestuurstraining (o.a. vergadering, beleidsplan, overdracht, feedback)</li>
<li>Organisatorische trainingen</li>
<li>Trainingen gericht op JD Internationaal</li>
</ul>
</div>
<h3 style="background-color: #578439; background-image: url('https://jongedemocraten.nl/templates/jd/images/TitleBackground.png'); background-repeat: repeat-x; color: white; font-size: 14px; line-height: 20px; font-weight: bold; padding: 2px 0px 2px 10px; margin: 0; vertical-align: middle;">Leon Ploegstra (Groningen)</h3>
<p><img style="float: left;" src="https://jongedemocraten.nl/images/landelijk/Schermafbeelding%202014-09-29%20om%2023.48.47.png" alt="" width="80" height="119" border="0" />Ik ben Leon Ploegstra en inmiddels al vier jaar actief lid bij de Jonge Democraten. Eerst heb ik twee jaar deel uitgemaakt van het afdelingsbestuur in Groningen, als Algemeen Secretaris en Voorzitter. Ook ben ik in die tijd naar een groot aantal IFLRY en LYMEC Congressen geweest en was ik voorzitter van het Team Straatsburgreis. Ten slotte ben ik in 2013-2013 ben Internationaal Secretaris geweest in het Landelijk Bestuur.</p>
<p><strong><a id="jdtoggle-8" href="#">Lees meer/minder</a></strong></p>
<div id="A8" style="padding-left: 0px; display: none;">Op dit moment zet ik me nog steeds in voor de JD, onder meer als actief lid van de Werkgroep Buitenlandse Zaken en binnenkort ook als trainer. Ook bezoek ik nog steeds geregeld de congressen van IFLRY en LYMEC. Trainingen: Nader in te vullen
<p>&nbsp;</p>
</div>
<h3 style="background-color: #578439; background-image: url('https://jongedemocraten.nl/templates/jd/images/TitleBackground.png'); background-repeat: repeat-x; color: white; font-size: 14px; line-height: 20px; font-weight: bold; padding: 2px 0px 2px 10px; margin: 0; vertical-align: middle;">Malu Pasman (Amsterdam)</h3>
<p><img style="float: left;" src="https://jongedemocraten.nl/images/landelijk/_MG_4648.jpg" alt="" width="80" height="80" border="0" /> Topbestuurders, vlijmscherpe debaters, organisatorische talenten en echte campagnetijgers: je komt ze bij de JD allemaal tegen. En dit is niet voor niets, de JD is een omgeving waarbinnen leden alle ruimte krijgen om zich te ontwikkelen en om hun kennis te delen met andere leden.</p>
<p><strong><a id="jdtoggle-9" href="#">Lees meer/minder</a></strong></p>
<div id="A9" style="padding-left: 0px; display: none;">
<p>Ik ben het meest ge&iuml;nteresseerd in de 'randvoorwaarden' van politiek succes en mijn trainingen zijn dan ook vooral op organisatorisch vlak. Het volgen van een bestuurstraining, het leren hoe je teams aanstuurt of oefenen met het opzetten van een campagne zijn allemaal zaken die bij kunnen dragen aan het behalen van (politieke) resultaten. Dit probeer ik te bewerkstelligen in een interactieve, informele en open sfeer: trainingen moeten naast nuttig namelijk vooral leuk zijn!</p>
<p>Dan nog kort over mijzelf: ik ben 24 jaar en woonachtig in Amsterdam. Onlangs heb ik mijn Master Communication Science afgerond en inmiddels ben ik werkzaam als IT-Consultant. Binnen de JD ben ik in 2013-2014 Landelijk Algemeen Secretaris en Vicevoorzitter geweest en deze functie heb ik het jaar ervoor ook binnen de afdeling Amsterdam vervuld. Tegenwoordig ben ik vooral op de achtergrond actief binnen het ICT-Team en de DEMO-Redactie en vind je me nog vaak op activiteiten bij mijn 'thuisafdeling' Amsterdam.</p>
<p><strong>Trainingen</strong></p>
<ul>
<li>Bestuurstraining</li>
<li>Organisatorische trainingen (teams aansturen, ledenactivering, missie- en visieontwikkeling, etc.).</li>
<li>Presenteren</li>
<li>Campagne</li>
</ul>
</div>
<h3 style="background-color: #578439; background-image: url('https://jongedemocraten.nl/templates/jd/images/TitleBackground.png'); background-repeat: repeat-x; color: white; font-size: 14px; line-height: 20px; font-weight: bold; padding: 2px 0px 2px 10px; margin: 0; vertical-align: middle;">Melvin Adjiembaks (Den Haag)</h3>
<p><img style="float: left;" src="https://jongedemocraten.nl/images/landelijk/Schermafbeelding%202014-09-30%20om%2000.36.32.png" alt="" width="80" height="99" border="0" />Het aanschouwen van een fantastische toespraak krijgt mij op het puntje van mijn stoel. Mensen kunnen mij ongelooflijk inspireren, en ik ben dan ook gefascineerd door de vraag hoe dat kan. Maar wat motiveert jou? Welke uitdagingen zie jij voor jezelf en de maatschappij om je heen? Welke rol zou je willen hebben en waarom?</p>
<p><strong><a id="jdtoggle-10" href="#">Lees meer/minder</a></strong></p>
<div id="A10" style="padding-left: 0px; display: none;">
<p>In mijn trainingen sta jij altijd centraal. Het ontwikkelen van vaardigheden en het opdoen van nieuwe kennis is namelijk het leukst als jij zelf de richting kan bepalen. Vind je dat nog even lastig, dan zal ik natuurlijk wat meer iniatief nemen. In een bestuurstraining gaan we samen op zoek naar de dynamiek binnen jullie groep. Ik begeleid jullie in het optimaliseren van jullie ontwikkelingsproces om van je bestuursperiode een leuke en productieve tijd te maken.</p>
<p>Presenteren is een vak op zich. Het is iets wat je altijd kan blijven ontwikkelen, ongeacht het feit of je onervaren bent en zenuwen hebt of juist heel ervaren bent, maar iets nieuws wilt leren. In mijn presentatietraining reik ik enkele trucs aan die je zullen helpen in het verbeteren van je presentatie.</p>
<p><strong>Trainingen</strong></p>
<ul>
<li>Bestuurstraining</li>
<li>Presentatietraining</li>
</ul>
</div>
<h3 style="background-color: #578439; background-image: url('https://jongedemocraten.nl/templates/jd/images/TitleBackground.png'); background-repeat: repeat-x; color: white; font-size: 14px; line-height: 20px; font-weight: bold; padding: 2px 0px 2px 10px; margin: 0; vertical-align: middle;">Nikolai Jacobs (Amsterdam)</h3>
<p><img style="float: left;" src="https://jongedemocraten.nl/images/landelijk/Schermafbeelding%202014-09-29%20om%2023.56.40.png" alt="" width="80" height="80" border="0" /> Ik ben Nikolai, 24 jaar. Sinds vorig jaar september werk ik voor het Rijk als trainee. Ik heb gestudeerd in Amsterdam (UvA, BSc planologie) en in Rotterdam (EUR, MSc bestuurskunde). Tijdens mijn studie ben ik actief geweest in medezeggenschap van de UvA en heb ik stage gelopen bij Berenschot. In de JD ben ik actief geweest in het afdelingsbestuur van Amsterdam, in het landelijk bestuur, als trainer en als congresvoorzitter. Verder schrijf ik zo nu en dan wat voor de DEMO.</p>
<p><strong><a id="jdtoggle-11" href="#">Lees meer/minder</a></strong></p>
<div id="A11" style="padding-left: 0px; display: none;">
<p><strong>Trainingen</strong></p>
<ul>
<li>Vergaderen.</li>
<li>Technisch voorzitten.</li>
<li>Teambuilding.</li>
<li>Beleidsontwikkeling- en evaluatie.</li>
<li>Feedback.</li>
</ul>
</div>
<h3 style="background-color: #578439; background-image: url('https://jongedemocraten.nl/templates/jd/images/TitleBackground.png'); background-repeat: repeat-x; color: white; font-size: 14px; line-height: 20px; font-weight: bold; padding: 2px 0px 2px 10px; margin: 0; vertical-align: middle;">Pauline Kastermans (Rotterdam)</h3>
<p><img style="float: left;" src="https://jongedemocraten.nl/images/landelijk/Schermafbeelding%202014-09-30%20om%2000.36.05.png" alt="" width="156" height="103" border="0" /> Het leukste vind ik het om als facilitator het leerproces van een enthousiaste groep te begeleiden. Dit kan op veel verschillende onderwerpen, maar mijn passie ligt bij het Europese en internationale door mijn ervaring binnen de JD Internationaal. Dit kan vari&euml;ren van een training Europese besluitvorming tot een onderhandelingssimulatie gebaseerd op de ontwikkelingen tijdens de Arabische lente. Ook internationale congressimulaties of het begeleiden van een twinning team binnen de afdeling behoren tot de mogelijkheden.</p>
<p><strong><a id="jdtoggle-12" href="#">Lees meer/minder</a></strong></p>
<div id="A12" style="padding-left: 0px; display: none;">
<p>Tijdens de Europese verkiezingen van 2014 was ik kandidaat voor D66, waardoor ik veel praktijkervaring heb opgedaan met campagne voeren, debatteren en media.</p>
<p>Naast ervaring bij de JD, heb ik veel internationale trainingen gegeven over het opzetten van jongerenorganisaties, campagne voeren en politieke filosofie. Ook heb ik in 2014 de Train-de-Trainer in Mensenrechteneducatie van de Raad van Europa gevolgd.</p>
<p><strong>Trainingen</strong></p>
<ul>
<li>Internationaal (simulatiespel onderhandelen in internationale situatie).</li>
<li>Europa (algemeen, Europese besluitvorming, LYMEC, Raad van Europa).</li>
<li>Bestuur.</li>
<li>Campagne.</li>
<li>Politieke filosofie  liberalisme in internationaal perspectief.</li>
<li>Ledenactivering.</li>
</ul>
</div>
<h3 style="background-color: #578439; background-image: url('https://jongedemocraten.nl/templates/jd/images/TitleBackground.png'); background-repeat: repeat-x; color: white; font-size: 14px; line-height: 20px; font-weight: bold; padding: 2px 0px 2px 10px; margin: 0; vertical-align: middle;">Puck Sanders (Nijmegen)</h3>
<p><img style="float: left;" src="http://jongedemocraten.nl/images/PS.jpg" alt="" width="80" border="0" /></p>
<p>Wat betekent kennis als je het niet kunt delen met anderen? Niets! Ik krijg er energie van om samen met anderen kennis interactief naar een hoger niveau te brengen. Toepassing van kennis en kennis in de praktijk is daarbij net zo belangrijk. Daarom ben ik trainer geworden voor de JD.</p>
<p><span style="font-size: 12px;">Bij mijn trainingen, probeer ik jou op het puntje van je stoel te krijgen. Niet door te luisteren wat ik te vertellen heb, maar door te doen! Daarbij probeer ik jou dingen die we behandelen vanuit meerdere perspectieven te laten bekijken.</span></p>
<p><strong><a id="jdtoggle-13" href="#">Lees meer/minder</a></strong></p>
<div id="A13" style="padding-left: 0px; display: none;">
<p><span style="font-size: 12px;">Mijn achtergrond als verenigingsbestuurder, campaigner, kandidaat en assistent-raadslid in de lokale politiek zorgen ervoor dat ik oefeningen tijdens trainingen kan illustreren met voorbeelden uit de praktijk. Plezier is daarbij heel belangrijk vind ik, en dat is denk ik ook in de geest van de JD.</span></p>
<p>Kan ik jou komen trainen? Wil je nog iets meer weten over mij of mijn trainingen? Neem gerust contact met me op of bekijk alvast mijn Linkedin-profiel (zie hieronder).</p>
<p><strong>Trainingen</strong></p>
<ul>
<li>Politiek en Strategische Communicatie (Presentatietraining, debattraining, framing)</li>
<li>Teambuilding/groepsvorming</li>
<li>Bestuur en Beleid voor verenigingsbestuurders</li>
</ul>
</div>
<h3 style="background-color: #578439; background-image: url('https://jongedemocraten.nl/templates/jd/images/TitleBackground.png'); background-repeat: repeat-x; color: white; font-size: 14px; line-height: 20px; font-weight: bold; padding: 2px 0px 2px 10px; margin: 0; vertical-align: middle;">Samira Rafaela (Amsterdam)</h3>
<p><img style="float: left;" src="https://jongedemocraten.nl/images/landelijk/Schermafbeelding%202014-09-29%20om%2023.52.07.png" alt="" width="80" height="90" border="0" /> Ik ben Samira Rafaela en voor de Jonge Democraten actief als portefeuillehouder Diversiteit en Participatie en trainer. Naast de Jonge Democraten heb ik ervaring als trainer via onder andere de Nationale Jeugdraad en via mijn eigen onderneming. Mijn passie voor het trainen is ontstaan toen ik ervoer hoeveel profijt anderen kunnen hebben van je eigen ervaringen en kennis als trainer. Ik train op regelmatige basis jongeren en begeleid ze bij hun carri&egrave;re pad. Als overheidstrainee heb ik zelf veel trainingen gehad die gericht zijn op de persoonlijke ontwikkeling en individuele rol binnen groepsverband. Ik beschik over veel kennis en theorie om te delen en wil dat graag overbrengen aan mijn JD-collegas.</p>
<p><strong><a id="jdtoggle-14" href="#">Lees meer/minder</a></strong></p>
<div id="A14" style="padding-left: 0px; display: none;">
<p>Ik haal veel energie uit het trainersvak door te ervaren hoe bepaalde technieken anderen verder kunnen helpen. Ik vind het geweldig om te zien hoe deelnemers aan het einde van een training kunnen veranderen en met goede hoop de uitdaging aangaan door de training die ze hebben ontvangen!</p>
<p>Als trainer pas ik altijd verschillende niveaus toe bij het ontwerpen van de trainingen. Ik houd rekening met het kennisniveau van de doelgroep en ga daarin gericht te werk. Ik werk gericht toe naar het uiteindelijk kunnen toepassen van de methodieken. Op basis van de successpiraal, probeer ik de deelnemers enthousiast te houden, te motiveren om te blijven doorzetten en uiteindelijk het succes te ervaren. Belangrijk vind ik dat deelnemers zich veilig voelen om zich te uiten en dat er een goede sfeer/dynamiek wordt gecre&euml;erd om iedereen te laten floreren en dat er gelachen kan worden... Anticiperen en participeren staan centraal bij mijn trainingen.</p>
<p><strong>Trainingen</strong></p>
<ul>
<li>Bestuurstraining</li>
<li>Politieke inhoud en presenteren ( visieformulering, personal branding, presenteren, gespreksleider)</li>
<li>Samenwerken en onderhandelen</li>
</ul>
</div>
<h3 style="background-color: #578439; background-image: url('https://jongedemocraten.nl/templates/jd/images/TitleBackground.png'); background-repeat: repeat-x; color: white; font-size: 14px; line-height: 20px; font-weight: bold; padding: 2px 0px 2px 10px; margin: 0; vertical-align: middle;">Sjoerd Wannet (Arnhem-Nijmegen)</h3>
<p><img style="float: left;" src="https://jongedemocraten.nl/images/landelijk/Schermafbeelding%202014-09-30%20om%2000.35.43.png" alt="" width="80" height="120" border="0" /> Mijn naam is Sjoerd Wannet en in het dagelijks leven ben ik pre-master student bestuurskunde aan de Radboud universiteit en fractievoorzitter van D66 Lingewaard (gemeente tussen Arnhem en Nijmegen).</p>
<p><strong><a id="jdtoggle-15" href="#">Lees meer/minder</a></strong></p>
<div id="A15" style="padding-left: 0px; display: none;">
<p>Het geven van trainingen in groepen geeft mij veel energie. Het is mooi om als trainer een groep te stimuleren het beste uit zichzelf te halen. Bij bestuurstrainingen kun je als trainer het verschil maken. Zolang je maar de juiste energie in de groep weet los te maken. Mijn devies is dan ook altijd: de groep zoveel mogelijk zelf laten doen. Als trainer begeleid je het proces maar is het uiteindelijk het bestuur die de klus moet klaren. Vandaar dat mijn bestuurstrainingen heel interactief zijn met een grote inbreng vanuit de groep en nadruk op de groep.</p>
<p>Tevens ben ik afgestudeerd docent geschiedenis maar heb ik besloten niet te gaan werken in het voortgezet onderwijs. Toch kribbelt het docentschap nog hier en daar en dat vindt een mooie uitweg in het trainerschap, of het nu een inhoudelijke training/activiteit is over (parlementaire) geschiedenis of een bloemlezing van mijn ervaring uit de lokale politiek. Dat is vaak een mix van een college met een interactief gedeelte, zeer geschikt als afdelingsactiviteit.</p>
<p>In mijn trainingen neem ik de ervaring mee die ik in meerdere jaren rondlopen bij de Jonge Democraten heb opgedaan. Als secretaris promotie van JD ArnhemNijmegen tot secretaris scholing en vorming in het landelijk bestuur. Daarnaast ben ik sinds maart 2010 verkozen in de gemeenteraad van Lingewaard.</p>
<p><strong>Trainingen</strong></p>
<ul>
<li>Bestuurstrainingen <em>(Nadruk op verwachtingsmanagement, groepsprocessen en beleidsdoelen).</em></li>
<li>Politieke vaardigheden <em>(Debat, politiek onderhandelen, werking van de lokale democratie).</em></li>
<li>Inhoudelijke trainingen over democratie en (parlementaire) geschiedenis.</li>
</ul>
</div>
<p>&nbsp;</p>
<h3 style="background-color: #578439; background-image: url('https://jongedemocraten.nl/templates/jd/images/TitleBackground.png'); background-repeat: repeat-x; color: white; font-size: 14px; line-height: 20px; font-weight: bold; padding: 2px 0px 2px 10px; margin: 0; vertical-align: middle;">Susanne Schilderman (Utrecht)</h3>
<p><img style="float: left;" src="https://jongedemocraten.nl/images/landelijk/Schermafbeelding%202014-09-29%20om%2023.56.17.png" alt="" width="80" height="96" border="0" /> Om mee te beginnen ik vind het prachtig om training te geven omdat ik het mooi vind om mensen te helpen om bepaalde vaardigheden (verder) te ontwikkelen, te zien dat mensen dingen leren en ook om mezelf te ontwikkelen als trainer. Daarom geef ik ook heel veel verschillende trainingen zowel op het vlak van bestuur, als organisatie als politiek en presentatie.</p>
<p><strong><a id="jdtoggle-16" href="#">Lees meer/minder</a></strong></p>
<div id="A16" style="padding-left: 0px; display: none;">
<p>Mijn trainingen zijn altijd erg interactief. Ik probeer me zoveel mogelijk te richten op het trainen van vaardigheden en kennisoverdracht doe ik tussendoor. Ik wil mensen altijd zelf iets laten ervaren en ik moedig iedereen aan om zelf kritisch te kijken naar theorie, zichzelf en elkaar. Daarnaast vind ik dat er altijd gelachen moeten worden, ook tijdens een debattraining.</p>
<p>In mijn trainingen neem ik de ervaring mee die ik in meerdere jaren op gedaan het bij de Jonge Democraten zowel in het landelijk bestuur (organisatie), het afdelingsbestuur (promotie), en in werkgroepen en teams. Ook ben ik D66 Utrecht lokaal actief.</p>
<p><strong>Trainingen</strong></p>
<ul>
<li>Bestuurstraining</li>
<li>Organisatorische trainingen (Congressimulatie, campagne en organisatie)</li>
<li>Politiek en presentatie (Presentatietraining, debattraining, brainstorm en visietraining)</li>
</ul>
</div>
<h3 style="background-color: #578439; background-image: url('https://jongedemocraten.nl/templates/jd/images/TitleBackground.png'); background-repeat: repeat-x; color: white; font-size: 14px; line-height: 20px; font-weight: bold; padding: 2px 0px 2px 10px; margin: 0; vertical-align: middle;">Tom Kunzler (Utrecht)</h3>
<p><img style="float: left;" src="https://jongedemocraten.nl/images/landelijk/Schermafbeelding%202014-09-29%20om%2023.55.57.png" alt="" width="80" height="104" border="0" /> Allereerst vind ik het enorm leuk om voor een groep te staan en kennis te kunnen overbrengen. Naast een jong sociaal-liberaal geluid te laten horen in de Nederlandse politiek is de belangrijkste taak van de Jonge Democraten scholing en vorming van de eigen leden. Er is veel kennis aanwezig onder oud-kaderleden en het is jammer als het wiel opnieuw uitgevonden moet worden.</p>
<p><strong><a id="jdtoggle-17" href="#">Lees meer/minder</a></strong></p>
<div id="A17" style="padding-left: 0px; display: none;">
<p>Ik zet graag mijn ervaring in die ik opgedaan heb als oud-afdelingsvoorzitter van de Jonge Democraten Arnhem-Nijmegen, congresvoorzitter, stem en notulencommissielid, kasco-lid en ervaring met het organiseren van activiteiten en twinnings.</p>
<p>Verder heb ik 2,5 jaar lang bij ProDemos gewerkt waar ik educatieve programmas gaf aan jongeren die het Binennhof bezochten. En geef ik momenteel nog elk jaar een gastcollege aan de Universiteit Utrecht over de geschiedenis en werking van het Nederlandse politieke bestel.</p>
<p><strong>Trainingen</strong></p>
<ul>
<li>Training/masterclass Nederlandse politiek en Nederlandse politieke geschiedenis (1750 - nu).</li>
<li>Training over de Provinciale politiek.</li>
<li>Het geven van debattrainingen en het leiden van simulaties van Kamerdebatten (rollenspel)</li>
<li>Verder kan ik besturen trainingen geven over het organiseren en uitvoeren van PJO-scholenprojecten.</li>
<li>Bestuurstrainingen over het opstellen van een afdelingsreglement.</li>
<li>Perstraining, hoe schrijf ik een goed persbericht en hoe kom ik in de lokale pers.</li>
<li>Algemene bestuurstrainingen, opstellen van beleidsplan en effici&euml;nt samenwerken.</li>
</ul>
</div>
"""
        p.save()
        ## Set word lid form
        form = Form()
        oldForm = Page.objects.get(slug = 'word-lid')
        form.parent = oldForm.parent
        oldForm.delete()
        form.title = "Word lid!"
        form.slug = 'word-lid'
        form.content = """
<p>Voor meer informatie over het aamelden en opzeggen van het lidmaatchap van de Jonge Democraten klik <a href="/lidmaatschap/">hier.</a> </p>
<p>Van een Nederlands rekeningnummer vindt u <a href="https://omnummertool.overopiban.nl/" target="_blank">hier</a> de bijbehorende IBAN.</p>
<p>Voor vragen kan je altijd een mailtje sturen naar <a href="mailto:info@jongedemocraten.nl">info@jongedemocraten.nl</a>!</p>"""
        form.button_text = "Aanmelden!"
        form.response = "<p>Bedankt voor je inschrijving. Je ontvangt een bevestigingsmail op het emailadres dat je hebt opgegeven.</p>"
        form.send_email = True
        form.email_from = "noreply@jongedemocraten.nl"
        form.email_copies = "ledenadministratie@jongedemocraten.nl"
        form.email_subject = "Bevestiging van inschrijving"
        form.email_message = """Beste aanmelder,

Bedankt voor je aanmelding. Hieronder vind je een overzicht van de gegevens die je hebt ingevoerd."""
        form.save()
        # Geslacht
        f = Field()
        f.form = form
        f.label = "Geslacht"
        f.field_type = fields.RADIO_MULTIPLE
        f.required = True
        f.visible = True
        f.choices = "Man, Vrouw"
        f.default = "Man"
        f.help_text = " "
        f.save()
        # Roepnaam
        f = Field()
        f.form = form
        f.label = "Roepnaam"
        f.field_type = fields.TEXT
        f.required = True
        f.visible = True
        f.choices = ""
        f.default = ""
        f.help_text = " "
        f.save()
        # Voorletters
        f = Field()
        f.form = form
        f.label = "Voorletters"
        f.field_type = fields.TEXT
        f.required = True
        f.visible = True
        f.choices = ""
        f.default = ""
        f.help_text = " "
        f.save()
        # Tussenvoegsels
        f = Field()
        f.form = form
        f.label = "Tussenvoegsels"
        f.field_type = fields.TEXT
        f.required = False
        f.visible = True
        f.choices = ""
        f.default = ""
        f.help_text = " "
        f.save()
        # Achternaam
        f = Field()
        f.form = form
        f.label = "Achternaam"
        f.field_type = fields.TEXT
        f.required = True
        f.visible = True
        f.choices = ""
        f.default = ""
        f.help_text = " "
        f.save()
        # Telefoonnummer
        f = Field()
        f.form = form
        f.label = "Telefoonnummer"
        f.field_type = fields.TEXT
        f.required = True
        f.visible = True
        f.choices = ""
        f.default = ""
        f.help_text = " "
        f.save()
        # E-mailadres
        f = Field()
        f.form = form
        f.label = "E-mailadres"
        f.field_type = fields.EMAIL
        f.required = True
        f.visible = True
        f.choices = ""
        f.default = ""
        f.help_text = " "
        f.save()
        # Straat
        f = Field()
        f.form = form
        f.label = "Straat"
        f.field_type = fields.TEXT
        f.required = True
        f.visible = True
        f.choices = ""
        f.default = ""
        f.help_text = " "
        f.save()
        # Huisnummer
        f = Field()
        f.form = form
        f.label = "Huisnummer"
        f.field_type = 100 # IntegerField
        f.required = True
        f.visible = True
        f.choices = ""
        f.default = ""
        f.help_text = " "
        f.save()
        # Toevoeging
        f = Field()
        f.form = form
        f.label = "Toevoeging"
        f.field_type = fields.TEXT
        f.required = False
        f.visible = True
        f.choices = ""
        f.default = ""
        f.help_text = " "
        f.save()
        # Postcode
        f = Field()
        f.form = form
        f.label = "Postcode"
        f.field_type = fields.TEXT
        f.required = True
        f.visible = True
        f.choices = ""
        f.default = ""
        f.help_text = " "
        f.save()
        # Woonplaats
        f = Field()
        f.form = form
        f.label = "Woonplaats"
        f.field_type = fields.TEXT
        f.required = True
        f.visible = True
        f.choices = ""
        f.default = ""
        f.help_text = " "
        f.save()
        # International Bank Account Number (IBAN)
        f = Field()
        f.form = form
        f.label = "International Bank Account Number (IBAN)"
        f.field_type = fields.TEXT
        f.required = True
        f.visible = True
        f.choices = ""
        f.default = ""
        f.help_text = 'Rekeningnummer omzetten naar IBAN: https://omnummertool.overopiban.nl/'
        f.save()
        # Geboortedatum
        f = Field()
        f.form = form
        f.label = "Geboortedatum"
        f.field_type = fields.DOB
        f.required = True
        f.visible = True
        f.choices = ""
        f.default = ""
        f.help_text = " "
        f.save()
        # Type lidmaatschap
        f = Field()
        f.form = form
        f.label = "Type lidmaatschap"
        f.field_type = fields.SELECT
        f.required = True
        f.visible = True
        f.choices = "€25: combilid JD & D66 (tussen 12 en 27 jaar), `€17,50: alleen JD (tussen 12 en 27 jaar)`, €25: alleen JD (ouder dan 27 jaar)"
        f.default = "€25: combilid JD & D66 (tussen 12 en 27 jaar)"
        f.help_text = " "
        f.save()
        # DEMO Magazine
        f = Field()
        f.form = form
        f.label = "DEMO Magazine"
        f.field_type = fields.RADIO_MULTIPLE
        f.required = True
        f.visible = True
        f.choices = "Alleen digitaal ontvangen, Per post ontvangen"
        f.default = "Alleen digitaal ontvangen"
        f.help_text = " "
        f.save()
        # Opmerkingen
        f = Field()
        f.form = form
        f.label = "Opmerkingen"
        f.field_type = fields.TEXTAREA
        f.required = False
        f.visible = True
        f.choices = ""
        f.default = ""
        f.help_text = " "
        f.save()
        # CAPTCHA
        f = Field()
        f.form = form
        f.label = "CAPTCHA"
        f.field_type = 101 # CaptchaField
        f.required = True
        f.visible = True
        f.choices = ""
        f.default = ""
        f.help_text = " "
        f.save()
        ## Set training aanvragen form
        form = Form()
        oldForm = Page.objects.get(slug = 'training-aanvragen')
        form.parent = oldForm.parent
        oldForm.delete()
        form.title = "Training aanvragen"
        form.slug = 'training-aanvragen'
        form.content = """
<p>Wil je als afdeling, team, werkgroep of commissie een training aanvragen? Vul dan dit formulier in. Voor meer informatie over de trainingen en trainers verwijzen we je graag naar de andere pagina's in het Portal.</p>
<p>Neem voor meer informatie contact op met de Secretaris Scholing en Vorming in het Landelijk Bestuur (<a href="mailto:scholing@jd.nl">scholing@jd.nl</a>).</p>"""
        form.button_text = "Verstuur"
        form.response = "<p>Bedankt voor je aanvraag. Je ontvangt een bevestigingsmail op het emailadres dat je hebt opgegeven.</p>"
        form.send_email = True
        form.email_from = "noreply@jongedemocraten.nl"
        form.email_copies = "scholing@jongedemocraten.nl"
        form.email_subject = "Bevestiging van trainingsaanvraag"
        form.email_message = """Beste aanvrager,

Bedankt voor je aanvraag. Hieronder vind je een overzicht van de gegevens die je hebt ingevoerd."""
        form.save()
        # Naam 
        f = Field()
        f.form = form
        f.label = "Naam"
        f.field_type = fields.TEXT
        f.required = True
        f.visible = True
        f.choices = ""
        f.default = ""
        f.help_text = " "
        f.save()
        # Emailadres
        f = Field()
        f.form = form
        f.label = "Emailadres"
        f.field_type = fields.EMAIL
        f.required = True
        f.visible = True
        f.choices = ""
        f.default = ""
        f.help_text = " "
        f.save()
        # Telefoonnummer
        f = Field()
        f.form = form
        f.label = "Telefoonnummer"
        f.field_type = fields.TEXT
        f.required = True
        f.visible = True
        f.choices = ""
        f.default = ""
        f.help_text = " "
        f.save()
        # Namens
        f = Field()
        f.form = form
        f.label = "Namens"
        f.field_type = fields.SELECT
        f.required = True
        f.visible = True
        f.choices = "Afdeling, Orgaan in afdeling, Landelijk team"
        f.default = "Afdeling"
        f.help_text = " "
        f.save()
        # Specificeer
        f = Field()
        f.form = form
        f.label = "Specificeer"
        f.field_type = fields.TEXT
        f.required = True
        f.visible = True
        f.choices = ""
        f.default = ""
        f.help_text = " "
        f.save()
        # Welke training wil je aanvragen?
        f = Field()
        f.form = form
        f.label = "Welke training wil je aanvragen?"
        f.field_type = fields.SELECT
        f.required = True
        f.visible = True
        f.choices = "Bestuurstraining, Debat Beginners, Debat Gevorderden, Speechen, Presenteren, Opiniërend schrijven, Manipulatie, Framing, Liberalisme, Pragmatisme, Duurzaamheid, Ontwikkelingssamenwerking, Europa, Onderhandelen, Campagne en Strategie, Congressimulatie, Ledenactivering, Organiseren, Formatiespel, Anders"
        f.default = "Bestuurstraining"
        f.help_text = " "
        f.save()
        # Indien anders, welke?
        f = Field()
        f.form = form
        f.label = "Indien anders, welke?"
        f.field_type = fields.TEXT
        f.required = False
        f.visible = True
        f.choices = ""
        f.default = ""
        f.help_text = " "
        f.save()
        # Voor hoeveel mensen is de training?
        f = Field()
        f.form = form
        f.label = "Voor hoeveel mensen is de training?"
        f.field_type = fields.TEXT
        f.required = False
        f.visible = True
        f.choices = ""
        f.default = ""
        f.help_text = " "
        f.save()
        # Heb je een voorkeur qua trainer?
        f = Field()
        f.form = form
        f.label = "Heb je een voorkeur qua trainer?"
        f.field_type = fields.TEXT
        f.required = False
        f.visible = True
        f.choices = ""
        f.default = ""
        f.help_text = " "
        f.save()
        # Eerste optie datum
        f = Field()
        f.form = form
        f.label = "Eerste optie datum"
        f.field_type = fields.DATE
        f.required = True
        f.visible = True
        f.choices = ""
        f.default = ""
        f.help_text = " "
        f.save()
        # Tweede optie datum
        f = Field()
        f.form = form
        f.label = "Tweede optie datum"
        f.field_type = fields.DATE
        f.required = False
        f.visible = True
        f.choices = ""
        f.default = ""
        f.help_text = " "
        f.save()
        # Derde optie datum
        f = Field()
        f.form = form
        f.label = "Derde optie datum"
        f.field_type = fields.DATE
        f.required = False
        f.visible = True
        f.choices = ""
        f.default = ""
        f.help_text = " "
        f.save()
        # Tijdstip
        f = Field()
        f.form = form
        f.label = "Tijdstip"
        f.field_type = fields.TEXT
        f.required = True
        f.visible = True
        f.choices = ""
        f.default = ""
        f.help_text = " "
        f.save()
        # Locatie
        f = Field()
        f.form = form
        f.label = "Locatie"
        f.field_type = fields.TEXT
        f.required = False
        f.visible = True
        f.choices = ""
        f.default = ""
        f.help_text = " "
        f.save()
        # Opmerkingen
        f = Field()
        f.form = form
        f.label = "Opmerkingen"
        f.field_type = fields.TEXTAREA
        f.required = False
        f.visible = True
        f.choices = ""
        f.default = ""
        f.help_text = " "
        f.save()
        # Vul deze captcha in!
        f = Field()
        f.form = form
        f.label = "Vul deze captcha in!"
        f.field_type = 101 # CaptchaField
        f.required = True
        f.visible = True
        f.choices = ""
        f.default = ""
        f.help_text = " "
        f.save()
        
    if (domain == "friesland.jongedemocraten.nl"):
        create_link("Frysk", "//fryslan.jongedemocraten.nl", "/")
    if (domain == "fryslan.jongedemocraten.nl"):
        create_link("Nederlands", "//friesland.jongedemocraten.nl", "/")
    if (domain == "internationaal.jongedemocraten.nl"):
        create_link("LYMEC", "http://www.lymec.org", "koepelorganisaties")
        create_link("IFLRY", "http://www.iflry.org", "koepelorganisaties")

def delete_page(slug):
    try:
        p = Page.objects.get(slug = slug)
        p.delete()
    except Page.DoesNotExist:
        print("Page with slug {0} does not exist".format(slug))

def remove_from_menu(slug):
    try:
        p = Page.objects.get(slug = slug)
        p.in_menus = []
        p.save()
    except Page.DoesNotExist:
        print("Page with slug {0} does not exist".format(slug))

def delete_extraneous_content(domain):
    if (domain == "website.jongedemocraten.nl"):
        delete_page('blog')
        remove_from_menu('contact')
    if (domain == "utrecht.jongedemocraten.nl"):
        remove_from_menu('werkgroepen')
        remove_from_menu('contact')

def page_new_parent(pageSlug, parentSlug):
    try:
        p = Page.objects.get(slug = pageSlug)
    except Page.DoesNotExist:
        print("Page with slug {0} does not exist".format(slug))
        return
    try:
        pp = Page.objects.get(slug = parentSlug)
    except Page.DoesNotExist:
        pp = None
    p.parent = pp
    p.save()

def modify_miscellaneous_content(domain):
    if (domain == "website.jongedemocraten.nl"):
        page_new_parent('mededelingen', 'organisatie')
        page_new_parent('jd-in-de-media', 'media')
        page_new_parent('persberichten', 'media')
        page_new_parent('politieke-opinie', 'media')
        page_new_parent('weblog', 'media')
    if (domain == "brabant.jongedemocraten.nl"):
        page_new_parent('regionaal-politiek-programma-rpp', 'politiek')
    if (domain == "internationaal.jongedemocraten.nl"):
        page_new_parent('young-democrats-english', '/')
        page_new_parent('studiereizen', 'activiteiten')

def create_social_media_button(buttonType, url):
    sb = Sidebar.objects.get()
    s = SocialMediaButton()
    s.type = buttonType
    s.url = url
    s.sidebar = sb
    s.save()

def set_social_media_buttons(domain):
    if (domain == 'website.jongedemocraten.nl'):
        create_social_media_button('FB', "https://www.facebook.com/jongedemocraten")
        create_social_media_button('LI', "https://linkedin.com/groups?gid=1039477")
        create_social_media_button('TW', "https://twitter.com/jongedemocraten")
        create_social_media_button('YT', "https://youtube.com/jongedemocraten")
    if (domain == 'amsterdam.jongedemocraten.nl'):
        create_social_media_button('FB', "https://facebook.com/pages/Jonge-Democraten-Amsterdam/163556367006942")
        create_social_media_button('TW', "https://twitter.com/JDAmsterdam")
        create_social_media_button('YT', "https://youtube.com/JongeDemocratenAdam")
    if (domain == 'arnhemnijmegen.jongedemocraten.nl'):
        create_social_media_button('FB', "https://facebook.com/groups/225827921166/")
        create_social_media_button('TW', "https://twitter.com/JDArnhmNijmgn")
    if (domain == 'brabant.jongedemocraten.nl'):
        create_social_media_button('FB', "https://facebook.com/groups/170404404717/")
        create_social_media_button('TW', "https://twitter.com/JD_Brabant")
    if (domain == 'groningen.jongedemocraten.nl'):
        create_social_media_button('FB', "https://facebook.com/group.php?gid=112050632172284")
        create_social_media_button('TW', "https://twitter.com/JD_Groningen")
    if (domain == 'leidenhaaglanden.jongedemocraten.nl'):
        create_social_media_button('FB', "https://facebook.com/JD.Leiden.Haaglanden")
        create_social_media_button('LI', "https://linkedin.com/groups/Jonge-Democraten-JD-Leiden-Haaglanden-4535613")
        create_social_media_button('TW', "https://twitter.com/JDLeiDenHaageo")
    if (domain == 'rotterdam.jongedemocraten.nl'):
        create_social_media_button('FB', "https://facebook.com/groups/75732134487/")
        create_social_media_button('TW', "https://twitter.com/jd_rotterdam")
    if (domain == 'twente.jongedemocraten.nl'):
        create_social_media_button('FB', "https://facebook.com/JDTwente/")
        create_social_media_button('TW', "https://twitter.com/JDTwente")
    if (domain == 'friesland.jongedemocraten.nl'):
        create_social_media_button('FB', "https://facebook.com/groups/210664798975018/")
        create_social_media_button('TW', "https://twitter.com/JDFryslan")
    if (domain == 'internationaal.jongedemocraten.nl'):
        pass
    if (domain == 'limburg.jongedemocraten.nl'):
        create_social_media_button('FB', "https://facebook.com/groups/jongedemocratenmaastricht/")
        create_social_media_button('TW', "https://twitter.com/jdmaastricht")
    if (domain == 'utrecht.jongedemocraten.nl'):
        create_social_media_button('FB', "https://facebook.com/group.php?gid=93502459706")
        create_social_media_button('TW', "https://twitter.com/JDUtrecht")

def restore_redirects(domain):
    if (domain == 'website.jongedemocraten.nl'):
        redirects = Redirect.objects.all()
        for r in redirects:
            site_id = int(r.old_path.split('/', 1)[0])
            domain = Site.objects.get(id = site_id).domain
            r.old_path = '/' + r.old_path.split('/', 1)[1]
            r.new_path = "https://{0}{1}".format(domain, r.new_path)
            r.save()

def set_sidebar_banner():
    sbw = SidebarBannerWidget()
    sbw.title = "Word lid"
    sbw.image = "/static/website/images/wordlid.jpg"
    sbw.url = "https://jongedemocraten.nl/word-actief/"
    sbw.description = "Word lid van de Jonge Democraten!"
    sbw.save()

def create_redirect(old_path, new_path):
    r = Redirect.objects.get_or_create(old_path = old_path, site_id = 1)
    r[0].new_path = new_path
    r[0].save()

def import_redirects(domain):
    """
    We will manually import the most recent month of URLs as redirects. 
    """
    if (domain == 'website.jongedemocraten.nl'):
        # Redirects to make department map work
        create_redirect('/afdelingen/Groningen/', '//groningen.jongedemocraten.nl')
        create_redirect('/afdelingen/Friesland/', '//friesland.jongedemocraten.nl')
        create_redirect('/afdelingen/Twente/', '//twente.jongedemocraten.nl')
        create_redirect('/afdelingen/Arnhem-Nijmegen/', '//arnhemnijmegen.jongedemocraten.nl')
        create_redirect('/afdelingen/Utrecht/', '//utrecht.jongedemocraten.nl')
        create_redirect('/afdelingen/Amsterdam/', '//amsterdam.jongedemocraten.nl')
        create_redirect('/afdelingen/Limburg/', '//limburg.jongedemocraten.nl')
        create_redirect('/afdelingen/Brabant/', '//brabant.jongedemocraten.nl')
        create_redirect('/afdelingen/Leiden-Haaglanden/', '//leidenhaaglanden.jongedemocraten.nl')
        create_redirect('/afdelingen/Rotterdam/', '//rotterdam.jongedemocraten.nl')
        # Example:
        # create_redirect('/old/url/ends/with/slash/', 'https://amsterdam.jongedemocraten.nl/new/full/URL/')

def twitter_query_for_domain(domain):
    if (domain == 'website.jongedemocraten.nl'):
        return 'jongedemocraten'
    if (domain == 'amsterdam.jongedemocraten.nl'):
        return 'JDAmsterdam'
    if (domain == 'arnhemnijmegen.jongedemocraten.nl'):
        return 'JDArnhmNijmgn'
    if (domain == 'brabant.jongedemocraten.nl'):
        return 'JD_Brabant'
    if (domain == 'groningen.jongedemocraten.nl'):
        return 'JD_Groningen'
    if (domain == 'leidenhaaglanden.jongedemocraten.nl'):
        return 'JDLeiDenHaageo'
    if (domain == 'rotterdam.jongedemocraten.nl'):
        return 'JD_Rotterdam'
    if (domain == 'twente.jongedemocraten.nl'):
        return 'JDTwente'
    if (domain == 'friesland.jongedemocraten.nl'):
        return 'jongedemocraten'
    if (domain == 'internationaal.jongedemocraten.nl'):
        return 'jongedemocraten'
    if (domain == 'limburg.jongedemocraten.nl'):
        return 'JDLimburg'
    if (domain == 'utrecht.jongedemocraten.nl'):
        return 'jongedemocraten'

    return 'jongedemocraten' # Default

class Command(BaseCommand):
    help = 'Set permissions, settings and other values.'
    option_list = BaseCommand.option_list + (
        make_option('--twitterconsumerkey',
                    dest='twitterconsumerkey',
                    default='',
                    help='TWITTER_CONSUMER_KEY'),
        make_option('--twitterconsumersecret',
                    dest='twitterconsumersecret',
                    default='',
                    help='TWITTER_CONSUMER_SECRET'),
        make_option('--twitteraccesstokenkey',
                    dest='twitteraccesstokenkey',
                    default='',
                    help='TWITTER_ACCESS_TOKEN_KEY'),
        make_option('--twitteraccesstokensecret',
                    dest='twitteraccesstokensecret',
                    default='',
                    help='TWITTER_ACCESS_TOKEN_SECRET'),
        make_option('--host',
                    dest='host',
                    default='localhost',
                    help='MySQL host'),
        make_option('--user',
                    dest='user',
                    default='mysql',
                    help='MySQL user'),
        make_option('--password',
                    dest='password',
                    default='password',
                    help='MySQL password'),
        make_option('--database',
                    dest='database',
                    default='database',
                    help='MySQL database'),
        make_option('--tableprefix',
                    dest='tableprefix',
                    default='2gWw',
                    help='Joomla table prefix')
    )


    def handle(self, *args, **options):
        sites = Site.objects.all()
        for site in sites:
            os.environ["MEZZANINE_SITE_ID"] = str(site.id)
            name = site.name
            site_id = site.id
            domain = site.domain
            print("Processing settings for {0}".format(domain))
            if (domain == 'website.jongedemocraten.nl'):
                save_setting('SITE_TAGLINE', '', domain)
                save_setting('SITE_TITLE', 'Jonge Democraten', domain)
            else:
                save_setting('SITE_TAGLINE', name, domain)
                save_setting('SITE_TITLE', 'Jonge Democraten {0}'.format(name), domain)

            save_setting('TWITTER_CONSUMER_KEY',
                options['twitterconsumerkey'], domain)
            save_setting('TWITTER_CONSUMER_SECRET',
                options['twitterconsumersecret'], domain)
            save_setting('TWITTER_ACCESS_TOKEN_KEY',
                options['twitteraccesstokenkey'], domain)
            save_setting('TWITTER_ACCESS_TOKEN_SECRET',
                options['twitteraccesstokensecret'], domain)
            save_setting('TWITTER_DEFAULT_NUM_TWEETS', '3', domain)
            save_setting('TWITTER_DEFAULT_QUERY',
                twitter_query_for_domain(domain), domain)
            save_setting('TWITTER_DEFAULT_QUERY_TYPE', 'search', domain)
            save_setting('ADMIN_MENU_COLLAPSED', 'False', domain)
            save_setting('BLOG_POST_PER_PAGE', '5', domain)
            save_setting('MAX_PAGING_LINKS', '10', domain)
            save_setting('RICHTEXT_FILTER_LEVEL', '1', domain)
            save_setting('PIWIK_SITE_ID', site_id, domain)
            save_setting('SEARCH_PER_PAGE', '10', domain)
            if (domain == 'website.jongedemocraten.nl'):
                save_setting('SIDEBAR_AGENDA_SITES', '3', domain)
            else:
                save_setting('SIDEBAR_AGENDA_SITES', '2', domain)

            create_page_for_each_blog_category()
            activate_twitter_widget()
            force_create_uploads_directory()
            create_column_element_widgets(domain)
            set_sidebar_blogs_for_domain(domain)
            set_social_media_buttons(domain)
            create_extra_content(domain)
            delete_extraneous_content(domain)
            modify_miscellaneous_content(domain)
            set_headers()
            create_mailinglists_and_templates(domain,
                options.get('host'),
                options.get('user'),
                options.get('password'),
                options.get('database'),
                options.get('tableprefix'))
            restore_redirects(domain)
            import_redirects(domain)

        set_sidebar_banner()
        create_newsletter_templates()

        save_group('Administrators')
        save_group('Master Content Managers')
        save_group('Content Managers')
        save_group('Publishers')
        
        save_group_permissions('Administrators', [
            "add_assignedkeyword",
            "add_blogcategory",
            "add_blogcategorypage",
            "add_blogpost",
            "add_captchastore",
            "add_columnelement",
            "add_columnelementwidget",
            "add_comment",
            "add_commentflag",
            "add_contenttype",
            "add_document",
            "add_documentlisting",
            "add_emailsubscriber",
            "add_emailsubscriberaccesstoken",
            "add_event",
            "add_eventcategory",
            "add_eventcolumnelement",
            "add_field",
            "add_fieldentry",
            "add_form",
            "add_formentry",
            "add_gallery",
            "add_galleryimage",
            "add_group",
            "add_homepage",
            "add_janeusrole",
            "add_janeussubscriber",
            "add_janeussubscriberaccesstoken",
            "add_janeususer",
            "add_keyword",
            "add_link",
            "add_logentry",
            "add_mailinglist",
            "add_newsletter",
            "add_newslettertemplate",
            "add_newslettertolist",
            "add_newslettertosubscriber",
            "add_occurrence",
            "add_page",
            "add_pageheaderimagewidget",
            "add_permission",
            "add_query",
            "add_rating",
            "add_redirect",
            "add_richtextpage",
            "add_rule",
            "add_session",
            "add_setting",
            "add_sidebar",
            "add_sidebarbannerwidget",
            "add_sidebarblogcategorywidget",
            "add_sidebartabswidget",
            "add_sidebartwitterwidget",
            "add_site",
            "add_sitepermission",
            "add_socialmediabutton",
            "add_subscriber",
            "add_threadedcomment",
            "add_tweet",
            "add_url",
            "add_user",
            "can_moderate",
            "change_assignedkeyword",
            "change_blogcategory",
            "change_blogcategorypage",
            "change_blogpost",
            "change_captchastore",
            "change_columnelement",
            "change_columnelementwidget",
            "change_comment",
            "change_commentflag",
            "change_contenttype",
            "change_document",
            "change_documentlisting",
            "change_emailsubscriber",
            "change_emailsubscriberaccesstoken",
            "change_event",
            "change_eventcategory",
            "change_eventcolumnelement",
            "change_field",
            "change_fieldentry",
            "change_form",
            "change_formentry",
            "change_gallery",
            "change_galleryimage",
            "change_group",
            "change_homepage",
            "change_janeusrole",
            "change_janeussubscriber",
            "change_janeussubscriberaccesstoken",
            "change_janeususer",
            "change_keyword",
            "change_link",
            "change_logentry",
            "change_mailinglist",
            "change_newsletter",
            "change_newslettertemplate",
            "change_newslettertolist",
            "change_newslettertosubscriber",
            "change_occurrence",
            "change_page",
            "change_pageheaderimagewidget",
            "change_permission",
            "change_query",
            "change_rating",
            "change_redirect",
            "change_richtextpage",
            "change_rule",
            "change_session",
            "change_setting",
            "change_sidebar",
            "change_sidebarbannerwidget",
            "change_sidebarblogcategorywidget",
            "change_sidebartabswidget",
            "change_sidebartwitterwidget",
            "change_site",
            "change_sitepermission",
            "change_socialmediabutton",
            "change_subscriber",
            "change_threadedcomment",
            "change_tweet",
            "change_url",
            "change_user",
            "delete_assignedkeyword",
            "delete_blogcategory",
            "delete_blogcategorypage",
            "delete_blogpost",
            "delete_captchastore",
            "delete_columnelement",
            "delete_columnelementwidget",
            "delete_comment",
            "delete_commentflag",
            "delete_contenttype",
            "delete_document",
            "delete_documentlisting",
            "delete_emailsubscriber",
            "delete_emailsubscriberaccesstoken",
            "delete_event",
            "delete_eventcategory",
            "delete_eventcolumnelement",
            "delete_field",
            "delete_fieldentry",
            "delete_form",
            "delete_formentry",
            "delete_gallery",
            "delete_galleryimage",
            "delete_group",
            "delete_homepage",
            "delete_janeusrole",
            "delete_janeussubscriber",
            "delete_janeussubscriberaccesstoken",
            "delete_janeususer",
            "delete_keyword",
            "delete_link",
            "delete_logentry",
            "delete_mailinglist",
            "delete_newsletter",
            "delete_newslettertemplate",
            "delete_newslettertolist",
            "delete_newslettertosubscriber",
            "delete_occurrence",
            "delete_page",
            "delete_pageheaderimagewidget",
            "delete_permission",
            "delete_query",
            "delete_rating",
            "delete_redirect",
            "delete_richtextpage",
            "delete_rule",
            "delete_session",
            "delete_setting",
            "delete_sidebar",
            "delete_sidebarbannerwidget",
            "delete_sidebarblogcategorywidget",
            "delete_sidebartabswidget",
            "delete_sidebartwitterwidget",
            "delete_site",
            "delete_sitepermission",
            "delete_socialmediabutton",
            "delete_subscriber",
            "delete_threadedcomment",
            "delete_tweet",
            "delete_url",
            "delete_user"
        ])

        save_group_permissions('Master Content Managers', [
#            "add_assignedkeyword",
#            "add_blogcategory",
#            "add_blogcategorypage",
#            "add_blogpost",
#            "add_captchastore",
#            "add_columnelement",
#            "add_columnelementwidget",
#            "add_comment",
#            "add_commentflag",
#            "add_contenttype",
#            "add_document",
#            "add_documentlisting",
            "add_emailsubscriber",
#            "add_emailsubscriberaccesstoken",
#            "add_event",
#            "add_eventcategory",
#            "add_eventcolumnelement",
#            "add_field",
#            "add_fieldentry",
#            "add_form",
#            "add_formentry",
#            "add_gallery",
#            "add_galleryimage",
#            "add_group",
#            "add_homepage",
#            "add_janeusrole",
#            "add_janeussubscriber",
#            "add_janeussubscriberaccesstoken",
#            "add_janeususer",
#            "add_keyword",
#            "add_link",
#            "add_logentry",
#            "add_mailinglist",
#            "add_newsletter",
            "add_newslettertemplate",
#            "add_newslettertolist",
            "add_newslettertosubscriber",
#            "add_occurrence",
#            "add_page",
#            "add_pageheaderimagewidget",
#            "add_permission",
#            "add_query",
#            "add_rating",
#            "add_redirect",
#            "add_richtextpage",
#            "add_rule",
#            "add_session",
#            "add_setting",
#            "add_sidebar",
            "add_sidebarbannerwidget",
#            "add_sidebarblogcategorywidget",
#            "add_sidebartabswidget",
#            "add_sidebartwitterwidget",
#            "add_site",
#            "add_sitepermission",
#            "add_socialmediabutton",
#            "add_subscriber",
#            "add_threadedcomment",
#            "add_tweet",
#            "add_url",
#            "add_user",
#            "can_moderate",
#            "change_assignedkeyword",
#            "change_blogcategory",
#            "change_blogcategorypage",
#            "change_blogpost",
#            "change_captchastore",
#            "change_columnelement",
#            "change_columnelementwidget",
#            "change_comment",
#            "change_commentflag",
#            "change_contenttype",
#            "change_document",
#            "change_documentlisting",
            "change_emailsubscriber",
#            "change_emailsubscriberaccesstoken",
#            "change_event",
#            "change_eventcategory",
#            "change_eventcolumnelement",
#            "change_field",
#            "change_fieldentry",
#            "change_form",
#            "change_formentry",
#            "change_gallery",
#            "change_galleryimage",
#            "change_group",
#            "change_homepage",
#            "change_janeusrole",
            "change_janeussubscriber",
#            "change_janeussubscriberaccesstoken",
#            "change_janeususer",
#            "change_keyword",
#            "change_link",
#            "change_logentry",
#            "change_mailinglist",
#            "change_newsletter",
            "change_newslettertemplate",
            "change_newslettertolist",
            "change_newslettertosubscriber",
#            "change_occurrence",
#            "change_page",
#            "change_pageheaderimagewidget",
#            "change_permission",
#            "change_query",
#            "change_rating",
#            "change_redirect",
#            "change_richtextpage",
#            "change_rule",
#            "change_session",
#            "change_setting",
#            "change_sidebar",
            "change_sidebarbannerwidget",
#            "change_sidebarblogcategorywidget",
#            "change_sidebartabswidget",
#            "change_sidebartwitterwidget",
#            "change_site",
#            "change_sitepermission",
#            "change_socialmediabutton",
#            "change_subscriber",
#            "change_threadedcomment",
#            "change_tweet",
#            "change_url",
#            "change_user",
#            "delete_assignedkeyword",
#            "delete_blogcategory",
#            "delete_blogcategorypage",
#            "delete_blogpost",
#            "delete_captchastore",
#            "delete_columnelement",
#            "delete_columnelementwidget",
#            "delete_comment",
#            "delete_commentflag",
#            "delete_contenttype",
#            "delete_document",
#            "delete_documentlisting",
            "delete_emailsubscriber",
#            "delete_emailsubscriberaccesstoken",
#            "delete_event",
#            "delete_eventcategory",
#            "delete_eventcolumnelement",
#            "delete_field",
#            "delete_fieldentry",
#            "delete_form",
#            "delete_formentry",
#            "delete_gallery",
#            "delete_galleryimage",
#            "delete_group",
#            "delete_homepage",
#            "delete_janeusrole",
#            "delete_janeussubscriber",
#            "delete_janeussubscriberaccesstoken",
#            "delete_janeususer",
#            "delete_keyword",
#            "delete_link",
#            "delete_logentry",
#            "delete_mailinglist",
#            "delete_newsletter",
            "delete_newslettertemplate",
            "delete_newslettertolist",
            "delete_newslettertosubscriber",
#            "delete_occurrence",
#            "delete_page",
#            "delete_pageheaderimagewidget",
#            "delete_permission",
#            "delete_query",
#            "delete_rating",
#            "delete_redirect",
#            "delete_richtextpage",
#            "delete_rule",
#            "delete_session",
#            "delete_setting",
#            "delete_sidebar",
            "delete_sidebarbannerwidget",
#            "delete_sidebarblogcategorywidget",
#            "delete_sidebartabswidget",
#            "delete_sidebartwitterwidget",
#            "delete_site",
#            "delete_sitepermission",
#            "delete_socialmediabutton"
#            "delete_subscriber",
#            "delete_threadedcomment",
#            "delete_tweet",
#            "delete_url",
#            "delete_user"
        ])

        save_group_permissions('Content Managers', [
#            "add_assignedkeyword",
#            "add_blogcategory",
            "add_blogcategorypage",
            "add_blogpost",
#            "add_captchastore",
#            "add_columnelement",
            "add_columnelementwidget",
#            "add_comment",
#            "add_commentflag",
#            "add_contenttype",
            "add_document",
            "add_documentlisting",
#            "add_emailsubscriber",
#            "add_emailsubscriberaccesstoken",
            "add_event",
#            "add_eventcategory",
#            "add_eventcolumnelement",
            "add_field",
            "add_fieldentry",
            "add_form",
            "add_formentry",
#            "add_gallery",
#            "add_galleryimage",
#            "add_group",
#            "add_homepage",
#            "add_janeusrole",
#            "add_janeussubscriber",
#            "add_janeussubscriberaccesstoken",
#            "add_janeususer",
#            "add_keyword",
            "add_link",
#            "add_logentry",
#            "add_mailinglist",
            "add_newsletter",
#            "add_newslettertemplate",
#            "add_newslettertolist",
#            "add_newslettertosubscriber",
            "add_occurrence",
            "add_page",
            "add_pageheaderimagewidget",
#            "add_permission",
#            "add_query",
#            "add_rating",
#            "add_redirect",
            "add_richtextpage",
#            "add_rule",
#            "add_session",
#            "add_setting",
#            "add_sidebar",
#            "add_sidebarbannerwidget",
            "add_sidebarblogcategorywidget",
#            "add_sidebartabswidget",
#            "add_sidebartwitterwidget",
#            "add_site",
#            "add_sitepermission",
            "add_socialmediabutton",
#            "add_subscriber",
#            "add_threadedcomment",
#            "add_tweet",
#            "add_url",
#            "add_user",
#            "can_moderate",
#            "change_assignedkeyword",
#            "change_blogcategory",
            "change_blogcategorypage",
            "change_blogpost",
#            "change_captchastore",
#            "change_columnelement",
            "change_columnelementwidget",
#            "change_comment",
#            "change_commentflag",
#            "change_contenttype",
            "change_document",
            "change_documentlisting",
#            "change_emailsubscriber",
#            "change_emailsubscriberaccesstoken",
            "change_event",
#            "change_eventcategory",
#            "change_eventcolumnelement",
            "change_field",
            "change_fieldentry",
            "change_form",
            "change_formentry",
#            "change_gallery",
#            "change_galleryimage",
#            "change_group",
            "change_homepage",
#            "change_janeusrole",
#            "change_janeussubscriber",
#            "change_janeussubscriberaccesstoken",
#            "change_janeususer",
#            "change_keyword",
            "change_link",
#            "change_logentry",
#            "change_mailinglist",
            "change_newsletter",
#            "change_newslettertemplate",
#            "change_newslettertolist",
#            "change_newslettertosubscriber",
            "change_occurrence",
            "change_page",
            "change_pageheaderimagewidget",
#            "change_permission",
#            "change_query",
#            "change_rating",
#            "change_redirect",
            "change_richtextpage",
#            "change_rule",
#            "change_session",
#            "change_setting",
            "change_sidebar",
#            "change_sidebarbannerwidget",
            "change_sidebarblogcategorywidget",
#            "change_sidebartabswidget",
            "change_sidebartwitterwidget",
#            "change_site",
#            "change_sitepermission",
            "change_socialmediabutton",
#            "change_subscriber",
#            "change_threadedcomment",
#            "change_tweet",
#            "change_url",
#            "change_user",
#            "delete_assignedkeyword",
#            "delete_blogcategory",
            "delete_blogcategorypage",
            "delete_blogpost",
#            "delete_captchastore",
#            "delete_columnelement",
            "delete_columnelementwidget",
#            "delete_comment",
#            "delete_commentflag",
#            "delete_contenttype",
            "delete_document",
            "delete_documentlisting",
#            "delete_emailsubscriber",
#            "delete_emailsubscriberaccesstoken",
            "delete_event",
#            "delete_eventcategory",
#            "delete_eventcolumnelement",
            "delete_field",
            "delete_fieldentry",
            "delete_form",
            "delete_formentry",
#            "delete_gallery",
#            "delete_galleryimage",
#            "delete_group",
#            "delete_homepage",
#            "delete_janeusrole",
#            "delete_janeussubscriber",
#            "delete_janeussubscriberaccesstoken",
#            "delete_janeususer",
#            "delete_keyword",
            "delete_link",
#            "delete_logentry",
#            "delete_mailinglist",
            "delete_newsletter",
#            "delete_newslettertemplate",
#            "delete_newslettertolist",
#            "delete_newslettertosubscriber",
            "delete_occurrence",
            "delete_page",
            "delete_pageheaderimagewidget",
#            "delete_permission",
#            "delete_query",
#            "delete_rating",
#            "delete_redirect",
            "delete_richtextpage",
#            "delete_rule",
#            "delete_session",
#            "delete_setting",
#            "delete_sidebar",
#            "delete_sidebarbannerwidget",
            "delete_sidebarblogcategorywidget",
#            "delete_sidebartabswidget",
#            "delete_sidebartwitterwidget",
#            "delete_site",
#            "delete_sitepermission",
            "delete_socialmediabutton"
#            "delete_subscriber",
#            "delete_threadedcomment",
#            "delete_tweet",
#            "delete_url",
#            "delete_user"
        ])

        save_group_permissions('Publishers', [
#            "add_assignedkeyword",
#            "add_blogcategory",
#            "add_blogcategorypage",
            "add_blogpost",
#            "add_captchastore",
#            "add_columnelement",
#            "add_columnelementwidget",
#            "add_comment",
#            "add_commentflag",
#            "add_contenttype",
#            "add_document",
#            "add_documentlisting",
#            "add_emailsubscriber",
#            "add_emailsubscriberaccesstoken",
            "add_event",
#            "add_eventcategory",
#            "add_eventcolumnelement",
#            "add_field",
#            "add_fieldentry",
#            "add_form",
#            "add_formentry",
#            "add_gallery",
#            "add_galleryimage",
#            "add_group",
#            "add_homepage",
#            "add_janeusrole",
#            "add_janeussubscriber",
#            "add_janeussubscriberaccesstoken",
#            "add_janeususer",
#            "add_keyword",
#            "add_link",
#            "add_logentry",
#            "add_mailinglist",
#            "add_newsletter",
#            "add_newslettertemplate",
#            "add_newslettertolist",
#            "add_newslettertosubscriber",
            "add_occurrence"
#            "add_page",
#            "add_pageheaderimagewidget",
#            "add_permission",
#            "add_query",
#            "add_rating",
#            "add_redirect",
#            "add_richtextpage",
#            "add_rule",
#            "add_session",
#            "add_setting",
#            "add_sidebar",
#            "add_sidebarbannerwidget",
#            "add_sidebarblogcategorywidget",
#            "add_sidebartabswidget",
#            "add_sidebartwitterwidget",
#            "add_site",
#            "add_sitepermission",
#            "add_socialmediabutton",
#            "add_subscriber",
#            "add_threadedcomment",
#            "add_tweet",
#            "add_url",
#            "add_user",
#            "can_moderate",
#            "change_assignedkeyword",
#            "change_blogcategory",
#            "change_blogcategorypage",
#            "change_blogpost",
#            "change_captchastore",
#            "change_columnelement",
#            "change_columnelementwidget",
#            "change_comment",
#            "change_commentflag",
#            "change_contenttype",
#            "change_document",
#            "change_documentlisting",
#            "change_emailsubscriber",
#            "change_emailsubscriberaccesstoken",
#            "change_event",
#            "change_eventcategory",
#            "change_eventcolumnelement",
#            "change_field",
#            "change_fieldentry",
#            "change_form",
#            "change_formentry",
#            "change_gallery",
#            "change_galleryimage",
#            "change_group",
#            "change_homepage",
#            "change_janeusrole",
#            "change_janeussubscriber",
#            "change_janeussubscriberaccesstoken",
#            "change_janeususer",
#            "change_keyword",
#            "change_link",
#            "change_logentry",
#            "change_mailinglist",
#            "change_newsletter",
#            "change_newslettertemplate",
#            "change_newslettertolist",
#            "change_newslettertosubscriber",
#            "change_occurrence",
#            "change_page",
#            "change_pageheaderimagewidget",
#            "change_permission",
#            "change_query",
#            "change_rating",
#            "change_redirect",
#            "change_richtextpage",
#            "change_rule",
#            "change_session",
#            "change_setting",
#            "change_sidebar",
#            "change_sidebarbannerwidget",
#            "change_sidebarblogcategorywidget",
#            "change_sidebartabswidget",
#            "change_sidebartwitterwidget",
#            "change_site",
#            "change_sitepermission",
#            "change_socialmediabutton",
#            "change_subscriber",
#            "change_threadedcomment",
#            "change_tweet",
#            "change_url",
#            "change_user",
#            "delete_assignedkeyword",
#            "delete_blogcategory",
#            "delete_blogcategorypage",
#            "delete_blogpost",
#            "delete_captchastore",
#            "delete_columnelement",
#            "delete_columnelementwidget",
#            "delete_comment",
#            "delete_commentflag",
#            "delete_contenttype",
#            "delete_document",
#            "delete_documentlisting",
#            "delete_emailsubscriber",
#            "delete_emailsubscriberaccesstoken",
#            "delete_event",
#            "delete_eventcategory",
#            "delete_eventcolumnelement",
#            "delete_field",
#            "delete_fieldentry",
#            "delete_form",
#            "delete_formentry",
#            "delete_gallery",
#            "delete_galleryimage",
#            "delete_group",
#            "delete_homepage",
#            "delete_janeusrole",
#            "delete_janeussubscriber",
#            "delete_janeussubscriberaccesstoken",
#            "delete_janeususer",
#            "delete_keyword",
#            "delete_link",
#            "delete_logentry",
#            "delete_mailinglist",
#            "delete_newsletter",
#            "delete_newslettertemplate",
#            "delete_newslettertolist",
#            "delete_newslettertosubscriber",
#            "delete_occurrence",
#            "delete_page",
#            "delete_pageheaderimagewidget",
#            "delete_permission",
#            "delete_query",
#            "delete_rating",
#            "delete_redirect",
#            "delete_richtextpage",
#            "delete_rule",
#            "delete_session",
#            "delete_setting",
#            "delete_sidebar",
#            "delete_sidebarbannerwidget",
#            "delete_sidebarblogcategorywidget",
#            "delete_sidebartabswidget",
#            "delete_sidebartwitterwidget",
#            "delete_site",
#            "delete_sitepermission",
#            "delete_socialmediabutton",
#            "delete_subscriber",
#            "delete_threadedcomment",
#            "delete_tweet",
#            "delete_url",
#            "delete_user"
        ])

        save_janeus_role('role-team-ict',
            ['Administrators'],
            [] # Empty sites = permissions on all sites
        )

        save_janeus_role('role-as-landelijk',
            ['Content Managers',
             'Master Content Managers'
            ],
            []
        )

        save_janeus_role('role-as-groningen',
            ['Content Managers'],
            ['groningen.jongedemocraten.nl']
        )

        save_janeus_role('role-as-friesland',
            ['Content Managers'],
            ['friesland.jongedemocraten.nl']
        )

        save_janeus_role('role-as-friesland',
            ['Content Managers'],
            ['fryslan.jongedemocraten.nl']
        )

        save_janeus_role('role-as-twente',
            ['Content Managers'],
            ['twente.jongedemocraten.nl']
        )

        save_janeus_role('role-as-arnhemnijmegen',
            ['Content Managers'],
            ['arnhemnijmegen.jongedemocraten.nl']
        )

        save_janeus_role('role-as-limburg',
            ['Content Managers'],
            ['limburg.jongedemocraten.nl']
        )

        save_janeus_role('role-as-brabant',
            ['Content Managers'],
            ['brabant.jongedemocraten.nl']
        )

        save_janeus_role('role-as-leidenhaaglanden',
            ['Content Managers'],
            ['leidenhaaglanden.jongedemocraten.nl']
        )

        save_janeus_role('role-as-amsterdam',
            ['Content Managers'],
            ['amsterdam.jongedemocraten.nl']
        )

        save_janeus_role('role-as-rotterdam',
            ['Content Managers'],
            ['rotterdam.jongedemocraten.nl']
        )

        save_janeus_role('role-as-utrecht',
            ['Content Managers'],
            ['utrecht.jongedemocraten.nl']
        )

        save_janeus_role('role-bestuur-landelijk',
            ['Publishers'],
            ['website.jongedemocraten.nl']
        )

        save_janeus_role('role-bestuur-groningen',
            ['Publishers'],
            ['groningen.jongedemocraten.nl']
        )

        save_janeus_role('role-bestuur-friesland',
            ['Publishers'],
            ['friesland.jongedemocraten.nl']
        )

        save_janeus_role('role-bestuur-friesland',
            ['Publishers'],
            ['fryslan.jongedemocraten.nl']
        )

        save_janeus_role('role-bestuur-twente',
            ['Publishers'],
            ['twente.jongedemocraten.nl']
        )

        save_janeus_role('role-bestuur-limburg',
            ['Publishers'],
            ['limburg.jongedemocraten.nl']
        )

        save_janeus_role('role-bestuur-brabant',
            ['Publishers'],
            ['brabant.jongedemocraten.nl']
        )

        save_janeus_role('role-bestuur-rotterdam',
            ['Publishers'],
            ['rotterdam.jongedemocraten.nl']
        )

        save_janeus_role('role-bestuur-leidenhaaglanden',
            ['Publishers'],
            ['leidenhaaglanden.jongedemocraten.nl']
        )

        save_janeus_role('role-bestuur-amsterdam',
            ['Publishers'],
            ['amsterdam.jongedemocraten.nl']
        )

        save_janeus_role('role-bestuur-utrecht',
            ['Publishers'],
            ['utrecht.jongedemocraten.nl']
        )

        save_janeus_role('role-bestuur-arnhemnijmegen',
            ['Publishers'],
            ['arnhemnijmegen.jongedemocraten.nl']
        )



