"""
RSS feed routes.
"""
from datetime import datetime, timezone
from email.utils import format_datetime
from html import escape as escape_html
from html.parser import HTMLParser
import re
from xml.sax.saxutils import escape

import markdown
from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session, joinedload

from cache import cache
from config import config
from models import Article, get_db

router = APIRouter(tags=["rss"])

ARTICLE_TYPE_PASSWORD = 2
RSS_CACHE_KEY = "feed:rss:v2"
RSS_CACHE_TTL_SECONDS = 3600
ATOM_NAMESPACE = "http://www.w3.org/2005/Atom"
CONTENT_NAMESPACE = "http://purl.org/rss/1.0/modules/content/"
SAFE_URL_PATTERN = re.compile(r"^(https?:|mailto:|tel:|/|#)", re.IGNORECASE)
ALLOWED_TAGS = {
    "a", "blockquote", "br", "code", "del", "details", "div", "em",
    "h1", "h2", "h3", "h4", "h5", "h6", "hr", "img", "li", "ol", "p",
    "pre", "section", "span", "strong", "summary", "table", "tbody",
    "td", "th", "thead", "tr", "ul",
}
GLOBAL_ALLOWED_ATTRS = {"class", "id", "title"}
ALLOWED_ATTRS_BY_TAG = {
    "a": {"href", "target", "rel"},
    "img": {"src", "alt", "title"},
}


class SafeHtmlParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.parts: list[str] = []
        self.open_tags: list[str] = []
        self.drop_depth = 0

    def handle_starttag(self, tag: str, attrs):
        tag = tag.lower()
        if self.drop_depth > 0:
            self.drop_depth += 1
            return
        if tag in {"script", "style", "iframe"}:
            self.drop_depth = 1
            return
        if tag not in ALLOWED_TAGS:
            return

        sanitized_attrs: list[str] = []
        allowed_attrs = ALLOWED_ATTRS_BY_TAG.get(tag, set())
        for name, value in attrs:
            attr_name = (name or "").lower()
            attr_value = value or ""
            if attr_name.startswith("on"):
                continue
            if attr_name not in GLOBAL_ALLOWED_ATTRS and attr_name not in allowed_attrs:
                continue
            if attr_name in {"href", "src"} and not SAFE_URL_PATTERN.match(attr_value.strip()):
                continue
            if attr_name == "target" and attr_value != "_blank":
                continue
            if tag == "a" and attr_name == "rel" and "_blank" not in [v for k, v in attrs if (k or "").lower() == "target"]:
                continue
            sanitized_attrs.append(f' {attr_name}="{escape_html(attr_value, quote=True)}"')

        if tag == "a" and any((name or "").lower() == "target" and (value or "") == "_blank" for name, value in attrs):
            if not any(attr.startswith(" rel=") for attr in sanitized_attrs):
                sanitized_attrs.append(' rel="noopener noreferrer"')

        self.parts.append(f"<{tag}{''.join(sanitized_attrs)}>")
        self.open_tags.append(tag)

    def handle_endtag(self, tag: str):
        tag = tag.lower()
        if self.drop_depth > 0:
            self.drop_depth -= 1
            return
        if tag in ALLOWED_TAGS and tag in self.open_tags:
            self.parts.append(f"</{tag}>")
            for index in range(len(self.open_tags) - 1, -1, -1):
                if self.open_tags[index] == tag:
                    self.open_tags.pop(index)
                    break

    def handle_startendtag(self, tag: str, attrs):
        self.handle_starttag(tag, attrs)
        if self.open_tags and self.open_tags[-1] == tag:
            self.handle_endtag(tag)

    def handle_data(self, data: str):
        if self.drop_depth == 0:
            self.parts.append(escape_html(data))

    def handle_entityref(self, name: str):
        if self.drop_depth == 0:
            self.parts.append(f"&{name};")

    def handle_charref(self, name: str):
        if self.drop_depth == 0:
            self.parts.append(f"&#{name};")

    def get_html(self) -> str:
        while self.open_tags:
            self.parts.append(f"</{self.open_tags.pop()}>")
        return "".join(self.parts)


