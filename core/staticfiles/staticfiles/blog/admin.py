from django.contrib import admin
from blog.models import *

# Register your models here.
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('email',)
admin.site.register(Subscribe,SubscribeAdmin)

class ContactAdmin(admin.ModelAdmin):
    list_display=('name','email','subject','message')

admin.site.register(ContactModel,ContactAdmin)

class ServiceItemInline(admin.TabularInline):
    model = ServiceItem
    extra = 1  # Number of empty forms to display

class ServiceAdmin(admin.ModelAdmin):
    list_display=('icon', 'service','icon_desc')
    inlines = [ServiceItemInline]

admin.site.register(ServiceModel,ServiceAdmin)

class ListItemInline(admin.TabularInline):
    model = ListItem
    extra = 1  # Number of empty forms to display

class AboutAdmin(admin.ModelAdmin):
    list_display=('image','tagline', 'para1', 'para2')
    inlines = [ListItemInline]
admin.site.register(AboutModel, AboutAdmin)

class ClientAdmin(admin.ModelAdmin):
    list_display= ('title', 'image')
admin.site.register(ClientModel, ClientAdmin)





class FeatureAdmin(admin.ModelAdmin):
    list_display=('icon', 'title','description')

admin.site.register(Features,FeatureAdmin)

class PortfolioAdmin(admin.ModelAdmin):
    list_display=('title','category','image')
admin.site.register(Portfolio,PortfolioAdmin)



class PortfolioImageInline(admin.TabularInline):
    model = PortfolioImage
    extra = 1  # Number of empty forms to display

@admin.register(Portfolio_details)
class PortDetAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'client', 'project_date')
    search_fields = ('title', 'category', 'client')
    inlines = [PortfolioImageInline]

@admin.register(PortfolioImage)
class PortfolioImageAdmin(admin.ModelAdmin):
    pass


class HeaderAdmin(admin.ModelAdmin):
    list_display = ('site_name','line1','line2')
admin.site.register(Header,HeaderAdmin)    


class HeroImageInline(admin.TabularInline):
    model = HeroImage
    extra = 1 

class HeroAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [HeroImageInline]

admin.site.register(Hero, HeroAdmin)

class FooterAdmin(admin.ModelAdmin):
    list_display = ('address','phone','email','newsletter')
admin.site.register(Footer,FooterAdmin)

class SocialAdmin(admin.ModelAdmin):
    list_display=('icon','link')
admin.site.register(Social,SocialAdmin)