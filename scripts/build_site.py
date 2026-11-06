# -*- coding: utf-8 -*-
from __future__ import annotations
import html, json, re, shutil
from pathlib import Path
from docx import Document
from docx_formatting import format_source_text

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
OUT = ROOT

def paragraphs(filename: str) -> list[str]:
    return [p.text for p in Document(DOCS / filename).paragraphs if p.text.strip()]

def source_lines(filename: str) -> list[int]:
    return [i + 1 for i, p in enumerate(Document(DOCS / filename).paragraphs) if p.text.strip()]

about = paragraphs("Who We Are - About US.docx")
about_lines = source_lines("Who We Are - About US.docx")
what_we_do = paragraphs("What We Do (1).docx")
what_we_do_lines = source_lines("What We Do (1).docx")
home = [what_we_do[0], what_we_do[1], what_we_do[5], what_we_do[6]]
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
    74: "Geliştirilmiş Güvenlik ve Buhar Kontrolü: Platform altındaki buhar boşluğunu ortadan kaldırarak patlayıcı gaz birikmesi riskini ortadan kaldırır ve çevre ile çalışma alanı güvenliğini destekler.",
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
floating_children[3]["titleEn"] = "HDPE Seal"
floating_roofs = item("internal-floating-roofs-and-seals", 57, None, [], [], floating_children, 56)
floating_roofs["titleTr"] = "İç Yüzer Tavanlar ve Fitiller"
floating_roofs["titleEn"] = "f-Internal Floating Roofs and Seals"
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
pigs_branch = item("pigs", None, None, [], [], [
    item("foam-pigs", 113, 113, [], [], src=112),
    item("solid-cast-pigs", 114, 114, [], [], src=113),
    item("steel-pigs", 115, 115, [], [], src=114),
], 112)
pigs_branch["titleTr"] = "Pigler"
pigs_branch["titleEn"] = "Pigs"
pig_descriptions = [
    (
        "Yüksek kaliteli poliüretan köpükten üretilen bu hafif ve esnek pigler; boru hatlarının kurutulması, suyu süpürme (dewatering) ve hafif temizlik işlemleri için idealdir. Dar dirseklerden ve farklı çaplardaki hatlardan kolayca geçebilme yeteneği sayesinde maksimum uyumluluk sunar. Genellikle hat ön hazırlığı ve genel bakım süreçlerinde pratik bir çözüm olarak tercih edilir.",
        "Made from high-quality polyurethane foam, these lightweight and flexible pigs are ideal for pipeline drying, dewatering, and light cleaning. Their ability to pass easily through tight bends and pipelines of varying diameters provides maximum versatility. They are commonly chosen as a practical solution for pipeline preparation and general maintenance.",
    ),
    (
        "Tek parça döküm poliüretan malzemeden üretilen bu sağlam pigler, yüksek aşınma direnci ve mükemmel sızdırmazlık özellikleri ile öne çıkar. Boru iç yüzeyindeki birikintilerin temizlenmesi, sıvıların hat dışına itilmesi ve rutin hat bakımı için uzun ömürlü bir performans sunar. Zorlu saha koşullarında bile formunu koruyarak güvenilir ve kesintisiz bir pigging operasyonu sağlar.",
        "Manufactured from one-piece cast polyurethane, these robust pigs stand out for their high abrasion resistance and excellent sealing. They deliver long-lasting performance when removing deposits from pipe interiors, displacing liquids from the line, and carrying out routine pipeline maintenance. They retain their shape in demanding field conditions, supporting reliable and uninterrupted pigging operations.",
    ),
    (
        "Çelik ana gövde üzerine monte edilen diskler, manşetler ve çelik tel fırçalardan oluşan bu dayanıklı pigler, en ağır temizlik ve kazıma operasyonları için tasarlanmıştır. Boru duvarındaki sert tortuları, pası, kalıntıları ve parafin birikintilerini sökmekte üstün performans gösterir. Aynı zamanda hat içi denetim (ILI) öncesi kalibrasyon ve yüksek mukavemet gerektiren endüstriyel hatlar için vazgeçilmezdir.",
        "Built around a steel body fitted with discs, cups, and steel wire brushes, these durable pigs are designed for the most demanding cleaning and scraping operations. They perform effectively in removing hard deposits, rust, debris, and paraffin buildup from pipe walls. They are also essential for calibration before in-line inspection (ILI) and for industrial pipelines requiring high mechanical strength.",
    ),
]
for pig_product, (description_tr, description_en) in zip(pigs_branch["children"], pig_descriptions):
    pig_product["tr"] = [{"text": description_tr, "source": "WhatsApp 2026-11-06"}]
    pig_product["en"] = [{"text": description_en, "source": "WhatsApp 2026-11-06"}]

pig_signallers = item("pig-signallers", 116, 116, [], [], [
    item("non-intrusive-pig-signaller", 117, 117, [], [], src=116),
    item("intrusive-pig-signaller", 118, 118, [], [], src=116),
], 115)
pig_signallers["titleEn"] = "Pig Signallers"
pig_signallers["children"][0]["tr"] = [{"text": "Non-intrusive manyetik tip ATEX sertifikalı pig işaretçisi, patlayıcı ortamların bulunduğu tehlikeli sahalarda boru hattına zarar vermeden pig geçişlerini dışarıdan tespit eden yüksek güvenilirlikli bir izleme cihazıdır. Bu gelişmiş manyetik sistem, pig gövdesine entegre edilen mıknatısların yarattığı manyetik alan değişimini ex-proof sensörleri vasıtasıyla boru duvarının dışından algılar. Boru delme işlemi gerektirmeyen sızdırmaz yapısı, alev sızdırmaz ATEX gövdesi ve kolay montaj avantajıyla, Zone 1 ve Zone 2 gibi riskli endüstriyel hatlarda maksimum operasyonel emniyet sağlar.", "source": "WhatsApp 2026-11-06"}]
pig_signallers["children"][0]["en"] = [{"text": "The ATEX-certified non-intrusive magnetic pig signaller is a high-reliability monitoring device that detects pig passage externally, without damaging the pipeline, in hazardous areas where explosive atmospheres may be present. This advanced magnetic system detects, from outside the pipe wall and through explosion-proof sensors, changes in the magnetic field created by magnets integrated into the pig body. Its sealed design requires no pipe drilling; together with its flameproof ATEX enclosure and easy installation, it provides maximum operational safety in hazardous industrial lines such as Zone 1 and Zone 2.", "source": "WhatsApp 2026-11-06"}]
pig_signallers["children"][1]["tr"] = [{"text": "Intrusive tip ATEX sertifikalı pig işaretçisi, yanıcı ve patlayıcı gaz/buhar içeren tehlikeli boru hatlarının içerisine mekanik bir tetikleyici uzatarak pig geçişlerini doğrudan temas yoluyla tespit eden güvenilir bir mekanik izleme cihazıdır. Bu sistem, pigin boru içindeki hareketi sırasında ex-proof gövde içerisindeki tetik mekanizmasını itmesiyle anlık ve kesin bir sinyal üretir. Sağlam, alev sızdırmaz ATEX tasarımı ve doğrudan temaslı algılama prensibi sayesinde, tehlikeli sahalardaki standart akışkan hatlarında net, güvenli ve yönetmeliklere tam uyumlu bir çözüm sunar.", "source": "WhatsApp 2026-11-06"}]
pig_signallers["children"][1]["en"] = [{"text": "The ATEX-certified intrusive pig signaller is a reliable mechanical monitoring device that detects pig passage by extending a mechanical trigger into hazardous pipelines carrying flammable and explosive gases or vapours, through direct contact. As the pig moves through the pipeline, it pushes the trigger mechanism inside the explosion-proof enclosure, generating an immediate and precise signal. Its robust, flameproof ATEX design and direct-contact detection principle provide a clear, safe, and fully compliant solution for standard fluid lines in hazardous areas.", "source": "WhatsApp 2026-11-06"}]
trv_item = {
    "id": "thermal-relief-valve",
    "titleTr": "Termal Emniyet Vanası (TRV)",
    "titleEn": "Thermal Relief Valve (TRV)",
    "tr": [{"text": "Termal Tahliye Vanası (TRV), kapalı bir hat veya ekipman hacminde hapsolmuş sıvının ısıl genleşmesi sonucu oluşan aşırı basınca karşı koruma sağlayan tahliye vanasıdır. Sıvı genleştikçe kapalı hacimdeki basınç yükselir; basınç set değerine ulaştığında yay yüklü vana açılarak küçük miktarda sıvıyı tahliye eder. Basınç güvenli seviyeye düştüğünde vana yeniden kapanır.", "source": "Valpro TRV"}],
    "en": [{"text": "Thermal Relief Valve (TRV) is an overpressure protection device designed to protect closed piping systems and equipment against excessive hydraulic pressure caused by thermal fluid expansion. As the trapped fluid warms and expands, pressure rises rapidly; once set pressure is reached, the spring-loaded valve opens to discharge a small volume of liquid, reseating tightly once safe pressure is restored.", "source": "Valpro TRV"}],
    "children": [],
    "source": 132
}
high_velocity_item = item(
    "high-velocity-pressure-vacuum-relief-valve",
    "Yüksek Hızlı Basınç Vakum Ventili",
    "High Velocity Pressure Vacuum Relief Valve",
    [], [], src="Mahmut Tunaz: 2026-11-06",
)
high_velocity_item["tr"] = [{
    "text": "En zorlu operasyonel koşullarda dahi üstün koruma sağlayan Yüksek Hızlı Basınç ve Vakum Ventilleri (High Velocity PV Valves), sisteminizi aşırı basınç ve vakum risklerine karşı güvence altına alır. Kargo gemilerinin yükleme ve tahliye süreçleri için özel olarak geliştirilen bu sistem; ani basınç değişimlerini ve buhar transferini kusursuz bir şekilde yöneterek, dinamik deniz koşullarında kargo tanklarınızın güvenliğini ve bütünlüğünü maksimum düzeyde korur.",
    "source": "User-provided product copy",
}]
high_velocity_item["en"] = [{
    "text": "Providing superior protection even under the most demanding operational conditions, High-Velocity Pressure and Vacuum Valves safeguard your system against the risks of overpressure and vacuum. Specifically developed for cargo ship loading and unloading operations, this advanced system flawlessly manages rapid pressure fluctuations and vapor transfer, ensuring the maximum safety and structural integrity of your cargo tanks during dynamic marine transfers.",
    "source": "User-provided product copy",
}]
valve_items = [
    item("ball-valves", "Küresel Vanalar", "Ball Valves", [], [], src=129),
    item("gate-valves", "Sürgülü Vanalar", "Gate Valves", [], [], src=130),
    item("butterfly-valves", "Kelebek Vanalar", "Butterfly Valves", [], [], src=131),
]
vent_silencer = item("vent-silencer", "Endüstriyel Susturucu", "Vent Silencer", [120], [120], src=119)