def sanitize_html(html: str | None) -> str:
    if not html:
        return ""
    parser = SafeHtmlParser()
    parser.feed(html)
    parser.close()
    return parser.get_html()


def format_rss_datetime(value: datetime | None) -> str | None:
    if not value:
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return format_datetime(value.astimezone(timezone.utc), usegmt=True)


def render_markdown_html(content: str | None) -> str:
    if not content:
        return ""

    return sanitize_html(
        markdown.markdown(
            content,
            extensions=["extra", "codehilite", "nl2br", "sane_lists"],
            output_format="html5",
        )
    )


def parse_attrs(raw_attrs: str = "") -> dict[str, str]:
    attrs: dict[str, str] = {}
    for key, value in re.findall(r'(\w+)="([^"]*)"', raw_attrs or ""):
        attrs[key] = value
    return attrs


def build_article_reference_renderer(db: Session):
    article_cache: dict[str, Article | None] = {}

    def render_article_reference(attrs: dict[str, str]) -> str:
        article_id = (attrs.get("id") or "").strip()
        if not article_id:
            return ""

        if article_id not in article_cache:
            article_cache[article_id] = (
                db.query(Article)
                .options(joinedload(Article.category))
                .filter(Article.id == int(article_id), Article.type != ARTICLE_TYPE_PASSWORD)
                .first()
                if article_id.isdigit()
                else None
            )

        article = article_cache[article_id]
        article_url = f"{config.SITE_URL}/article/{article_id}"
        if not article:
            return (
                f'<a class="custom-article-ref" href="{escape_xml_text(article_url)}">'
                '<span class="custom-article-ref__label">文章</span>'
                f'<span class="custom-article-ref__title">文章 #{escape_xml_text(article_id)}</span>'
                '<span class="custom-article-ref__meta">引用文章不存在或不可公开访问</span>'
                '</a>'
            )

        label = article.category.name if article.category and article.category.name else "未分类"
        meta_parts = []
        if article.category and article.category.name:
            meta_parts.append(article.category.name)
        if article.summary:
            meta_parts.append(article.summary[:48] + "..." if len(article.summary) > 48 else article.summary)
        meta = " · ".join(meta_parts) or f"文章 #{article.id}"

        return (
            f'<a class="custom-article-ref" href="{escape_xml_text(article_url)}">'
            f'<span class="custom-article-ref__label">{escape_xml_text(label)}</span>'
            f'<span class="custom-article-ref__title">{escape_xml_text(article.title)}</span>'
            f'<span class="custom-article-ref__meta">{escape_xml_text(meta)}</span>'
            '</a>'
        )

    return render_article_reference


def preprocess_custom_markdown(content: str, db: Session) -> str:
    if not content:
        return ""

    render_article_reference = build_article_reference_renderer(db)

    def replace_timeline(match: re.Match[str]) -> str:
        inner = match.group(1) or ""
        event_matches = re.findall(r'\[timeline-event([^\]]*)\]([\s\S]*?)\[/timeline-event\]', inner)
        items: list[str] = []

        for raw_attrs, body in event_matches:
            attrs = parse_attrs(raw_attrs)
            rendered_body = render_markdown_html(preprocess_custom_markdown((body or "").strip(), db))
            items.append(
                '<div class="custom-timeline__item">'
                '<div class="custom-timeline__dot"></div>'
                '<div class="custom-timeline__card">'
                '<div class="custom-timeline__meta">'
                f'<span class="custom-timeline__date">{escape_xml_text(attrs.get("date", ""))}</span>'
                f'<div class="custom-timeline__title">{escape_xml_text(attrs.get("title", ""))}</div>'
                '</div>'
                f'<div class="custom-timeline__body">{rendered_body}</div>'
                '</div>'
                '</div>'
            )

        if not items:
            return ""

        return f'<section class="custom-timeline">{"".join(items)}</section>'

    def replace_folded_content(match: re.Match[str]) -> str:
        attrs = parse_attrs(match.group(1) or "")
        title = (attrs.get("title") or "").strip() or "展开查看"
        body = render_markdown_html(preprocess_custom_markdown((match.group(2) or "").strip(), db))
        return (
            '<details class="custom-folded-content">'
            f'<summary class="custom-folded-content__summary">{escape_xml_text(title)}</summary>'
            f'<div class="custom-folded-content__body">{body}</div>'
            '</details>'
        )

    processed = content
    processed = re.sub(r'\[timeline\]([\s\S]*?)\[/timeline\]', replace_timeline, processed)
    processed = re.sub(
        r'\[folded_content([^\]]*)\]([\s\S]*?)\[/folded(?:_|\s+)content\]',
        replace_folded_content,
        processed,
    )
    processed = re.sub(
        r'\[article([^\]]*)\]',
        lambda match: render_article_reference(parse_attrs(match.group(1) or "")),
        processed,
    )
    return processed


