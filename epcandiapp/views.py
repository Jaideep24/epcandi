from django.shortcuts import get_object_or_404, render
from .models import *
# Create your views here.


def _base_context():
    return {
        "advertisement_banners": AdvertisementBanner.objects.filter(is_active=True)
    }


def _render_static_page(request, template_name, extra_context=None):
    context = {}
    if extra_context:
        context.update(extra_context)
    context.update(_base_context())
    return render(request, template_name, context)

def home_page(request):
    # Home should show the News listing page.
    return news_page(request)


def news_page(request):
    context = {"News": News.objects.all().values()}
    context.update(_base_context())
    return render(request, "epcandiapp/news.html", context)


def article_page(request):
    context = {"Articles": Articles.objects.all().values()}
    context.update(_base_context())
    return render(request, "epcandiapp/articles.html", context)


def article_detail_page(request, article_id):
    article = get_object_or_404(Articles, id=article_id)
    context = {"article": article}
    context.update(_base_context())
    return render(request, "epcandiapp/article_detail.html", context)


def interview_page(request):
    context = {"Interviews": Interview.objects.all().values()}
    context.update(_base_context())
    return render(request, "epcandiapp/interview.html", context)


def equipment_page(request):
    context = {"Equipment_News": Equipment_News.objects.all().values()}
    context.update(_base_context())
    return render(request, "epcandiapp/equipment_news.html", context)


def events_page(request):
    context = {"events": Events.objects.all().order_by("-start_date")}
    context.update(_base_context())
    return render(request, "epcandiapp/events.html", context)


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
    if request.method == "POST":
        # Get form data
        query_type = request.POST.get("query_type", "Feedback / Suggestions").strip()
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
        context = {}
        context.update(_base_context())
        return render(request, "epcandiapp/contact.html", context)


def tenders_page(request):
    return _render_static_page(request, "epcandiapp/tenders.html")


def catalogs_page(request):
    return _render_static_page(request, "epcandiapp/catalogs.html")


def about_page(request):
    return _render_static_page(request, "epcandiapp/about.html")


def disclaimer_page(request):
    return _render_static_page(request, "epcandiapp/disclaimer.html")


def privacy_page(request):
    return _render_static_page(request, "epcandiapp/privacy.html")


def jobs_page(request):
    return _render_static_page(request, "epcandiapp/jobs.html")


def advertise_page(request):
    return _render_static_page(request, "epcandiapp/advertise.html")


def media_kit_page(request):
    return _render_static_page(request, "epcandiapp/media_kit.html")