categories = [
    {"id":"storage-tank-equipments", "title":ref(0), "items":[high_velocity_item, trv_item, pvrv, inline, endline, emergency, gauge, floating_roofs]},
    {"id":"fire-fighting-equipments", "title":ref(84), "items":fire_items},
    {"id":"pig-cleaning-equipments", "title":{"text": "3-Pig Signaller & Pigs", "source": "Products (3).docx:157"}, "items":[
        pigs_branch, pig_signallers]},
    {"id":"industrial-silencers", "title":ref(119), "items":[vent_silencer]},
    {"id":"floatin-suction-units", "title":ref(121), "items":floating_suction_children, "descriptionTr":refs([122],"tr"), "descriptionEn":refs([122])},
    {"id":"retractable-grounding-cable", "title":ref(126), "items":[], "descriptionTr":refs([127],"tr"), "descriptionEn":refs([127])},
    {"id":"loading-arms", "title":ref(128), "items":[]},
    {"id":"industrial-valves", "title":ref(129), "items":valve_items},
    {"id":"gas-scrubber-systems", "title":ref(133), "items":[]},
    {"id":"seperators", "title":ref(134), "items":[]},
    {"id":"spare-parts-for-refineries", "title":{"text":"11-Spare Part for Refineries & Tank Terminals","source":"Mahmut Tunaz: 2026-11-04"}, "items":[], "descriptionTr":[{"text":"Tank terminalleri, rafineriler, petrol ve gaz boru hatları ve offshore platformların operasyonel sürekliliği için kritik önem taşıyan mekanik, enstrümantasyon, conta ve hardware grubu yedek parçalarını güvenle tedarik ediyoruz. Sektörün zorlu koşullarına tam uyumlu, uluslararası standartlardaki ürün çözümlerimizle tesislerinizin kesintisiz ve güvenli çalışmasını sağlıyoruz.","source":"Mahmut Tunaz: 2026-11-04"}], "descriptionEn":[{"text":"We reliably supply the mechanical, instrumentation, gasket, and hardware group spare parts that are critical for the operational continuity of tank terminals, refineries, oil & gas pipelines, and offshore platforms. With our product solutions that fully comply with the industry's demanding conditions and international standards, we ensure your facilities operate continuously and safely.","source":"Mahmut Tunaz: 2026-11-04"}]},
]
category_titles_tr=[
    "1-Depolama Tankı Ekipmanları", "2-Yangın Söndürme", "3-Pig Sinyal Vericileri & Pigler",
    "4-Susturucular", "5-Yüzer Emiş", "6-Topraklama RGR", "7-Dolum Kolları",
    "8-Vanalar", "9-Gaz Yıkama", "10-Seperatörler", "11-Rafineri ve Tank Terminali Yedek Parça",
]
for category,title_tr in zip(categories,category_titles_tr):
    category["titleTr"]=title_tr
    category["titleEn"]=category["title"]["text"]
    category["titleEn"] = category["titleEn"].removeprefix("-")
categories[1]["titleTr"] = "2-Yangın Söndürme (ATEX & FM / UL Onaylı)"
categories[1]["titleEn"] = "2-Fire Fighting Equipments (ATEX & FM / UL Approved)"
categories[1]["title"]["text"] = categories[1]["titleEn"]

def remove_product_letter_prefix(nodes):
    for node in nodes:
        for field in ("titleTr", "titleEn", "navTitleEn"):
            value = node.get(field)
            if value:
                node[field] = re.sub(r"^[A-Ga-g][ -]+", "", value).strip().rstrip(":").strip()
        remove_product_letter_prefix(node.get("items", []))
        remove_product_letter_prefix(node.get("children", []))

remove_product_letter_prefix(categories)

def category_title(category, language):
    if language != "en":
        return category["titleTr"]
    return category["titleEn"].strip().rstrip(":").strip()

ABOUT_TURKISH_OVERRIDE = {
    1: "NarTech olarak, Petrol & Gaz, Petrokimya, Kimya, Su, Upstream, Downstream ve Offshore sektörlerinde 10 yılı aşkın mühendislik deneyimimizle, müşterilerimize güvenilir, teknik açıdan doğru ve ekonomik çözümler sunuyoruz.",
}

ABOUT_ENGLISH_OVERRIDE = {
    7: "As NarTech, our engineering team brings over 10 years of experience across the Oil & Gas, Petrochemical, Chemical, Water, Upstream, Downstream, and Offshore sectors. We provide our clients with dependable, technically sound, and cost-effective solutions.",
    8: "For refineries, tank farms, and natural gas pipeline applications, we supply a wide range of engineering-approved products, primarily storage tank equipment, valves, and fire protection systems. We also ensure fast, dependable access to critical spare parts for industrial facilities and terminals.",
    9: "We treat every project first and foremost as an engineering challenge. We approach the entire process, from product selection through procurement, from this same technical perspective.",
    10: "The projects we deliver for leading EPC contractors and end users give us direct insight into complex industrial requirements. We provide solutions that fully comply with international standards and project specifications.",
    11: "Our commitment is simple: delivering the right product, the right solution, at the right time.",
}

WHAT_WE_DO_ENGLISH_OVERRIDE = {
    7: "Based on our clients' technical requirements, project needs, and project specifications, we design, develop, and deliver the most suitable products and solutions.",
    8: "Combining deep engineering expertise, technical know-how, and international partnerships, we deliver dependable and efficient solutions tailored to the specific requirements of every project.",
    9: "To us, the right product does more than meet technical specifications. It brings together safety, performance, operational efficiency, and long-term value.",
}

# Persist only the concise copy used by the pages.
content = {
    "home":{"titleTr":home[0],"bodyTr":home[1],"titleEn":home[2],"bodyEn":home[3]},
    "about":{"titleTr":about[0].split('/')[0].strip(' :'),"paragraphsTr":[{"text":ABOUT_TURKISH_OVERRIDE.get(i, about[i]),"source":f"Who We Are - About US.docx:{about_lines[i]}"} for i in range(1,6)],"titleEn":about[6],"paragraphsEn":[{"text":ABOUT_ENGLISH_OVERRIDE.get(i, about[i]),"source":f"Who We Are - About US.docx:{about_lines[i]}"} for i in range(7,12)]},
    "whatWeDo":{"titleTr":what_we_do[0],"paragraphsTr":[{"text":what_we_do[i],"source":f"What We Do (1).docx:{what_we_do_lines[i]}"} for i in range(1,5)],"titleEn":what_we_do[5],"paragraphsEn":[{"text":WHAT_WE_DO_ENGLISH_OVERRIDE.get(i, what_we_do[i]),"source":f"What We Do (1).docx:{what_we_do_lines[i]}"} for i in range(6,10)]},
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
        ("about","about.html","Hakkımızda","Who We Are"),
        ("what-we-do","what-we-do.html","Ne Yapıyoruz","What We Do"),
        ("products","products.html","Ürünler","Products"),
        ("services","services.html","Hizmetler","Services"),
        ("calculator","calculator.html","Hesaplama","Calculation"),
        ("career","career.html","Kariyer","Career"),
        ("contact","contact.html","İletişim","Contact Us"),
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
        ("calculator.html", "Hesaplama", "Calculation"),
        ("career.html", "Kariyer", "Career"),
        ("faq.html", "SSS", "FAQ"),
    ]
    links = "".join(f'<li><a href="{prefix}{path}"><span class="lang-tr">{esc(tr)}</span><span class="lang-en">{esc(en)}</span></a></li>' for path, tr, en in entries)
    return f'''<footer class="site-footer" role="contentinfo"><div class="footer-inner">
<section class="footer-brand-block"><a class="footer-brand" href="{prefix}index.html" aria-label="NarTech ana sayfa" data-aria-tr="NarTech ana sayfa" data-aria-en="NarTech home page"><img src="{prefix}assets/images/nartech-logo-transparent.png" width="1958" height="803" alt="NarTech"></a><p class="footer-tagline"><span class="footer-tagline-dot" aria-hidden="true"></span><span class="lang-tr">{esc(content['home']['titleTr'])}</span><span class="lang-en">{esc(content['home']['titleEn'])}</span></p></section>
<nav class="footer-group footer-site" aria-label="Hızlı Erişim" data-aria-tr="Hızlı Erişim" data-aria-en="Quick Links"><h2 class="footer-heading"><span class="lang-tr">Hızlı Erişim</span><span class="lang-en">Quick Links</span></h2><ul class="footer-links">{links}</ul></nav>
<nav class="footer-group footer-contact" aria-label="İletişim" data-aria-tr="İletişim" data-aria-en="Contact Us"><h2 class="footer-heading"><span class="lang-tr">İletişim</span><span class="lang-en">Contact Us</span></h2><div class="footer-contact-details"><p class="footer-contact-address"><span class="lang-tr">Fatih Mah. 30020 Sok. Güzelyalı Sit. Güzel Yalı Sitesi No: 29B İç Kapı No: 4, Mezitli, Mersin, Türkiye</span><span class="lang-en">Fatih Mah. 30020 Sok. Güzelyalı Sit. Güzel Yalı Sitesi No: 29B İç Kapı No: 4, Mezitli, Mersin, Türkiye</span></p><p class="footer-contact-email"><a href="mailto:sales@nartech.com.tr">sales@nartech.com.tr</a></p></div><a class="footer-cta" href="{prefix}contact.html#contact-form"><span class="lang-tr">Teklif Gönder</span><span class="lang-en">Send Request</span><span aria-hidden="true">↗</span></a></nav>
</div></footer>'''

