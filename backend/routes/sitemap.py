"""
Sitemap Routes
"""
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from config import config
from models import Article, Category, FriendLink, Tag, get_db

router = APIRouter(tags=["sitemap"])

ARTICLE_TYPE_PASSWORD = 2


def iso_lastmod(value: datetime | None) -> str | None:
    if not value:
        return None
    return value.date().isoformat()


def pick_latest(*values: datetime | None) -> datetime | None:
    normalized_values = [value for value in values if value]
    return max(normalized_values) if normalized_values else None


def append_url(
    urlset: Element,
    loc: str,
    lastmod: datetime | None = None,
    changefreq: str | None = None,
    priority: str | None = None
):
    url = SubElement(urlset, "url")
    SubElement(url, "loc").text = loc

    normalized_lastmod = iso_lastmod(lastmod)
    if normalized_lastmod:
        SubElement(url, "lastmod").text = normalized_lastmod
    if changefreq:
        SubElement(url, "changefreq").text = changefreq
    if priority:
        SubElement(url, "priority").text = priority


@router.get("/sitemap.xml", include_in_schema=False)
def get_sitemap(db: Session = Depends(get_db)):
    site_url = config.SITE_URL

    articles = db.query(Article).filter(Article.type != ARTICLE_TYPE_PASSWORD).all()
    categories = db.query(Category).all()
    tags = db.query(Tag).all()
    friend_links = db.query(FriendLink).filter(FriendLink.is_show == 1).all()

    latest_article_time = pick_latest(*(article.update_time or article.create_time for article in articles))
    latest_category_time = pick_latest(*(category.create_time for category in categories))
    latest_tag_time = pick_latest(*(tag.create_time for tag in tags))
    latest_friend_link_time = pick_latest(*(link.create_time for link in friend_links))
    latest_site_time = pick_latest(
        latest_article_time,
        latest_category_time,
        latest_tag_time,
        latest_friend_link_time
    )

    urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    append_url(urlset, f"{site_url}/", latest_site_time, "daily", "1.0")
    append_url(urlset, f"{site_url}/archive", latest_article_time, "daily", "0.9")
    append_url(urlset, f"{site_url}/category", pick_latest(latest_category_time, latest_article_time), "daily", "0.8")
    append_url(urlset, f"{site_url}/tag", pick_latest(latest_tag_time, latest_article_time), "daily", "0.8")
    append_url(urlset, f"{site_url}/about", latest_site_time, "monthly", "0.5")
    append_url(urlset, f"{site_url}/links", latest_friend_link_time, "weekly", "0.6")
    append_url(urlset, f"{site_url}/message", latest_site_time, "weekly", "0.4")

    for article in articles:
        append_url(
            urlset,
            f"{site_url}/article/{article.id}",
            article.update_time or article.create_time,
            "weekly",
            "0.8"
        )

    for category in categories:
        append_url(
            urlset,
            f"{site_url}/category?category={category.id}",
            category.create_time,
            "weekly",
            "0.7"
        )

    for tag in tags:
        append_url(
            urlset,
            f"{site_url}/tag?tag={tag.id}",
            tag.create_time,
            "weekly",
            "0.6"
        )

    xml_body = tostring(urlset, encoding="utf-8", xml_declaration=True)
    return Response(content=xml_body, media_type="application/xml")
