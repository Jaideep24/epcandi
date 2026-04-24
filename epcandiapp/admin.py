from django.contrib import admin
from django import forms
import re
from .models import *
# Register your models here.

admin.site.site_header = "EPC & I Administration"
admin.site.site_title = "EPC & I Admin"
admin.site.index_title = "Dashboard"
admin.site.enable_nav_sidebar = True


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
	list_display = ("heading", "published_on", "top_news")
	list_filter = ("top_news",)
	search_fields = ("heading", "news")
	ordering = ("-published_on", "-top_news", "-id")
	date_hierarchy = "published_on"
	list_per_page = 25
	fields = ("heading", "published_on", "top_news", "news")


class FocusAdminForm(forms.ModelForm):
	NEW_CATEGORY_VALUE = "__new__"

	category = forms.ChoiceField(required=False)
	new_category = forms.CharField(
		required=False,
		max_length=200,
		help_text='Pick "Create New Category" and enter a custom category name.',
	)

	class Meta:
		model = Focus
		fields = "__all__"

	class Media:
		js = ("epcandiapp/focus_admin_category.js",)

	@staticmethod
	def _sort_key(category_name):
		match = re.fullmatch(r"Category\s+(\d+)", category_name or "")
		if match:
			return (0, int(match.group(1)))
		return (1, (category_name or "").lower())

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		existing_categories = list(
			Focus.objects.exclude(category__isnull=True)
			.exclude(category__exact="")
			.values_list("category", flat=True)
			.distinct()
		)

		ordered_values = sorted(set(existing_categories), key=self._sort_key)

		instance_category = (getattr(self.instance, "category", "") or "").strip()
		if instance_category and instance_category not in ordered_values:
			ordered_values.append(instance_category)
			ordered_values = sorted(set(ordered_values), key=self._sort_key)

		choices = [("", "Select category")]
		choices.extend((value, value) for value in ordered_values)
		choices.append((self.NEW_CATEGORY_VALUE, "Create New Category"))
		self.fields["category"].choices = choices
		if instance_category and instance_category in ordered_values:
			self.fields["category"].initial = instance_category
		self.fields["new_category"].widget.attrs.update({"placeholder": "e.g. Category 3"})

	def clean(self):
		cleaned_data = super().clean()
		selected_category = (cleaned_data.get("category") or "").strip()
		new_category = (cleaned_data.get("new_category") or "").strip()

		if selected_category == self.NEW_CATEGORY_VALUE:
			if not new_category:
				self.add_error("new_category", "Please enter a new category name.")
			else:
				cleaned_data["category"] = new_category
		elif selected_category:
			cleaned_data["category"] = selected_category
		elif new_category:
			cleaned_data["category"] = new_category
		else:
			self.add_error("category", "Select a category or create a new one.")

		return cleaned_data


@admin.register(Focus)
class FocusAdmin(admin.ModelAdmin):
	form = FocusAdminForm
	fields = ("heading", "category", "new_category", "article")
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


