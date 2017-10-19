<h1>Design</h1>
The design of different jdwebsite components is explained in this document.

<h3> Django and Mezzanine</h3>
The project is build on [Mezzanine](http://mezzanine.jupo.org/) and [Django](https://www.djangoproject.com/).  
To understand the design, and to work with the code, it is essential to have a basic understanding of both Django and Mezzanine.

<h3>Multitenancy</h3>
Mezzanine makes use of Django’s sites app to support multiple sites in a single project. 
[[doc](http://mezzanine.jupo.org/docs/multi-tenancy.html)] 

* Multitenancy is used to create indpendent Site instances for local departments.  
* Departments can have a customized website with default elements. 
* Forces a consistent look among the department sites.
* Department sites have indepenent permissions.
* There is only a single Django instance and database to setup and maintain.

The SiteRelated Mezzanine class is used to create site related models of which the scope is automatically limited
 to its site. 

# jdpages
The jpdages module contains models and views for website elements such as header, sidebar and pages.
These elements based on Mezzanine SiteRelated and Page objects. 

## Page
A page is always derived from Mezzanine Page. It contains content for a single page (with url) on the website.

Custom pages allow the backend user to create a customizable page. 
Examples are a BlogCategoryPage which has a BlogCategory as input field, and a DocumentListing page that shows uploaded documents.

## Blog (category/post/page)

The Mezzanine blog categories and posts models are used without modifications. 
The views and templates are modified to remove functionality for the frontend user, and to modify the style. 

There are blog categories and blog posts in the Mezzanine blog application. 
Always make clear which of the two you mean when talking about blog related functionality.

There are two blog related views and templates: one for a blog category page, and one for a single blog post,

* A BlogCategoryPage page type shows all blog posts in a blog category on a single page. The page is shown in the menu. Its blog category and header can be set in the admin.
* A single blog posts is shown using the Mezzanine blog detail view function, in combination with a custom template that includes the page header image of the homepage.

## Page header image
The page header is the image on top of each page (not site). Below the site header and menu bar.

Multiple images can be added from the media library to function als page header image. The images need to be exactly 610 x 290 pixels to be accepted.
In case multiple images are set, a random image will be selected on each page request. 
In case no image is set, the homepage image will be used. 

<h3>Example - add header to new custom page</h3>

Add an inline admin field for the header type and (optional) header images to the new custom page in `jdpages/admin.py`,
```Python
class ExamplePageAdmin(PageAdmin):
    inlines = [PageHeaderImageInline]    
admin.site.register(Example, ExamplePageAdmin)
```
This allow content managers to add a page header to the page in the page admin.

Add a `add_header_images()` processor for the new custom page, derived from Mezzanine Page, in `jdpages/page_processors.py`,
```Python
@processor_for(ExamplePage)
def add_header_images(request, page):
    ...
```

Finally, include the header template in your custom page template to show the image header on the page,
```Python
{% if page_header %}
    {% include "elements/page_header_image.html" %}
{% endif %}
```

## Events

The [jonge-democraten/mezzanine-fullcalendar](https://github.com/jonge-democraten/mezzanine-fullcalendar) app is used for events.

An Event has Occurrences. 
Events and Occurrences can be created and modified in the Mezzanine admin.
Templates using the fullcalendar template tags are used to create event views customized for jdwebsite.

The event sidebar and page column widgets can be set, via the admin, to show events for,
 
* All sites
* Current site
* Current and main site

The calendar on the main site shows events for all sites (departments). The color for each site can be set in `local_settings.py` with the `FULLCALENDAR_SITE_COLORS` variable.
A legend with site name and colour is then shown in the calendar view.

[mezzanine-fullcalendar](https://github.com/jonge-democraten/mezzanine-fullcalendar) was forked to be used by jdwebsite.  
Improve and maintain mezzanine-fullcalendar.
