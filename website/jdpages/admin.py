import logging

from django.conf import settings
from django.contrib import admin
from django.forms.models import ModelForm
from django.contrib.admin import TabularInline

from mezzanine.core.admin import TabularDynamicInlineAdmin
from mezzanine.core.admin import StackedDynamicInlineAdmin
from mezzanine.forms.models import Form
from mezzanine.forms.admin import FormAdmin
from mezzanine.pages.admin import PageAdmin
from mezzanine.pages.models import RichTextPage
from mezzanine.utils.admin import SingletonAdmin

from website.jdpages.models import BlogCategoryPage
from website.jdpages.models import Footer
from website.jdpages.models import FooterLink
from website.jdpages.models import FooterLinks
from website.jdpages.models import FooterInfo
from website.jdpages.models import HomePage
from website.jdpages.models import OrganisationPage
from website.jdpages.models import OrganisationPartPage
from website.jdpages.models import OrganisationMember
from website.jdpages.models import OrganisationPartMember
from website.jdpages.models import VisionPage
from website.jdpages.models import VisionsPage
from website.jdpages.models import ActionBanner
from website.jdpages.models import PageHeaderImage
from website.jdpages.models import SidebarAgenda
from website.jdpages.models import SidebarSocial
from website.jdpages.models import SidebarTwitter
from website.jdpages.models import SidebarLink
from website.jdpages.models import SidebarRichText
from website.jdpages.models import SocialMediaUrls

logger = logging.getLogger(__name__)


class AlwaysChangedModelForm(ModelForm):
    """
    A django modelform that is always changed and will thus always be saved and validated.
    To be used for inlines that should also be created with their default/initial values.
    """
    def has_changed(self):
        """
        Should return True if data differs from initial.
        Unchanged inlines will also get validated and saved by always returning true here.
        """
        return True


class FooterLinkInline(TabularDynamicInlineAdmin):
    model = FooterLink


class FooterLinksAdmin(admin.ModelAdmin):
    model = FooterLinks
    inlines = [FooterLinkInline]


class PageHeaderImageInline(TabularDynamicInlineAdmin):
    model = PageHeaderImage
    verbose_name = "Header Image"
    verbose_name_plural = "Header Images"


class ActionBannerInline(StackedDynamicInlineAdmin):
    model = ActionBanner
    extra = 1
    verbose_name = "Action Banner"
    verbose_name_plural = "Action Banner"


class SidebarAgendaInline(TabularDynamicInlineAdmin):
    model = SidebarAgenda
    form = AlwaysChangedModelForm
    extra = 0
    verbose_name = "Sidebar Agenda"
    verbose_name_plural = "Sidebar Agenda"


class SidebarSocialInline(TabularDynamicInlineAdmin):
    model = SidebarSocial
    form = AlwaysChangedModelForm
    extra = 0
    verbose_name = "Sidebar Social"
    verbose_name_plural = "Sidebar Social"


class SidebarTwitterInline(TabularDynamicInlineAdmin):
    model = SidebarTwitter
    form = AlwaysChangedModelForm
    extra = 0
    verbose_name = "Sidebar twitter"
    verbose_name_plural = "Sidebar Twitter"


class SidebarLinkInline(TabularDynamicInlineAdmin):
    model = SidebarLink
    form = AlwaysChangedModelForm
    extra = 0
    verbose_name = "Sidebar Links"
    verbose_name_plural = "Sidebar Links"


class SidebarRichTextInline(StackedDynamicInlineAdmin):
    model = SidebarRichText
    form = AlwaysChangedModelForm
    extra = 1
    verbose_name = "Sidebar Content"
    verbose_name_plural = "Sidebar Content"


class HomePageAdmin(PageAdmin):
    model = HomePage
    inlines = [PageHeaderImageInline, ActionBannerInline, SidebarAgendaInline, SidebarTwitterInline, SidebarSocialInline]


class VisionsPageAdmin(PageAdmin):
    model = VisionsPage
    inlines = [PageHeaderImageInline, SidebarTwitterInline]
    verbose_name = "Standpunten Pagina"
    verbose_name_plural = "Standpunten Pagina"


class VisionPageAdmin(PageAdmin):
    model = VisionPage
    inlines = [PageHeaderImageInline, SidebarTwitterInline]
    verbose_name = "Standpunt Pagina"
    verbose_name_plural = "Standpunt Pagina"


class OrganisationPageAdmin(PageAdmin):
    model = OrganisationPage
    inlines = [PageHeaderImageInline, SidebarTwitterInline]
    verbose_name = "Organisatie Pagina"
    verbose_name_plural = "Organisatie Pagina"


class OrganisationPartPageAdmin(PageAdmin):
    model = OrganisationPartPage
    inlines = [PageHeaderImageInline, SidebarTwitterInline]
    verbose_name = "Organisatieonderdeel Pagina"
    verbose_name_plural = "Organisatieonderdeel Pagina"


class OrganisationMemberAdmin(admin.ModelAdmin):
    model = OrganisationMember
    verbose_name = "Organisatie Lid"
    verbose_name_plural = "Organisatie Leden"
    list_display = (
        'name',
        'image',
        'facebook_url',
        'twitter_url',
    )
    search_fields = ['name']


class OrganisationPartMemberAdmin(admin.ModelAdmin):
    model = OrganisationPartMember
    verbose_name = "Organisatie Functie"
    verbose_name_plural = "Organisatie Functies"
    list_display = (
        'member',
        'organisation_part',
        'role',
    )
    search_fields = ['member__name']


class RichtTextPageAdmin(PageAdmin):
    inlines = [
        PageHeaderImageInline, SidebarAgendaInline, SidebarSocialInline,
        SidebarTwitterInline, SidebarLinkInline, SidebarRichTextInline
    ]


class BlogPageAdmin(PageAdmin):
    inlines = [PageHeaderImageInline]


class CustomFormAdmin(FormAdmin):
    model = Form
    inlines = [PageHeaderImageInline, SidebarRichTextInline]
    inlines.insert(0, FormAdmin.inlines[0])


class FooterAdmin(SingletonAdmin):
    model = Footer
    verbose_name = "Footer"
    verbose_name_plural = "Footer"


class SocialMediaUrlsAdmin(SingletonAdmin):
    model = SocialMediaUrls
    verbose_name = "Social media urls"
    verbose_name_plural = "Social media urls"


admin.site.unregister(RichTextPage)
admin.site.register(RichTextPage, RichtTextPageAdmin)

admin.site.unregister(Form)
admin.site.register(Form, CustomFormAdmin)

admin.site.register(HomePage, HomePageAdmin)
admin.site.register(OrganisationPartPage, OrganisationPartPageAdmin)
admin.site.register(OrganisationPage, OrganisationPageAdmin)
admin.site.register(VisionPage, VisionPageAdmin)
admin.site.register(VisionsPage, VisionsPageAdmin)
admin.site.register(BlogCategoryPage, BlogPageAdmin)

admin.site.register(OrganisationMember, OrganisationMemberAdmin)
admin.site.register(OrganisationPartMember, OrganisationPartMemberAdmin)

admin.site.register(Footer, FooterAdmin)
admin.site.register(FooterInfo)
admin.site.register(FooterLinks, FooterLinksAdmin)
admin.site.register(SocialMediaUrls, SocialMediaUrlsAdmin)
