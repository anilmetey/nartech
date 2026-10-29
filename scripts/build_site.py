from __future__ import annotations
import html, json, re, shutil
from pathlib import Path
from docx import Document

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
OUT = ROOT

def paragraphs(filename: str) -> list[str]:
    return [p.text for p in Document(DOCS / filename).paragraphs if p.text.strip()]

def source_lines(filename: str) -> list[int]:
    return [i + 1 for i, p in enumerate(Document(DOCS / filename).paragraphs) if p.text.strip()]

home = paragraphs("Home.docx")
about = paragraphs("About US.docx")
about_lines = source_lines("About US.docx")
services = paragraphs("Supervision Services.docx")
service_lines = source_lines("Supervision Services.docx")
product_text = paragraphs("Products (1).docx")
product_lines = source_lines("Products (1).docx")

def ref(index: int) -> dict:
    return {"text": product_text[index], "source": f"Products (1).docx:{product_lines[index]}"}

def text_at_product_line(line: int) -> str:
    return product_text[product_lines.index(line)]

def refs(indices):
    return [ref(i) for i in indices]

def item(id, title_tr=None, title_en=None, tr=None, en=None, children=None, src=None):
    def text_at(index):
        if index is None:
            return None
        return product_text[index] if isinstance(index, int) else index
    return {
        "id": id,
        "titleTr": text_at(title_tr),
        "titleEn": text_at(title_en),
        "tr": refs(tr or []),
        "en": refs(en or []),
        "children": children or [],
        "source": src,
    }

# The category order and all product wording come from Products (1).docx.
pvrv = item("pressure-vacuum-relief-valve", 2, 7, [3, 4, 5, 6], [8, 9, 10, 11], src=1)
pvrv["navTitleEn"] = text_at_product_line(2)
inline = item("inline-flame-arrester", 13, 19, [14, 15, 16, 17, 18], [20, 21, 22, 23, 24], src=12)
inline["navTitleEn"] = text_at_product_line(21)
endline = item("end-line-flame-arrester", 26, 31, [27, 28, 29, 30], [32, 33, 34, 35], src=25)
endline["navTitleEn"] = text_at_product_line(37)
emergency_en_title = "Emergency Relief Valve"
emergency_en_blob = [p.strip() for p in product_text[41].split("\n") if p.strip()]
emergency_en_title_position = emergency_en_blob.index(emergency_en_title)
emergency_en_first = emergency_en_blob[emergency_en_title_position + 1]
emergency = item("emergency-relief-valve", 37, None, [38, 39, 40, 41], [42, 43, 44], src=36)
emergency["titleEn"] = emergency_en_title
emergency["en"].insert(0, {"text": emergency_en_first, "source": f"Products (1).docx:{product_lines[41]}"})
emergency["navTitleEn"] = text_at_product_line(56)
gauge = item("gauge-hatch", 46, 52, [47, 48, 49, 50, 51], [53, 54, 55, 56], src=45)
gauge["navTitleEn"] = text_at_product_line(70)

floating_children = [
    item("pontoon-type-ifr", 58, None, [59, 60, 61, 62, 63, 64, 65, 66, 67], [], src=57),
    item("full-contact-type-ifr", 68, None, [69, 70, 71, 72, 73, 74, 75, 76, 77], [], src=68),
    item("chemraz-xpe-seal", 78, None, [79], [], src=78),
    item("hdpe-seal", 80, None, [81], [], src=80),
    item("ldpe-seal", 82, None, [83], [], src=82),
]
floating_roofs = item("internal-floating-roofs-and-seals", 57, None, [], [], floating_children, 56)
floating_roofs["titleTr"] = "İç Yüzer Tavanlar ve Fitiller"
floating_roofs["titleEn"] = text_at_product_line(83)
floating_suction_children = [
    item("pipe-type-floating-suction-unit", 123, None, [], [], src=122),
    item("hose-type-floating-suction-unit", 124, None, [], [], src=123),
    item("oil-skimmer", 125, None, [], [], src=124),
]