def layout(title: str, body: str, current: str, prefix="", lang="tr", title_en=None) -> str:
    css_version = "nartech-mobile-contact-20261106-1"
    js_version = "nartech-home-flow-20261105-1"
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
    return f'<p data-source="{esc(entry["source"])}">{format_source_text(entry["text"], entry["source"], lang)}</p>'

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
    ("EMNİYET & YANGIN SERTİFİKASYONU","SAFETY & FIRE CERTIFICATION","ATEX & FM / UL","ATEX & FM / UL","Patlayıcı Ortam ve Yangın Güvenliği","Explosive Atmosphere and Fire Safety"),
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
nar_story_html='''<div class="about-nar-story nar-story-box"><div class="lang-tr"><p class="nar-story-lead">Türkçedeki “nar” sözcüğü, nar meyvesini ifade eder.</p><p>Dışarıdan bakıldığında bir nar tektir. Onu açtığınızda, içinde birbirinden farklı yüzlerce tane keşfedersiniz.</p><p>Nar bizi temsil eder. Her bir tanesi bizlerden biridir; geçmişlerimiz, fikirlerimiz, deneyimlerimiz ve güçlü yanlarımız farklı olsa da bir bütün olarak birleşiriz.</p><p class="nar-story-motto">Dışarıdan biriz. İçimiz zengin. Birlikte güçlüyüz.</p></div><div class="lang-en"><p class="nar-story-lead">“Nar” means pomegranate in Turkish.</p><p>From the outside, a pomegranate is one. Open it, and you discover hundreds of unique seeds inside.</p><p>Nar represents us. Each seed is one of us, different in our backgrounds, ideas, experiences and strengths, yet united as one.</p><p class="nar-story-motto">One outside. Rich inside. Strong together.</p></div></div>'''
home_flow_items=[
    ("Standartlar", "International Standards", "Güvenlik · kalite · performans", "Safety · quality · performance", "What We Do (1).docx:2", "What We Do (1).docx:7"),
    ("Teknik Gereksinimler", "Technical Requirements", "Proje ihtiyaçları · özel şartnameler", "Project needs · specific specifications", "What We Do (1).docx:3", "What We Do (1).docx:8"),
    ("Mühendislik Uzmanlığı", "Engineering Expertise", "Teknik bilgi birikimi · uluslararası iş ortaklıkları", "Technical know-how · international partnerships", "What We Do (1).docx:4", "What We Do (1).docx:9"),
    ("Doğru Ürün", "The Right Product", "Operasyonel verimlilik · uzun vadeli değer", "Operational efficiency · long-term value", "What We Do (1).docx:5", "What We Do (1).docx:10"),
]
home_flow_card_items=[]
for index,(title_tr,title_en,detail_tr,detail_en,source_tr,source_en) in enumerate(home_flow_items):
    home_flow_card_items.append(f'''<article class="home-what-card" role="listitem" data-source="{esc(source_tr)}"><h3><span class="lang-tr">{esc(title_tr)}</span><span class="lang-en" data-source="{esc(source_en)}">{esc(title_en)}</span></h3><p><span class="lang-tr">{esc(detail_tr)}</span><span class="lang-en">{esc(detail_en)}</span></p></article>''')
home_flow_cards=''.join(home_flow_card_items)
home_what_desktop_paths=[
    ("M125 195 C125 245 390 270 500 315", "0s"),
    ("M375 195 C375 245 440 275 500 315", "0.18s"),
    ("M625 195 C625 245 560 275 500 315", "0.36s"),
    ("M875 195 C875 245 610 270 500 315", "0.54s"),
    ("M500 365 C430 395 270 420 167 450", "0.72s"),
    ("M500 365 C500 395 500 420 500 450", "0.9s"),
    ("M500 365 C570 395 730 420 833 450", "1.08s"),
]
home_what_mobile_paths=[
    ("M250 130 C250 220 410 285 500 390", "0s"),
    ("M750 130 C750 220 590 285 500 390", "0.18s"),
    ("M250 310 C250 350 405 370 500 390", "0.36s"),
    ("M750 310 C750 350 595 370 500 390", "0.54s"),
    ("M500 448 C430 520 270 560 175 625", "0.72s"),
    ("M500 448 C500 520 500 560 500 625", "0.9s"),
    ("M500 448 C570 520 730 560 825 625", "1.08s"),
]
def flow_svg_paths(paths):
    return ''.join(f'<path class="home-what-track" d="{path}"/><path class="home-what-particles" d="{path}" style="--flow-delay:{delay}"/>' for path,delay in paths)

home_flow_graphic=f'''<svg class="home-what-connectors home-what-connectors--desktop" viewBox="0 0 1000 500" preserveAspectRatio="none" aria-hidden="true">{flow_svg_paths(home_what_desktop_paths)}</svg><svg class="home-what-connectors home-what-connectors--mobile" viewBox="0 0 1000 700" preserveAspectRatio="none" aria-hidden="true">{flow_svg_paths(home_what_mobile_paths)}</svg>'''
home_what_board=f'''<div class="home-what-board" data-home-flow>{home_flow_graphic}<div class="home-what-cards" role="list">{home_flow_cards}</div><div class="home-what-hub"><img src="assets/images/nartech-logo-transparent.png" width="1958" height="803" alt="NarTech"></div><div class="home-what-outcomes"><div><span class="lang-tr">Tank Terminalleri</span><span class="lang-en">Tank Terminals</span></div><div><span class="lang-tr">Rafineriler</span><span class="lang-en">Refineries</span></div><div><span class="lang-tr">Yükleniciler</span><span class="lang-en">Contractors</span></div></div></div>'''
home_body=f'''<div class="home-page"><div class="page-wrap"><section class="home-hero"><div class="home-hero-copy"><h1><span class="lang-tr">{esc(content['home']['titleTr'])}</span><span class="lang-en">{esc(content['home']['titleEn'])}</span></h1><p><span class="lang-tr">{esc(content['home']['bodyTr'])}</span><span class="lang-en">{esc(content['home']['bodyEn'])}</span></p><div class="home-actions"><a class="button button-primary" href="products.html"><span class="lang-tr">Ürünler</span><span class="lang-en">Products</span></a><a class="button" href="contact.html#contact-form"><span class="lang-tr">İletişime Geç</span><span class="lang-en">Get in Touch</span></a></div></div><figure class="home-hero-media"><img src="assets/images/home-4k.jpeg" alt="NarTech Depolama Tankı ve Terminal Ekipmanları Sahası" data-alt-tr="NarTech Depolama Tankı ve Terminal Ekipmanları Sahası" data-alt-en="NarTech storage tank and terminal equipment facility" width="3840" height="1723" fetchpriority="high" decoding="async"></figure></section>
<section class="home-proof-strip" aria-label="Mühendislik Göstergeleri" data-aria-tr="Mühendislik Göstergeleri" data-aria-en="Engineering Indicators">{home_proof_html}</section>
<section class="home-who-section" aria-labelledby="home-who-heading"><div class="home-who-heading"><div class="about-subtitle"><span class="lang-tr">BİZ KİMİZ</span><span class="lang-en">WHO WE ARE</span></div><h2 id="home-who-heading"><span class="lang-tr">Biz Kimiz</span><span class="lang-en">Who We Are</span></h2></div><div class="home-who-copy"><div class="lang-tr">{home_about_tr}</div><div class="lang-en">{home_about_en}</div>{nar_story_html}</div></section>
<section class="home-what-section" aria-labelledby="home-what-heading"><div class="home-what-heading"><h2 id="home-what-heading"><span class="lang-tr">Ne Yapıyoruz</span><span class="lang-en">What We Do</span></h2><p class="home-what-subtitle"><span class="lang-tr">{esc(content['whatWeDo']['titleTr'])}</span><span class="lang-en">{esc(content['whatWeDo']['titleEn'].strip())}</span></p></div>{home_what_board}</section></div></div>'''
(OUT/"index.html").write_text(layout(content["home"]["titleTr"],home_body,"home",title_en=content["home"]["titleEn"]),encoding="utf-8")
# Keep the fallback free of copy that is not supplied in the source documents.
(OUT/"404.html").write_text('<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=./index.html"></head><body></body></html>',encoding="utf-8")