def escape_xml_text(value: str | None) -> str:
    return escape(value or "")


def wrap_cdata(value: str | None) -> str:
    normalized = (value or "").replace("]]>", "]]]]><![CDATA[>")
    return f"<![CDATA[{normalized}]]>"


def build_rss_xml(db: Session) -> bytes:
    site_url = config.SITE_URL
    feed_url = f"{site_url}/rss.xml"
    articles = (
        db.query(Article)
        .options(joinedload(Article.category))
        .filter(Article.type != ARTICLE_TYPE_PASSWORD)
        .order_by(Article.create_time.desc())
        .all()
    )

    latest_update = max(
        (article.update_time or article.create_time for article in articles if article.update_time or article.create_time),
        default=None,
    )

    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        f'<rss version="2.0" xmlns:atom="{ATOM_NAMESPACE}" xmlns:content="{CONTENT_NAMESPACE}">',
        "<channel>",
        f"<title>{escape_xml_text('MoZhi Blog')}</title>",
        f"<link>{escape_xml_text(f'{site_url}/')}</link>",
        f"<description>{escape_xml_text('MoZhi Blog RSS Feed')}</description>",
        "<language>zh-cn</language>",
        "<generator>MoZhi Blog</generator>",
        f'<atom:link href="{escape_xml_text(feed_url)}" rel="self" type="application/rss+xml" />',
    ]

    last_build_date = format_rss_datetime(latest_update)
    if last_build_date:
        lines.append(f"<lastBuildDate>{escape_xml_text(last_build_date)}</lastBuildDate>")

    for article in articles:
        article_url = f"{site_url}/article/{article.id}"
        summary = (article.summary or "").strip()
        full_html = render_markdown_html(preprocess_custom_markdown(article.content, db))
        pub_date = format_rss_datetime(article.create_time or article.update_time)

        lines.append("<item>")
        lines.append(f"<title>{escape_xml_text(article.title)}</title>")
        lines.append(f"<link>{escape_xml_text(article_url)}</link>")
        lines.append(f'<guid isPermaLink="true">{escape_xml_text(article_url)}</guid>')

        if pub_date:
            lines.append(f"<pubDate>{escape_xml_text(pub_date)}</pubDate>")

        if summary:
            lines.append(f"<description>{wrap_cdata(summary)}</description>")
        elif full_html:
            lines.append(f"<description>{wrap_cdata(full_html)}</description>")

        lines.append(f"<content:encoded>{wrap_cdata(full_html)}</content:encoded>")

        if article.category and article.category.name:
            lines.append(f"<category>{escape_xml_text(article.category.name)}</category>")

        lines.append("</item>")

    lines.extend(["</channel>", "</rss>"])
    return "\n".join(lines).encode("utf-8")


@router.get("/rss.xml", include_in_schema=False)
def get_rss_feed(db: Session = Depends(get_db)):
    xml_body = cache.get_or_set(RSS_CACHE_KEY, lambda: build_rss_xml(db), ttl_seconds=RSS_CACHE_TTL_SECONDS)
    return Response(
        content=xml_body,
        media_type="application/rss+xml; charset=utf-8",
        headers={
            "Content-Type": "application/rss+xml; charset=utf-8",
            "Cache-Control": f"public, max-age={RSS_CACHE_TTL_SECONDS}",
        },
    )
