from django.contrib import admin
from .models import *
# Register your models here.

admin.site.site_header = "EPC & I Administration"
admin.site.site_title = "EPC & I Admin"
admin.site.index_title = "Dashboard"


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
	list_display = ("heading",)
	list_filter = ("top_news",)
	search_fields = ("heading", "news")
	ordering = ("-top_news", "-id")
	list_per_page = 25


@admin.register(Focus)
class FocusAdmin(admin.ModelAdmin):
	list_display = ("heading",)
	list_filter = ("category",)
	search_fields = ("heading", "article")
	ordering = ("-id",)
	list_per_page = 25


@admin.register(GuestArticle)
class GuestArticleAdmin(admin.ModelAdmin):
	list_display = ("heading",)
	search_fields = ("heading", "article")
	ordering = ("-id",)
	list_per_page = 25


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
	list_display = ("heading",)
	search_fields = ("heading", "interview")
	ordering = ("-id",)
	list_per_page = 25


@admin.register(EquipmentNews)
class EquipmentNewsAdmin(admin.ModelAdmin):
	list_display = ("heading",)
	search_fields = ("heading", "equipment_news")
	ordering = ("-id",)
	list_per_page = 25


@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
	list_display = ("name",)
	list_filter = ("start_date", "end_date")
	search_fields = ("name", "venue", "contact_details")
	ordering = ("-start_date",)
	list_per_page = 25


class PageContentAdmin(admin.ModelAdmin):
	list_display = ("title",)
	list_filter = ("is_published", "updated_at")
	search_fields = ("title", "heading", "content")
	ordering = ("-updated_at",)
	readonly_fields = ("updated_at",)
	list_per_page = 25


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


@admin.register(SquareFoot)
class SquareFootAdmin(admin.ModelAdmin):
	list_display = ("heading",)
	search_fields = ("heading", "square_foot")
	ordering = ("-id",)
	list_per_page = 25


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
	list_display = ("heading",)
	search_fields = ("heading", "shopping_cart")
	ordering = ("-id",)
	list_per_page = 25


@admin.register(AdvertisementBanner)
class AdvertisementBannerAdmin(admin.ModelAdmin):
	list_display = ("name",)
	list_filter = ("is_active",)
	search_fields = ("name", "link")


@admin.register(SubscribeForm)
class SubscribeFormAdmin(admin.ModelAdmin):
	list_display = ("name_display",)
	list_filter = ("subscription_type", "created_at")
	search_fields = ("email", "first_name", "last_name", "organisation")
	readonly_fields = ("created_at",)
	list_per_page = 30

	@admin.display(description="Name")
	def name_display(self, obj):
		return f"{obj.first_name} {obj.last_name}".strip() or "N/A"



@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
	list_display = ("name",)
	list_filter = ("query_type", "created_at")
	search_fields = ("email", "name", "organisation", "subject")
	readonly_fields = ("created_at",)
	list_per_page = 30
