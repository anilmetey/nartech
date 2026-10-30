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
about = paragraphs("Who We Are - About US.docx")
about_lines = source_lines("Who We Are - About US.docx")
what_we_do = paragraphs("What We Do (1).docx")
what_we_do_lines = source_lines("What We Do (1).docx")
services = paragraphs("Supervision Services.docx")
service_lines = source_lines("Supervision Services.docx")
product_text = paragraphs("Products (3).docx")
product_lines = source_lines("Products (3).docx")

# Turkish translations of English-only source paragraphs. The English source remains
# unchanged; these translations carry the same product and service information.
PRODUCT_TURKISH = {
    58: "Ponton Tipi Yüzer Tavan",
    59: "API 650 gibi uluslararası standartlara uygun olarak tasarlanıp tedarik edilen iç yüzer tavan (IFR), petrol ürünleri, yakıtlar ve kimyasallar için sabit çatılı depolama tanklarının içine yerleştirilen ve sıvı seviyesiyle birlikte yükselip alçalan hareketli bir platformdur.",
    60: "Platformun altındaki içi boş bölmeler (pontoonlar) buharı hapseder ve kaldırma kuvveti sağlayarak tavanın sıvı yüzeyinde dengeli biçimde yüzmesini sağlar. Bu, en yaygın ve çok yönlü tasarımdır.",
    61: "Temel İşlevler ve Faydalar",
    62: "Üstün Emisyon Azaltımı: Sıvı yüzeyi ile sabit tavan arasındaki buhar boşluğunu azaltarak ürünün buharlaşmasını ve uçucu organik bileşiklerin (VOC) atmosfere salınmasını etkili biçimde sınırlar.",
    63: "Çevre ve Çalışanların Korunması: Zararlı buhar salımını kontrol ederek çevreyi korur, yerel hava kirliliğini azaltır ve depolama tesisi çevresindeki güvenli çalışma koşullarını destekler.",
    64: "Dengeli Kararlılık ve Güvenlik: Entegre pontoonlar, tavanın dengeli ve güvenilir biçimde yüzmesini sağlar; yangın risklerini azaltır ve uzun ömürlü, çevreye duyarlı depolama çalışmalarını destekler.",
    65: "Tedarik ve Kalite Güvencemiz",
    66: "Güvenilir bir küresel tedarikçi olarak bu yüksek performanslı iç yüzer tavan sistemlerini API 650 dâhil uluslararası standartlara uygun biçimde tedarik ediyoruz.",
    67: "Sektör deneyimimiz ve küresel sertifikalı ürünlerimizle depolama tesisleriniz için yüksek güvenlik, çevre mevzuatına uyum ve uzun dönemli güvenilirlik sağlıyoruz.",
    68: "Tam Temas Tipi IFR",
    69: "API 650 gibi uluslararası standartlara uygun olarak tasarlanıp tedarik edilen iç yüzer tavan (IFR), petrol ürünleri, yakıtlar ve kimyasallar için sabit çatılı depolama tanklarının içine yerleştirilen ve sıvı seviyesiyle birlikte yükselip alçalan hareketli bir platformdur.",
    70: "Tam Temas Tipi: Platformun alt yüzeyi depolanan sıvıyla doğrudan ve tamamen temas eder; altında hava veya buhar boşluğu kalmaz. Bu yapı, buharlaşmayı en aza indirmek için yüksek uçuculuğa sahip ürünlerde uygundur.",
    71: "Temel İşlevler ve Faydalar",
    72: "Sıfıra Yakın VOC Emisyonu: Platform sıvıyla doğrudan ve tam temas ettiğinden emisyonları kontrol eder ve atmosfere buhar kaybını en aza indirerek çevre gerekliliklerini karşılamaya yardımcı olur.",
    73: "Çevrenin Korunması: Yüksek uçuculuğa sahip ürünler ve agresif kimyasallar için uygun olan bu yapı, zararlı buhar ve kokuların çevreye yayılmasını önlemeye yardımcı olur.",
    74: "Geliştirilmiş Güvenlik ve Buhar Kontrolü: Platform altındaki buhar boşluğunu ortadan kaldırarak patlayıcı gaz birikmesi riskini azaltır ve çevre ile çalışma alanı güvenliğini destekler.",
    75: "Tedarik ve Kalite Güvencemiz",
    76: "Güvenilir bir küresel tedarikçi olarak bu yüksek performanslı iç yüzer tavan sistemlerini API 650 dâhil uluslararası standartlara uygun biçimde tedarik ediyoruz.",
    77: "Sektör deneyimimiz ve küresel sertifikalı ürünlerimizle depolama tesisleriniz için yüksek güvenlik, çevre mevzuatına uyum ve uzun dönemli güvenilirlik sağlıyoruz.",
    78: "Chemraz XPE Contası",
    79: "Chemraz XPE contalar, IFR sistemlerinde en zorlu koşullarda dahi çok agresif kimyasallara ve yüksek sıcaklıklara karşı güçlü kimyasal dayanım ve ısıl kararlılık sağlar; sızıntıyı en aza indirir ve akışkan uyumluluğunu artırır.",
    80: "HDPE Contası",
    81: "Yüksek yoğunluklu polietilen (HDPE) esaslı elemanlar, IFR çevre sızdırmazlık uygulamalarında yüksek mekanik dayanım ve aşınma direnci sunarak uzun ömürlü ve güvenilir çalışmayı destekler.",
    82: "LDPE Contası",
    83: "Düşük yoğunluklu polietilen (LDPE) contalar, esnekliği ve buhar sızdırmazlığı sağlayan özellikleriyle IFR tavanlarında uçucu organik bileşik (VOC) emisyonlarını sınırlar ve çevresel güvenliği destekler.",
    85: "A Sabit Köpük Monitörü",
    86: "Sabit Köpük Monitörü, endüstriyel tesislerde ve tank çiftliklerinde büyük miktarda su-köpük çözeltisini uzak mesafelere hızla iletmek için kullanılan, yüksek kapasiteli ve sabit bir yangın söndürme cihazıdır.",
    87: "NFPA 11 Uyumu: Kritik risklere karşı uygun köpük tahliyesi, köpük örtüsü oluşumu ve hızlı yangın söndürme sağlamak üzere NFPA 11 standartlarına uygun tasarlanır.",
    88: "UL / FM Onayları: Önde gelen küresel güvenlik kuruluşları UL ve FM tarafından sertifikalandırılmıştır; acil müdahalede güvenilirliği, dayanıklılığı ve performansı güvence altına alır.",
    89: "B Köpük Yapıcı",
    90: "Köpük Yapıcı, düşük hızlı köpük akışının istendiği açık yüzer tavanlı depolama tanklarını korumak için kullanılan özel bir tahliye cihazıdır. Çalışma prensibi köpük odasına benzer; ancak köpük yapıcı, köpüğü depolamadan doğrudan akıtarak yanıcı sıvı yüzeylerini korumak üzere düşük genleşmeli köpük üretir.",
    91: "NFPA 11 Uyumu: Doğru hava-köpük emişi, düşük genleşmeli köpük üretimi ve güvenilir tahliye performansı sağlamak üzere NFPA 11 standartlarına uygun tasarlanır.",
    92: "UL / FM Onayları: UL ve FM sertifikaları üretim kalitesini, performansı ve kritik endüstriyel yangın koruma sistemlerindeki güvenliği destekler.",
    93: "C Köpük Karıştırıcı (Oranlayıcı)",
    94: "Köpük Karıştırıcı (oranlayıcı), acil durumda etkili bir köpük çözeltisi oluşturmak için su ile köpük konsantresini önceden belirlenmiş doğru oranda otomatik olarak karıştıran kritik bir yangın koruma cihazıdır.",
    95: "NFPA 11 Uyumu: Endüstriyel yangın söndürme sistemlerinde doğru oranlama, güvenilir çalışma ve uygun köpük çözeltisi iletimi sağlamak üzere NFPA 11 standartlarına uygun tasarlanır.",
    96: "UL / FM Onayları: UL ve FM sertifikaları tank çiftlikleri ve tesisler için üretim kalitesini, çalışma hassasiyetini ve güvenliği destekler.",
    97: "D Köpük Üstten Dökme Cihazı",
    98: "Köpük odası olarak da bilinen Köpük Üstten Dökme Cihazı, sabit çatılı depolama tanklarının gövdesine monte edilir ve genleşmiş yangın söndürme köpüğünü yanan sıvı yüzeyine doğrudan, sıvının içine dalmadan, nazikçe verir.",
    99: "NFPA 11 Uyumu: Yanıcı sıvı yüzeylerine uygun hava emişi, güvenilir düşük genleşmeli köpük üretimi ve doğru dağıtım sağlamak üzere NFPA 11 standartlarına uygun tasarlanır.",
    100: "UL / FM Onayları: UL ve FM sertifikaları tank çiftliklerinde üretim kalitesini, çalışma güvenilirliğini ve yangın güvenliğini destekler.",
    101: "E Kenar Sızdırmazlığı Köpük Dökme Cihazı",
    102: "Kenar Sızdırmazlığı Köpük Dökme Cihazı, dış yüzer tavanlı tankların dairesel kenar sızdırmazlık alanını korumak için tasarlanmış özel bir yangın koruma cihazıdır. Genleşmiş köpüğü, kenar yangınlarının görülme olasılığının en yüksek olduğu hassas sızdırmazlık bölgesine doğrudan iletir.",
    103: "NFPA 11 Uyumu: Sızdırmazlık alanına doğru hava emişi, güvenilir düşük genleşmeli köpük üretimi ve hedefli tahliye sağlamak üzere NFPA 11 standartlarına uygun tasarlanır.",
    104: "UL / FM Onayları: UL ve FM sertifikaları tank kenarı yangın koruması için üretim kalitesini, çalışma hassasiyetini ve güvenliği destekler.",
    105: "F Köpük Tankı",
    106: "Köpük Tankı (genellikle bladder tank oranlama sistemi), köpük konsantresini yangın koruma sisteminde depolayan ve acil durumda doğru oranda su hattına otomatik olarak veren, ön borulaması yapılmış basınçlı bir kaptır.",
    107: "NFPA 11 Uyumu: Endüstriyel yangın söndürme sistemlerinde doğru sıvı oranlama, bladder bütünlüğü ve güvenilir köpük çözeltisi üretimi sağlamak üzere NFPA 11 standartlarına uygun tasarlanır.",
    108: "UL / FM Onayları: UL ve FM sertifikaları depolama tankları ve tesislerde üretim kalitesini, çalışma hassasiyetini ve güvenliği destekler.",
    109: "G Köpük ve Su Sprinkleri",
    110: "Tank çiftliklerinde kullanılan köpük ve su sprinklerleri; pompa istasyonları, manifold alanları, tanker dolum sahaları ve ikincil sızdırmazlık havuzları gibi yüksek riskli çevre bölgelerini koruyan otomatik tahliye nozullarıdır. Bu nozullar, eşit su püskürtmesi veya hava emişli köpük örtüsünü hızla iletir.",
    111: "UL / FM Onayları ve K-Faktörü Hassasiyeti: UL ve FM sertifikaları ile farklı hassas K-faktörü seçenekleri; doğru hidrolik tasarım hesaplarını, üretim kalitesini ve tank çiftliğinin kritik alanlarında kesintisiz korumayı destekler.",
    113: "A Köpük Pigleri",
    114: "B Katı Döküm Pigleri",
    115: "C Çelik Pigler",
    116: "Pig Sinyal Vericileri",
    117: "A Müdahalesiz Tip Pig Sinyal Vericisi",
    118: "B Müdahaleli Tip Pig Sinyal Vericisi",
    119: "4-Endüstriyel Susturucular",
    120: "Endüstriyel Susturucu; fan, blower ve egzoz sistemleri gibi ekipmanların oluşturduğu yüksek çalışma gürültüsünü önemli ölçüde azaltmak için tasarlanmış kritik bir ses kontrol cihazıdır. Gürültü seviyesini 85 dB'ye kadar düşürerek çalışanları iş güvenliği mevzuatına uygun biçimde işitme kaybı ve uzun vadeli sağlık risklerinden korur. Ayrıca çevresel gürültü kirliliğini azaltarak daha güvenli, verimli ve mevzuata uygun bir çalışma ortamı sağlar.",
    121: "5-Yüzer Emiş Üniteleri",
    122: "Yüzer Emiş Ünitesi, depolama tanklarında sıvıyı en temiz yüzey seviyesinden çekmek için tasarlanmış bir sistemdir; özellikle havacılık yakıtları ve kimyasallarda kullanılır. En temiz ürünün üst seviyeden alınmasını sağlayarak tankın dibinde biriken su, tortu ve çamurun pompalanmasını önler.",
    123: "A Boru Tipi Yüzer Emiş Ünitesi",
    124: "B Hortum Tipi Yüzer Emiş Ünitesi",
    125: "C Yağ Sıyırıcı",
    126: "6-Geri Sarmalı Topraklama Kablosu",
    127: "ATEX sertifikalı Geri Sarmalı Topraklama Makarası (RGR), API standartlarına uygun olarak yüzer tavanlı tanklardaki statik elektriği güvenli biçimde boşaltmak için tasarlanmıştır. Yüzer tavan ile tank gövdesi arasında doğrudan elektrik bağlantısı kurar; yıldırım sırasında akımın ve biriken yüklerin hızla toprağa iletilmesini sağlar.",
    128: "7-Dolum Kolları",
    129: "8-Endüstriyel Vanalar",
    130: "A Küresel Vanalar",
    131: "B Sürgülü Vanalar",
    132: "C Kelebek Vanalar",
    133: "9-Gaz Yıkama Sistemleri",
    134: "10-Seperatörler",
    135: "11-Rafineri Yedek Parçaları",
}

