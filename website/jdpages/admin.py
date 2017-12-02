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
from website.jdpages.models import ThatsWhyItem
from website.jdpages.models import WordLidPage

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
    verbose_name = "Footer link"
    verbose_name_plural = "Footer links"

class FooterLinksAdmin(admin.ModelAdmin):
    model = FooterLinks
    inlines = [FooterLinkInline]

class PageHeaderImageInline(TabularDynamicInlineAdmin):
    model = PageHeaderImage
    verbose_name = "Header image"
    verbose_name_plural = "Header images"

class ActionBannerInline(StackedDynamicInlineAdmin):
    model = ActionBanner
    extra = 1
    verbose_name = "Action banner"
    verbose_name_plural = "Action banners"

class SidebarAgendaInline(TabularDynamicInlineAdmin):
    model = SidebarAgenda
    form = AlwaysChangedModelForm
    extra = 0
    verbose_name = "Agenda sidebar"
    verbose_name_plural = "Agenda sidebars"

class SidebarSocialInline(TabularDynamicInlineAdmin):
    model = SidebarSocial
    form = AlwaysChangedModelForm
    extra = 0
    verbose_name = "Social sidebar"
    verbose_name_plural = "Social sidebars"

class SidebarTwitterInline(TabularDynamicInlineAdmin):
    model = SidebarTwitter
    form = AlwaysChangedModelForm
    extra = 0
    verbose_name = "Twitter sidebar"
    verbose_name_plural = "Twitter sidebars"

class SidebarLinkInline(TabularDynamicInlineAdmin):
    model = SidebarLink
    form = AlwaysChangedModelForm
    extra = 0
    verbose_name = "Link list sidebar"
    verbose_name_plural = "Link list sidebars"

class SidebarRichTextInline(StackedDynamicInlineAdmin):
    model = SidebarRichText
    extra = 1
    verbose_name = "Content sidebar"
    verbose_name_plural = "Content sidebars"

class ThatsWhyInline(TabularDynamicInlineAdmin):
    model = ThatsWhyItem
    form = AlwaysChangedModelForm
    extra = 0
    verbose_name = "That's why item"
    verbose_name_plural = "That's why items"

class HomePageAdmin(PageAdmin):
    model = HomePage
    inlines = [PageHeaderImageInline, ActionBannerInline, SidebarAgendaInline, SidebarTwitterInline, SidebarSocialInline]

class VisionsPageAdmin(PageAdmin):
    model = VisionsPage
    inlines = [PageHeaderImageInline, SidebarTwitterInline]
    verbose_name = "Standpuntenpagina"
    verbose_name_plural = "Standpuntenpagina's"

    def get_form(self, request, obj=None, **kwargs):
        # remove the '+' (add) button for vision pages, should not be created here
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["vision_pages"].widget.can_add_related = False
        return form

class VisionPageAdmin(PageAdmin):
    model = VisionPage
    inlines = [PageHeaderImageInline, SidebarTwitterInline]
    verbose_name = "Standpuntpagina"
    verbose_name_plural = "Standpuntpagina's"

class OrganisationPageAdmin(PageAdmin):
    model = OrganisationPage
    inlines = [PageHeaderImageInline, SidebarTwitterInline]
    verbose_name = "Organisatiepagina"
    verbose_name_plural = "Organisatiepagina's"

    def get_form(self, request, obj=None, **kwargs):
        # remove the '+' (add) button for part pages, should not be created here
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["organisation_part_pages"].widget.can_add_related = False
        return form

class OrganisationPartPageAdmin(PageAdmin):
    model = OrganisationPartPage
    inlines = [PageHeaderImageInline, SidebarTwitterInline]
    verbose_name = "Organisatieonderdeelpagina"
    verbose_name_plural = "Organisatieonderdeelpagina's"

class OrganisationMemberAdmin(admin.ModelAdmin):
    model = OrganisationMember
    verbose_name = "Organisatielid"
    verbose_name_plural = "Organisatieleden"
    list_display = (
        'name',
        'image',
        'facebook_url',
        'twitter_url',
    )
    search_fields = ['name']

class OrganisationPartMemberAdmin(admin.ModelAdmin):
    model = OrganisationPartMember
    verbose_name = "Organisatiefunctie"
    verbose_name_plural = "Organisatiefuncties"
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

class WordLidAdmin(PageAdmin):
    model = WordLidPage
    inlines = [
      PageHeaderImageInline, ActionBannerInline, SidebarTwitterInline, SidebarLinkInline, ThatsWhyInline
    ]

class CustomFormAdmin(FormAdmin):
    model = Form
    inlines = [PageHeaderImageInline, SidebarRichTextInline]
    inlines.insert(0, FormAdmin.inlines[0])

class FooterAdmin(SingletonAdmin):
    model = Footer
    verbose_name = "Footer"
    verbose_name_plural = "Footers"

class SocialMediaUrlsAdmin(SingletonAdmin):
    model = SocialMediaUrls
    verbose_name = "Social media url list"
    verbose_name_plural = "Social media url lists"

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
admin.site.register(WordLidPage, WordLidAdmin)

admin.site.register(OrganisationMember, OrganisationMemberAdmin)
admin.site.register(OrganisationPartMember, OrganisationPartMemberAdmin)

admin.site.register(Footer, FooterAdmin)
admin.site.register(FooterInfo)
admin.site.register(FooterLinks, FooterLinksAdmin)
admin.site.register(SocialMediaUrls, SocialMediaUrlsAdmin)