# About and services: exact text from their source documents.
about_intro_tr=''.join(p_html(x,"tr") for x in content["about"]["paragraphsTr"][:2])
about_intro_en=''.join(p_html(x,"en") for x in content["about"]["paragraphsEn"][:2])
about_rest_tr=''.join(p_html(x,"tr") for x in content["about"]["paragraphsTr"][2:])
about_rest_en=''.join(p_html(x,"en") for x in content["about"]["paragraphsEn"][2:])
about_body=f'''<div class="page-wrap about-page"><div class="page-heading"><h1><span class="lang-tr">{esc(about[0].split('/')[0].strip(' :'))}</span><span class="lang-en">{esc(about[6])}</span></h1></div><section class="about-hero"><div class="about-hero-copy"><div class="about-subtitle"><span class="lang-tr">BİZ KİMİZ</span><span class="lang-en">WHO WE ARE</span></div><div class="lang-tr">{about_intro_tr}</div><div class="lang-en">{about_intro_en}</div></div><figure class="about-hero-media"><img src="assets/images/home-4k.jpeg" alt="NarTech Depolama Tankı ve Terminal Ekipmanları Sahası" data-alt-tr="NarTech Depolama Tankı ve Terminal Ekipmanları Sahası" data-alt-en="NarTech storage tank and terminal equipment facility" width="3840" height="1723" fetchpriority="high" decoding="async"></figure></section><section class="about-approach"><div class="about-subtitle"><span class="lang-tr">MÜHENDİSLİK YAKLAŞIMIMIZ</span><span class="lang-en">OUR ENGINEERING APPROACH</span></div><div class="lang-tr"><div class="about-cards-grid"><div class="about-card"><div class="about-card-badge">01</div><h3>Çözüm Odaklı Mühendislik</h3>{p_html(content["about"]["paragraphsTr"][2],"tr")}</div><div class="about-card"><div class="about-card-badge">02</div><h3>Uluslararası Standart ve Şartname Uyumu</h3>{p_html(content["about"]["paragraphsTr"][3],"tr")}</div></div><div class="about-commitment">{p_html(content["about"]["paragraphsTr"][4],"tr")}</div></div><div class="lang-en"><div class="about-cards-grid"><div class="about-card"><div class="about-card-badge">01</div><h3>Engineering-First Solutions</h3>{p_html(content["about"]["paragraphsEn"][2],"en")}</div><div class="about-card"><div class="about-card-badge">02</div><h3>International Standards &amp; Compliance</h3>{p_html(content["about"]["paragraphsEn"][3],"en")}</div></div><div class="about-commitment">{p_html(content["about"]["paragraphsEn"][4],"en")}</div></div></section><section class="about-story-section"><div class="about-story-box"><div class="about-subtitle"><span class="lang-tr">İSMİMİZİN ANLAMI</span><span class="lang-en">THE MEANING OF OUR NAME</span></div><div class="lang-tr"><p class="story-lead">Türkçedeki “nar” sözcüğü, nar meyvesini ifade eder.</p><p>Dışarıdan bakıldığında bir nar tektir. Onu açtığınızda, içinde birbirinden farklı yüzlerce tane keşfedersiniz.</p><p>Nar bizi temsil eder. Her bir tanesi bizlerden biridir; geçmişlerimiz, fikirlerimiz, deneyimlerimiz ve güçlü yanlarımız farklı olsa da bir bütün olarak birleşiriz.</p><div class="story-motto-pill">Dışarıdan biriz. İçimiz zengin. Birlikte güçlüyüz.</div></div><div class="lang-en"><p class="story-lead">“Nar” means pomegranate in Turkish.</p><p>From the outside, a pomegranate is one. Open it, and you discover hundreds of unique seeds inside.</p><p>Nar represents us. Each seed is one of us, different in our backgrounds, ideas, experiences and strengths, yet united as one.</p><div class="story-motto-pill">One outside. Rich inside. Strong together.</div></div></div></section></div>'''
(OUT/"about.html").write_text(layout(about[0].split('/')[0].strip(' :'),about_body,"about",title_en=about[6]),encoding="utf-8")

what_we_do_tr=''.join(p_html(entry,"tr") for entry in content["whatWeDo"]["paragraphsTr"])
what_we_do_en=''.join(p_html(entry,"en") for entry in content["whatWeDo"]["paragraphsEn"])
what_we_do_body=f'''<div class="page-wrap what-we-do-page"><div class="page-heading"><h1><span class="lang-tr">{esc(content["whatWeDo"]["titleTr"])}</span><span class="lang-en">{esc(content["whatWeDo"]["titleEn"])}</span></h1></div><section class="what-we-do-copy"><div class="lang-tr"><div class="what-we-do-grid">{what_we_do_tr}</div></div><div class="lang-en"><div class="what-we-do-grid">{what_we_do_en}</div></div></section></div>'''
(OUT/"what-we-do.html").write_text(layout(content["whatWeDo"]["titleTr"],what_we_do_body,"what-we-do",title_en="What We Do"),encoding="utf-8")

service_cards=[]
for service in content["services"]["items"]:
    paragraphs_html=''.join(f'<p data-source="{esc(paragraph["source"])}"><span class="lang-tr">{format_source_text(paragraph["text"], paragraph["source"], "tr")}</span><span class="lang-en">{format_source_text(paragraph["textEn"], paragraph["source"], "en")}</span></p>' for paragraph in service["paragraphs"])
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
products_body=f'''<div class="page-wrap catalog-page"><div class="page-heading"><h1><span class="lang-tr">Ürünler</span><span class="lang-en">Products</span></h1></div><div class="catalog-layout"><div class="catalog-content">{''.join(category_details)}</div></div>{product_standards_note}</div>'''
(OUT/"products.html").write_text(layout("Ürünler",products_body,"products",title_en="Products"),encoding="utf-8")

# Category pages show product names; detail pages include each mapped source paragraph.

def localized_specs_table(rows):
    table_rows = []
    for label_tr, label_en, value_tr, value_en in rows:
        table_rows.append(
            f'<tr><th scope="row"><span class="lang-tr">{html.escape(label_tr)}</span>'
            f'<span class="lang-en">{html.escape(label_en)}</span></th><td>'
            f'<div class="lang-tr">{html.escape(value_tr)}</div>'
            f'<div class="lang-en">{html.escape(value_en)}</div></td></tr>'
        )
    return (
        '<div class="product-specs-wrap"><h3 class="specs-heading">'
        '<span class="lang-tr">Teknik Özellikler</span>'
        '<span class="lang-en">Technical Specifications</span></h3>'
        f'<table class="product-specs-table"><tbody>{"".join(table_rows)}'
        '</tbody></table></div>'
    )


