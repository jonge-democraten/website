import pymysql

import os

from optparse import make_option
from urllib.parse import urlparse, parse_qs
from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site

from mezzanine.pages.models import RichTextPage
from mezzanine.blog.management.base import BaseImporterCommand
# from website.jdpages.models import JDPage


def get_post_url(cur, table_prefix, post_id):
    cur.execute('SELECT * FROM '+table_prefix+'_content WHERE id=%s;',
                (post_id,))
    post = cur.fetchone()
    name = "%d-%s.html" % (post[0], post[3])
    cur.execute('SELECT * FROM '+table_prefix+'_categories WHERE id=%s;',
                (post[10],))
    cat = cur.fetchone()
    return cat[9]+'/'+name


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
        site = Site(domain=domain, name=name)
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
        
        
        #######################################################################
        # Get all pages for the specified site
        #######################################################################
        print("### MIGRATING PAGES ###")
        cur.execute('SELECT * FROM '+options.get('tableprefix')+'_menu WHERE menutype=%s;', sites[menuid] )
        for menu in cur.fetchall():
            url = urlparse(menu[6])
            qs = parse_qs(url.query)
            ifblog. = False
            if 'view' in qs and qs['view'][0] == 'category' and 'layout' in qs and qs['layout'][0] == 'blog':
                isblog = True
            if 'id' in qs:
                print('| + ' + menu[5]+' => '+ qs['id'][0])
                # _content.state  has the following values
                #  0 = unpublished
                #  1 = published
                # -1 = archived
                # -2 = marked for deletion
                cur.execute('SELECT * FROM '+options.get('tableprefix')+'_content WHERE catid=%s and state=1 AND asset_id;', (qs['id'][0],))
                for page in cur.fetchall():
                    if isblog:
                        self.add_post(title=page[2], 
                                    content=page[5]+page[6],
                                    old_url=get_post_url(cur, options.get('tableprefix'),page[0]),
                                    #old_id=page[0])#,
                                    #old_parent_id=menu[0]))
                    else:
                        self.add_page(  title=page[2], 
                                    content=page[5]+page[6],
                                    old_url=get_post_url(cur, options.get('tableprefix'),page[0]),
                                    old_id=page[0])#
                                    #old_parent_id=menu[0])
                    print('| | | '+page[3])
            else:
                print('| | ' + menu[5])

        


