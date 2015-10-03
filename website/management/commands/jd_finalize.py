import os

from django.core.management.base import BaseCommand, CommandError
from mezzanine.conf.models import Setting
from django.contrib.auth.models import User, Group, Permission
from django.contrib.sites.models import Site
from janeus.models import JaneusRole
from optparse import make_option

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
                    help='TWITTER_ACCESS_TOKEN_SECRET')
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
            save_setting('SIDEBAR_AGENDA_SITES', '2', domain)

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
            "add_newslettertolist",
            "add_newslettertosubscriber",
#            "add_occurrence",
#            "add_page",
#            "add_pageheaderimagewidget",
#            "add_permission",
#            "add_query",
#            "add_rating",
#            "add_redirect",
#            "add_richtextpage",
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
            "add_newslettertolist",
#            "add_newslettertosubscriber",
            "add_occurrence",
            "add_page",
            "add_pageheaderimagewidget",
#            "add_permission",
#            "add_query",
#            "add_rating",
#            "add_redirect",
            "add_richtextpage",
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



