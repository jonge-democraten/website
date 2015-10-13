import pymysql

import os
from datetime import datetime

from optparse import make_option
from urllib.parse import urlparse, parse_qs
from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site

from mezzanine.pages.models import RichTextPage, Link
from mezzanine.blog.management.base import BaseImporterCommand
# from website.jdpages.models import JDPage
from fullcalendar.models import create_event
from website.jdpages.models import HomePage


def get_post_url(cur, table_prefix, post_id):
    cur.execute('SELECT * FROM '+table_prefix+'_content WHERE id=%s;',
                (post_id,))
    post = cur.fetchone()
    name = "%d-%s.html" % (post[0], post[3])
    cur.execute('SELECT * FROM '+table_prefix+'_categories WHERE id=%s;',
                (post[10],))
    cat = cur.fetchone()
    return '/'+cat[9]+'/'+name+'/'


class Command(BaseImporterCommand):
    args = 'mysql://user:password@host/database'
    help = 'Import pages from the old JD Joomla database'
    option_list = BaseImporterCommand.option_list + (
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

    def handle_import(self, options):
        try:
            db = pymysql.connect(host=options.get('host'),
                                 user=options.get('user'),
                                 password=options.get('password'),
                                 database=options.get('database'))
        except pymysql.err.OperationalError as e:
            raise CommandError(e)
        cur = db.cursor()
        # Get all menu types
        cur.execute('SELECT * FROM '+options.get('tableprefix')+'_menu_types;')
        print("Beschikbare sites:")
        sites = dict()
        for menutype in cur.fetchall():
            print('%d\t%s' % (menutype[0], menutype[1]))
            sites[menutype[0]]= menutype[1]
        while True:
            menuid = input("Site id om te migreren: ")
            if int(menuid) in sites:
                menuid = int(menuid)
                break
            else:
                print("Ongeldige keuze")
        print("Maak Mezzanine site aan:")
        domain = input("\tDomein naam:\t")
        name = input("\tNaam:\t")
        site, created = Site.objects.get_or_create(domain=domain)
        site.name = name
        site.save()
        os.environ["MEZZANINE_SITE_ID"] = str(site.id)
        
        #######################################################################
        # Get all events for the specified site
        #######################################################################
        print("### MIGRATING EVENTS ###")
        categories = {}
        cur.execute('SELECT assets.title, assets.name FROM '+options.get('tableprefix')+'_categories as cat JOIN '+options.get('tableprefix')+'_assets as assets ON cat.asset_id = assets.id WHERE cat.extension = "com_jevents";')
        for c in cur.fetchall():
            categories[int(c[1].split(".")[-1])] = c[0]
        for k in categories:
            print("[%d]\t'%s'" % (k, categories[k]))
        while True:
            cat = input("Events categorie om te migreren:")
            if cat == "-1":
                break
            if cat.isdigit() and int(cat) in categories:
                break
            else:
                print("Ongeldige keuze")
        cur.execute('SELECT vevdetail.summary, vevdetail.description, vevdetail.dtstart, vevdetail.dtend, vevdetail.location, vevent.created ' \
                    'FROM joomla.2gWw_jevents_catmap AS catmap ' \
                    'LEFT JOIN joomla.2gWw_jevents_vevent AS vevent ON catmap.evid = vevent.ev_id ' \
                    'LEFT JOIN joomla.2gWw_jevents_vevdetail AS vevdetail ON vevent.detail_id = vevdetail.evdet_id ' \
                    'WHERE vevent.catid = %s;', (cat,))
        for event in cur.fetchall():
            e = create_event(event[0], None, event[1], datetime.fromtimestamp(int(event[2])), datetime.fromtimestamp(int(event[3])))
            e.publish_date = event[5]
            e.save()
            occurrences = e.occurrence_set.all()
            for o in occurrences:
                o.location = event[4]
                o.save()
            e.save()
        
        
        #######################################################################
        # Get all pages for the specified site
        #######################################################################
        print("### MIGRATING PAGES ###")
        cur.execute('SELECT * FROM '+options.get('tableprefix')+'_menu WHERE menutype=%s and published=1;', sites[menuid] )
        for menu in cur.fetchall():
            menutype = menu[7]
            if menutype == "url":
                # TODO: handmatig migreren
                print("Link")
            elif menutype == "component":
                url = urlparse(menu[6])
                qs = parse_qs(url.query)
                if 'option' in qs and qs['option'][0] == 'com_content':
                    # Blogpost or page
                    if 'view' in qs and qs['view'][0] == 'article':
                        # Page 
                        # _content.state  has the following values
                        #  0 = unpublished
                        #  1 = published
                        # -1 = archived
                        # -2 = marked for deletion
                        if 'id' in qs:
                            cur.execute('SELECT id, title, introtext, `fulltext` ' \
                                        'FROM '+options.get('tableprefix')+'_content ' \
                                        'WHERE id=' + qs['id'][0] + ' and state=1;')
                            if menu[2].startswith('Home') or menu[2].startswith('Wjelk'):
                                # Homepage
                                page = cur.fetchall()[0]
                                h = HomePage()
                                h.title = menu[2]
                                h.content = page[2] + page[3]
                                h.save()
                                h.set_slug('/')
                                h.save()
                                print("Imported homepage")
                            else:
                                # Regular page
                                for page in cur.fetchall():
                                    self.add_page(  title=menu[2],
                                                    content=page[2]+page[3],
                                                    old_url=get_post_url(cur, options.get('tableprefix'), page[0]),
                                                    old_id=menu[0],
                                                    old_parent_id=menu[9])

                    if 'view' in qs and qs['view'][0] == 'category' and 'layout' in qs and qs['layout'][0] == 'blog' and 'id' in qs:
                        # Blogpost
                        # _content.state  has the following values
                        #  0 = unpublished
                        #  1 = published
                        # -1 = archived
                        # -2 = marked for deletion
                        cur.execute('SELECT content.*, category.title FROM '+options.get('tableprefix')+'_content as content LEFT JOIN '+options.get('tableprefix')+'_categories as category ON content.catid = category.id WHERE content.catid=%s and content.state=1;', (qs['id'][0],))
                        for page in cur.fetchall():
                            self.add_post(title=page[2],
                                    pub_date=page[18],
                                    content=page[5]+page[6],
                                    categories=(page[34],),
                                    old_url=get_post_url(cur, options.get('tableprefix'),page[0]))
                print("Component")
            else:
                print("Unknown: ", menu[0])
            continue
        


