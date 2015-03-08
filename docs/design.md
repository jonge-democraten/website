<h1>Design</h1>
The design of different components is explained in this document.  

## Sidebar
A Sidebar model represents the information that should be shown in a sidebar on the webpage.
 
* One Sidebar per Site; a singleton within a Site.
* A Sidebar is automatically created when a new site is created.
* The Sidebar is editable via a SingletonAdmin

<h3>Sidebar widgets</h3>
SidebarWidget models are configurable elements of a Sidebar.  
They can be add to a Sidebar via a TabularInline in the admin.

<h3>Sidebar items</h3>
A view representing a SidebarWidget.

* Contains the template filename that draws this item.
* Contains the information need by the template.
* Created in `context_processor.py` for each context.

<h3>Example</h3>
This example shows how to create a SidebarWidget for a new element that you want to show in the sidebar.

**Widget model**  
Create a new widget model type that can be added to a sidebar,
```Python
class ExampleSidebarWidget(SiteRelated):
    title = models.CharField(max_length=200)
    sidebar = models.ForeignKey(Sidebar, blank=False, null=False)
    example = models.ForeignKey(Example, blank=False, null=True)
```

**View item**  
Crate a view item for the new widget,
```Python
class ExampleSidebarItem(SiteRelated):

    def __init__(self, example, max_posts):
        self.title = example.title
        
    def get_template_name(self):
        return "example_item.html"
```

**Template**  
Create a Django template that renders the item and its children (optional).
The item is available in the template as `{{ item }}`,
```HTML
<div class="moduletable">
    <div class="custom"  >
        <h1>{{ item.title }}</h1>
    </div>
</div>
```

**Context processor**  
Create the items in a context request in `jdpages/context_processors.py`,
```Python
def sidebar(request):
    example_widgets = ExampleSidebarWidget.objects.filter(active=True)
    for widget in example_widgets:
        item = ExampleSidebarItem(widget)
        sidebar_items.append(item)
```

**Admin interface**  
Create a TabularInline admin,
```Python
class ExampleSidebarWidgetInline(admin.TabularInline):
    model = ExampleSidebarWidget
```

Add the Inline to the SidebarAdmin inlines,
```Python
class SidebarAdmin(SingletonAdmin):
    model = Sidebar
    inlines = (ExampleSidebarWidgetInline,)
```