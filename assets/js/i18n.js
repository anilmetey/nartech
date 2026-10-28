/**
 * Nartech Engineering Comprehensive Bilingual Dictionary (TR / EN)
 * Complete parity for all pages, product subheadings, and appointment forms.
 */
const translations = {
  tr: {
    // Navigation
    nav_home: "Ana Sayfa",
    nav_about: "Hakkımızda",
    nav_products: "Ürünler & Ekipmanlar",
    nav_services: "Saha Süpervizörlüğü",
    nav_faq: "SSS",
    nav_contact: "İletişim & Teklif",
    nav_rfq_btn: "Teklif Al (RFQ)",
    nav_appointment_btn: "Randevu Al",
    
    // Taglines & Hero
    company_title: "Nartech Mühendislik",
    company_subtitle: "Endüstriyel Akış & Depolama Güvenlik Sistemleri",
    hero_tagline: "Doğru Mühendislik. Doğru Ürün. Doğru Zamanda.",
    hero_title: "Petrol, Gaz ve Endüstriyel Tesisler İçin Yüksek Standartlı Mühendislik Çözümleri",
    hero_desc: "Petrol & Gaz, Petrokimya, Kimya, Su, Upstream, Downstream ve Offshore sektörlerinde; uluslararası güvenlik, kalite ve performans standartlarına tam uyumlu mühendislik çözümleri sunuyor; müşterilerimizin şartnamelerine özel tasarlanmış ürünler geliştiriyoruz.",
    hero_cta_primary: "Mühendislik Teklifi Al (RFQ)",
    hero_cta_appointment: "Mühendislik Randevusu Al",
    hero_cta_secondary: "Ürün Kataloğunu İncele",
    hero_sectors_label: "Hizmet Verilen Sektörler:",
    hero_badge_photo: "CANLI PROJE UYGULAMASI: TANK ÇİFTLİĞİ VE TERMİNAL EKİPMANLARI",

    // Specs Bar
    spec_exp_val: "10+ Yıl",
    spec_exp_lbl: "Sektörel Mühendislik Deneyimi",
    spec_std_val: "API & EN",
    spec_std_lbl: "API 650, 2000 ve EN ISO 16852 Uyumu",
    spec_cert_val: "FM & ATEX",
    spec_cert_lbl: "Patlayıcı Ortam ve Yangın Güvenliği",
    spec_eng_val: "%100",
    spec_eng_lbl: "Proje Şartnamesine Özel Boyutlandırma",

    // Slogan Section
    slogan_sub: "Mühendislik Felsefemiz",
    slogan_title: "Her Proje, Bizim İçin Önce Bir Mühendislik Problemidir.",
    slogan_desc: "Ürün seçiminden tedarike kadar tüm süreci bu bakış açısıyla ele alıyoruz. Sektörün önde gelen EPC yüklenicileri ve son kullanıcıları için gerçekleştirdiğimiz projeler, kompleks endüstriyel ihtiyaçları yakından tanımamızı sağlıyor; uluslararası standartlara ve proje şartnamelerine tam uyumlu çözümler sunuyoruz.",
    slogan_goal: "Hedefimiz basit: Doğru ürünü, doğru çözümü, doğru zamanda sunmak.",

    // Appointment / Randevu Section
    appointment_title: "Mühendislik Randevusu Alın",
    appointment_sub: "Ad Soyad, Telefon ve Açıklama girerek uzman mühendislik ekibimizle randevu oluşturun. Bilgiler doğrudan sisteme e-posta ile iletilir.",
    form_appointment_fullname: "Adınız Soyadınız",
    form_appointment_phone: "Telefon Numaranız",
    form_appointment_date: "Tercih Edilen Tarih",
    form_appointment_desc: "Açıklama / Randevu Talebi Notu",
    form_appointment_desc_ph: "Lütfen randevu konusu, projeniz veya görüşmek istediğiniz teknik ekipman hakkında kısa bilgi giriniz...",
    form_appointment_submit: "Randevu Talebini E-posta İle Gönder",
    form_appointment_success: "Randevu talebiniz başarıyla alındı ve teknik ekibimize e-posta bildirimi olarak iletildi. En kısa sürede sizinle iletişime geçilecektir.",

    // Products Section
    products_badge: "Mühendislik Onaylı Ürün Grubu",
    products_title: "Rafineri, Tank Çiftliği ve Boru Hattı Ekipmanları",
    products_desc: "Tüm ürünlerimiz uluslararası güvenlik, basınç ve sızdırmazlık standartlarına (API 650, API 2000, EN ISO 16852, ATEX, FM/UL) uygun olarak boyutlandırılır ve temin edilir.",
    products_all_btn: "Tüm Ürünleri Gör",
    filter_all: "Tümü",
    filter_tank: "Depolama Tankı Ekipmanları",
    filter_fire: "Yangın Söndürme (FM/UL)",
    filter_pig: "Pig & Temizleme",
    filter_other: "Vana, Emiş & Çevre",

    // Categories in products.html
    cat_1_title: "Depolama Tankı Ekipmanları",
    cat_1_desc: "API 650 ve API 2000 standartlarına uygun, ATEX sertifikalı kritik tank koruma ve güvenlik donanımları.",
    cat_2_title: "Yangın Söndürme Ekipmanları (FM / UL Onaylı)",
    cat_2_desc: "Rafineri, petrokimya ve tank çiftlikleri için FM onaylı ve UL listeli yüksek standartlı yangın koruma donanımları.",
    cat_3_title: "Pig Temizleme Ekipmanları & Dedektörleri",
    cat_3_desc: "Boru hatlarında temizlik, ürün ayrıştırma ve geçiş takibi için endüstri standardı ekipmanlar.",
    cat_4_title: "Endüstriyel Susturucular (Gürültü Kontrolü ≤ 85 dB)",
    cat_5_title: "Yüzer Emiş Üniteleri (Havacılık ve Temiz Ürün Emişi)",
    cat_6_title: "Geri Sarmalı Topraklama Kablosu (ATEX RGR)",
    cat_7_title: "Dolum Kolları, Vanalar ve Proses Sistemleri",

    // Supervision Services Section
    services_badge: "Teknik Denetim ve Güvenlik",
    services_title: "Saha Süpervizörlük Hizmetleri",
    services_desc: "Uzman mühendis kadromuzla rafineri ve terminallerde kritik tank ekipmanlarının montaj, set değeri ve sızdırmazlık kontrollerini sahada gerçekleştiriyoruz.",
    service_1_title: "PVRV Set Değerlerinin Kontrolü",
    service_1_desc: "Basınç vakum ventilleri (PVRV), tankların aşırı basınç veya vakum altında kalarak deforme olmasını ya da patlamasını önleyen en kritik emniyet ekipmanlarıdır.",
    service_1_detail: "Fiziksel ve fonksiyonel set değeri doğrulama kontrolleri uzmanlarımızca sahada raporlanır.",
    service_2_title: "İç Yüzer Tavanların (IFR) Kontrolü",
    service_2_desc: "Uçucu organik bileşik (VOC) emisyonlarını azaltmak ve ürün kaybını önlemek amacıyla kullanılan iç yüzer tavanlar, hassas mekanik montaj gerektirir.",
    service_2_detail: "Rim seal (kenar sızdırmazlık) fitillerinin montaj kalitesi, iniş bacaklarının (leg settings) doğru pozisyonlandırılması ve drenaj sistemlerinin çalışabilirliği denetlenir.",
    service_3_title: "Dış Yüzer Tavanların (EFR) Kontrolü",
    service_3_desc: "Uçucu organik bileşik (VOC) emisyonlarını azaltmak ve ürün kaybını önlemek amacıyla kullanılan dış yüzer tavanlar hassas denetim gerektirir.",
    service_3_detail: "Rim seal (kenar sızdırmazlık) fitillerinin montaj kalitesi ve sızdırmazlık performansı denetlenir.",

    // Spare Parts & EPC Section
    epc_title: "EPC Yüklenicileri ve Tesisler İçin Kritik Yedek Parça Erişimi",
    epc_desc: "Endüstriyel tesisler ve terminaller için kritik yedek parçalara hızlı ve güvenilir erişim sağlıyoruz. Duruş sürelerini minimuma indiren güvenilir tedarik zinciri altyapısı.",

    // RFQ / Contact
    rfq_badge: "Doğrudan Mühendislik İletişimi",
    rfq_modal_title: "Mühendislik Teklif Talebi (RFQ)",
    rfq_modal_sub: "Şartnamenize ve proses koşullarınıza uygun teklif almak için lütfen detayları iletiniz.",
    form_fullname: "Adınız Soyadınız",
    form_company: "Şirket / Kurum Adı",
    form_email: "Kurumsal E-posta",
    form_phone: "Telefon Numarası",
    form_product: "İlgilenilen Ürün / Hizmet",
    form_details: "Proje Şartnamesi & Proses Koşulları",
    form_details_placeholder: "Lütfen ürün tipi, tank çapı, çalışma basıncı/sıcaklığı, akışkan cinsi veya ilgili standartları belirtiniz...",
    form_submit: "Teklif Talebini Gönder",
    form_sending: "Gönderiliyor...",
    form_success: "Talebiniz başarıyla alındı. Mühendislik ekibimiz en kısa sürede şartnamenizi inceleyip sizinle iletişime geçecektir.",
    form_error: "Form gönderilirken bir hata oluştu. Lütfen bilgilerinizi kontrol edip tekrar deneyiniz.",

    // Footer
    footer_desc: "Petrol & Gaz, Petrokimya, Kimya, Su, Upstream, Downstream ve Offshore sektörlerine uluslararası standartlarda mühendislik çözümleri ve ekipman tedariki.",
    footer_quick_links: "Hızlı Bağlantılar",
    footer_products_col: "Ürün Grupları",
    footer_contact_col: "İletişim & Lokasyon",
    footer_tagline: "Doğru Mühendislik. Doğru Ürün. Doğru Zamanda.",
    footer_rights: "Tüm hakları saklıdır. Uluslararası standartlara uygun mühendislik güvencesi.",
    footer_direct_rfq: "Doğrudan Teklif İletin →",
    footer_privacy: "Gizlilik & KVKK Politikası"
  },
  en: {
    // Navigation
    nav_home: "Home",
    nav_about: "About Us",
    nav_products: "Products & Equipment",
    nav_services: "Field Supervision",
    nav_faq: "FAQ",
    nav_contact: "Contact & RFQ",
    nav_rfq_btn: "Request a Quote (RFQ)",
    nav_appointment_btn: "Book Appointment",

    // Taglines & Hero
    company_title: "Nartech Engineering",
    company_subtitle: "Industrial Flow & Storage Safety Systems",
    hero_tagline: "The Right Engineering. The Right Product. The Right Time.",
    hero_title: "High-Specification Engineering Solutions for Oil, Gas & Industrial Facilities",
    hero_desc: "In the Oil & Gas, Petrochemical, Chemical, Water, Upstream, Downstream, and Offshore sectors, we deliver international-standard engineering solutions in full compliance with global safety, quality, and performance codes, and develop products tailor-made to our client's specifications.",
    hero_cta_primary: "Request Engineering Quote (RFQ)",
    hero_cta_appointment: "Book Engineering Appointment",
    hero_cta_secondary: "Explore Product Range",
    hero_sectors_label: "Sectors Served:",
    hero_badge_photo: "LIVE FIELD APPLICATION: TANK FARM & TERMINAL EQUIPMENT",

    // Specs Bar
    spec_exp_val: "10+ Years",
    spec_exp_lbl: "Specialized Engineering Experience",
    spec_std_val: "API & EN",
    spec_std_lbl: "API 650, 2000 & EN ISO 16852 Compliance",
    spec_cert_val: "FM & ATEX",
    spec_cert_lbl: "Explosive Atmosphere & Fire Safety",
    spec_eng_val: "100%",
    spec_eng_lbl: "Custom Sized to Project Specifications",

    // Slogan Section
    slogan_sub: "Our Engineering Philosophy",
    slogan_title: "For Us, Every Project is First and Foremost an Engineering Problem.",
    slogan_desc: "We approach the entire process from product selection to procurement from this same perspective. The projects we have delivered for leading EPC contractors and end users give us close, first-hand insight into complex industrial requirements, enabling us to provide solutions fully aligned with international standards and project specifications.",
    slogan_goal: "Our goal is simple: the right product, the right solution, at the right time.",

    // Appointment / Randevu Section
    appointment_title: "Book an Engineering Appointment",
    appointment_sub: "Schedule an on-site audit or technical session by providing your Name, Phone Number, and Agenda notes. Notifications are dispatched directly to engineering email.",
    form_appointment_fullname: "Full Name",
    form_appointment_phone: "Phone Number",
    form_appointment_date: "Preferred Date",
    form_appointment_desc: "Description / Consultation Notes",
    form_appointment_desc_ph: "Please specify consultation topic, project requirements, or target equipment...",
    form_appointment_submit: "Submit Appointment via Email",
    form_appointment_success: "Your appointment request has been recorded and dispatched to our engineering email. We will contact you shortly.",

    // Products Section
    products_badge: "Engineering Approved Range",
    products_title: "Refinery, Tank Farm and Pipeline Equipment",
    products_desc: "All our products are sized and supplied in accordance with international safety, pressure, and containment standards (API 650, API 2000, EN ISO 16852, ATEX, FM/UL).",
    products_all_btn: "View All Products",
    filter_all: "All",
    filter_tank: "Storage Tank Equipment",
    filter_fire: "Fire Fighting (FM/UL)",
    filter_pig: "Pigging & Cleaning",
    filter_other: "Valves, Suction & Safety",

    // Categories in products.html
    cat_1_title: "Storage Tank Equipments",
    cat_1_desc: "API 650 and API 2000 certified, ATEX approved critical tank safety and containment equipment.",
    cat_2_title: "Fire Fighting Equipments (FM / UL Approved)",
    cat_2_desc: "FM Approved and UL Listed high-standard fire suppression equipment for refineries, petrochemical plants, and tank farms.",
    cat_3_title: "Pig Cleaning Equipments & Pig Signallers",
    cat_3_desc: "Industry-standard pipeline scrapers, batching pigs, and intrusive/non-intrusive passage detectors.",
    cat_4_title: "Industrial Silencers (Noise Control <= 85 dB)",
    cat_5_title: "Floating Suction Units (Aviation & Clean Product Draw)",
    cat_6_title: "Retractable Grounding Cable (ATEX RGR)",
    cat_7_title: "Loading Arms, Valves and Process Systems",

    // Supervision Services Section
    services_badge: "Technical Audit & Integrity",
    services_title: "Field Supervision Services",
    services_desc: "With our experienced engineering team, we carry out on-site inspection, set-point verification, and seal integrity audits for critical tank equipment in refineries and terminals.",
    service_1_title: "PVRV Set Value Verification",
    service_1_desc: "Pressure Vacuum Relief Valves (PVRV) are the most critical safety equipment preventing tanks from collapsing under vacuum or over-pressurizing.",
    service_1_detail: "Physical and functional set-point verification checks are rigorously audited and reported on-site.",
    service_2_title: "Internal Floating Roof (IFR) Inspection",
    service_2_desc: "Internal floating roofs used to curb volatile organic compound (VOC) emissions and prevent product evaporation require precise mechanical assembly.",
    service_2_detail: "Rim seal installation quality, landing leg settings positioning, and drainage system operability are thoroughly audited.",
    service_3_title: "External Floating Roof (EFR) Inspection",
    service_3_desc: "External floating roofs deployed to reduce VOC emissions and eliminate product loss require exacting mechanical installation checks.",
    service_3_detail: "Rim seal installation quality and sealing effectiveness are evaluated under field operating conditions.",

    // Spare Parts & EPC Section
    epc_title: "Fast Access to Critical Spare Parts for EPCs and Operators",
    epc_desc: "We ensure fast, reliable access to critical spare parts for industrial facilities and terminals, minimizing operational downtime with a dependable supply chain.",

    // RFQ / Contact
    rfq_badge: "Direct Engineering Communication",
    rfq_modal_title: "Request for Engineering Quotation (RFQ)",
    rfq_modal_sub: "Please provide your project specifications and process conditions to receive a compliant technical offer.",
    form_fullname: "Full Name",
    form_company: "Company / Organization",
    form_email: "Corporate Email",
    form_phone: "Phone Number",
    form_product: "Equipment / Service of Interest",
    form_details: "Project Specifications & Operating Conditions",
    form_details_placeholder: "Specify tank diameter, operating temperature/pressure, medium, flow rate or target standards...",
    form_submit: "Submit RFQ",
    form_sending: "Submitting...",
    form_success: "Your RFQ has been received. Our engineering department will review your specifications and contact you shortly.",
    form_error: "An error occurred while submitting. Please check the fields and try again.",

    // Footer
    footer_desc: "International-standard engineering solutions and equipment procurement for Oil & Gas, Petrochemical, Chemical, Water, Upstream, Downstream, and Offshore facilities.",
    footer_quick_links: "Quick Links",
    footer_products_col: "Product Lines",
    footer_contact_col: "Contact & Location",
    footer_tagline: "Right Engineering. Right Product. Right Time.",
    footer_rights: "All rights reserved. Certified to international engineering standards.",
    footer_direct_rfq: "Submit Direct RFQ →",
    footer_privacy: "Privacy Policy"
  }
};

if (typeof module !== 'undefined' && module.exports) {
  module.exports = translations;
}