def ref(index: int) -> dict:
    return {"text": product_text[index], "source": f"Products (3).docx:{product_lines[index]}"}

def localized_ref(index: int, language: str) -> dict:
    entry = ref(index)
    if language == "tr" and index in PRODUCT_TURKISH:
        entry["text"] = PRODUCT_TURKISH[index]
    return entry

def text_at_product_line(line: int) -> str:
    return product_text[product_lines.index(line)]

def refs(indices, language="en"):
    return [localized_ref(i, language) for i in indices]

def item(id, title_tr=None, title_en=None, tr=None, en=None, children=None, src=None):
    def text_at(index, language):
        if index is None:
            return None
        if not isinstance(index, int):
            return index
        return PRODUCT_TURKISH.get(index, product_text[index]) if language == "tr" else product_text[index]
    return {
        "id": id,
        "titleTr": text_at(title_tr, "tr"),
        "titleEn": text_at(title_en, "en"),
        "tr": refs(tr or [], "tr"),
        "en": refs(en or []),
        "children": children or [],
        "source": src,
    }

# The category order and all product wording come from Products (3).docx.
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
emergency["tr"][-1]["text"] = product_text[41].split("\n\nEmergency Relief Valve\n", 1)[0]
emergency["en"].insert(0, {"text": emergency_en_first, "source": f"Products (3).docx:{product_lines[41]}"})
emergency["navTitleEn"] = text_at_product_line(56)
gauge = item("gauge-hatch", 46, 52, [47, 48, 49, 50, 51], [53, 54, 55, 56], src=45)
gauge["en"].append({"text": "Available in locked, unlocked, and closed-to-atmosphere types.", "source": f"Products (3).docx:{product_lines[51]}"})
gauge["navTitleEn"] = text_at_product_line(70)

