from django.db import migrations


ABOUT_CONTENT = """It is often said that the progress of any nation can be gauged by the development of its infrastructure and the level of investment in construction activities. The importance of infrastructure for sustained economic development is well recognized in India. Over the past decade, the country has made remarkable progress, attracting significant investments across infrastructure and construction sectors, including highways, airports, ports, railways, telecommunications, technology, and the construction of roads and bridges.

EPC & I strives to provide construction professionals with comprehensive national news coverage that impacts the future of their industry. It offers a powerful combination of insight and analysis on top news stories, the latest industry updates, in-depth features, and special reports, along with access to breaking news and personalized content. This makes EPC & I a valuable resource for those seeking reliable and timely information on infrastructure development in India.

Recognizing the immense potential of the sector, EPC & I presents a magazine that features thought-provoking and well-researched articles contributed by top and middle management professionals from not only India but also across the Asia-Pacific region. These contributions bring diverse perspectives and expert knowledge to the forefront of the construction and engineering ecosystem.

Northern Lights Communications is proud to bring a fresh and dynamic perspective to the infrastructure and construction community. With a clean, contemporary design, high-quality printing, and intelligent, incisive editorial, EPC & I is both visually engaging and highly informative. It also serves as an effective platform for product promotion, acting as a comprehensive sourcebook for consumers, retailers, and manufacturers, and providing thousands of buyers with direct access to businesses.

*****

Readership Profile

EPC & I reaches out to industry leaders and opinion-makers who are at the forefront of infrastructure development, as well as policymakers who shape industry-friendly regulations. The platform effectively connects with a wide spectrum of professionals, including corporate organizations, engineering and construction companies, civil and electrical contractors, structural engineers, architects, OEMs, project consultants, building and construction contractors, site engineers, and interior designers.

EPC & I stands as an effective communication platform for promoting new business concepts, showcasing achievements and success stories, and strengthening brand value within the infrastructure and construction industry."""


def seed_pages(apps, schema_editor):
    SitePage = apps.get_model("epcandiapp", "SitePage")

    pages = [
        {
            "slug": "about",
            "title": "ABOUT EPC&I",
            "heading": "ABOUT US",
            "content": ABOUT_CONTENT,
        },
        {
            "slug": "tenders",
            "title": "EPC&I TENDERS",
            "heading": "TENDERS",
            "content": "Tender listings will be published here soon.",
        },
        {
            "slug": "catalogs",
            "title": "EPC&I CATALOGS",
            "heading": "CATALOGS",
            "content": "Catalog resources will be available here soon.",
        },
        {
            "slug": "disclaimer",
            "title": "EPC&I DISCLAIMER",
            "heading": "DISCLAIMER",
            "content": "Content is published for information purposes. Please verify details independently before making business decisions.",
        },
        {
            "slug": "privacy",
            "title": "EPC&I PRIVACY",
            "heading": "PRIVACY",
            "content": "Privacy details and data handling policies are maintained on this page.",
        },
        {
            "slug": "jobs",
            "title": "EPC&I JOBS",
            "heading": "JOBS",
            "content": "Current openings and career opportunities will be listed here.",
        },
        {
            "slug": "advertise",
            "title": "ADVERTISE WITH EPC&I",
            "heading": "ADVERTISE",
            "content": "For advertising opportunities, please use the contact page and mention your campaign requirements.",
        },
        {
            "slug": "media-kit",
            "title": "EPC&I MEDIA KIT",
            "heading": "MEDIA KIT",
            "content": "Media kit details will be shared here for partners and advertisers.",
        },
        {
            "slug": "shopping-cart",
            "title": "EPC&I SHOPPING CART",
            "heading": "SHOPPING CART",
            "content": "Shopping cart content will be added here.",
        },
    ]

    for page in pages:
        SitePage.objects.update_or_create(
            slug=page["slug"],
            defaults={
                "title": page["title"],
                "heading": page["heading"],
                "content": page["content"],
                "is_published": True,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ("epcandiapp", "0007_sitepage"),
    ]

    operations = [
        migrations.RunPython(seed_pages, migrations.RunPython.noop),
    ]