SPECS_TABLES = {
    "pressure-vacuum-relief-valve": '''<div class="product-specs-wrap"><h3 class="specs-heading"><span class="lang-tr">Teknik Özellikler</span><span class="lang-en">Technical Specifications</span></h3><table class="product-specs-table"><tbody><tr><th scope="row"><span class="lang-tr">Tip</span><span class="lang-en">Type</span></th><td><div class="lang-tr">Atmosferik ve Borulu Tip Basınç Vakum Emniyet Vanası (PVRV)</div><div class="lang-en">Atmospheric and Pipe-Away Type Pressure Vacuum Relief Valve (PVRV)</div></td></tr><tr><th scope="row"><span class="lang-tr">Çap</span><span class="lang-en">Size</span></th><td>2″ - 12″ / DN50 - DN300</td></tr><tr><th scope="row"><span class="lang-tr">Tasarım &amp; Test</span><span class="lang-en">Design &amp; Test</span></th><td>API 2000</td></tr><tr><th scope="row"><span class="lang-tr">Set Basınç &amp; Vakum Aralığı</span><span class="lang-en">Set Pressure &amp; Vacuum Range</span></th><td>+3.5 mbar / -2.5 mbar — +900 mbar / -900 mbar</td></tr><tr><th scope="row"><span class="lang-tr">Bağlantı</span><span class="lang-en">Connection</span></th><td>ASME B16.5 / DIN EN 1092-1</td></tr><tr><th scope="row"><span class="lang-tr">Malzeme</span><span class="lang-en">Materials</span></th><td><div class="lang-tr">Karbon Çelik, Alüminyum, Paslanmaz Çelik 304/304L, Paslanmaz Çelik 316/316L</div><div class="lang-en">Carbon Steel, Aluminium, Stainless Steel 304/304L, Stainless Steel 316/316L</div></td></tr><tr><th scope="row"><span class="lang-tr">Sertifikalar</span><span class="lang-en">Certifications</span></th><td><div class="lang-tr">2014/34/EU (ATEX Sertifikası), EN 10204 Tip 3.1 veya 2.2 Malzeme Sertifikası</div><div class="lang-en">2014/34/EU (ATEX Certificate), EN 10204 Type 3.1 or 2.2 Material Certificate</div></td></tr></tbody></table></div>''',

    "inline-flame-arrester": '''<div class="product-specs-wrap"><h3 class="specs-heading"><span class="lang-tr">Teknik Özellikler</span><span class="lang-en">Technical Specifications</span></h3><table class="product-specs-table"><tbody><tr><th scope="row"><span class="lang-tr">Tip</span><span class="lang-en">Type</span></th><td><div class="lang-tr">Deflegrasyon ve Detonasyon Tipi Hat İçi Alev Kapanı</div><div class="lang-en">Deflagration and Detonation Type Inline Flame Arrester</div></td></tr><tr><th scope="row"><span class="lang-tr">Çap</span><span class="lang-en">Size</span></th><td>1″ - 24″ / DN 25 - DN 600</td></tr><tr><th scope="row"><span class="lang-tr">Tasarım &amp; Test</span><span class="lang-en">Design &amp; Test</span></th><td>EN ISO 16852</td></tr><tr><th scope="row"><span class="lang-tr">Bağlantı</span><span class="lang-en">Connection</span></th><td>ASME B16.5 / DIN EN 1092-1</td></tr><tr><th scope="row"><span class="lang-tr">Malzeme</span><span class="lang-en">Materials</span></th><td><div class="lang-tr">Karbon Çelik, Alüminyum, Paslanmaz Çelik 304/304L, Paslanmaz Çelik 316/316L</div><div class="lang-en">Carbon Steel, Aluminium, Stainless Steel 304/304L, Stainless Steel 316/316L</div></td></tr><tr><th scope="row"><span class="lang-tr">Sertifikalar</span><span class="lang-en">Certifications</span></th><td><div class="lang-tr">2014/34/EU (ATEX Sertifikası IIA &amp; IIB), EN 10204 Tip 3.1 veya 2.2 Malzeme Sertifikası</div><div class="lang-en">2014/34/EU (ATEX Certificate IIA &amp; IIB), EN 10204 Type 3.1 or 2.2 Material Certificate</div></td></tr><tr><th scope="row"><span class="lang-tr">Gaz Grubu</span><span class="lang-en">Gas Group</span></th><td>IIA, IIB</td></tr></tbody></table></div>''',

    "end-line-flame-arrester": '''<div class="product-specs-wrap"><h3 class="specs-heading"><span class="lang-tr">Teknik Özellikler</span><span class="lang-en">Technical Specifications</span></h3><table class="product-specs-table"><tbody><tr><th scope="row"><span class="lang-tr">Tip</span><span class="lang-en">Type</span></th><td><div class="lang-tr">Deflegrasyon ve Detonasyon Tipi Hat İçi Alev Kapanı</div><div class="lang-en">Deflagration and Detonation Type Inline Flame Arrester</div></td></tr><tr><th scope="row"><span class="lang-tr">Çap</span><span class="lang-en">Size</span></th><td>2″ - 12″ / DN50 - DN300</td></tr><tr><th scope="row"><span class="lang-tr">Tasarım &amp; Test</span><span class="lang-en">Design &amp; Test</span></th><td>EN ISO 16852</td></tr><tr><th scope="row"><span class="lang-tr">Bağlantı</span><span class="lang-en">Connection</span></th><td>ASME B16.5 / DIN EN 1092-1</td></tr><tr><th scope="row"><span class="lang-tr">Malzeme</span><span class="lang-en">Materials</span></th><td><div class="lang-tr">Karbon Çelik, Alüminyum, Paslanmaz Çelik 304/304L, Paslanmaz Çelik 316/316L</div><div class="lang-en">Carbon Steel, Aluminium, Stainless Steel 304/304L, Stainless Steel 316/316L</div></td></tr><tr><th scope="row"><span class="lang-tr">Sertifikalar</span><span class="lang-en">Certifications</span></th><td><div class="lang-tr">2014/34/EU (ATEX Sertifikası IIA &amp; IIB), EN 10204 Tip 3.1 veya 2.2 Malzeme Sertifikası</div><div class="lang-en">2014/34/EU (ATEX Certificate IIA &amp; IIB), EN 10204 Type 3.1 or 2.2 Material Certificate</div></td></tr><tr><th scope="row"><span class="lang-tr">Gaz Grubu</span><span class="lang-en">Gas Group</span></th><td>IIA, IIB</td></tr></tbody></table></div>''',

    "emergency-relief-valve": localized_specs_table(
    [
        ("Tip", "Type", "Emergency Relief Valve", "Emergency Relief Valve"),
        ("Çap", "Size", '8″ - 24″ / DN 200 - DN 600', '8″ - 24″ / DN 200 - DN 600'),
        ("Malzeme", "Materials", "Karbon Çelik, Alüminyum, Paslanmaz Çelik 304/304L, Paslanmaz Çelik 316/316L", "Carbon Steel, Aluminium, Stainless Steel 304/304L, Stainless Steel 316/316L"),
        ("Set Basınç", "Set Pressure", "+5 mbar / +900 mbar", "+5 mbar / +900 mbar"),
        ("Bağlantı", "Connection", "ASME B16.5 / DIN EN 1092-1 / API 650 Bağlantısı", "ASME B16.5 / DIN EN 1092-1 / API 650 Connection"),
        ("Tasarım & Test", "Design & Test", "API 2000 / API 650", "API 2000 / API 650"),
        ("Sertifikalar", "Certifications", "ATEX Sertifikası IIB, Tip 3.1 veya 2.2 Malzeme Sertifikası", "ATEX Certificate IIB, Type 3.1 or 2.2 Material Certificate"),
    ]),
    "gauge-hatch": localized_specs_table(
    [
        ("Tip", "Type", "Kilitli Tip Ölçüm Kapağı, Atmosferik Tip Ölçüm Kapağı, Atmosfere Kapalı Tip Ölçüm Kapağı", "Locked Type Gauge Hatch, Atmospheric Type Gauge Hatch, Non-Atmospheric Type Gauge Hatch"),
        ("Çap", "Size", '2″ - 12″ / DN 50 - DN 300', '2″ - 12″ / DN 50 - DN 300'),
        ("Malzeme", "Materials", "Karbon Çelik, Alüminyum, Paslanmaz Çelik 304/304L, Paslanmaz Çelik 316/316L", "Carbon Steel, Aluminium, Stainless Steel 304/304L, Stainless Steel 316/316L"),
        ("Set Basınç Aralığı", "Set Pressure Range", "+5 mbar / +50 mbar", "+5 mbar / +50 mbar"),
        ("Bağlantı", "Connection", "ASME B16.5 / DIN EN 1092-1 / API 650 Bağlantısı", "ASME B16.5 / DIN EN 1092-1 / API 650 Connection"),
        ("Tasarım & Test", "Design & Test", "API 2000 / API 650", "API 2000 / API 650"),
        ("Sertifikalar", "Certifications", "ATEX Sertifikası IIB, Tip 3.1 veya 2.2 Malzeme Sertifikası", "ATEX Certificate IIB, Type 3.1 or 2.2 Material Certificate"),
    ]),
    "thermal-relief-valve": '''<div class="product-specs-wrap"><h3 class="specs-heading"><span class="lang-tr">Teknik Özellikler</span><span class="lang-en">Technical Specifications</span></h3><table class="product-specs-table"><tbody><tr><th scope="row"><span class="lang-tr">Tip</span><span class="lang-en">Type</span></th><td><div class="lang-tr">Yay Yüklü Termal Tahliye Vanası (TRV)</div><div class="lang-en">Spring-Loaded Thermal Relief Valve (TRV)</div></td></tr><tr><th scope="row"><span class="lang-tr">Çap</span><span class="lang-en">Size</span></th><td>1″ x 2″ - 12″ x 16″ / DN25 x DN50 - DN300 x DN400</td></tr><tr><th scope="row"><span class="lang-tr">Tasarım</span><span class="lang-en">Design</span></th><td>EN ISO 4126-1 / ASME BPVC Section VIII / API 526 / ASME B16.34</td></tr><tr><th scope="row"><span class="lang-tr">Set Basınç Aralığı</span><span class="lang-en">Set Pressure Range</span></th><td>0,5 - 425 barg</td></tr><tr><th scope="row"><span class="lang-tr">Bağlantı</span><span class="lang-en">Connection</span></th><td>ASME B16.5 / ASME B16.25 / DIN EN 1092-1</td></tr><tr><th scope="row"><span class="lang-tr">Malzeme</span><span class="lang-en">Materials</span></th><td><div class="lang-tr">ASME/ASTM ve EN Karbon Çelik, Paslanmaz Çelik<br>Özel Alaşımlar; Hastelloy, Inconel, Duplex, Super Duplex</div><div class="lang-en">ASME/ASTM and EN Carbon Steel, Stainless Steel<br>Special Alloys; Hastelloy, Inconel, Duplex, Super Duplex</div></td></tr><tr><th scope="row"><span class="lang-tr">Sertifikalar</span><span class="lang-en">Certifications</span></th><td>2014/68/EU (PED)<br>2014/34/EU (ATEX)<br>ASME UV / V Stamped / National Board<br>EN 10204 Type 3.1, 3.2, 2.2</td></tr><tr><th scope="row"><span class="lang-tr">Testler</span><span class="lang-en">Tests</span></th><td>EN ISO 4126 / API 527 / ASME B16.34</td></tr></tbody></table></div>'''
}

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
        media = '' if obj["id"] == "vent-silencer" else '<span class="product-card-media" aria-hidden="true"></span>'
        category_items.append(f'<a class="product-card" href="{prefix}products/{esc(obj["id"])}.html">{media}<h2><span class="lang-tr">{esc(title_for(obj,"tr"))}</span><span class="lang-en">{esc(title_for(obj,"en"))}</span></h2></a>')
    if category_items:
        intro_tr=''.join(p_html(entry,"tr") for entry in cat.get("descriptionTr",[]))
        intro_en=''.join(p_html(entry,"en") for entry in cat.get("descriptionEn",[]))
        intro=f'<div class="lang-tr">{intro_tr}</div><div class="lang-en">{intro_en}</div>' if intro_tr or intro_en else ''
        content_html=f'<div class="category-intro">{intro}</div><div class="product-grid">{"".join(category_items)}</div>'
    else:
        intro_tr=''.join(p_html(entry,"tr") for entry in cat.get("descriptionTr",[]))
        intro_en=''.join(p_html(entry,"en") for entry in cat.get("descriptionEn",[]))
        intro=f'<div class="lang-tr">{intro_tr}</div><div class="lang-en">{intro_en}</div>' if intro_tr or intro_en else ''
        if cat["id"] == "industrial-silencers":
            content_html=f'<div class="category-intro">{intro}</div>' if intro else ''
        else:
            content_html=f'<div class="category-feature-layout"><div class="category-media" aria-hidden="true"></div><div class="category-intro">{intro}</div></div>' if intro else ''
    catalog_content_class = "catalog-content"
    body=f'''<div class="page-wrap catalog-page"><div class="breadcrumbs"><a href="{prefix}products.html"><span class="lang-tr">Ürünler</span><span class="lang-en">Products</span></a></div><div class="page-heading"><h1 id="{esc(cat['id'])}"><span class="lang-tr">{esc(category_title(cat,"tr"))}</span><span class="lang-en">{esc(category_title(cat,"en"))}</span></h1></div><div class="catalog-layout"><nav class="catalog-index" aria-label="Ürünler" data-aria-tr="Ürünler" data-aria-en="Products">{''.join(cat_nav)}</nav><div class="{catalog_content_class}">{content_html}</div></div></div>'''
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
        has_specs = obj["id"] in SPECS_TABLES
        specs_html = SPECS_TABLES.get(obj["id"], "")
        layout_class = "detail-layout product-detail-specs" if has_specs else ("detail-layout detail-layout-copy" if obj["id"] == "vent-silencer" else "detail-layout")
        media_div = "" if has_specs or obj["id"] == "vent-silencer" else '<div class="detail-media" aria-hidden="true"></div>'
        product_content=f'<div class="{layout_class}">{media_div}<article class="product-copy"><h1><span class="lang-tr">{esc(title_tr)}</span><span class="lang-en">{esc(title_en or title_tr)}</span></h1>{content_html}{specs_html}<a class="button quote-action" href="../contact.html?product={esc(obj["id"])}"><span class="lang-tr">Gönder</span><span class="lang-en">Send</span></a></article></div>' if not obj["children"] else f'<article class="product-copy"><h1><span class="lang-tr">{esc(title_tr)}</span><span class="lang-en">{esc(title_en or title_tr)}</span></h1>{content_html}<a class="button quote-action" href="../contact.html?product={esc(obj["id"])}"><span class="lang-tr">Gönder</span><span class="lang-en">Send</span></a></article>'
        detail=f'''<div class="page-wrap product-detail"><div class="breadcrumbs"><a href="../products.html"><span class="lang-tr">Ürünler</span><span class="lang-en">Products</span></a> / <a href="../categories/{esc(cat['id'])}.html"><span class="lang-tr">{esc(category_title(cat,"tr"))}</span><span class="lang-en">{esc(category_title(cat,"en"))}</span></a></div>{product_content}</div>'''
        (OUT/"products"/(obj["id"]+".html")).write_text(layout(title_tr,detail,"products","../",title_en=title_en),encoding="utf-8")