fire_items = [
    item("fixed-foam-monitor", 85, None, [86, 87, 88], [], src=84),
    item("foam-maker", 89, None, [90, 91, 92], [], src=88),
    item("foam-mixer-proportioner", 93, None, [94, 95, 96], [], src=92),
    item("foam-top-pourer", 97, None, [98, 99, 100], [], src=96),
    item("rim-seal-foam-pourer", 101, None, [102, 103, 104], [], src=100),
    item("foam-tanks", 105, None, [106, 107, 108], [], src=104),
    item("foam-water-sprinkler", 109, None, [110, 111], [], src=108),
]
pig_signallers = item("pig-signallers", 116, None, [], [], [
    item("non-intrusive-pig-signaller", 117, None, [], [], src=116),
    item("intrusive-pig-signaller", 118, None, [], [], src=116),
], 115)
valve_items = [
    item("ball-valves", 130, None, [], [], src=129),
    item("gate-valves", 131, None, [], [], src=130),
    item("butterfly-valves", 132, None, [], [], src=131),
]

categories = [
    {"id":"storage-tank-equipments", "title":ref(0), "items":[pvrv, inline, endline, emergency, gauge, floating_roofs]},
    {"id":"fire-fighting-equipments", "title":ref(84), "items":fire_items},
    {"id":"pig-cleaning-equipments", "title":ref(112), "items":[
        item("foam-pigs",113,None,[],[],src=112), item("solid-cast-pigs",114,None,[],[],src=113),
        item("steel-pigs",115,None,[],[],src=114), pig_signallers]},
    {"id":"industrial-silencers", "title":ref(119), "items":[], "description":refs([120])},
    {"id":"floatin-suction-units", "title":ref(121), "items":floating_suction_children, "description":refs([122])},
    {"id":"retractable-grounding-cable", "title":ref(126), "items":[], "description":refs([127])},
    {"id":"loading-arms", "title":ref(128), "items":[]},
    {"id":"industrial-valves", "title":ref(129), "items":valve_items},
    {"id":"gas-scrubber-systems", "title":ref(133), "items":[]},
    {"id":"seperators", "title":ref(134), "items":[]},
    {"id":"spare-parts-for-refineries", "title":ref(135), "items":[]},
]
category_titles_tr=[
    "1-Depolama Tankı Ekipmanları", "2-Yangın Söndürme", "3-Pig Temizleme",
    "4-Susturucular", "5-Yüzer Emiş", "6-Topraklama RGR", "7-Dolum Kolları",
    "8-Vanalar", "9-Gaz Yıkama", "10-Seperatörler", "11-Yedek Parça",
]
for category,title_tr in zip(categories,category_titles_tr):
    category["titleTr"]=title_tr
    category["titleEn"]=category["title"]["text"]

def category_title(category, language):
    return category["titleEn"] if language == "en" else category["titleTr"]