floating_children = [
    item("pontoon-type-ifr", 58, "Pontoon Type IFR", [59, 60, 61, 62, 63, 64, 65, 66, 67], [59, 60, 61, 62, 63, 64, 65, 66, 67], src=57),
    item("full-contact-type-ifr", 68, 68, [69, 70, 71, 72, 73, 74, 75, 76, 77], [69, 70, 71, 72, 73, 74, 75, 76, 77], src=68),
    item("chemraz-xpe-seal", 78, 78, [79], [79], src=78),
    item("hdpe-seal", 80, 80, [81], [81], src=80),
    item("ldpe-seal", 82, 82, [83], [83], src=82),
]
floating_roofs = item("internal-floating-roofs-and-seals", 57, None, [], [], floating_children, 56)
floating_roofs["titleTr"] = "İç Yüzer Tavanlar ve Fitiller"
floating_roofs["titleEn"] = "Internal Floating Roofs and Seals"
floating_suction_children = [
    item("pipe-type-floating-suction-unit", 123, 123, [], [], src=122),
    item("hose-type-floating-suction-unit", 124, 124, [], [], src=123),
    item("oil-skimmer", 125, 125, [], [], src=124),
]

fire_items = [
    item("fixed-foam-monitor", 85, 85, [86, 87, 88], [86, 87, 88], src=84),
    item("foam-maker", 89, 89, [90, 91, 92], [90, 91, 92], src=88),
    item("foam-mixer-proportioner", 93, 93, [94, 95, 96], [94, 95, 96], src=92),
    item("foam-top-pourer", 97, 97, [98, 99, 100], [98, 99, 100], src=96),
    item("rim-seal-foam-pourer", 101, 101, [102, 103, 104], [102, 103, 104], src=100),
    item("foam-tanks", 105, 105, [106, 107, 108], [106, 107, 108], src=104),
    item("foam-water-sprinkler", 109, 109, [110, 111], [110, 111], src=108),
]
pig_signallers = item("pig-signallers", 116, 116, [], [], [
    item("non-intrusive-pig-signaller", 117, 117, [], [], src=116),
    item("intrusive-pig-signaller", 118, 118, [], [], src=116),
], 115)
pig_signallers["titleEn"] = "Pig Signallers"
valve_items = [
    item("ball-valves", 130, 130, [], [], src=129),
    item("gate-valves", 131, 131, [], [], src=130),
    item("butterfly-valves", 132, 132, [], [], src=131),
]

