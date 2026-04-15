from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.http import JsonResponse
from django.core.cache import cache
from django.db.models import Avg
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import admin
from django.utils import timezone
from datetime import timedelta
from urllib.parse import urlparse
import hashlib
import json
from .models import *
# Create your views here.


PAGE_SIZE_OPTIONS = [2, 10, 20, 50]
ANALYTICS_WINDOW_OPTIONS = [7, 14, 30, 90]
TRACK_RATE_LIMIT_PER_MINUTE = 240
ALLOWED_TRACK_EVENT_TYPES = {
    "page_view",
    "link_click",
    "button_click",
    "form_submit",
    "scroll_depth",
    "scroll_percentage",
    "performance",
    "session_end",
    "session_heartbeat",
    "video_play",
    "download_click",
    "custom_event",
    "conversion",
}

SENSITIVE_METADATA_KEYS = {
    "password",
    "pass",
    "passwd",
    "pwd",
    "secret",
    "token",
    "access_token",
    "refresh_token",
    "authorization",
    "auth",
    "cookie",
    "set-cookie",
    "csrf",
    "session",
    "email",
    "phone",
    "mobile",
    "otp",
    "credit_card",
    "card_number",
    "cvv",
}

MAX_METADATA_STRING_LENGTH = 300


def _base_context():
    return {
        "right_advertisements": RightAdvertisement.objects.filter(is_active=True),
        "left_advertisements": LeftAdvertisement.objects.filter(is_active=True),
        "banner_advertisement": BannerAdvertisement.objects.filter(is_active=True).order_by("display_order", "id").first(),
        "latest_issue": LatestIssue.objects.order_by("-updated_at", "-id").first(),
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


def _render_detail_page(request, *, page_title, toolbar_title, detail_title, detail_body, back_url, back_label, detail_date=None):
    context = {
        "detail_title": detail_title,
        "detail_body": detail_body,
        "back_url": back_url,
        "back_label": back_label,
        "toolbar_title": toolbar_title,
        "page_title": page_title,
        "detail_is_html": False,
        "detail_date": detail_date,
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
    top_news_only = request.GET.get("top_news") == "on"
    if top_news_only:
        queryset = News.objects.filter(top_news=True).order_by("-published_on", "-id")
        query_text = request.GET.get("q", "").strip()
        if query_text:
            queryset = queryset.filter(heading__icontains=query_text)
        context = {
            "News": queryset,
            "page_obj": None,
            "page_size": _safe_page_size(request.GET.get("page_size")),
            "page_size_options": PAGE_SIZE_OPTIONS,
            "q": query_text,
        }
    else:
        queryset = News.objects.order_by("-published_on", "-id")
        context = _paginated_listing_context(request, queryset, title_field="heading")
        context["News"] = context["page_obj"].object_list

    context["top_news_only"] = top_news_only
    context["show_top_news_filter"] = True
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
        detail_date=item.published_on,
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
    if item.banner:
        media_html = (
            '<div class="event-detail-media-box">'
            f'<img src="{item.banner.url}" alt="{item.name} banner" class="list-event-image">'
            "</div>"
        )
    else:
        media_html = '<div class="event-detail-media-box event-detail-media-empty">No banner available</div>'

    detail_body = (
        '<div class="event-detail-split">'
        f'<div class="event-detail-media">{media_html}</div>'
        '<div class="event-detail-content">'
        f"<p><b>Dates:</b> {item.start_date:%d/%m/%Y} - {item.end_date:%d/%m/%Y}</p>"
        f"<p><b>Venue:</b> {item.venue}</p>"
        f"<p><b>Timing:</b> {item.timings}</p>"
        f"<p><b>Contact:</b> {item.contact_details}</p>"
        f'<p><b>Website:</b> <a href="{item.website}" target="_blank" rel="noopener noreferrer">{item.website}</a></p>'
        "</div>"
        "</div>"
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


def _anonymize_ip(ip_address):
    if not ip_address:
        return ""
    return hashlib.sha256(ip_address.encode("utf-8")).hexdigest()[:16]


def _safe_int(value, default=None):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _safe_float(value, default=None):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _sanitize_metadata(value, depth=0):
    if depth > 4:
        return "[truncated]"

    if isinstance(value, dict):
        clean = {}
        for key, val in value.items():
            key_str = str(key)[:80]
            if key_str.lower() in SENSITIVE_METADATA_KEYS:
                clean[key_str] = "[redacted]"
                continue
            clean[key_str] = _sanitize_metadata(val, depth + 1)
        return clean

    if isinstance(value, list):
        return [_sanitize_metadata(item, depth + 1) for item in value[:50]]

    if isinstance(value, (str, bytes)):
        as_text = value.decode("utf-8", errors="ignore") if isinstance(value, bytes) else value
        return as_text[:MAX_METADATA_STRING_LENGTH]

    if isinstance(value, (int, float, bool)) or value is None:
        return value

    return str(value)[:MAX_METADATA_STRING_LENGTH]


def _analytics_filter_options(window_start):
    devices = list(
        AnalyticsUser.objects.filter(last_seen__date__gte=window_start)
        .exclude(device_type="")
        .values_list("device_type", flat=True)
        .distinct()
    )
    sources = list(
        AnalyticsSession.objects.filter(start_time__date__gte=window_start)
        .exclude(source="")
        .values_list("source", flat=True)
        .distinct()
    )
    countries = list(
        AnalyticsUser.objects.filter(last_seen__date__gte=window_start)
        .exclude(country="")
        .values_list("country", flat=True)
        .distinct()
    )
    browsers = list(
        AnalyticsUser.objects.filter(last_seen__date__gte=window_start)
        .exclude(browser="")
        .values_list("browser", flat=True)
        .distinct()
    )
    operating_systems = list(
        AnalyticsUser.objects.filter(last_seen__date__gte=window_start)
        .exclude(operating_system="")
        .values_list("operating_system", flat=True)
        .distinct()
    )
    event_types = list(
        AnalyticsEvent.objects.filter(timestamp__date__gte=window_start)
        .exclude(event_type="")
        .values_list("event_type", flat=True)
        .distinct()
    )
    return {
        "devices": sorted(devices),
        "sources": sorted(sources),
        "countries": sorted(countries),
        "browsers": sorted(browsers),
        "operating_systems": sorted(operating_systems),
        "event_types": sorted(event_types),
    }


def _analytics_request_filters(request):
    today = timezone.localdate()
    days = _safe_int(request.GET.get("days"), 30)
    if days not in ANALYTICS_WINDOW_OPTIONS:
        days = 30

    window_start = today - timedelta(days=days - 1)
    return {
        "today": today,
        "days": days,
        "window_start": window_start,
        "device": (request.GET.get("device") or "").strip()[:20],
        "source": (request.GET.get("source") or "").strip()[:120],
        "country": (request.GET.get("country") or "").strip()[:100],
        "browser": (request.GET.get("browser") or "").strip()[:100],
        "operating_system": (request.GET.get("operating_system") or "").strip()[:100],
        "event_type": (request.GET.get("event_type") or "").strip()[:80],
        "q": (request.GET.get("q") or "").strip()[:120],
    }


def _build_analytics_scopes(filters):
    users_qs = AnalyticsUser.objects.filter(last_seen__date__gte=filters["window_start"])
    sessions_qs = AnalyticsSession.objects.filter(start_time__date__gte=filters["window_start"])
    events_qs = AnalyticsEvent.objects.filter(timestamp__date__gte=filters["window_start"])

    if filters["device"]:
        users_qs = users_qs.filter(device_type=filters["device"])
        sessions_qs = sessions_qs.filter(user__device_type=filters["device"])
        events_qs = events_qs.filter(user__device_type=filters["device"])
    if filters["source"]:
        sessions_qs = sessions_qs.filter(source=filters["source"])
        events_qs = events_qs.filter(session__source=filters["source"])
    if filters["country"]:
        users_qs = users_qs.filter(country=filters["country"])
        sessions_qs = sessions_qs.filter(user__country=filters["country"])
        events_qs = events_qs.filter(user__country=filters["country"])
    if filters["browser"]:
        users_qs = users_qs.filter(browser=filters["browser"])
        sessions_qs = sessions_qs.filter(user__browser=filters["browser"])
        events_qs = events_qs.filter(user__browser=filters["browser"])
    if filters["operating_system"]:
        users_qs = users_qs.filter(operating_system=filters["operating_system"])
        sessions_qs = sessions_qs.filter(user__operating_system=filters["operating_system"])
        events_qs = events_qs.filter(user__operating_system=filters["operating_system"])
    if filters["event_type"]:
        events_qs = events_qs.filter(event_type=filters["event_type"])
        sessions_qs = sessions_qs.filter(events__event_type=filters["event_type"]).distinct()
        users_qs = users_qs.filter(events__event_type=filters["event_type"]).distinct()
    if filters["q"]:
        q = filters["q"]
        users_qs = users_qs.filter(user_id__icontains=q)
        sessions_qs = sessions_qs.filter(session_id__icontains=q)
        events_qs = events_qs.filter(page_url__icontains=q)

    return users_qs, sessions_qs, events_qs


def _detect_source(referrer):
    if not referrer:
        return "direct"
    host = (urlparse(referrer).netloc or "").lower()
    if "google" in host:
        return "google"
    if "linkedin" in host:
        return "linkedin"
    if "facebook" in host:
        return "facebook"
    if "instagram" in host:
        return "instagram"
    if "twitter" in host or "x.com" in host:
        return "x"
    return host or "referral"


def _derive_client_context(request):
    ua = request.META.get("HTTP_USER_AGENT", "")
    ua_lower = ua.lower()

    browser = "Other"
    if "edg/" in ua_lower:
        browser = "Edge"
    elif "chrome/" in ua_lower:
        browser = "Chrome"
    elif "firefox/" in ua_lower:
        browser = "Firefox"
    elif "safari/" in ua_lower:
        browser = "Safari"

    operating_system = "Other"
    if "windows" in ua_lower:
        operating_system = "Windows"
    elif "mac os" in ua_lower or "macintosh" in ua_lower:
        operating_system = "macOS"
    elif "linux" in ua_lower:
        operating_system = "Linux"
    elif "android" in ua_lower:
        operating_system = "Android"
    elif "iphone" in ua_lower or "ipad" in ua_lower:
        operating_system = "iOS"

    device_type = "desktop"
    if any(token in ua_lower for token in ["mobile", "iphone", "android"]):
        device_type = "mobile"
    elif "ipad" in ua_lower or "tablet" in ua_lower:
        device_type = "tablet"

    country = (
        request.META.get("HTTP_CF_IPCOUNTRY")
        or request.META.get("HTTP_X_COUNTRY")
        or request.META.get("HTTP_X_COUNTRY_CODE")
        or ""
    )[:100]
    city = (request.META.get("HTTP_X_CITY") or "")[:100]

    return {
        "browser": browser,
        "operating_system": operating_system,
        "device_type": device_type,
        "language": (request.META.get("HTTP_ACCEPT_LANGUAGE", "").split(",")[0] or "")[:32],
        "country": country,
        "city": city,
    }


def _calculate_tracker_kpis(filters, users_qs, sessions_qs, events_qs):
    now = timezone.now()
    active_threshold = now - timedelta(minutes=30)
    realtime_threshold = now - timedelta(minutes=5)

    total_users = users_qs.count()
    active_users = users_qs.filter(last_seen__gte=active_threshold).count()
    sessions_count = sessions_qs.count()
    page_views_count = events_qs.filter(event_type="page_view").count()
    active_sessions_5m = events_qs.filter(timestamp__gte=realtime_threshold).values("session_id").distinct().count()

    bounced_sessions = sessions_qs.filter(is_bounced=True).count()
    bounce_rate = round((bounced_sessions / sessions_count) * 100, 2) if sessions_count else 0

    avg_session_seconds = 0
    closed_sessions = sessions_qs.filter(end_time__isnull=False)
    if closed_sessions.exists():
        total_seconds = 0
        for session in closed_sessions:
            total_seconds += max((session.end_time - session.start_time).total_seconds(), 0)
        avg_session_seconds = int(total_seconds / closed_sessions.count()) if closed_sessions.count() else 0

    new_users = users_qs.filter(first_seen__date__gte=filters["window_start"]).count()
    returning_users = max(total_users - new_users, 0)

    return {
        "window_start": filters["window_start"],
        "total_users": total_users,
        "active_users": active_users,
        "sessions_count": sessions_count,
        "page_views_count": page_views_count,
        "active_sessions_5m": active_sessions_5m,
        "bounce_rate": bounce_rate,
        "avg_session_seconds": avg_session_seconds,
        "new_users": new_users,
        "returning_users": returning_users,
    }


def _top_pages(events_qs, limit=8):
    rows = (
        events_qs.filter(event_type="page_view")
        .values("page_url")
        .annotate(total=Count("id"))
        .order_by("-total")[:limit]
    )
    return [
        {
            "page_url": row["page_url"] or "(unknown)",
            "total": row["total"],
        }
        for row in rows
    ]


def _device_breakdown(users_qs):
    rows = (
        users_qs
        .values("device_type")
        .annotate(total=Count("id"))
        .order_by("-total")
    )
    total = sum(row["total"] for row in rows) or 1
    data = []
    for row in rows:
        label = row["device_type"] or "unknown"
        percent = round((row["total"] / total) * 100, 2)
        data.append({"label": label, "total": row["total"], "percent": percent})
    return data


def _source_breakdown(sessions_qs):
    rows = (
        sessions_qs
        .values("source")
        .annotate(total=Count("id"))
        .order_by("-total")
    )
    total = sum(row["total"] for row in rows) or 1
    data = []
    for row in rows:
        label = row["source"] or "direct"
        percent = round((row["total"] / total) * 100, 2)
        data.append({"label": label, "total": row["total"], "percent": percent})
    return data


def _country_breakdown(users_qs):
    rows = users_qs.values("country").annotate(total=Count("id")).order_by("-total")
    total = sum(row["total"] for row in rows) or 1
    data = []
    for row in rows:
        label = row["country"] or "unknown"
        percent = round((row["total"] / total) * 100, 2)
        data.append({"label": label, "total": row["total"], "percent": percent})
    return data


def _top_events(events_qs, limit=10):
    rows = (
        events_qs.exclude(event_type="page_view")
        .values("event_type", "event_name")
        .annotate(total=Count("id"))
        .order_by("-total")[:limit]
    )
    data = []
    for row in rows:
        label = row["event_name"] or row["event_type"]
        data.append({"label": label, "event_type": row["event_type"], "total": row["total"]})
    return data


def _conversion_metrics(events_qs):
    signup_success = events_qs.filter(event_type="conversion", event_name="signup_success").count()
    login_success = events_qs.filter(event_type="conversion", event_name="login_success").count()
    purchase_completed = events_qs.filter(event_type="conversion", event_name="purchase_completed").count()
    add_to_cart = events_qs.filter(event_type="conversion", event_name="add_to_cart").count()
    lead_generated = events_qs.filter(event_type="conversion", event_name="lead_generated").count()

    # Form submissions are treated as leads in this site context.
    if lead_generated == 0:
        lead_generated = events_qs.filter(event_type="form_submit").count()

    return [
        {"label": "Signup Success", "value": signup_success},
        {"label": "Login Success", "value": login_success},
        {"label": "Purchase Completed", "value": purchase_completed},
        {"label": "Add To Cart", "value": add_to_cart},
        {"label": "Leads Generated", "value": lead_generated},
    ]


def _performance_metrics(events_qs):
    perf_qs = events_qs.filter(event_type="performance")
    avg_values = perf_qs.aggregate(
        avg_load=Avg("duration_ms"),
        avg_ttfb=Avg("ttfb_ms"),
        avg_lcp=Avg("lcp_ms"),
        avg_fid=Avg("fid_ms"),
        avg_cls=Avg("cls"),
    )

    def _clean_num(value, digits=0):
        if value is None:
            return 0
        return round(value, digits)

    return [
        {"label": "Avg Load (ms)", "value": _clean_num(avg_values.get("avg_load"))},
        {"label": "Avg TTFB (ms)", "value": _clean_num(avg_values.get("avg_ttfb"))},
        {"label": "Avg LCP (ms)", "value": _clean_num(avg_values.get("avg_lcp"))},
        {"label": "Avg FID (ms)", "value": _clean_num(avg_values.get("avg_fid"))},
        {"label": "Avg CLS", "value": _clean_num(avg_values.get("avg_cls"), 3)},
    ]


def _top_navigation_paths(events_qs, limit=10):
    rows = events_qs.filter(event_type="page_view").values("session_id", "page_url", "timestamp").order_by("session_id", "timestamp")

    transitions = {}
    last_by_session = {}
    for row in rows:
        sid = row["session_id"]
        page = row["page_url"] or "(unknown)"
        prev = last_by_session.get(sid)
        if prev and prev != page:
            key = f"{prev} -> {page}"
            transitions[key] = transitions.get(key, 0) + 1
        last_by_session[sid] = page

    sorted_transitions = sorted(transitions.items(), key=lambda item: item[1], reverse=True)[:limit]
    return [{"path": key, "total": total} for key, total in sorted_transitions]


def _daily_page_view_series(events_qs, window_start, today, days=14):
    series_start = today - timedelta(days=days - 1)
    if series_start < window_start:
        series_start = window_start

    rows = (
        events_qs.filter(event_type="page_view", timestamp__date__gte=series_start)
        .annotate(day=TruncDate("timestamp"))
        .values("day")
        .annotate(total=Count("id"))
        .order_by("day")
    )
    counts_map = {row["day"]: row["total"] for row in rows}

    data = []
    cursor = series_start
    while cursor <= today:
        data.append(
            {
                "date": cursor,
                "label": cursor.strftime("%d %b"),
                "total": counts_map.get(cursor, 0),
            }
        )
        cursor += timedelta(days=1)

    max_total = max((item["total"] for item in data), default=1)
    for item in data:
        item["percent"] = int((item["total"] / max_total) * 100) if max_total else 0

    return data


@csrf_exempt
@require_http_methods(["POST"])
def track_event_api(request):
    rate_ip = request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")[0].strip() or request.META.get("REMOTE_ADDR", "") or "anon"
    rate_key = f"track_rate:{rate_ip}"
    current_hits = cache.get(rate_key, 0)
    if current_hits >= TRACK_RATE_LIMIT_PER_MINUTE:
        return JsonResponse({"ok": False, "error": "Rate limit exceeded."}, status=429)
    cache.set(rate_key, current_hits + 1, timeout=60)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"ok": False, "error": "Invalid JSON payload."}, status=400)

    user_id = (payload.get("user_id") or "").strip()[:64]
    session_id = (payload.get("session_id") or "").strip()[:64]
    event_type = (payload.get("event_type") or "").strip()[:80]

    if not user_id or not session_id or not event_type:
        return JsonResponse({"ok": False, "error": "user_id, session_id and event_type are required."}, status=400)
    if event_type not in ALLOWED_TRACK_EVENT_TYPES:
        return JsonResponse({"ok": False, "error": "Unsupported event_type."}, status=400)

    ip_source = rate_ip
    anonymized_ip = _anonymize_ip(ip_source)
    derived = _derive_client_context(request)

    analytics_user, _ = AnalyticsUser.objects.get_or_create(
        user_id=user_id,
        defaults={
            "anonymized_ip": anonymized_ip,
            "country": ((payload.get("country") or derived["country"]) or "")[:100],
            "city": ((payload.get("city") or derived["city"]) or "")[:100],
            "device_type": ((payload.get("device_type") or derived["device_type"]) or "")[:20],
            "browser": ((payload.get("browser") or derived["browser"]) or "")[:100],
            "operating_system": ((payload.get("operating_system") or derived["operating_system"]) or "")[:100],
            "language": ((payload.get("language") or derived["language"]) or "")[:32],
        },
    )

    analytics_user.anonymized_ip = anonymized_ip
    analytics_user.country = (payload.get("country") or derived["country"] or analytics_user.country or "")[:100]
    analytics_user.city = (payload.get("city") or derived["city"] or analytics_user.city or "")[:100]
    analytics_user.device_type = (payload.get("device_type") or derived["device_type"] or analytics_user.device_type or "")[:20]
    analytics_user.browser = (payload.get("browser") or derived["browser"] or analytics_user.browser or "")[:100]
    analytics_user.operating_system = (payload.get("operating_system") or derived["operating_system"] or analytics_user.operating_system or "")[:100]
    analytics_user.language = (payload.get("language") or derived["language"] or analytics_user.language or "")[:32]
    analytics_user.save()

    referrer = (payload.get("referrer") or request.META.get("HTTP_REFERER") or "")[:400]
    page_url = (payload.get("page_url") or request.path or "")[:400]
    source = ((payload.get("source") or "").strip() or _detect_source(referrer))[:120]

    session_defaults = {
        "entry_page": page_url,
        "referrer": referrer,
        "source": source,
        "utm_source": (payload.get("utm_source") or "")[:120],
        "utm_medium": (payload.get("utm_medium") or "")[:120],
        "utm_campaign": (payload.get("utm_campaign") or "")[:120],
    }
    analytics_session, created = AnalyticsSession.objects.get_or_create(
        session_id=session_id,
        defaults={"user": analytics_user, **session_defaults},
    )

    if not created:
        changed = False
        if analytics_session.user_id != analytics_user.id:
            analytics_session.user = analytics_user
            changed = True
        if source and not analytics_session.source:
            analytics_session.source = source
            changed = True
        if page_url and not analytics_session.entry_page:
            analytics_session.entry_page = page_url
            changed = True
        if referrer and not analytics_session.referrer:
            analytics_session.referrer = referrer
            changed = True
        if event_type == "session_end":
            analytics_session.exit_page = page_url[:400]
            analytics_session.end_time = timezone.now()
            changed = True
        if event_type != "page_view":
            analytics_session.is_bounced = False
            changed = True
        if changed:
            analytics_session.save()

    if created and event_type != "page_view":
        analytics_session.is_bounced = False
        analytics_session.save(update_fields=["is_bounced"])

    metadata = payload.get("metadata")
    if metadata is None:
        metadata = {}
    if not isinstance(metadata, dict):
        metadata = {"value": str(metadata)}
    metadata = _sanitize_metadata(metadata)
    metadata_json = json.dumps(metadata, separators=(",", ":"))
    if len(metadata_json) > 5000:
        metadata_json = metadata_json[:5000]

    AnalyticsEvent.objects.create(
        event_type=event_type,
        user=analytics_user,
        session=analytics_session,
        page_url=page_url,
        referrer=referrer,
        event_name=(payload.get("event_name") or "")[:120],
        metadata_json=metadata_json,
        duration_ms=_safe_int(payload.get("duration_ms")),
        scroll_depth=_safe_int(payload.get("scroll_depth")),
        ttfb_ms=_safe_int(payload.get("ttfb_ms")),
        lcp_ms=_safe_int(payload.get("lcp_ms")),
        fid_ms=_safe_int(payload.get("fid_ms")),
        cls=_safe_float(payload.get("cls")),
    )

    return JsonResponse({"ok": True})


@require_http_methods(["GET"])
@staff_member_required(login_url="/admin/login/")
def analytics_data_api(request):
    filters = _analytics_request_filters(request)
    users_qs, sessions_qs, events_qs = _build_analytics_scopes(filters)
    kpis = _calculate_tracker_kpis(filters, users_qs, sessions_qs, events_qs)
    payload = {
        "window_start": kpis["window_start"].isoformat(),
        "today": filters["today"].isoformat(),
        "filters": {
            "days": filters["days"],
            "device": filters["device"],
            "source": filters["source"],
            "country": filters["country"],
            "browser": filters["browser"],
            "operating_system": filters["operating_system"],
            "event_type": filters["event_type"],
            "q": filters["q"],
        },
        "metrics": {
            "total_users": kpis["total_users"],
            "active_users": kpis["active_users"],
            "active_sessions_5m": kpis["active_sessions_5m"],
            "sessions": kpis["sessions_count"],
            "page_views": kpis["page_views_count"],
            "bounce_rate": kpis["bounce_rate"],
            "avg_session_seconds": kpis["avg_session_seconds"],
            "new_users": kpis["new_users"],
            "returning_users": kpis["returning_users"],
        },
        "top_pages": _top_pages(events_qs),
        "top_events": _top_events(events_qs),
        "device_breakdown": _device_breakdown(users_qs),
        "source_breakdown": _source_breakdown(sessions_qs),
        "country_breakdown": _country_breakdown(users_qs),
        "conversion_metrics": _conversion_metrics(events_qs),
        "performance_metrics": _performance_metrics(events_qs),
        "top_navigation_paths": _top_navigation_paths(events_qs),
        "timeline_page_views": _daily_page_view_series(events_qs, kpis["window_start"], filters["today"]),
    }
    return JsonResponse(payload)


@staff_member_required(login_url="/admin/login/")
def analytics_page(request):
    # Dashboard is intentionally restricted to admin/staff users.

    filters = _analytics_request_filters(request)
    users_qs, sessions_qs, events_qs = _build_analytics_scopes(filters)
    kpis = _calculate_tracker_kpis(filters, users_qs, sessions_qs, events_qs)
    today = filters["today"]
    window_start = kpis["window_start"]

    content_cards = [
        {"label": "News", "value": News.objects.count()},
        {"label": "Focus", "value": Focus.objects.count()},
        {"label": "Equipment News", "value": EquipmentNews.objects.count()},
        {"label": "Guest Articles", "value": GuestArticle.objects.count()},
        {"label": "Interviews", "value": Interview.objects.count()},
        {"label": "Events", "value": Events.objects.count()},
    ]

    engagement_cards = [
        {"label": "Subscribe Forms", "value": SubscribeForm.objects.count()},
        {"label": "Contact Forms", "value": ContactForm.objects.count()},
        {"label": "Right Ads", "value": RightAdvertisement.objects.filter(is_active=True).count()},
        {"label": "Left Ads", "value": LeftAdvertisement.objects.filter(is_active=True).count()},
        {"label": "Published Pages", "value": AboutPage.objects.filter(is_published=True).count() + DisclaimerPage.objects.filter(is_published=True).count() + PrivacyPage.objects.filter(is_published=True).count()},
    ]

    recent_cards = [
        {"label": f"Subscriptions (Last {filters['days']} Days)", "value": SubscribeForm.objects.filter(created_at__date__gte=window_start).count()},
        {"label": f"Contacts (Last {filters['days']} Days)", "value": ContactForm.objects.filter(created_at__date__gte=window_start).count()},
        {"label": "Upcoming/Ongoing Events", "value": Events.objects.filter(end_date__gte=today).count()},
    ]

    traffic_cards = [
        {"label": "Total Users", "value": kpis["total_users"]},
        {"label": "Active Users (30m)", "value": kpis["active_users"]},
        {"label": "Active Sessions (5m)", "value": kpis["active_sessions_5m"]},
        {"label": f"Sessions ({filters['days']} Days)", "value": kpis["sessions_count"]},
        {"label": f"Page Views ({filters['days']} Days)", "value": kpis["page_views_count"]},
        {"label": "Bounce Rate %", "value": kpis["bounce_rate"]},
        {"label": "Avg Session (Sec)", "value": kpis["avg_session_seconds"]},
        {"label": "New Users", "value": kpis["new_users"]},
        {"label": "Returning Users", "value": kpis["returning_users"]},
    ]

    category_map = dict(SECTOR_CHOICES)
    focus_by_sector = []
    for row in Focus.objects.values("category").annotate(total=Count("id")).order_by("-total"):
        focus_by_sector.append(
            {
                "name": category_map.get(row["category"], row["category"]),
                "total": row["total"],
            }
        )

    max_focus_total = max((item["total"] for item in focus_by_sector), default=1)
    for item in focus_by_sector:
        item["percent"] = int((item["total"] / max_focus_total) * 100) if max_focus_total else 0

    recent_subscriptions = SubscribeForm.objects.order_by("-created_at")[:8]
    recent_contacts = ContactForm.objects.order_by("-created_at")[:8]
    upcoming_events = Events.objects.filter(end_date__gte=today).order_by("start_date")[:8]
    top_pages = _top_pages(events_qs)
    top_events = _top_events(events_qs)
    device_breakdown = _device_breakdown(users_qs)
    source_breakdown = _source_breakdown(sessions_qs)
    country_breakdown = _country_breakdown(users_qs)
    conversion_metrics = _conversion_metrics(events_qs)
    performance_metrics = _performance_metrics(events_qs)
    top_navigation_paths = _top_navigation_paths(events_qs)
    timeline_page_views = _daily_page_view_series(events_qs, window_start, today, days=filters["days"])

    max_device_total = max((item["total"] for item in device_breakdown), default=1)
    for item in device_breakdown:
        item["chart_percent"] = int((item["total"] / max_device_total) * 100) if max_device_total else 0

    max_source_total = max((item["total"] for item in source_breakdown), default=1)
    for item in source_breakdown:
        item["chart_percent"] = int((item["total"] / max_source_total) * 100) if max_source_total else 0

    context = admin.site.each_context(request)
    context.update({
        "content_cards": content_cards,
        "engagement_cards": engagement_cards,
        "recent_cards": recent_cards,
        "traffic_cards": traffic_cards,
        "conversion_metrics": conversion_metrics,
        "performance_metrics": performance_metrics,
        "focus_by_sector": focus_by_sector,
        "recent_subscriptions": recent_subscriptions,
        "recent_contacts": recent_contacts,
        "upcoming_events": upcoming_events,
        "top_pages": top_pages,
        "top_events": top_events,
        "top_navigation_paths": top_navigation_paths,
        "device_breakdown": device_breakdown,
        "source_breakdown": source_breakdown,
        "country_breakdown": country_breakdown,
        "timeline_page_views": timeline_page_views,
        "selected_days": filters["days"],
        "selected_device": filters["device"],
        "selected_source": filters["source"],
        "selected_country": filters["country"],
        "selected_browser": filters["browser"],
        "selected_operating_system": filters["operating_system"],
        "selected_event_type": filters["event_type"],
        "selected_query": filters["q"],
        "analytics_filter_options": _analytics_filter_options(window_start),
        "analytics_window_options": ANALYTICS_WINDOW_OPTIONS,
        "window_start": window_start,
        "today": today,
    })
    return render(request, "admin/analytics_dashboard.html", context)


@staff_member_required(login_url="/admin/login/")
def analytics_group_page(request):
    today = timezone.localdate()

    def _section_filters(prefix):
        days = _safe_int(request.GET.get(f"{prefix}_days"), 30)
        if days not in ANALYTICS_WINDOW_OPTIONS:
            days = 30
        return {
            "days": days,
            "window_start": today - timedelta(days=days - 1),
            "device": (request.GET.get(f"{prefix}_device") or "").strip()[:20],
            "source": (request.GET.get(f"{prefix}_source") or "").strip()[:120],
            "country": (request.GET.get(f"{prefix}_country") or "").strip()[:100],
            "browser": (request.GET.get(f"{prefix}_browser") or "").strip()[:100],
            "operating_system": (request.GET.get(f"{prefix}_operating_system") or "").strip()[:100],
            "event_type": (request.GET.get(f"{prefix}_event_type") or "").strip()[:80],
            "q": (request.GET.get(f"{prefix}_q") or "").strip()[:120],
        }

    user_filters = _section_filters("u")
    session_filters = _section_filters("s")
    event_filters = _section_filters("e")

    users_base = AnalyticsUser.objects.filter(last_seen__date__gte=user_filters["window_start"])
    sessions_base = AnalyticsSession.objects.filter(start_time__date__gte=session_filters["window_start"])
    events_base = AnalyticsEvent.objects.filter(timestamp__date__gte=event_filters["window_start"])

    user_filter_options = {
        "devices": sorted(
            users_base.exclude(device_type="").values_list("device_type", flat=True).distinct()
        ),
        "countries": sorted(
            users_base.exclude(country="").values_list("country", flat=True).distinct()
        ),
        "browsers": sorted(
            users_base.exclude(browser="").values_list("browser", flat=True).distinct()
        ),
        "operating_systems": sorted(
            users_base.exclude(operating_system="").values_list("operating_system", flat=True).distinct()
        ),
    }

    session_filter_options = {
        "sources": sorted(
            sessions_base.exclude(source="").values_list("source", flat=True).distinct()
        ),
        "devices": sorted(
            sessions_base.exclude(user__device_type="").values_list("user__device_type", flat=True).distinct()
        ),
        "countries": sorted(
            sessions_base.exclude(user__country="").values_list("user__country", flat=True).distinct()
        ),
        "browsers": sorted(
            sessions_base.exclude(user__browser="").values_list("user__browser", flat=True).distinct()
        ),
        "operating_systems": sorted(
            sessions_base.exclude(user__operating_system="").values_list("user__operating_system", flat=True).distinct()
        ),
    }

    event_filter_options = {
        "event_types": sorted(
            events_base.exclude(event_type="").values_list("event_type", flat=True).distinct()
        ),
        "sources": sorted(
            events_base.exclude(session__source="").values_list("session__source", flat=True).distinct()
        ),
        "devices": sorted(
            events_base.exclude(user__device_type="").values_list("user__device_type", flat=True).distinct()
        ),
        "countries": sorted(
            events_base.exclude(user__country="").values_list("user__country", flat=True).distinct()
        ),
        "browsers": sorted(
            events_base.exclude(user__browser="").values_list("user__browser", flat=True).distinct()
        ),
        "operating_systems": sorted(
            events_base.exclude(user__operating_system="").values_list("user__operating_system", flat=True).distinct()
        ),
    }

    users_qs = users_base
    if user_filters["device"]:
        users_qs = users_qs.filter(device_type=user_filters["device"])
    if user_filters["country"]:
        users_qs = users_qs.filter(country=user_filters["country"])
    if user_filters["browser"]:
        users_qs = users_qs.filter(browser=user_filters["browser"])
    if user_filters["operating_system"]:
        users_qs = users_qs.filter(operating_system=user_filters["operating_system"])
    if user_filters["source"]:
        users_qs = users_qs.filter(sessions__source=user_filters["source"]).distinct()
    if user_filters["event_type"]:
        users_qs = users_qs.filter(events__event_type=user_filters["event_type"]).distinct()
    if user_filters["q"]:
        q = user_filters["q"]
        users_qs = users_qs.filter(user_id__icontains=q)

    sessions_qs = sessions_base
    if session_filters["device"]:
        sessions_qs = sessions_qs.filter(user__device_type=session_filters["device"])
    if session_filters["source"]:
        sessions_qs = sessions_qs.filter(source=session_filters["source"])
    if session_filters["country"]:
        sessions_qs = sessions_qs.filter(user__country=session_filters["country"])
    if session_filters["browser"]:
        sessions_qs = sessions_qs.filter(user__browser=session_filters["browser"])
    if session_filters["operating_system"]:
        sessions_qs = sessions_qs.filter(user__operating_system=session_filters["operating_system"])
    if session_filters["event_type"]:
        sessions_qs = sessions_qs.filter(events__event_type=session_filters["event_type"]).distinct()
    if session_filters["q"]:
        q = session_filters["q"]
        sessions_qs = sessions_qs.filter(session_id__icontains=q)

    events_qs = events_base
    if event_filters["device"]:
        events_qs = events_qs.filter(user__device_type=event_filters["device"])
    if event_filters["source"]:
        events_qs = events_qs.filter(session__source=event_filters["source"])
    if event_filters["country"]:
        events_qs = events_qs.filter(user__country=event_filters["country"])
    if event_filters["browser"]:
        events_qs = events_qs.filter(user__browser=event_filters["browser"])
    if event_filters["operating_system"]:
        events_qs = events_qs.filter(user__operating_system=event_filters["operating_system"])
    if event_filters["event_type"]:
        events_qs = events_qs.filter(event_type=event_filters["event_type"])
    if event_filters["q"]:
        q = event_filters["q"]
        events_qs = events_qs.filter(page_url__icontains=q)

    users = users_qs.order_by("-last_seen")[:200]
    sessions = sessions_qs.order_by("-start_time")[:200]
    events = events_qs.order_by("-timestamp")[:400]

    context = admin.site.each_context(request)
    context.update({
        "users": users,
        "sessions": sessions,
        "events": events,
        "users_total": users_qs.count(),
        "sessions_total": sessions_qs.count(),
        "events_total": events_qs.count(),
        "user_filters": user_filters,
        "session_filters": session_filters,
        "event_filters": event_filters,
        "user_filter_options": user_filter_options,
        "session_filter_options": session_filter_options,
        "event_filter_options": event_filter_options,
        "analytics_window_options": ANALYTICS_WINDOW_OPTIONS,
    })
    return render(request, "admin/analytics_group.html", context)


def focus_page(request):
    queryset = Focus.objects.order_by("-id")
    context = _paginated_listing_context(request, queryset, title_field="heading")
    context["focus_items"] = context["page_obj"].object_list
    context.update(_base_context())
    return render(request, "epcandiapp/focus.html", context)


def shopping_cart_page(request):
    queryset = ShoppingCart.objects.order_by("-id")
    context = _paginated_listing_context(request, queryset, title_field="heading")
    context["shopping_cart_items"] = context["page_obj"].object_list
    context.update(_base_context())
    return render(request, "epcandiapp/shopping_cart.html", context)


def shopping_cart_detail_page(request, shopping_cart_id):
    item = get_object_or_404(ShoppingCart, id=shopping_cart_id)
    return _render_detail_page(
        request,
        page_title=f"{item.heading} | EPC&I Shopping Cart",
        toolbar_title="SHOPPING CART",
        detail_title=item.heading,
        detail_body=item.shopping_cart,
        back_url="shopping_cart",
        back_label="Back to Shopping Cart",
    )


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
    queryset = SquareFoot.objects.order_by("-id")
    context = _paginated_listing_context(request, queryset, title_field="heading")
    context["square_foot_items"] = context["page_obj"].object_list
    context.update(_base_context())
    return render(request, "epcandiapp/square_foot.html", context)


def square_foot_detail_page(request, square_foot_id):
    item = get_object_or_404(SquareFoot, id=square_foot_id)
    return _render_detail_page(
        request,
        page_title=f"{item.heading} | EPC&I Square Foot",
        toolbar_title="SQUARE FOOT",
        detail_title=item.heading,
        detail_body=item.square_foot,
        back_url="square_foot",
        back_label="Back to Square Foot",
    )


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