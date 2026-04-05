from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(News)
admin.site.register(Articles)
admin.site.register(Equipment_News)
admin.site.register(Events)
admin.site.register(Interview)


@admin.register(AdvertisementBanner)
class AdvertisementBannerAdmin(admin.ModelAdmin):
	list_display = ("name", "link", "display_order", "is_active", "created_at")
	list_filter = ("is_active",)
	search_fields = ("name", "link")


@admin.register(SubscribeForm)
class SubscribeFormAdmin(admin.ModelAdmin):
	list_display = ("first_name", "last_name", "email", "mobile", "subscription_type", "created_at")
	list_filter = ("subscription_type", "created_at")
	search_fields = ("email", "first_name", "last_name", "organisation")
	readonly_fields = ("created_at",)


@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
	list_display = ("name", "email", "query_type", "subject", "created_at")
	list_filter = ("query_type", "created_at")
	search_fields = ("email", "name", "organisation", "subject")
	readonly_fields = ("created_at",)