# API 2000 form — formula and disclaimer are supplied by the user.
calculator_body='''<div class="page-wrap form-page"><div class="page-heading"><h1><span class="lang-tr">API 2000 Hesaplama</span><span class="lang-en">API 2000 Calculation</span></h1></div><div class="steps"><span class="step-indicator" data-step-indicator="1" aria-current="step">1</span><span class="step-indicator" data-step-indicator="2">2</span><span class="step-indicator" data-step-indicator="3">3</span></div><section class="form-panel" id="calc-step-email"><form id="calc-email-form" class="form-grid"><div class="form-field"><label for="calc-email"><span class="lang-tr">E-posta</span><span class="lang-en">Email</span></label><input id="calc-email" name="email" type="email" autocomplete="email" required></div><button class="button button-primary" type="submit"><span class="lang-tr">Devam</span><span class="lang-en">Continue</span></button></form></section><section class="form-panel" id="calc-step-inputs" hidden><form id="calc-input-form" class="form-grid"><div class="form-field"><label for="tank-capacity"><span class="lang-tr">Tank Kapasitesi (m³)</span><span class="lang-en">Tank Capacity (m³)</span></label><input id="tank-capacity" name="tank_capacity_m3" type="number" min="0.01" step="any" required></div><div class="form-field"><label for="fill-rate"><span class="lang-tr">Maksimum Dolum Debisi (m³/h)</span><span class="lang-en">Max Fill Rate (m³/h)</span></label><input id="fill-rate" name="max_fill_rate_m3h" type="number" min="0" step="any" required></div><div class="form-field"><label for="empty-rate"><span class="lang-tr">Maksimum Boşaltım Debisi (m³/h)</span><span class="lang-en">Max Empty Rate (m³/h)</span></label><input id="empty-rate" name="max_empty_rate_m3h" type="number" min="0" step="any" required></div><div class="form-field"><label for="flash-point"><span class="lang-tr">Ürünün Parlama Noktası 37°C Üzerinde</span><span class="lang-en">Product Flash Point Above 37°C</span></label><select id="flash-point" name="product_flash_point_above_37c"><option value="true" data-i18n-tr="Evet" data-i18n-en="Yes">Evet</option><option value="false" data-i18n-tr="Hayır" data-i18n-en="No">Hayır</option></select></div><div><button class="button button-primary" type="submit"><span class="lang-tr">Hesapla</span><span class="lang-en">Calculate</span></button></div></form></section><section class="form-panel" id="calc-step-results" hidden><div id="calc-results" class="calc-results"></div><p class="legal-copy"><span class="lang-tr">Yasal Uyarı ve Sorumluluk Reddi: Bu raporda sunulan tüm hesaplamalar, veriler ve sonuçlar yalnızca bilgi amaçlıdır ve hiçbir şekilde mühendislik veya ticari açıdan bağlayıcılığı yoktur. Kesin ekipman seçimi, boyutlandırma ve projelendirme aşamalarında saha koşulları, meteorolojik veriler, boru hattı dinamikleri ve yerel/uluslararası standartlar göz önünde bulundurularak doğrulama yapılması gerekmektedir.</span><span class="lang-en">Legal Notice and Disclaimer: All calculations, data, and results in this report are for informational purposes only and are not binding for engineering or commercial purposes. Final equipment selection, sizing, and project design must be verified by taking site conditions, meteorological data, pipeline dynamics, and applicable local and international standards into account.</span></p><button class="button button-primary" id="calc-send" type="button"><span class="lang-tr">Gönder</span><span class="lang-en">Send</span></button><p class="form-status" id="calc-status" role="status" aria-live="polite"></p><button class="button" id="calc-back" type="button"><span class="lang-tr">Geri</span><span class="lang-en">Back</span></button></section></div>'''
(OUT/"calculator.html").write_text(layout("API 2000 Hesaplama",calculator_body,"calculator",title_en="API 2000 Calculation"),encoding="utf-8")

