import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="render_richtext")
def render_richtext(value):
    """Render stored rich text and clean known legacy tokens."""
    if not value:
        return ""

    text = str(value)

    # Remove legacy image marker tokens such as [!image2:n!].
    text = re.sub(r"\[!image\d+:n!\]", "", text, flags=re.IGNORECASE)

    # Normalize non-breaking spaces to avoid odd wrapping and large gaps.
    text = text.replace("&nbsp;", " ")

    # Repair legacy mojibake where question marks split words (e.g., MOBISCREEN?EVO)
    # only in text nodes, never inside HTML tags/attributes like image URLs.
    parts = re.split(r"(<[^>]+>)", text)
    cleaned_parts = []
    for part in parts:
        if part.startswith("<") and part.endswith(">"):
            cleaned_parts.append(part)
        else:
            cleaned_parts.append(re.sub(r"(?<=[A-Za-z0-9])\?(?=[A-Za-z0-9])", " ", part))
    text = "".join(cleaned_parts)

    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # If rich HTML blocks exist, keep structure untouched and only trim noisy blank lines.
    has_html_tags = bool(re.search(r"<\s*[a-zA-Z][^>]*>", text))
    if has_html_tags:
        text = re.sub(r"\n{3,}", "\n\n", text)
    else:
        # For plain text, preserve newlines for readability.
        text = text.replace("\n", "<br>\n")

    return mark_safe(text)
