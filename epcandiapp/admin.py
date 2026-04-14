from django.contrib import admin
from .models import *
# Register your models here.

admin.site.site_header = "EPC & I Administration"
admin.site.site_title = "EPC & I Admin"
admin.site.index_title = "Dashboard"
admin.site.enable_nav_sidebar = True


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
	list_display = ("heading",)
	list_filter = ("updated_at",)
	search_fields = ("heading", "content")
	ordering = ("-updated_at",)
	readonly_fields = ("updated_at",)
	exclude = ("title", "is_published")
	list_per_page = 25

	def save_model(self, request, obj, form, change):
		# Keep data model compatibility while exposing only one label field in admin.
		obj.title = obj.heading
		obj.is_published = True
		super().save_model(request, obj, form, change)


@admin.register(AboutPage)
class AboutPageAdmin(PageContentAdmin):
	pass


@admin.register(DisclaimerPage)
class DisclaimerPageAdmin(PageContentAdmin):
	pass


@admin.register(PrivacyPage)
class PrivacyPageAdmin(PageContentAdmin):
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


@admin.register(RightAdvertisement)
class RightAdvertisementAdmin(admin.ModelAdmin):
	list_display = ("name",)
	list_filter = ("is_active",)
	search_fields = ("name", "link")


@admin.register(LeftAdvertisement)
class LeftAdvertisementAdmin(admin.ModelAdmin):
	list_display = ("name",)
	list_filter = ("is_active",)
	search_fields = ("name", "link")


@admin.register(BannerAdvertisement)
class BannerAdvertisementAdmin(admin.ModelAdmin):
	list_display = ("name",)
	list_filter = ("is_active",)
	search_fields = ("name", "link")


@admin.register(LatestIssue)
class LatestIssueAdmin(admin.ModelAdmin):
	list_display = ("title", "updated_at")
	search_fields = ("title",)
	readonly_fields = ("updated_at",)
	list_per_page = 25


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


