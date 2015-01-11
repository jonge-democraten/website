import pymysql

from optparse import make_option
from urllib.parse import urlparse, parse_qs
from django.core.management.base import BaseCommand, CommandError

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


class Command(BaseCommand):
    args = 'mysql://user:password@host/database'
    help = 'Import pages from the old JD Joomla database'
    option_list = BaseCommand.option_list + (
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
        for menutype in cur.fetchall():
            print('+ '+menutype[1])
            cur.execute('SELECT * FROM '+options.get('tableprefix')+'_menu WHERE menutype=%s;', (menutype[1],))
            for menu in cur.fetchall():
                url = urlparse(menu[6])
                qs = parse_qs(url.query)
                if 'id' in qs:
                    print('| + ' + menu[5]+' => '+ qs['id'][0])
                    cur.execute('SELECT * FROM '+options.get('tableprefix')+'_content WHERE catid=%s;', (qs['id'][0],))
                    for page in cur.fetchall():
                        print('| | | '+page[3])
                else:
                    print('| | ' + menu[5])


