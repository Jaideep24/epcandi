from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from .models import *
# Create your views here.


PAGE_SIZE_OPTIONS = [2, 10, 20, 50]


def _base_context():
    return {
        "advertisement_banners": AdvertisementBanner.objects.filter(is_active=True)
    }


def _safe_page_size(raw_value):
    try:
        size = int(raw_value)
    except (TypeError, ValueError):
        size = 20
    if size not in PAGE_SIZE_OPTIONS:
        size = 20
    return size


def _paginated_listing_context(request, queryset, title_field):
    page_size = _safe_page_size(request.GET.get("page_size"))
    query_text = request.GET.get("q", "").strip()

    if query_text:
        queryset = queryset.filter(**{f"{title_field}__icontains": query_text})

    paginator = Paginator(queryset, page_size)
    page_obj = paginator.get_page(request.GET.get("page"))

    return {
        "page_obj": page_obj,
        "page_size": page_size,
        "page_size_options": PAGE_SIZE_OPTIONS,
        "q": query_text,
    }


def _render_page_model(request, model_class):
    page = model_class.objects.filter(is_published=True).order_by("-updated_at", "-id").first()
    if page is None:
        page = model_class.objects.order_by("-updated_at", "-id").first()
    if page is None:
        context = {
            "page": {
                "title": "Page Not Configured",
                "heading": "CONTENT PENDING",
                "content": "Please add content for this page in the admin panel.",
            }
        }
    else:
        context = {"page": page}
    context.update(_base_context())
    return render(request, "epcandiapp/site_page.html", context)


def _render_detail_page(request, *, page_title, toolbar_title, detail_title, detail_body, back_url, back_label):
    context = {
        "detail_title": detail_title,
        "detail_body": detail_body,
        "back_url": back_url,
        "back_label": back_label,
        "toolbar_title": toolbar_title,
        "page_title": page_title,
        "detail_is_html": False,
    }
    context.update(_base_context())
    return render(request, "epcandiapp/detail_page.html", context)


def _render_error_page(request, *, status_code, page_title, heading, message):
    context = {
        "status_code": status_code,
        "page_title": page_title,
        "heading": heading,
        "message": message,
    }
    context.update(_base_context())
    return render(request, "epcandiapp/error_page.html", context, status=status_code)

def home_page(request):
    # Home should show the News listing page.
    return news_page(request)


def news_page(request):
    queryset = News.objects.order_by("-top_news", "-id")
    context = _paginated_listing_context(request, queryset, title_field="heading")
    context["News"] = context["page_obj"].object_list
    context.update(_base_context())
    return render(request, "epcandiapp/news.html", context)


def news_detail_page(request, news_id):
    item = get_object_or_404(News, id=news_id)
    return _render_detail_page(
        request,
        page_title=f"{item.heading} | EPC&I News",
        toolbar_title="NEWS",
        detail_title=item.heading,
        detail_body=item.news,
        back_url="news",
        back_label="Back to News",
    )


def focus_detail_page(request, focus_id):
    focus_item = get_object_or_404(Focus, id=focus_id)
    context = {"article": focus_item}
    context.update(_base_context())
    return render(request, "epcandiapp/article_detail.html", context)


def article_detail_page(request, article_id):
    # Backward-compatible alias for the old route name.
    return focus_detail_page(request, article_id)


def guest_article_detail_page(request, guest_article_id):
    article = get_object_or_404(GuestArticle, id=guest_article_id)
    context = {"article": article}
    context.update(_base_context())
    return render(request, "epcandiapp/article_detail.html", context)


def interview_detail_page(request, interview_id):
    item = get_object_or_404(Interview, id=interview_id)
    return _render_detail_page(
        request,
        page_title=f"{item.heading} | EPC&I Interviews",
        toolbar_title="INTERVIEWS",
        detail_title=item.heading,
        detail_body=item.interview,
        back_url="guest_article",
        back_label="Back to Interviews & Guest Article",
    )


def equipment_page(request):
    queryset = EquipmentNews.objects.order_by("-id")
    context = _paginated_listing_context(request, queryset, title_field="heading")
    context["equipment_items"] = context["page_obj"].object_list
    context.update(_base_context())
    return render(request, "epcandiapp/equipment_news.html", context)


def equipment_detail_page(request, equipment_id):
    item = get_object_or_404(EquipmentNews, id=equipment_id)
    return _render_detail_page(
        request,
        page_title=f"{item.heading} | EPC&I Equipment News",
        toolbar_title="EQUIPMENT NEWS",
        detail_title=item.heading,
        detail_body=item.equipment_news,
        back_url="equipment",
        back_label="Back to Equipment News",
    )


def events_page(request):
    queryset = Events.objects.all().order_by("-start_date", "-id")
    context = _paginated_listing_context(request, queryset, title_field="name")
    context["events"] = context["page_obj"].object_list
    context.update(_base_context())
    return render(request, "epcandiapp/events.html", context)


def event_detail_page(request, event_id):
    item = get_object_or_404(Events, id=event_id)
    detail_body = (
        f"<b>Dates:</b> {item.start_date:%d/%m/%Y} - {item.end_date:%d/%m/%Y}<br><br>"
        f"<b>Venue:</b> {item.venue}<br><br>"
        f"<b>Timing:</b> {item.timings}<br><br>"
        f"<b>Contact:</b> {item.contact_details}<br><br>"
        f"<b>Website:</b> {item.website}"
    )
    context = {
        "detail_title": item.name,
        "detail_body": detail_body,
        "detail_is_html": True,
        "back_url": "events",
        "back_label": "Back to Events",
        "toolbar_title": "EVENTS",
        "page_title": f"{item.name} | EPC&I Events",
    }
    context.update(_base_context())
    return render(request, "epcandiapp/detail_page.html", context)