career_body = '''<div class="career-page">
<section class="career-hero">
  <div class="page-wrap career-hero-wrap">
    <div class="page-heading career-page-heading"><h1 class="career-heading">
      <span class="lang-tr">Kariyer</span>
      <span class="lang-en">Career</span>
    </h1></div>
    <div class="career-hero-inner">
    <div class="career-hero-copy">
      <div class="about-subtitle"><span class="lang-tr">KÜRESEL VİZYON &amp; EKİP</span><span class="lang-en">GLOBAL VISION &amp; TEAM</span></div>
      <blockquote class="career-manifesto-card">
        <div class="career-manifesto-mark" aria-hidden="true">“</div>
        <p class="career-lead">
          <span class="lang-tr">NarTech çatısı altında; dünya pazarlarıyla bağ kurar, uluslararası ticaretin kalbinde yer alır ve geleceğin global ticaret ekosistemini birlikte tasarlarız.</span>
          <span class="lang-en">Under the roof of NarTech, we connect with global markets, stand at the heart of international trade, and co-design the future of the global trade ecosystem.</span>
        </p>
        <p class="career-invitation">
          <span class="lang-tr">Eğer küresel vizyona sahip, yetenekli ve sınır tanımayan bir profesyonelseniz; kariyerinize ivme kazandıracak en doğru ekibe katılın, <strong class="career-spotlight">NarTech’te yeriniz hazır!</strong></span>
          <span class="lang-en">If you are a talented, visionary professional without boundaries, join the team that will accelerate your career—<strong class="career-spotlight">your place at NarTech is ready!</strong></span>
        </p>
      </blockquote>
      <div class="career-hero-actions">
        <a class="button button-primary" href="#open-positions">
          <span class="lang-tr">Açık Rolleri İnceleyin</span>
          <span class="lang-en">Explore Open Roles</span>
          <span aria-hidden="true">↓</span>
        </a>
        <a class="button" href="mailto:sales@nartech.com.tr?subject=Kariyer%20Basvurusu%20-%20NarTech">
          <span class="lang-tr">Doğrudan CV Gönderin</span>
          <span class="lang-en">Submit Resume</span>
          <span aria-hidden="true">✉</span>
        </a>
      </div>
    </div>

    <figure class="career-hero-media">
      <picture>
        <source srcset="assets/images/career.webp" type="image/webp">
        <img src="assets/images/career-4k.jpeg" srcset="assets/images/career.jpeg 1920w, assets/images/career-4k.jpeg 3840w" sizes="(max-width: 900px) 100vw, 620px" alt="NarTech Global Ticaret ve Mühendislik Çalışma Ekosistemi" data-alt-tr="NarTech Global Ticaret ve Mühendislik Çalışma Ekosistemi" data-alt-en="NarTech Global Trade and Engineering Workspace Ecosystem" width="3840" height="2557" loading="eager" fetchpriority="high">
      </picture>
      <div class="career-stat-badge stat-badge-top">
        <span class="stat-badge-num">10+</span>
        <span class="stat-badge-desc">
          <span class="lang-tr">Yıllık Endüstriyel Miras</span>
          <span class="lang-en">Years Industrial Heritage</span>
        </span>
      </div>
      <div class="career-stat-badge stat-badge-bottom">
        <span class="stat-badge-icon" aria-hidden="true">🌍</span>
        <span class="stat-badge-desc">
          <span class="lang-tr">Uluslararası Ticaret Ağı</span>
          <span class="lang-en">Global Trade Network</span>
        </span>
      </div>
    </figure>
    </div>
  </div>
</section>

<!-- Values Section -->
<section class="career-section career-values-section">
  <div class="page-wrap">
    <div class="section-title-wrap text-center">
      <div class="about-subtitle"><span class="lang-tr">NEDEN NARTECH?</span><span class="lang-en">WHY NARTECH?</span></div>
      <h2><span class="lang-tr">Sizi Neler Bekliyor?</span><span class="lang-en">What to Expect at NarTech</span></h2>
      <p class="section-lead-muted"><span class="lang-tr">Yeteneklerinizin değer bulduğu, inisiyatif alabileceğiniz ve sınırlarınızı aşabileceğiniz bir ekosistem.</span><span class="lang-en">An ecosystem where your talent is valued, initiative is empowered, and professional boundaries expand.</span></p>
    </div>
    <div class="career-values-grid">
      <article class="career-value-card">
        <div class="career-value-badge">01</div>
        <div class="career-value-icon">🌐</div>
        <h3><span class="lang-tr">Global Ticaretin Kalbinde</span><span class="lang-en">Heart of Global Trade</span></h3>
        <p><span class="lang-tr">Dünya pazarlarıyla doğrudan bağ kurarak, kritik enerji, depolama ve endüstriyel tedarik zincirlerinin merkezinde uluslararası ölçekte rol alırsınız.</span><span class="lang-en">Work at the center of international trade, directly connecting with global markets and mission-critical storage and energy supply chains.</span></p>
      </article>

      <article class="career-value-card">
        <div class="career-value-badge">02</div>
        <div class="career-value-icon">⚙️</div>
        <h3><span class="lang-tr">Mühendislik Standartları</span><span class="lang-en">Engineering Rigor</span></h3>
        <p><span class="lang-tr">API 650, API 2000, EN ISO 16852 ve ATEX gibi uluslararası normlara tam uyumlu birinci sınıf projelerde teknik bilgi birikiminizi derinleştirirsiniz.</span><span class="lang-en">Deepen your technical expertise across world-class projects compliant with API 650, API 2000, EN ISO 16852, and ATEX standards.</span></p>
      </article>

      <article class="career-value-card">
        <div class="career-value-badge">03</div>
        <div class="career-value-icon">🚀</div>
        <h3><span class="lang-tr">Çevik &amp; İnisiyatif Veren Kültür</span><span class="lang-en">Agile &amp; Empowered Culture</span></h3>
        <p><span class="lang-tr">Bürokrasiden uzak, fikirlerin dinlendiği ve hızla hayata geçirildiği şeffaf, dinamik ve başarıyı ödüllendiren bir çalışma ortamı.</span><span class="lang-en">A lean, flat structure where ideas are heard and executed swiftly, fostering initiative and rewarding proactive achievement.</span></p>
      </article>

      <article class="career-value-card">
        <div class="career-value-badge">04</div>
        <div class="career-value-icon">📈</div>
        <h3><span class="lang-tr">Sınır Tanımayan İvme</span><span class="lang-en">Boundless Growth</span></h3>
        <p><span class="lang-tr">Uluslararası iş ortaklıkları, küresel fuarlar ve dinamik projelerle kariyerinizi dünya ölçeğinde ileriye taşıyacak fırsatlar.</span><span class="lang-en">Accelerate your career through global partnerships, international exhibitions, and dynamic cross-border industrial operations.</span></p>
      </article>
    </div>
  </div>
</section>

<!-- Open Roles Section -->
<section class="career-section career-roles-section" id="open-positions">
  <div class="page-wrap">
    <div class="section-title-wrap text-center">
      <div class="about-subtitle"><span class="lang-tr">AÇIK ROLLER &amp; ODAKLAR</span><span class="lang-en">OPEN ROLES &amp; FOCUS AREAS</span></div>
      <h2><span class="lang-tr">Ekibimize Katılın</span><span class="lang-en">Join Our Team</span></h2>
      <p class="section-lead-muted"><span class="lang-tr">Aşağıdaki alanlarda veya profilinize uygun genel başvuruda yerinizi alın.</span><span class="lang-en">Find your place among our active roles or submit a general application.</span></p>
    </div>

    <div class="career-roles-grid">
      <!-- Role 1 -->
      <div class="career-role-card">
        <div class="role-header">
          <div class="role-tags">
            <span class="role-tag role-tag-dept"><span class="lang-tr">Global Satış &amp; Ticaret</span><span class="lang-en">Global Merchandising</span></span>
            <span class="role-tag role-tag-loc"><span class="lang-tr">Mersin / Hibrit</span><span class="lang-en">Mersin / Hybrid</span></span>
          </div>
          <h3 class="role-title"><span class="lang-tr">Uluslararası Ticaret &amp; İş Geliştirme Uzmanı</span><span class="lang-en">Global Trade &amp; Business Development</span></h3>
        </div>
        <p class="role-desc">
          <span class="lang-tr">Dünya pazarlarında müşteri ve tedarikçi ağlarını genişletme, uluslararası teklif hazırlama ve küresel ticaret operasyonlarını yönetme.</span>
          <span class="lang-en">Expanding client and supplier networks across global markets, managing cross-border commercial bids, and driving trade operations.</span>
        </p>
        <ul class="role-points">
          <li><span class="lang-tr">Akıcı İngilizce (ikinci dil avantajdır)</span><span class="lang-en">Fluent English (second language is an asset)</span></li>
          <li><span class="lang-tr">Dış ticaret, lojistik ve sözleşme yönetimi deneyimi</span><span class="lang-en">Experience in foreign trade, logistics, and contracts</span></li>
        </ul>
        <div class="role-action">
          <a class="button button-outline" href="mailto:sales@nartech.com.tr?subject=Kariyer%20Basvurusu%20-%20Uluslararasi%20Ticaret"><span class="lang-tr">Başvuru Yap</span><span class="lang-en">Apply for Role</span> ↗</a>
        </div>
      </div>

      <!-- Role 2 -->
      <div class="career-role-card">
        <div class="role-header">
          <div class="role-tags">
            <span class="role-tag role-tag-dept"><span class="lang-tr">Mühendislik &amp; Satış</span><span class="lang-en">Engineering &amp; Sales</span></span>
            <span class="role-tag role-tag-loc"><span class="lang-tr">Mersin / Saha</span><span class="lang-en">Mersin / Field</span></span>
          </div>
          <h3 class="role-title"><span class="lang-tr">Mekanik &amp; Proses Satış Mühendisi</span><span class="lang-en">Technical Sales &amp; Application Engineer</span></h3>
        </div>
        <p class="role-desc">
          <span class="lang-tr">Depolama tankı ve terminal ekipmanları için teknik şartname analizi, müşteri danışmanlığı ve ürün mühendisliği hesaplamaları.</span>
          <span class="lang-en">Technical specification analysis, customer consulting, and engineering sizing for storage tank and terminal equipment.</span>
        </p>
        <ul class="role-points">
          <li><span class="lang-tr">Makine, Kimya veya Petrol Mühendisliği lisansı</span><span class="lang-en">Degree in Mechanical, Chemical, or Petroleum Engineering</span></li>
          <li><span class="lang-tr">API 650, API 2000 veya endüstriyel vana bilgisi</span><span class="lang-en">Knowledge of API 650, API 2000, or industrial valves</span></li>
        </ul>
        <div class="role-action">
          <a class="button button-outline" href="mailto:sales@nartech.com.tr?subject=Kariyer%20Basvurusu%20-%20Satis%20Muhendisi"><span class="lang-tr">Başvuru Yap</span><span class="lang-en">Apply for Role</span> ↗</a>
        </div>
      </div>

      <!-- Role 3 -->
      <div class="career-role-card">
        <div class="role-header">
          <div class="role-tags">
            <span class="role-tag role-tag-dept"><span class="lang-tr">Saha Hizmetleri</span><span class="lang-en">Field Services</span></span>
            <span class="role-tag role-tag-loc"><span class="lang-tr">Proje Sahaları</span><span class="lang-en">Project Sites</span></span>
          </div>
          <h3 class="role-title"><span class="lang-tr">Saha Denetim &amp; Süpervizörlük Uzmanı</span><span class="lang-en">Field Supervision &amp; Inspection Specialist</span></h3>
        </div>
        <p class="role-desc">
          <span class="lang-tr">Mekanik montaj sahalarında PVRV set point testleri, dahili yüzer tavan (IFR) denetimleri ve yerinde teknik süpervizörlük kontrolleri.</span>
          <span class="lang-en">PVRV set point testing, internal floating roof (IFR) inspections, and on-site technical supervision at mechanical installation sites.</span>
        </p>
        <ul class="role-points">
          <li><span class="lang-tr">Tank terminali veya rafineri saha deneyimi</span><span class="lang-en">Tank terminal or refinery on-site experience</span></li>
          <li><span class="lang-tr">İSG ve saha güvenlik standartlarına tam uyum</span><span class="lang-en">Strict commitment to HSE standards</span></li>
        </ul>
        <div class="role-action">
          <a class="button button-outline" href="mailto:sales@nartech.com.tr?subject=Kariyer%20Basvurusu%20-%20Saha%20Supervizorlugu"><span class="lang-tr">Başvuru Yap</span><span class="lang-en">Apply for Role</span> ↗</a>
        </div>
      </div>

      <!-- Role 4: Genel Başvuru -->
      <div class="career-role-card career-role-general">
        <div class="role-header">
          <div class="role-tags">
            <span class="role-tag role-tag-dept"><span class="lang-tr">Tüm Birimler</span><span class="lang-en">All Departments</span></span>
            <span class="role-tag role-tag-loc"><span class="lang-tr">Esnek</span><span class="lang-en">Flexible</span></span>
          </div>
          <h3 class="role-title"><span class="lang-tr">Genel Başvuru</span><span class="lang-en">General Application</span></h3>
        </div>
        <p class="role-desc">
          <span class="lang-tr">Yukarıdaki rollerden bağımsız olarak; küresel vizyonunuza, dinamizminize ve NarTech’e değer katacağınıza inanıyorsanız sizi tanımak isteriz!</span>
          <span class="lang-en">Regardless of specific open roles, if you believe your global vision and drive will enrich NarTech, we look forward to meeting you!</span>
        </p>
        <ul class="role-points">
          <li><span class="lang-tr">Sınır tanımayan, sonuç odaklı profesyoneller</span><span class="lang-en">Ambitious, boundary-pushing professionals</span></li>
          <li><span class="lang-tr">Özgeçmişiniz İK veri tabanımızda öncelikli saklanır</span><span class="lang-en">Your profile receives priority review in our talent pool</span></li>
        </ul>
        <div class="role-action">
          <a class="button button-outline" href="mailto:sales@nartech.com.tr?subject=Kariyer%20Genel%20Basvurusu%20-%20NarTech"><span class="lang-tr">Genel Başvuru Yap</span><span class="lang-en">Submit Application</span> ↗</a>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Recruitment Process Section -->
<section class="career-section career-process-section">
  <div class="page-wrap">
    <div class="section-title-wrap text-center">
      <div class="about-subtitle"><span class="lang-tr">NASIL ÇALIŞIYORUZ?</span><span class="lang-en">HOW WE HIRE</span></div>
      <h2><span class="lang-tr">İşe Alım Yolculuğu</span><span class="lang-en">Our Recruitment Journey</span></h2>
      <p class="section-lead-muted"><span class="lang-tr">Adaylarımızın zamanına saygı duyan, şeffaf ve hızlı ilerleyen 4 adımlı süreç.</span><span class="lang-en">A transparent, rapid 4-step process respecting every candidate's time.</span></p>
    </div>

    <div class="career-process-grid">
      <div class="career-step-item">
        <div class="step-num-box">01</div>
        <h4><span class="lang-tr">Başvuru &amp; İnceleme</span><span class="lang-en">Application Review</span></h4>
        <p><span class="lang-tr">Özgeçmişiniz insan kaynakları ve ilgili departman liderleri tarafından 48 saat içinde incelenir.</span><span class="lang-en">Your CV is reviewed within 48 hours by HR and department leaders.</span></p>
      </div>
      <div class="career-step-item">
        <div class="step-num-box">02</div>
        <h4><span class="lang-tr">Tanışma Görüşmesi</span><span class="lang-en">Culture &amp; Intro</span></h4>
        <p><span class="lang-tr">Kültürümüz, hedefleriniz ve ortak vizyonumuz üzerine ilk karşılıklı değerlendirme toplantısı.</span><span class="lang-en">An introductory conversation exploring shared vision, culture, and goals.</span></p>
      </div>
      <div class="career-step-item">
        <div class="step-num-box">03</div>
        <h4><span class="lang-tr">Teknik Değerlendirme</span><span class="lang-en">Technical Deep-Dive</span></h4>
        <p><span class="lang-tr">Rolün gerektirdiği uzmanlık alanında vaka analizi ve karşılıklı teknik sohbet.</span><span class="lang-en">Role-specific discussion, case assessment, and domain expertise alignment.</span></p>
      </div>
      <div class="career-step-item">
        <div class="step-num-box">04</div>
        <h4><span class="lang-tr">Teklif &amp; Katılım</span><span class="lang-en">Offer &amp; Welcome</span></h4>
        <p><span class="lang-tr">Şeffaf teklif süreci ve NarTech’in global ticaret ekosistemine hızlı oryantasyon.</span><span class="lang-en">A transparent offer package and onboarding into our global trade ecosystem.</span></p>
      </div>
    </div>
  </div>
</section>

<!-- Direct Application / CTA Section -->
<section class="career-application" id="application-channel">
  <div class="page-wrap">
    <div class="career-application-panel">
      <div class="career-application-copy">
        <div class="about-subtitle"><span class="lang-tr">EKİBİMİZE KATILIN</span><span class="lang-en">JOIN OUR TEAM</span></div>
        <h2><span class="lang-tr">Başvuru Kanalı</span><span class="lang-en">Application Channel</span></h2>
        <p><span class="lang-tr">Güncel özgeçmişinizi ve ilgilendiğiniz uzmanlık alanını belirterek bize e-posta gönderin veya iletişim sayfamızdan ulaşın.</span><span class="lang-en">Email your current CV and the area you are interested in, or reach us through our contact page.</span></p>
      </div>
      <div class="career-application-actions">
        <a class="button career-apply-button" href="mailto:sales@nartech.com.tr?subject=Kariyer%20Basvurusu%20-%20NarTech">
          <span class="career-action-label"><span class="lang-tr">E-posta ile Başvur</span><span class="lang-en">Apply by Email</span></span>
          <span class="career-action-detail">sales@nartech.com.tr</span>
          <span class="career-action-icon" aria-hidden="true">↗</span>
        </a>
        <a class="button career-contact-button" href="contact.html">
          <span class="career-action-label"><span class="lang-tr">İletişim Sayfası</span><span class="lang-en">Contact Page</span></span>
          <span class="career-action-detail"><span class="lang-tr">Bize ulaşın</span><span class="lang-en">Get in touch</span></span>
          <span class="career-action-icon" aria-hidden="true">→</span>
        </a>
      </div>
    </div>
  </div>
</section>
</div>'''
(OUT/"career.html").write_text(layout("Kariyer",career_body,"career",title_en="Career"),encoding="utf-8")

