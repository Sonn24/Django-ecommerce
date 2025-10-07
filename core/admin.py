from django.contrib import admin
from .models import *


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)
make_refund_accepted.short_description = 'Update orders to refund granted'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered', 'being_delivered', 'received',
                    'refund_requested', 'refund_granted',
                    'shipping_address', 'billing_address',
                    'payment', 'coupon']
    list_display_links = ['user', 'shipping_address', 'billing_address', 'payment', 'coupon']
    list_filter = ['ordered', 'being_delivered', 'received', 'refund_requested', 'refund_granted']
    search_fields = ['user__username', 'ref_code']
    actions = [make_refund_accepted]


class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'street_address', 'apartment_address',
                    'country', 'zip', 'address_type', 'default']
    list_filter = ['default', 'address_type', 'country']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip']


# ✅ Inline models for Item
class ItemSizeInline(admin.TabularInline):
    model = ItemSize
    extra = 1


class ItemColorInline(admin.TabularInline):
    model = ItemColor
    extra = 1


class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'discount_price']
    list_filter = ['category', 'label']
    search_fields = ['title', 'description']
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ItemSizeInline, ItemColorInline]  # ✅ Show sizes + colors inline


# =====================
# Model Registrations
# =====================
admin.site.register(Item, ItemAdmin)        # ✅ Only once, with custom admin
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile)


class FeatureAdmin(admin.ModelAdmin):
    list_display = ('icon', 'title', 'description')
admin.site.register(Features, FeatureAdmin)


class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'image')
admin.site.register(Portfolio, PortfolioAdmin)


class PortfolioImageInline(admin.TabularInline):
    model = PortfolioImage
    extra = 1


@admin.register(Portfolio_details)
class PortDetAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'client', 'project_date')
    search_fields = ('title', 'category', 'client')
    inlines = [PortfolioImageInline]


@admin.register(PortfolioImage)
class PortfolioImageAdmin(admin.ModelAdmin):
    pass


class HeaderAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'line1', 'line2')
admin.site.register(Header, HeaderAdmin)


class HeroImageInline(admin.TabularInline):
    model = HeroImage
    extra = 1


class HeroAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [HeroImageInline]
admin.site.register(Hero, HeroAdmin)


class FooterAdmin(admin.ModelAdmin):
    list_display = ('address', 'phone', 'email', 'newsletter')
admin.site.register(Footer, FooterAdmin)


class SocialAdmin(admin.ModelAdmin):
    list_display = ('icon', 'link')
admin.site.register(Social, SocialAdmin)


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('email',)
admin.site.register(Subscribe, SubscribeAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'message')
admin.site.register(ContactModel, ContactAdmin)


class ServiceItemInline(admin.TabularInline):
    model = ServiceItem
    extra = 1


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('icon', 'service', 'icon_desc')
    inlines = [ServiceItemInline]
admin.site.register(ServiceModel, ServiceAdmin)


class ListItemInline(admin.TabularInline):
    model = ListItem
    extra = 1


class AboutAdmin(admin.ModelAdmin):
    list_display = ('image', 'tagline', 'para1', 'para2')
    inlines = [ListItemInline]
admin.site.register(AboutModel, AboutAdmin)


class ClientAdmin(admin.ModelAdmin):
    list_display = ('title', 'image')
admin.site.register(ClientModel, ClientAdmin)