def subscribe_page(request):
    if request.method == "POST":
        # Get form data
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        designation = request.POST.get("designation", "").strip()
        organisation = request.POST.get("organisation", "").strip()
        address = request.POST.get("address", "").strip()
        city = request.POST.get("city", "").strip()
        state = request.POST.get("state", "").strip()
        pincode = request.POST.get("pincode", "").strip()
        telephone = request.POST.get("telephone", "").strip()
        mobile = request.POST.get("mobile", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()
        subscription_type = request.POST.get("subscription_type", "0").strip()
        
        # Basic validation
        if not all([first_name, last_name, email, password]):
            context = {"errors": "Please fill in all required fields."}
        elif password != confirm_password:
            context = {"errors": "Passwords do not match."}
        else:
            try:
                # Save to database
                SubscribeForm.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    designation=designation,
                    organisation=organisation,
                    address=address,
                    city=city,
                    state=state,
                    pincode=pincode,
                    telephone=telephone,
                    mobile=mobile,
                    email=email,
                    password=password,
                    subscription_type=subscription_type
                )
                context = {"message": "Thank you! Your registration has been submitted. We will get back to you soon."}
            except Exception as e:
                context = {"errors": f"An error occurred: {str(e)}"}
        context.update(_base_context())
        return render(request, "epcandiapp/subscribe.html", context)
    else:
        context = {}
        context.update(_base_context())
        return render(request, "epcandiapp/subscribe.html", context)


def contact_page(request):
    selected_query_type = request.GET.get("query_type", "Feedback / Suggestions").strip() or "Feedback / Suggestions"
    if request.method == "POST":
        # Get form data
        query_type = request.POST.get("query_type", selected_query_type).strip()
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        organisation = request.POST.get("organisation", "").strip()
        subject = request.POST.get("subject", "").strip()
        message_text = request.POST.get("message", "").strip()
        
        # Basic validation
        if not all([name, email, subject, message_text]):
            context = {"errors": "Please fill in all required fields."}
        else:
            try:
                # Save to database
                ContactForm.objects.create(
                    query_type=query_type,
                    name=name,
                    email=email,
                    organisation=organisation,
                    subject=subject,
                    message=message_text
                )
                context = {"message": "Thank you! Your message has been received. We will get back to you soon."}
            except Exception as e:
                context = {"errors": f"An error occurred: {str(e)}"}
        context.update(_base_context())
        return render(request, "epcandiapp/contact.html", context)
    else:
        context = {"selected_query_type": selected_query_type}
        context.update(_base_context())
        return render(request, "epcandiapp/contact.html", context)


def about_page(request):
    return _render_page_model(request, AboutPage)


def disclaimer_page(request):
    return _render_page_model(request, DisclaimerPage)


def privacy_page(request):
    return _render_page_model(request, PrivacyPage)


def focus_page(request):
    queryset = Focus.objects.order_by("-id")
    context = _paginated_listing_context(request, queryset, title_field="heading")
    context["focus_items"] = context["page_obj"].object_list
    context.update(_base_context())
    return render(request, "epcandiapp/focus.html", context)


def shopping_cart_page(request):
    return _render_page_model(request, ShoppingCartPage)


def guest_article_page(request):
    page_size = _safe_page_size(request.GET.get("page_size"))
    query_text = request.GET.get("q", "").strip()
    section = request.GET.get("section", "interviews").strip().lower()
    if section not in {"interviews", "guest-articles"}:
        section = "interviews"

    interviews_queryset = Interview.objects.order_by("-id")
    guest_articles_queryset = GuestArticle.objects.order_by("-id")

    if query_text:
        interviews_queryset = interviews_queryset.filter(heading__icontains=query_text)
        guest_articles_queryset = guest_articles_queryset.filter(heading__icontains=query_text)

    if section == "guest-articles":
        page_obj = Paginator(guest_articles_queryset, page_size).get_page(request.GET.get("page"))
    else:
        page_obj = Paginator(interviews_queryset, page_size).get_page(request.GET.get("page"))

    context = {
        "section": section,
        "items": page_obj.object_list,
        "page_obj": page_obj,
        "page_size": page_size,
        "page_size_options": PAGE_SIZE_OPTIONS,
        "q": query_text,
    }
    context.update(_base_context())
    return render(request, "epcandiapp/guest_article.html", context)


def square_foot_page(request):
    context = {
        "page": {
            "title": "Square Foot",
            "heading": "SQUARE FOOT",
            "content": "Square Foot content will be added soon.",
        }
    }
    context.update(_base_context())
    return render(request, "epcandiapp/site_page.html", context)


def bad_request_page(request, exception):
    return _render_error_page(
        request,
        status_code=400,
        page_title="Bad Request | EPC&I",
        heading="BAD REQUEST",
        message="The request could not be understood. Please try again.",
    )


def permission_denied_page(request, exception):
    return _render_error_page(
        request,
        status_code=403,
        page_title="Permission Denied | EPC&I",
        heading="PERMISSION DENIED",
        message="You do not have permission to access this page.",
    )


def page_not_found_page(request, exception):
    return _render_error_page(
        request,
        status_code=404,
        page_title="Page Not Found | EPC&I",
        heading="PAGE NOT FOUND",
        message="The page you are looking for does not exist or has been moved.",
    )


def server_error_page(request):
    return _render_error_page(
        request,
        status_code=500,
        page_title="Server Error | EPC&I",
        heading="SERVER ERROR",
        message="Something went wrong on our side. Please try again later.",
    )