contact_body = '''<div class="page-wrap form-page contact-page"><div class="page-heading"><h1><span class="lang-tr">İletişim</span><span class="lang-en">Contact Us</span></h1></div><div class="contact-layout"><aside class="contact-info-panel"><div class="contact-info-card"><div class="contact-badge"><span class="lang-tr">Merkez Ofis &amp; Satış</span><span class="lang-en">Head Office &amp; Sales</span></div><h2 class="contact-office-title"><span class="lang-tr">Türkiye Merkez Ofis + Satış</span><span class="lang-en">Head Office &amp; Sales (Turkey)</span></h2><div class="contact-item"><div class="contact-item-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg></div><div class="contact-item-text"><strong class="contact-item-label"><span class="lang-tr">Adres</span><span class="lang-en">Address</span></strong><p class="contact-item-value"><span class="lang-tr">Fatih Mah. 30020 Sok. Güzelyalı Sit. Güzel Yalı Sitesi No: 29B İç Kapı No: 4, Mezitli, Mersin, Türkiye</span><span class="lang-en">Fatih Mah. 30020 Sok. Güzelyalı Sit. Güzel Yalı Sitesi No: 29B, Apt. 4, Mezitli, Mersin, Türkiye</span></p></div></div><div class="contact-item"><div class="contact-item-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg></div><div class="contact-item-text"><strong class="contact-item-label"><span class="lang-tr">E-Posta</span><span class="lang-en">Email</span></strong><p class="contact-item-value"><a href="mailto:sales@nartech.com.tr">sales@nartech.com.tr</a></p></div></div><div class="contact-note"><span class="lang-tr">Proje talepleriniz, teknik şartname uyumu ve ürün teklifleri için bizimle doğrudan iletişime geçebilir veya formu doldurabilirsiniz.</span><span class="lang-en">For project inquiries, technical specification compliance, and quotation requests, reach out directly or submit the form.</span></div></div></aside><section class="form-panel contact-form-panel"><form id="contact-form" class="form-grid"><input name="product" id="contact-product" type="hidden"><div class="form-field"><label for="contact-name"><span class="lang-tr">Ad Soyad</span><span class="lang-en">Full Name</span></label><input id="contact-name" name="name" autocomplete="name" required></div><div class="form-field"><label for="contact-phone"><span class="lang-tr">Telefon No</span><span class="lang-en">Phone</span></label><input id="contact-phone" name="phone" type="tel" autocomplete="tel" required></div><div class="form-field"><label for="contact-message"><span class="lang-tr">Açıklama</span><span class="lang-en">Description</span></label><textarea id="contact-message" name="description" required></textarea></div><button class="button button-primary" type="submit"><span class="lang-tr">Gönder</span><span class="lang-en">Send</span></button><p class="form-status" id="contact-status" role="status" aria-live="polite"></p></form></section></div></div>'''
(OUT/"contact.html").write_text(layout("İletişim",contact_body,"contact",title_en="Contact Us"),encoding="utf-8")

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
urls=['index.html','about.html','what-we-do.html','services.html','products.html','calculator.html','career.html','faq.html','contact.html']
urls += [f'categories/{c["id"]}.html' for c in categories]
urls += [f'products/{x["id"]}.html' for c in categories for x in flatten(c['items'])]
base_url='https://nartech.com.tr/'
sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{base_url if u == "index.html" else base_url + u}</loc></url>\n' for u in urls)+'</urlset>\n'
(OUT/"sitemap.xml").write_text(sitemap,encoding="utf-8")
print(f"Generated {len(urls)} source-backed pages.")