categories = [
    {"id":"storage-tank-equipments", "title":ref(0), "items":[pvrv, inline, endline, emergency, gauge, floating_roofs]},
    {"id":"fire-fighting-equipments", "title":ref(84), "items":fire_items},
    {"id":"pig-cleaning-equipments", "title":ref(112), "items":[
        item("foam-pigs",113,113,[],[],src=112), item("solid-cast-pigs",114,114,[],[],src=113),
        item("steel-pigs",115,115,[],[],src=114), pig_signallers]},
    {"id":"industrial-silencers", "title":ref(119), "items":[], "descriptionTr":refs([120],"tr"), "descriptionEn":refs([120])},
    {"id":"floatin-suction-units", "title":ref(121), "items":floating_suction_children, "descriptionTr":refs([122],"tr"), "descriptionEn":refs([122])},
    {"id":"retractable-grounding-cable", "title":ref(126), "items":[], "descriptionTr":refs([127],"tr"), "descriptionEn":refs([127])},
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
    category["titleEn"] = category["titleEn"].removeprefix("-")

def category_title(category, language):
    if language != "en":
        return category["titleTr"]
    return category["titleEn"].strip().rstrip(":").strip()

# Persist only the concise copy used by the pages.
content = {
    "home":{"titleTr":home[0],"bodyTr":home[1],"titleEn":home[2],"bodyEn":home[3]},
    "about":{"titleTr":about[0],"paragraphsTr":[{"text":about[i],"source":f"Who We Are - About US.docx:{about_lines[i]}"} for i in range(1,6)],"titleEn":about[6],"paragraphsEn":[{"text":about[i],"source":f"Who We Are - About US.docx:{about_lines[i]}"} for i in range(7,12)]},
    "whatWeDo":{"titleTr":what_we_do[0],"paragraphsTr":[{"text":what_we_do[i],"source":f"What We Do (1).docx:{what_we_do_lines[i]}"} for i in range(1,5)],"titleEn":what_we_do[5],"paragraphsEn":[{"text":what_we_do[i],"source":f"What We Do (1).docx:{what_we_do_lines[i]}"} for i in range(6,10)]},
    "services":{
        "titleTr":services[0],
        "titleEn":"FIELD SUPERVISION SERVICE",
        "items":[
            {"title":services[1],"titleEn":"1. Pressure Vacuum Relief Valve (PVRV) Set Point Inspection","titleSource":f"Supervision Services.docx:{service_lines[1]}","paragraphs":[
                {"text":services[2],"textEn":"Pressure vacuum relief valves are critical safety devices that prevent tanks from deforming or rupturing under excessive pressure or vacuum.","source":f"Supervision Services.docx:{service_lines[2]}"},
                {"text":services[3],"textEn":"Physical and Functional Inspection","source":f"Supervision Services.docx:{service_lines[3]}"}
            ]},
            {"title":services[4],"titleEn":"2. Internal Floating Roof (IFR) Inspection","titleSource":f"Supervision Services.docx:{service_lines[4]}","paragraphs":[
                {"text":services[5],"textEn":"Internal floating roofs are used to reduce volatile organic compound (VOC) emissions and product loss, and require precise mechanical installation.","source":f"Supervision Services.docx:{service_lines[5]}"},
                {"text":services[6],"textEn":"Sealing Elements and Equipment: The installation quality of rim seals, correct positioning of leg settings, and operability of drainage systems are inspected.","source":f"Supervision Services.docx:{service_lines[6]}"}
            ]},
            {"title":services[7],"titleEn":"3. External Floating Roof (IFR) Inspection","titleSource":f"Supervision Services.docx:{service_lines[7]}","paragraphs":[
                {"text":services[8],"textEn":"External floating roofs are used to reduce volatile organic compound (VOC) emissions and product loss, and require precise mechanical installation.","source":f"Supervision Services.docx:{service_lines[8]}"},
                {"text":services[9],"textEn":"Sealing Elements and Equipment: The installation quality of rim seals is inspected.","source":f"Supervision Services.docx:{service_lines[9]}"}
            ]}
        ]
    },
    "categories":categories,
}
(OUT / "content" / "site-content.json").write_text(json.dumps(content,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def esc(value) -> str:
    return html.escape(str(value or ""), quote=True)

def nav(prefix: str, current: str) -> str:
    entries = [
        ("home","index.html","Ana Sayfa","Home"),
        ("about","about.html","Hakkımızda","Who We Are"),
        ("what-we-do","what-we-do.html","Ne Yapıyoruz","What We Do"),
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
    links.append(f'<a class="mobile-nav-brand" href="{prefix}index.html" aria-label="NarTech ana sayfa" data-aria-tr="NarTech ana sayfa" data-aria-en="NarTech home page"><img src="{prefix}assets/images/nartech-logo-transparent.png" width="1958" height="803" alt="NarTech"></a>')
    return "\n".join(links)

def footer(prefix: str) -> str:
    entries = [
        ("index.html", "Ana Sayfa", "Home"),
        ("about.html", "Hakkımızda", "Who We Are"),
        ("what-we-do.html", "Ne Yapıyoruz", "What We Do"),
        ("products.html", "Ürünler", "Products"),
        ("services.html", "Hizmetler", "Services"),
        ("calculator.html", "Hesaplama", "Calculator"),
        ("faq.html", "SSS", "FAQ"),
    ]
    links = "".join(f'<li><a href="{prefix}{path}"><span class="lang-tr">{esc(tr)}</span><span class="lang-en">{esc(en)}</span></a></li>' for path, tr, en in entries)
    return f'''<footer class="site-footer" role="contentinfo"><div class="footer-inner">
<section class="footer-brand-block"><a class="footer-brand" href="{prefix}index.html" aria-label="NarTech ana sayfa" data-aria-tr="NarTech ana sayfa" data-aria-en="NarTech home page"><img src="{prefix}assets/images/logo-white.png" width="1024" height="472" alt="NarTech"></a><p class="footer-tagline"><span class="footer-tagline-dot" aria-hidden="true"></span><span class="lang-tr">{esc(content['home']['titleTr'])}</span><span class="lang-en">{esc(content['home']['titleEn'])}</span></p></section>
<nav class="footer-group footer-site" aria-label="Hızlı Erişim" data-aria-tr="Hızlı Erişim" data-aria-en="Quick Links"><svg class="footer-orbit" viewBox="0 0 1000 1000" preserveAspectRatio="none" aria-hidden="true" focusable="false"><rect x="6" y="6" width="988" height="988" rx="24" pathLength="1000"/></svg><h2 class="footer-heading"><span class="lang-tr">Hızlı Erişim</span><span class="lang-en">Quick Links</span></h2><ul class="footer-links">{links}</ul></nav>
<nav class="footer-group footer-contact" aria-label="İletişim" data-aria-tr="İletişim" data-aria-en="Contact"><h2 class="footer-heading"><span class="lang-tr">İletişim</span><span class="lang-en">Contact</span></h2><a class="footer-cta" href="{prefix}contact.html#contact-form"><span class="lang-tr">Teklif Gönder</span><span class="lang-en">Send Request</span><span aria-hidden="true">↗</span></a></nav>
</div></footer>'''

def layout(title: str, body: str, current: str, prefix="", lang="tr", title_en=None) -> str:
    css_version = "naragro-home-flow-20261030-9" if current == "home" else "naragro-footer-responsive-20261030-6"
    js_version = "nartech-localization-20261030-1"
    title_en = title_en or title
    return f'''<!doctype html>
<html lang="{lang}" data-language="tr" data-title-tr="{esc(title)} | NarTech" data-title-en="{esc(title_en)} | NarTech">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} | NarTech</title>
<link rel="stylesheet" href="{prefix}assets/css/main.css?v={css_version}">
<script defer src="{prefix}assets/js/app.js?v={js_version}"></script>
</head>
<body>
<header class="site-header"><div class="header-inner"><a class="brand" href="{prefix}index.html" aria-label="NarTech" data-aria-tr="NarTech" data-aria-en="NarTech"><img src="{prefix}assets/images/nartech-logo-transparent.png" width="1958" height="803" alt="NarTech"></a><button class="nav-toggle" type="button" data-nav-toggle aria-controls="site-nav" aria-expanded="false" aria-label="Menüyü Aç" data-open-label-tr="Menüyü Aç" data-open-label-en="Open menu" data-close-label-tr="Menüyü Kapat" data-close-label-en="Close menu"><span></span><span></span><span></span></button><nav class="site-nav" id="site-nav" aria-label="Site" data-aria-tr="Site" data-aria-en="Navigation">{nav(prefix,current)}</nav></div></header>
<button class="nav-backdrop" type="button" data-nav-close tabindex="-1" aria-hidden="true"></button>
<main>{body}</main>{footer(prefix)}</body></html>'''

def p_html(entry: dict, lang: str) -> str:
    return f'<p data-source="{esc(entry["source"])}">{esc(entry["text"])}</p>'

def title_for(obj: dict, lang: str) -> str:
    key="titleEn" if lang=="en" and obj.get("titleEn") else "titleTr"
    value = obj.get(key) or obj.get("titleEn") or ""
    return value.lstrip("-").strip().rstrip(":").strip() if lang == "en" else value

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

# Homepage proof strip
home_proof_items=[
    ("MÜHENDİSLİK DENEYİMİ","ENGINEERING EXPERIENCE","10+ Yıl","10+ Years","Sektörel Mühendislik Deneyimi","Industrial Engineering Experience"),
    ("ULUSLARARASI STANDARTLAR","INTERNATIONAL STANDARDS","API & EN","API & EN","API 650, 2000 ve EN ISO 16852 Uyumu","API 650, 2000 and EN ISO 16852 Compliance"),
    ("EMNİYET & YANGIN SERTİFİKASYONU","SAFETY & FIRE CERTIFICATION","FM & ATEX","FM & ATEX","Patlayıcı Ortam ve Yangın Güvenliği","Explosive Atmosphere and Fire Safety"),
    ("PROJE & ŞARTNAME UYUMU","PROJECT SPECIFICATIONS","Özel Tasarım","Tailored Products","Müşteri şartnamelerine göre","To client specifications"),
]
home_proof_cards=[]
for index,(tr_kicker,en_kicker,tr_value,en_value,tr_detail,en_detail) in enumerate(home_proof_items):
    if index == 0:
        tr_value_html=f'<span class="lang-tr" data-count-up="10" data-count-suffix="+ Yıl">{esc(tr_value)}</span>'
        en_value_html=f'<span class="lang-en" data-count-up="10" data-count-suffix="+ Years">{esc(en_value)}</span>'
    else:
        tr_value_html=f'<span class="lang-tr">{esc(tr_value)}</span>'
        en_value_html=f'<span class="lang-en">{esc(en_value)}</span>'
    home_proof_cards.append(f'<div class="home-proof-item" style="--proof-delay:{index*110}ms"><span class="home-proof-kicker"><span aria-hidden="true"></span><span class="lang-tr">{esc(tr_kicker)}</span><span class="lang-en">{esc(en_kicker)}</span></span><strong class="home-proof-value">{tr_value_html}{en_value_html}</strong><span class="home-proof-detail"><span class="lang-tr">{esc(tr_detail)}</span><span class="lang-en">{esc(en_detail)}</span></span></div>')
home_proof_html=''.join(home_proof_cards)
home_about_tr=''.join(p_html(x,"tr") for x in content["about"]["paragraphsTr"][:2])
home_about_en=''.join(p_html(x,"en") for x in content["about"]["paragraphsEn"][:2])
home_flow_items=[
    ("Standartlar", "International Standards", "Güvenlik · kalite · performans", "Safety · quality · performance", "What We Do (1).docx:2", "What We Do (1).docx:7"),
    ("Teknik Gereksinimler", "Technical Requirements", "Proje ihtiyaçları · özel şartnameler", "Project needs · specific specifications", "What We Do (1).docx:3", "What We Do (1).docx:8"),
    ("Mühendislik Uzmanlığı", "Engineering Expertise", "Teknik bilgi birikimi · uluslararası iş ortaklıkları", "Technical know-how · international partnerships", "What We Do (1).docx:4", "What We Do (1).docx:9"),
    ("Doğru Ürün", "The Right Product", "Operasyonel verimlilik · uzun vadeli değer", "Operational efficiency · long-term value", "What We Do (1).docx:5", "What We Do (1).docx:10"),
]
home_flow_card_items=[]
for index,(title_tr,title_en,detail_tr,detail_en,source_tr,source_en) in enumerate(home_flow_items):
    home_flow_card_items.append(f'''<article class="home-flow-card" role="listitem" style="--flow-delay:{index*55}ms" data-source="{esc(source_tr)}"><h3><span class="lang-tr">{esc(title_tr)}</span><span class="lang-en" data-source="{esc(source_en)}">{esc(title_en)}</span></h3><p><span class="lang-tr">{esc(detail_tr)}</span><span class="lang-en">{esc(detail_en)}</span></p></article>''')
home_flow_cards=''.join(home_flow_card_items)
home_flow_desktop_paths=[
    "M125 144 C125 180 385 174 482 232",
    "M375 144 C375 178 445 187 492 232",
    "M625 144 C625 178 555 187 508 232",
    "M875 144 C875 180 615 174 518 232",
]
home_flow_mobile_paths=[
    "M250 136 C250 204 420 245 490 326",
    "M750 136 C750 204 580 245 510 326",
    "M250 264 C250 288 430 306 492 326",
    "M750 264 C750 288 570 306 508 326",
]
def flow_svg_paths(paths, output_path):
    source_paths=''.join(f'<path class="home-flow-track" d="{path}"/><path class="home-flow-particles" d="{path}" style="--flow-delay:{.3+index*.14:.2f}s"/>' for index,path in enumerate(paths))
    return f'{source_paths}<path class="home-flow-track" d="{output_path}"/><path class="home-flow-particles home-flow-particles--output" d="{output_path}" style="--flow-delay:.82s"/>'
home_flow_desktop_svg=flow_svg_paths(home_flow_desktop_paths,"M500 272 C500 302 500 328 500 354")
home_flow_mobile_svg=flow_svg_paths(home_flow_mobile_paths,"M500 366 C500 383 500 400 500 418")
home_flow_graphic=f'''<svg class="home-flow-lines home-flow-lines--desktop" viewBox="0 0 1000 464" preserveAspectRatio="none" aria-hidden="true">{home_flow_desktop_svg}</svg><svg class="home-flow-lines home-flow-lines--mobile" viewBox="0 0 1000 500" preserveAspectRatio="none" aria-hidden="true">{home_flow_mobile_svg}</svg>'''
home_body=f'''<div class="home-page"><div class="page-wrap"><section class="home-hero"><div class="home-hero-copy"><h1><span class="lang-tr">{esc(content['home']['titleTr'])}</span><span class="lang-en">{esc(content['home']['titleEn'])}</span></h1><p><span class="lang-tr">{esc(content['home']['bodyTr'])}</span><span class="lang-en">{esc(content['home']['bodyEn'])}</span></p><div class="home-actions"><a class="button button-primary" href="products.html"><span class="lang-tr">Ürünler</span><span class="lang-en">Products</span></a><a class="button" href="calculator.html"><span class="lang-tr">Hesaplama</span><span class="lang-en">Calculator</span></a><a class="button" href="contact.html#contact-form"><span class="lang-tr">Randevu Oluştur</span><span class="lang-en">Book an Appointment</span></a></div></div><figure class="home-hero-media"><img src="assets/images/home.jpeg" alt="NarTech Depolama Tankı ve Terminal Ekipmanları Sahası" data-alt-tr="NarTech Depolama Tankı ve Terminal Ekipmanları Sahası" data-alt-en="NarTech storage tank and terminal equipment facility" width="1170" height="525" fetchpriority="high" decoding="async"></figure></section>
<section class="home-proof-strip" aria-label="Mühendislik Göstergeleri" data-aria-tr="Mühendislik Göstergeleri" data-aria-en="Engineering Indicators">{home_proof_html}</section>
<section class="home-who-section" aria-labelledby="home-who-heading"><div class="home-who-heading"><h2 id="home-who-heading"><span class="lang-tr">Hakkımızda</span><span class="lang-en">Who We Are</span></h2></div><div class="home-who-copy"><div class="lang-tr">{home_about_tr}</div><div class="lang-en">{home_about_en}</div></div></section>
<section class="home-what-section" aria-labelledby="home-what-heading"><div class="home-what-heading"><h2 id="home-what-heading"><span class="lang-tr">Ne Yapıyoruz</span><span class="lang-en">What We Do</span></h2><p class="home-what-subtitle"><span class="lang-tr">{esc(content['whatWeDo']['titleTr'])}</span><span class="lang-en">{esc(content['whatWeDo']['titleEn'].strip())}</span></p></div><div class="home-what-flow" data-home-flow><div class="home-flow-visual"><div class="home-flow-cards" role="list">{home_flow_cards}</div>{home_flow_graphic}<div class="home-flow-orbit" aria-hidden="true"></div><div class="home-flow-hub"><img src="assets/images/nartech-logo-transparent.png" width="1958" height="803" alt="NarTech"></div><div class="home-flow-output"><strong><span class="lang-tr">Mühendislik Çözümleri</span><span class="lang-en">Engineering Solutions</span></strong><span><span class="lang-tr">Güvenilir · verimli · sürdürülebilir</span><span class="lang-en">Reliable · efficient · sustainable</span></span></div></div></div></section></div></div>'''
(OUT/"index.html").write_text(layout(content["home"]["titleTr"],home_body,"home",title_en=content["home"]["titleEn"]),encoding="utf-8")
# Keep the fallback free of copy that is not supplied in the source documents.
(OUT/"404.html").write_text('<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=./index.html"></head><body></body></html>',encoding="utf-8")

# About and services: exact text from their source documents.
about_intro_tr=''.join(p_html(x,"tr") for x in content["about"]["paragraphsTr"][:2])
about_intro_en=''.join(p_html(x,"en") for x in content["about"]["paragraphsEn"][:2])
about_rest_tr=''.join(p_html(x,"tr") for x in content["about"]["paragraphsTr"][2:])
about_rest_en=''.join(p_html(x,"en") for x in content["about"]["paragraphsEn"][2:])
about_body=f'''<div class="page-wrap"><div class="page-heading"><h1><span class="lang-tr">{esc(about[0].split('/')[0].strip(' :'))}</span><span class="lang-en">{esc(about[6])}</span></h1></div><section class="about-intro"><article class="about-intro-copy"><div class="lang-tr">{about_intro_tr}</div><div class="lang-en">{about_intro_en}</div></article><figure class="about-media"><img src="assets/images/home.jpeg" alt="NarTech Depolama Tankı ve Terminal Ekipmanları Sahası" data-alt-tr="NarTech Depolama Tankı ve Terminal Ekipmanları Sahası" data-alt-en="NarTech storage tank and terminal equipment facility" width="1170" height="525" loading="lazy" decoding="async"></figure></section><article class="copy-section"><div class="lang-tr">{about_rest_tr}</div><div class="lang-en">{about_rest_en}</div></article></div>'''
(OUT/"about.html").write_text(layout(about[0],about_body,"about",title_en=about[6]),encoding="utf-8")

what_we_do_tr=''.join(p_html(entry,"tr") for entry in content["whatWeDo"]["paragraphsTr"])
what_we_do_en=''.join(p_html(entry,"en") for entry in content["whatWeDo"]["paragraphsEn"])
what_we_do_body=f'''<div class="page-wrap what-we-do-page"><div class="page-heading"><h1><span class="lang-tr">{esc(content["whatWeDo"]["titleTr"])}</span><span class="lang-en">{esc(content["whatWeDo"]["titleEn"])}</span></h1></div><section class="what-we-do-copy"><div class="lang-tr"><div class="what-we-do-grid">{what_we_do_tr}</div></div><div class="lang-en"><div class="what-we-do-grid">{what_we_do_en}</div></div></section></div>'''
(OUT/"what-we-do.html").write_text(layout(content["whatWeDo"]["titleTr"],what_we_do_body,"what-we-do",title_en="What We Do"),encoding="utf-8")

service_cards=[]
for service in content["services"]["items"]:
    paragraphs_html=''.join(f'<p data-source="{esc(paragraph["source"])}"><span class="lang-tr">{esc(paragraph["text"])}</span><span class="lang-en">{esc(paragraph["textEn"])}</span></p>' for paragraph in service["paragraphs"])
    service_cards.append(f'<details class="service-item" open><summary data-source="{esc(service["titleSource"])}"><span class="lang-tr">{esc(service["title"])}</span><span class="lang-en">{esc(service["titleEn"])}</span></summary>{paragraphs_html}</details>')
services_body=f'''<div class="page-wrap"><div class="page-heading"><h1><span class="lang-tr">{esc(content["services"]["titleTr"])}</span><span class="lang-en">{esc(content["services"]["titleEn"])}</span></h1></div><div class="service-list">{''.join(service_cards)}</div></div>'''
(OUT/"services.html").write_text(layout(content["services"]["titleTr"],services_body,"services",title_en=content["services"]["titleEn"]),encoding="utf-8")

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
    intro_tr=''.join(p_html(entry,"tr") for entry in cat.get("descriptionTr",[]))
    intro_en=''.join(p_html(entry,"en") for entry in cat.get("descriptionEn",[]))
    intro=f'<div class="lang-tr">{intro_tr}</div><div class="lang-en">{intro_en}</div>' if intro_tr or intro_en else ''
    category_label=f'<span class="lang-tr">{esc(category_title(cat,"tr"))}</span><span class="lang-en">{esc(category_title(cat,"en"))}</span>'
    if not children and not intro:
        category_details.append(f'<div class="tree-root-label" id="{esc(cat["id"])}">{category_label}</div>')
    else:
        category_details.append(f'''<details class="tree-group" id="{esc(cat['id'])}"><summary>{category_label}</summary><div class="tree-children"><div class="tree-copy">{intro}</div>{''.join(children)}</div></details>''')
product_standards_tr=ref(product_lines.index(197))
product_standards_en=ref(product_lines.index(198))
product_standards_note=f'<section class="copy-section"><div class="lang-tr">{p_html(product_standards_tr,"tr")}</div><div class="lang-en">{p_html(product_standards_en,"en")}</div></section>'
products_body=f'''<div class="page-wrap catalog-page"><div class="page-heading"><h1><span class="lang-tr">Ürünler</span><span class="lang-en">Products</span></h1></div><div class="catalog-layout"><nav class="catalog-index" aria-label="Ürünler" data-aria-tr="Ürünler" data-aria-en="Products">{''.join(index_links)}</nav><div class="catalog-content">{''.join(category_details)}</div></div>{product_standards_note}</div>'''
(OUT/"products.html").write_text(layout("Ürünler",products_body,"products",title_en="Products"),encoding="utf-8")

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
        category_items.append(f'<a class="product-card" href="{prefix}products/{esc(obj["id"])}.html"><span class="product-card-media" aria-hidden="true"></span><h2><span class="lang-tr">{esc(title_for(obj,"tr"))}</span><span class="lang-en">{esc(title_for(obj,"en"))}</span></h2></a>')
    if category_items:
        intro_tr=''.join(p_html(entry,"tr") for entry in cat.get("descriptionTr",[]))
        intro_en=''.join(p_html(entry,"en") for entry in cat.get("descriptionEn",[]))
        intro=f'<div class="lang-tr">{intro_tr}</div><div class="lang-en">{intro_en}</div>' if intro_tr or intro_en else ''
        content_html=f'<div class="category-intro">{intro}</div><div class="product-grid">{"".join(category_items)}</div>'
    else:
        intro_tr=''.join(p_html(entry,"tr") for entry in cat.get("descriptionTr",[]))
        intro_en=''.join(p_html(entry,"en") for entry in cat.get("descriptionEn",[]))
        intro=f'<div class="lang-tr">{intro_tr}</div><div class="lang-en">{intro_en}</div>' if intro_tr or intro_en else ''
        content_html=f'<div class="category-feature-layout"><div class="category-media" aria-hidden="true"></div><div class="category-intro">{intro}</div></div>' if intro else ''
    body=f'''<div class="page-wrap catalog-page"><div class="breadcrumbs"><a href="{prefix}products.html"><span class="lang-tr">Ürünler</span><span class="lang-en">Products</span></a></div><div class="page-heading"><h1 id="{esc(cat['id'])}"><span class="lang-tr">{esc(category_title(cat,"tr"))}</span><span class="lang-en">{esc(category_title(cat,"en"))}</span></h1></div><div class="catalog-layout"><nav class="catalog-index" aria-label="Ürünler" data-aria-tr="Ürünler" data-aria-en="Products">{''.join(cat_nav)}</nav><div class="catalog-content">{content_html}</div></div></div>'''
    (OUT/"categories"/(cat["id"]+".html")).write_text(layout(category_title(cat,"tr"),body,"products",prefix,title_en=category_title(cat,"en")),encoding="utf-8")

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
        (OUT/"products"/(obj["id"]+".html")).write_text(layout(title_tr,detail,"products","../",title_en=title_en),encoding="utf-8")

# API 2000 form — formula and disclaimer are supplied by the user.
calculator_body='''<div class="page-wrap form-page"><div class="page-heading"><h1><span class="lang-tr">API 2000 Hesaplama</span><span class="lang-en">API 2000 Calculator</span></h1></div><div class="steps"><span class="step-indicator" data-step-indicator="1" aria-current="step">1</span><span class="step-indicator" data-step-indicator="2">2</span><span class="step-indicator" data-step-indicator="3">3</span></div><section class="form-panel" id="calc-step-email"><form id="calc-email-form" class="form-grid"><div class="form-field"><label for="calc-email"><span class="lang-tr">E-posta</span><span class="lang-en">Email</span></label><input id="calc-email" name="email" type="email" autocomplete="email" required></div><button class="button button-primary" type="submit"><span class="lang-tr">Devam</span><span class="lang-en">Continue</span></button></form></section><section class="form-panel" id="calc-step-inputs" hidden><form id="calc-input-form" class="form-grid"><div class="form-field"><label for="tank-capacity"><span class="lang-tr">Tank Kapasitesi (m³)</span><span class="lang-en">Tank Capacity (m³)</span></label><input id="tank-capacity" name="tank_capacity_m3" type="number" min="0.01" step="any" required></div><div class="form-field"><label for="fill-rate"><span class="lang-tr">Maksimum Dolum Debisi (m³/h)</span><span class="lang-en">Max Fill Rate (m³/h)</span></label><input id="fill-rate" name="max_fill_rate_m3h" type="number" min="0" step="any" required></div><div class="form-field"><label for="empty-rate"><span class="lang-tr">Maksimum Boşaltım Debisi (m³/h)</span><span class="lang-en">Max Empty Rate (m³/h)</span></label><input id="empty-rate" name="max_empty_rate_m3h" type="number" min="0" step="any" required></div><div class="form-field"><label for="flash-point"><span class="lang-tr">Ürünün Parlama Noktası 37°C Üzerinde</span><span class="lang-en">Product Flash Point Above 37°C</span></label><select id="flash-point" name="product_flash_point_above_37c"><option value="true" data-i18n-tr="Evet" data-i18n-en="Yes">Evet</option><option value="false" data-i18n-tr="Hayır" data-i18n-en="No">Hayır</option></select></div><div><button class="button button-primary" type="submit"><span class="lang-tr">Hesapla</span><span class="lang-en">Calculate</span></button></div></form></section><section class="form-panel" id="calc-step-results" hidden><div id="calc-results" class="calc-results"></div><p class="legal-copy"><span class="lang-tr">Yasal Uyarı ve Sorumluluk Reddi: Bu raporda sunulan tüm hesaplamalar, veriler ve sonuçlar yalnızca bilgi amaçlıdır ve hiçbir şekilde mühendislik veya ticari açıdan bağlayıcılığı yoktur. Kesin ekipman seçimi, boyutlandırma ve projelendirme aşamalarında saha koşulları, meteorolojik veriler, boru hattı dinamikleri ve yerel/uluslararası standartlar göz önünde bulundurularak doğrulama yapılması gerekmektedir.</span><span class="lang-en">Legal Notice and Disclaimer: All calculations, data, and results in this report are for informational purposes only and are not binding for engineering or commercial purposes. Final equipment selection, sizing, and project design must be verified by taking site conditions, meteorological data, pipeline dynamics, and applicable local and international standards into account.</span></p><button class="button button-primary" id="calc-send" type="button"><span class="lang-tr">Gönder</span><span class="lang-en">Send</span></button><p class="form-status" id="calc-status" role="status" aria-live="polite"></p><button class="button" id="calc-back" type="button"><span class="lang-tr">Geri</span><span class="lang-en">Back</span></button></section></div>'''
(OUT/"calculator.html").write_text(layout("API 2000 Hesaplama",calculator_body,"calculator",title_en="API 2000 Calculator"),encoding="utf-8")

contact_body='''<div class="page-wrap form-page"><div class="page-heading"><h1><span class="lang-tr">İletişim</span><span class="lang-en">Contact</span></h1></div><div class="form-panel"><form id="contact-form" class="form-grid"><input name="product" id="contact-product" type="hidden"><div class="form-field"><label for="contact-name"><span class="lang-tr">Ad Soyad</span><span class="lang-en">Full Name</span></label><input id="contact-name" name="name" autocomplete="name" required></div><div class="form-field"><label for="contact-phone"><span class="lang-tr">Telefon No</span><span class="lang-en">Phone</span></label><input id="contact-phone" name="phone" type="tel" autocomplete="tel" required></div><div class="form-field"><label for="contact-message"><span class="lang-tr">Açıklama</span><span class="lang-en">Description</span></label><textarea id="contact-message" name="description" required></textarea></div><button class="button button-primary" type="submit"><span class="lang-tr">Gönder</span><span class="lang-en">Send</span></button><p class="form-status" id="contact-status" role="status" aria-live="polite"></p></form></div></div>'''
(OUT/"contact.html").write_text(layout("İletişim",contact_body,"contact",title_en="Contact"),encoding="utf-8")

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
(OUT/"faq.html").write_text(layout("Sıkça Sorulan Sorular",faq_body,"faq",title_en="FAQ"),encoding="utf-8")

# Sitemap uses the site origin already listed in robots.txt.
urls=['index.html','about.html','what-we-do.html','services.html','products.html','calculator.html','faq.html','contact.html']
urls += [f'categories/{c["id"]}.html' for c in categories]
urls += [f'products/{x["id"]}.html' for c in categories for x in flatten(c['items'])]
base_url='https://nartech.com.tr/'
sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{base_url if u == "index.html" else base_url + u}</loc></url>\n' for u in urls)+'</urlset>\n'
(OUT/"sitemap.xml").write_text(sitemap,encoding="utf-8")
print(f"Generated {len(urls)} source-backed pages.")
