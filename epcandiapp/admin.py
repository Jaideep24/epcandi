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


@admin.register(AnalyticsUser)
class AnalyticsUserAdmin(admin.ModelAdmin):
	list_display = ("user_id", "device_type", "country", "last_seen")
	search_fields = ("user_id", "country", "city", "browser", "operating_system")
	readonly_fields = ("first_seen", "last_seen")
	list_filter = ("device_type", "country", "language", "first_seen")


@admin.register(AnalyticsSession)
class AnalyticsSessionAdmin(admin.ModelAdmin):
	list_display = ("session_id", "user", "source", "is_bounced", "start_time", "end_time")
	search_fields = ("session_id", "user__user_id", "entry_page", "exit_page", "utm_source", "utm_campaign")
	readonly_fields = ("start_time",)
	list_filter = ("is_bounced", "source", "utm_source", "utm_medium", "start_time")


@admin.register(AnalyticsEvent)
class AnalyticsEventAdmin(admin.ModelAdmin):
	list_display = ("event_type", "event_name", "session", "page_url", "timestamp")
	search_fields = ("event_type", "event_name", "page_url", "referrer", "session__session_id", "user__user_id")
	readonly_fields = ("timestamp",)
	list_filter = ("event_type", "timestamp")
