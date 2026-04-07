from django.contrib import admin
from .models import *
# Register your models here.

admin.site.site_header = "EPC & I Administration"
admin.site.site_title = "EPC & I Admin"
admin.site.index_title = "Content Management"


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
	list_display = ("heading", "category", "top_news")
	list_filter = ("category", "top_news")
	search_fields = ("heading", "news")
	ordering = ("-top_news", "-id")


@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):
	list_display = ("heading",)
	search_fields = ("heading", "article")
	ordering = ("-id",)


@admin.register(GuestArticle)
class GuestArticleAdmin(admin.ModelAdmin):
	list_display = ("heading",)
	search_fields = ("heading", "article")
	ordering = ("-id",)


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
	list_display = ("heading",)
	search_fields = ("heading", "Interview")
	ordering = ("-id",)


@admin.register(Equipment_News)
class EquipmentNewsAdmin(admin.ModelAdmin):
	list_display = ("heading",)
	search_fields = ("heading", "equipment_news")
	ordering = ("-id",)


@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
	list_display = ("name", "start_date", "end_date", "venue")
	list_filter = ("start_date", "end_date")
	search_fields = ("name", "venue", "contact_details")
	ordering = ("-start_date",)


class PageContentAdmin(admin.ModelAdmin):
	list_display = ("title", "heading", "is_published", "updated_at")
	list_filter = ("is_published", "updated_at")
	search_fields = ("title", "heading", "content")
	ordering = ("-updated_at",)


@admin.register(AboutPage)
class AboutPageAdmin(PageContentAdmin):
	pass


@admin.register(DisclaimerPage)
class DisclaimerPageAdmin(PageContentAdmin):
	pass


@admin.register(PrivacyPage)
class PrivacyPageAdmin(PageContentAdmin):
	pass


@admin.register(ShoppingCartPage)
class ShoppingCartPageAdmin(PageContentAdmin):
	pass


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