# Persist only the concise copy used by the pages.
content = {
    "home":{"titleTr":home[0],"bodyTr":home[1],"titleEn":home[2],"bodyEn":home[3]},
    "about":{"titleTr":about[0],"paragraphsTr":[{"text":about[i],"source":f"About US.docx:{about_lines[i]}"} for i in range(1,6)],"titleEn":about[6],"paragraphsEn":[{"text":about[i],"source":f"About US.docx:{about_lines[i]}"} for i in range(7,12)]},
    "services":{"title":services[0],"items":[{"title":services[i],"titleSource":f"Supervision Services.docx:{service_lines[i]}","paragraphs":[{"text":services[j],"source":f"Supervision Services.docx:{service_lines[j]}"} for j in (i+1,i+2)]} for i in (1,4,7)]},
    "categories":categories,
}
(OUT / "content" / "site-content.json").write_text(json.dumps(content,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def esc(value) -> str:
    return html.escape(str(value or ""), quote=True)

def nav(prefix: str, current: str) -> str:
    entries = [
        ("home","index.html","Ana Sayfa","Home"),
        ("about","about.html","Hakkımızda","About Us"),
        ("products","products.html","Ürünler","Products"),
        ("services","services.html","Hizmetler","Services"),
        ("calculator","calculator.html","Hesaplama","Calculator"),
        ("faq","faq.html","Sıkça Sorulan Sorular","FAQ"),
        ("contact","contact.html","İletişim","Contact"),
    ]
    links=[]
    for key,path,tr,en in entries:
        current_attr=' aria-current="page"' if key==current else ""
        links.append(f'<a href="{prefix}{path}"{current_attr}><span class="lang-tr">{esc(tr)}</span><span class="lang-en">{esc(en)}</span></a>')
    links.append('<span class="language-toggle" aria-label="TR EN"><button type="button" data-set-language="tr" aria-pressed="true">TR</button><button type="button" data-set-language="en" aria-pressed="false">EN</button></span>')
    return "\n".join(links)

def footer(prefix: str) -> str:
    return f'''<footer class="site-footer"><div class="footer-inner"><div class="footer-mark-line"><a class="footer-brand" href="{prefix}index.html" aria-label="NarTech"><img src="{prefix}assets/images/logo-white.png" width="1024" height="472" alt="NarTech"></a><div class="footer-tagline"><span class="footer-tagline-dot" aria-hidden="true"></span><span class="lang-tr">{esc(content['home']['titleTr'])}</span><span class="lang-en">{esc(content['home']['titleEn'])}</span></div></div><nav class="footer-nav" aria-label="Site"><a href="{prefix}products.html"><span class="lang-tr">Ürünler</span><span class="lang-en">Products</span></a><a href="{prefix}about.html"><span class="lang-tr">Hakkımızda</span><span class="lang-en">About Us</span></a><a href="{prefix}services.html"><span class="lang-tr">Hizmetler</span><span class="lang-en">Services</span></a><a href="{prefix}calculator.html"><span class="lang-tr">Hesaplama</span><span class="lang-en">Calculator</span></a><a href="{prefix}faq.html"><span class="lang-tr">SSS</span><span class="lang-en">FAQ</span></a><a href="{prefix}contact.html"><span class="lang-tr">İletişim</span><span class="lang-en">Contact</span></a></nav></div></footer>'''

def layout(title: str, body: str, current: str, prefix="", lang="tr") -> str:
    return f'''<!doctype html>
<html lang="{lang}" data-language="tr">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} | NarTech</title>
<link rel="stylesheet" href="{prefix}assets/css/main.css?v=source-home-photo-2">
<script defer src="{prefix}assets/js/app.js?v=source-home-photo-2"></script>
</head>
<body>
<header class="site-header"><div class="header-inner"><a class="brand" href="{prefix}index.html" aria-label="NarTech"><img src="{prefix}assets/images/nartech-logo-transparent.png" width="1958" height="803" alt="NarTech"></a><button class="nav-toggle" type="button" data-nav-toggle aria-controls="site-nav" aria-expanded="false" aria-label="Menüyü Aç"><span></span><span></span><span></span></button><nav class="site-nav" id="site-nav" aria-label="Site">{nav(prefix,current)}</nav></div></header>
<button class="nav-backdrop" type="button" data-nav-close tabindex="-1" aria-hidden="true"></button>
<main>{body}</main>{footer(prefix)}</body></html>'''

def p_html(entry: dict, lang: str) -> str:
    return f'<p data-source="{esc(entry["source"])}">{esc(entry["text"])}</p>'

def title_for(obj: dict, lang: str) -> str:
    key="titleEn" if lang=="en" and obj.get("titleEn") else "titleTr"
    return obj.get(key) or obj.get("titleEn") or ""

def link_for(obj: dict, prefix: str, code="") -> str:
    href=f"{prefix}products/{esc(obj['id'])}.html"
    visible=esc(title_for(obj,"tr"))
    english=esc(obj.get("navTitleEn") or title_for(obj,"en"))
    labels = f'<span class="tree-index" aria-hidden="true">{esc(code)}</span>' if code else ""
    if obj.get("titleTr") and (obj.get("navTitleEn") or obj.get("titleEn")):
        label=f'{labels}<span class="lang-tr">{visible}</span><span class="lang-en">{english}</span>'
    else:
        label=f'{labels}{visible}'
    return f'<a class="tree-link" href="{href}">{label}</a>'

def branch_for(obj: dict, prefix: str, code="") -> str:
    title=title_for(obj,"tr")
    tree_title_en=obj.get("navTitleEn") or obj.get("titleEn")
    if obj.get("titleTr") and tree_title_en:
        title_html=f'<span class="lang-tr">{esc(title_for(obj,"tr"))}</span><span class="lang-en">{esc(tree_title_en)}</span>'
    else:
        title_html=esc(title)
    number=f'<span class="tree-index" aria-hidden="true">{esc(code)}</span>' if code else ""
    parts=[f'<details class="tree-branch"><summary>{number}{title_html}</summary><div class="tree-children">']
    for child in obj["children"]:
        if child["children"]:
            parts.append(branch_for(child,prefix))
        else:
            parts.append(link_for(child,prefix))
    if not obj["children"]:
        # The source provides no deeper breakdown for this item; it remains a valid detail link.
        parts.append(link_for(obj,prefix))
    parts.append('</div></details>')
    return "".join(parts)

# Homepage
home_categories=[]
for category in categories:
    label=f'<span class="lang-tr">{esc(category_title(category,"tr"))}</span><span class="lang-en">{esc(category_title(category,"en"))}</span>'
    home_categories.append(f'<a class="home-category-link" href="categories/{esc(category["id"])}.html">{label}<span aria-hidden="true">↗</span></a>')
home_about_tr=''.join(p_html(entry,"tr") for entry in content["about"]["paragraphsTr"][:2])
home_about_en=''.join(p_html(entry,"en") for entry in content["about"]["paragraphsEn"][:2])
home_services=[]
for service in content["services"]["items"]:
    service_copy=''.join(p_html(paragraph,"tr") for paragraph in service["paragraphs"])
    home_services.append(f'<article class="home-service-row"><h3>{esc(service["title"])}</h3><div>{service_copy}</div></article>')
home_feature_tr=p_html(pvrv["tr"][0],"tr")
home_feature_en=p_html(pvrv["en"][0],"en")
home_body=f'''<div class="home-page"><div class="page-wrap"><section class="home-hero"><div class="home-hero-copy"><h1><span class="lang-tr">{esc(content['home']['titleTr'])}</span><span class="lang-en">{esc(content['home']['titleEn'])}</span></h1><p><span class="lang-tr">{esc(content['home']['bodyTr'])}</span><span class="lang-en">{esc(content['home']['bodyEn'])}</span></p><div class="home-actions"><a class="button button-primary" href="products.html"><span class="lang-tr">Ürünler</span><span class="lang-en">Products</span></a><a class="button" href="calculator.html"><span class="lang-tr">Hesaplama</span><span class="lang-en">Calculator</span></a><a class="button" href="contact.html#contact-form"><span class="lang-tr">Randevu Oluştur</span><span class="lang-en">Appointment</span></a></div></div><figure class="home-hero-media"><img src="assets/images/home.jpeg" alt="NarTech Depolama Tankı ve Terminal Ekipmanları Sahası" width="1170" height="525" fetchpriority="high" decoding="async"></figure></section>
<section class="home-feature-section"><article class="home-feature"><div><div class="home-feature-category"><span class="lang-tr">{esc(category_title(categories[0],"tr"))}</span><span class="lang-en">{esc(category_title(categories[0],"en"))}</span></div><h2><a href="products/{esc(pvrv['id'])}.html"><span class="lang-tr">{esc(title_for(pvrv,"tr"))}</span><span class="lang-en">{esc(title_for(pvrv,"en"))}</span></a></h2></div><div class="lang-tr">{home_feature_tr}</div><div class="lang-en">{home_feature_en}</div></article></section>
<section class="home-section home-products-section"><div class="home-section-heading"><h2><span class="lang-tr">Ürünler</span><span class="lang-en">Products</span></h2></div><nav class="home-category-grid" aria-label="Ürünler">{''.join(home_categories)}</nav></section>
<section class="home-about-section"><div class="home-about-heading"><h2><span class="lang-tr">Hakkımızda</span><span class="lang-en">About Us</span></h2><a class="home-section-link" href="about.html"><span class="lang-tr">Hakkımızda</span><span class="lang-en">About Us</span><span aria-hidden="true">↗</span></a></div><div class="home-about-copy"><div class="lang-tr">{home_about_tr}</div><div class="lang-en">{home_about_en}</div></div></section>
<section class="home-section home-services-section"><div class="home-section-heading"><h2><span class="lang-tr">Hizmetler</span><span class="lang-en">Services</span></h2><a class="home-section-link" href="services.html"><span class="lang-tr">Hizmetler</span><span class="lang-en">Services</span><span aria-hidden="true">↗</span></a></div><div class="home-service-list">{''.join(home_services)}</div></section></div></div>'''
(OUT/"index.html").write_text(layout(content["home"]["titleTr"],home_body,"home"),encoding="utf-8")
# Keep the fallback free of copy that is not supplied in the source documents.
(OUT/"404.html").write_text('<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=./index.html"></head><body></body></html>',encoding="utf-8")

# About and services: exact text from their source documents.
about_intro_tr=''.join(p_html(x,"tr") for x in content["about"]["paragraphsTr"][:2])
about_intro_en=''.join(p_html(x,"en") for x in content["about"]["paragraphsEn"][:2])
about_rest_tr=''.join(p_html(x,"tr") for x in content["about"]["paragraphsTr"][2:])
about_rest_en=''.join(p_html(x,"en") for x in content["about"]["paragraphsEn"][2:])
about_body=f'''<div class="page-wrap"><div class="page-heading"><h1><span class="lang-tr">{esc(about[0].split('/')[0].strip(' :'))}</span><span class="lang-en">{esc(about[6])}</span></h1></div><section class="about-intro"><article class="about-intro-copy"><div class="lang-tr">{about_intro_tr}</div><div class="lang-en">{about_intro_en}</div></article><figure class="about-media"><img src="assets/images/home.jpeg" alt="NarTech Depolama Tankı ve Terminal Ekipmanları Sahası" width="1170" height="525" loading="lazy" decoding="async"></figure></section><article class="copy-section"><div class="lang-tr">{about_rest_tr}</div><div class="lang-en">{about_rest_en}</div></article></div>'''
(OUT/"about.html").write_text(layout(about[0],about_body,"about"),encoding="utf-8")
service_cards=[]
for service in content["services"]["items"]:
    paragraphs_html=''.join(f'<p data-source="{esc(paragraph["source"])}">{esc(paragraph["text"])}</p>' for paragraph in service["paragraphs"])
    service_cards.append(f'<details class="service-item"><summary data-source="{esc(service["titleSource"])}">{esc(service["title"])}</summary>{paragraphs_html}</details>')
services_body=f'''<div class="page-wrap"><div class="page-heading"><h1>{esc(services[0])}</h1></div><div class="service-list">{''.join(service_cards)}</div></div>'''
(OUT/"services.html").write_text(layout(services[0],services_body,"services"),encoding="utf-8")

# Main product page: category list with keyboard accessible, native, right-indented details.
index_links=[]
category_details=[]
for n,cat in enumerate(categories,1):
    index_links.append(f'<a href="#{esc(cat["id"])}"><span class="lang-tr">{esc(category_title(cat,"tr"))}</span><span class="lang-en">{esc(category_title(cat,"en"))}</span></a>')
    children=[]
    for obj in cat["items"]:
        if obj["children"]:
            children.append(branch_for(obj,""))
        else:
            children.append(link_for(obj,""))
    intro=''.join(p_html(entry,"tr") for entry in cat.get("description",[]))
    category_label=f'<span class="lang-tr">{esc(category_title(cat,"tr"))}</span><span class="lang-en">{esc(category_title(cat,"en"))}</span>'
    if not children and not intro:
        category_details.append(f'<div class="tree-root-label" id="{esc(cat["id"])}">{category_label}</div>')
    else:
        category_details.append(f'''<details class="tree-group" id="{esc(cat['id'])}"><summary>{category_label}</summary><div class="tree-children"><div class="tree-copy">{intro}</div>{''.join(children)}</div></details>''')
product_standards_tr=ref(product_lines.index(197))
product_standards_en=ref(product_lines.index(198))
product_standards_note=f'<section class="copy-section"><div class="lang-tr">{p_html(product_standards_tr,"tr")}</div><div class="lang-en">{p_html(product_standards_en,"en")}</div></section>'
products_body=f'''<div class="page-wrap catalog-page"><div class="page-heading"><h1><span class="lang-tr">Ürünler</span><span class="lang-en">Products</span></h1></div><div class="catalog-layout"><nav class="catalog-index" aria-label="Ürünler">{''.join(index_links)}</nav><div class="catalog-content">{''.join(category_details)}</div></div>{product_standards_note}</div>'''
(OUT/"products.html").write_text(layout("Ürünler",products_body,"products"),encoding="utf-8")

# Category pages show product names; detail pages include each mapped source paragraph.
for cat in categories:
    prefix="../"
    child_nodes=[]
    for obj in cat["items"]:
        child_nodes.append(obj)
    cat_nav=[]
    for n,other in enumerate(categories,1):
        label=f'<span class="lang-tr">{esc(category_title(other,"tr"))}</span><span class="lang-en">{esc(category_title(other,"en"))}</span>'
        cat_nav.append(f'<a href="{prefix}categories/{esc(other["id"])}.html"'+(' aria-current="location"' if other is cat else '')+f'>{label}</a>')
    category_items=[]
    for obj in child_nodes:
        category_items.append(f'<a class="product-card" href="{prefix}products/{esc(obj["id"])}.html"><span class="product-card-media" aria-hidden="true"></span><h2>{esc(title_for(obj,"tr"))}</h2></a>')
    if category_items:
        intro=''.join(p_html(entry,"tr") for entry in cat.get("description",[]))
        content_html=f'<div class="category-intro">{intro}</div><div class="product-grid">{"".join(category_items)}</div>'
    else:
        intro=''.join(p_html(entry,"tr") for entry in cat.get("description",[]))
        content_html=f'<div class="category-feature-layout"><div class="category-media" aria-hidden="true"></div><div class="category-intro">{intro}</div></div>' if intro else ''
    body=f'''<div class="page-wrap catalog-page"><div class="breadcrumbs"><a href="{prefix}products.html"><span class="lang-tr">Ürünler</span><span class="lang-en">Products</span></a></div><div class="page-heading"><h1 id="{esc(cat['id'])}"><span class="lang-tr">{esc(category_title(cat,"tr"))}</span><span class="lang-en">{esc(category_title(cat,"en"))}</span></h1></div><div class="catalog-layout"><nav class="catalog-index" aria-label="Ürünler">{''.join(cat_nav)}</nav><div class="catalog-content">{content_html}</div></div></div>'''
    (OUT/"categories"/(cat["id"]+".html")).write_text(layout(category_title(cat,"tr"),body,"products",prefix),encoding="utf-8")

# Flatten only the supplied hierarchy so each existing product title has a detail URL.
def flatten(nodes):
    for node in nodes:
        yield node
        yield from flatten(node["children"])

for generated_page in (OUT/"products").glob("*.html"):
    generated_page.unlink()
for cat in categories:
    all_nodes=list(flatten(cat["items"]))
    for obj in all_nodes:
        if obj["children"] and not obj["tr"] and not obj["en"]:
            # A source-defined grouping: display its children on the page without invented prose.
            children=''.join(link_for(child,prefix) for child in obj["children"])
            content_html=f'<div class="product-child-list">{children}</div>'
        else:
            tr_html=''.join(p_html(x,"tr") for x in obj["tr"])
            en_html=''.join(p_html(x,"en") for x in obj["en"])
            content_html=f'<div class="lang-tr">{tr_html}</div><div class="lang-en">{en_html or tr_html}</div>'
            if obj["children"]:
                content_html+=f'<div class="product-child-list">'+''.join(link_for(child,prefix) for child in obj["children"])+"</div>"
        title_tr=title_for(obj,"tr")
        title_en=title_for(obj,"en")
        product_content=f'<div class="detail-layout"><div class="detail-media" aria-hidden="true"></div><article class="product-copy"><h1><span class="lang-tr">{esc(title_tr)}</span><span class="lang-en">{esc(title_en or title_tr)}</span></h1>{content_html}<a class="button quote-action" href="../contact.html?product={esc(obj["id"])}"><span class="lang-tr">Gönder</span><span class="lang-en">Send</span></a></article></div>' if not obj["children"] else f'<article class="product-copy"><h1><span class="lang-tr">{esc(title_tr)}</span><span class="lang-en">{esc(title_en or title_tr)}</span></h1>{content_html}<a class="button quote-action" href="../contact.html?product={esc(obj["id"])}"><span class="lang-tr">Gönder</span><span class="lang-en">Send</span></a></article>'
        detail=f'''<div class="page-wrap product-detail"><div class="breadcrumbs"><a href="../products.html"><span class="lang-tr">Ürünler</span><span class="lang-en">Products</span></a> / <a href="../categories/{esc(cat['id'])}.html"><span class="lang-tr">{esc(category_title(cat,"tr"))}</span><span class="lang-en">{esc(category_title(cat,"en"))}</span></a></div>{product_content}</div>'''
        (OUT/"products"/(obj["id"]+".html")).write_text(layout(title_tr,detail,"products","../"),encoding="utf-8")

# API 2000 form — formula and disclaimer are supplied by the user.
calculator_body='''<div class="page-wrap form-page"><div class="page-heading"><h1><span class="lang-tr">API 2000 Hesaplama</span><span class="lang-en">API 2000 Calculator</span></h1></div><div class="steps"><span class="step-indicator" data-step-indicator="1" aria-current="step">1</span><span class="step-indicator" data-step-indicator="2">2</span><span class="step-indicator" data-step-indicator="3">3</span></div><section class="form-panel" id="calc-step-email"><form id="calc-email-form" class="form-grid"><div class="form-field"><label for="calc-email">E-posta</label><input id="calc-email" name="email" type="email" autocomplete="email" required></div><button class="button button-primary" type="submit">Devam</button></form></section><section class="form-panel" id="calc-step-inputs" hidden><form id="calc-input-form" class="form-grid"><div class="form-field"><label for="tank-capacity">Tank Capacity (m³)</label><input id="tank-capacity" name="tank_capacity_m3" type="number" min="0.01" step="any" required></div><div class="form-field"><label for="fill-rate">Max Fill Rate (m³/h)</label><input id="fill-rate" name="max_fill_rate_m3h" type="number" min="0" step="any" required></div><div class="form-field"><label for="empty-rate">Max Empty Rate (m³/h)</label><input id="empty-rate" name="max_empty_rate_m3h" type="number" min="0" step="any" required></div><div class="form-field"><label for="flash-point">Product Flash Point Above 37°C</label><select id="flash-point" name="product_flash_point_above_37c"><option value="true">True</option><option value="false">False</option></select></div><div><button class="button button-primary" type="submit">Hesapla</button></div></form></section><section class="form-panel" id="calc-step-results" hidden><div id="calc-results" class="calc-results"></div><p class="legal-copy">Yasal Uyarı ve Sorumluluk Reddi: Bu raporda sunulan tüm hesaplamalar, veriler ve sonuçlar yalnızca bilgi amaçlıdır ve hiçbir şekilde mühendislik veya ticari açıdan bağlayıcılığı yoktur. Kesin ekipman seçimi, boyutlandırma ve projelendirme aşamalarında saha koşulları, meteorolojik veriler, boru hattı dinamikleri ve yerel/uluslararası standartlar göz önünde bulundurularak doğrulama yapılması gerekmektedir.</p><button class="button button-primary" id="calc-send" type="button">Gönder</button><p class="form-status" id="calc-status" role="status" aria-live="polite"></p><button class="button" id="calc-back" type="button">Geri</button></section></div>'''
(OUT/"calculator.html").write_text(layout("API 2000 Hesaplama",calculator_body,"calculator"),encoding="utf-8")

contact_body='''<div class="page-wrap form-page"><div class="page-heading"><h1><span class="lang-tr">İletişim</span><span class="lang-en">Contact</span></h1></div><div class="form-panel"><form id="contact-form" class="form-grid"><input name="product" id="contact-product" type="hidden"><div class="form-field"><label for="contact-name"><span class="lang-tr">Ad Soyad</span><span class="lang-en">Name Surname</span></label><input id="contact-name" name="name" autocomplete="name" required></div><div class="form-field"><label for="contact-phone"><span class="lang-tr">Telefon No</span><span class="lang-en">Phone</span></label><input id="contact-phone" name="phone" type="tel" autocomplete="tel" required></div><div class="form-field"><label for="contact-message"><span class="lang-tr">Açıklama</span><span class="lang-en">Description</span></label><textarea id="contact-message" name="description" required></textarea></div><button class="button button-primary" type="submit"><span class="lang-tr">Gönder</span><span class="lang-en">Send</span></button><p class="form-status" id="contact-status" role="status" aria-live="polite"></p></form></div></div>'''
(OUT/"contact.html").write_text(layout("İletişim",contact_body,"contact"),encoding="utf-8")

# FAQ questions are phrased from supplied product information; answers remain source text.
pvrv_sizing_tr=ref(4)
pvrv_sizing_en=ref(9)
faq_entries=[
    ("Basınç vakum ventili hangi tanklarda kullanılır?","Which tanks use a pressure vacuum relief valve?",ref(3),ref(8)),
    ("PVRV kapasitesi hangi standarda göre belirlenir?","Which standard is used to size a PVRV?",pvrv_sizing_tr,pvrv_sizing_en),
    ("Basınç vakum ventili hangi tiplerde bulunur?","Which types of pressure vacuum valve are available?",ref(6),ref(11)),
    ("Alev tutucu hangi standarda göre tasarlanıp test edilir?","Which standard is used to design and test a flame arrester?",ref(14),ref(20)),
]
faq_items=[]
for question_tr,question_en,answer_tr,answer_en in faq_entries:
    questions=f'<span class="lang-tr">{esc(question_tr)}</span><span class="lang-en">{esc(question_en)}</span>'
    answers=f'<div class="lang-tr">{p_html(answer_tr,"tr")}</div><div class="lang-en">{p_html(answer_en,"en")}</div>'
    faq_items.append(f'<details class="faq-item"><summary>{questions}</summary><div class="faq-answer">{answers}</div></details>')
faq_body=f'''<div class="page-wrap"><div class="page-heading"><h1><span class="lang-tr">Sıkça Sorulan Sorular</span><span class="lang-en">FAQ</span></h1></div><section class="faq-list">{"".join(faq_items)}</section></div>'''
(OUT/"faq.html").write_text(layout("Sıkça Sorulan Sorular",faq_body,"faq"),encoding="utf-8")

# Sitemap uses the site origin already listed in robots.txt.
urls=['index.html','about.html','services.html','products.html','calculator.html','faq.html','contact.html']
urls += [f'categories/{c["id"]}.html' for c in categories]
urls += [f'products/{x["id"]}.html' for c in categories for x in flatten(c['items'])]
base_url='https://nartech.com.tr/'
sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{base_url if u == "index.html" else base_url + u}</loc></url>\n' for u in urls)+'</urlset>\n'
(OUT/"sitemap.xml").write_text(sitemap,encoding="utf-8")
print(f"Generated {len(urls)} source-backed pages.")
