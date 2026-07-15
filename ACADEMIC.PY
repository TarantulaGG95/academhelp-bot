import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    filters, ContextTypes, ConversationHandler
)

BOT_TOKEN = "8852741001:AAFZxKwuXDpgk9YAf6Fc5sMdIeH2v6uCKg8"
ADMIN_ID = 5846813939
MENEJER_TEL = "+998946267555"
MENEJER_TG = "@Karaevmladshii"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

(
    TIL_TANLASH, XIZMAT_TURI, ENTRY_XIZMAT, MIDDLE_XIZMAT,
    PREMIUM_XIZMAT, HAJM_TANLASH, TEMA, MUDDAT,
    TALABLAR, KONTAKT, TOLOV_TURI, CHEK,
) = range(12)

# === UNIVERSITETLAR ===
UNIVERSITETLAR = {
    "BuxDU": "Buxoro Davlat Universiteti (BuxDU)",
    "BDTI": "Buxoro Davlat Tibbiyot Instituti (BDTI)",
    "BMTI": "Buxoro Muhandislik-Texnologiya Instituti (BMTI)",
    "BDPI": "Buxoro Davlat Pedagogika Instituti (BDPI)",
    "BPXTI": "Buxoro Psixologiya va Xorijiy Tillar Instituti (BPXTI)",
    "BITI": "Buxoro Innovatsion Tibbiyot Instituti (BITI)",
    "TZU": "Turon Zarmed Universiteti (TZU)",
    "OXU": "Osiyo Xalqaro Universiteti (OXU)",
    "BIU": "Buxoro Innovatsiyalar Universiteti (BIU)",
    "TYIU": "Turkiston Yangi Innovatsiyalar Universiteti (TYIU)",
    "AndDU": "Andijon Davlat Universiteti (AndDU)",
    "ADTI": "Andijon Davlat Tibbiyot Instituti (ADTI)",
    "ADPI": "Andijon Davlat Pedagogika Instituti (ADPI)",
    "AMTI": "Andijon Mashinasozlik Instituti (AMTI)",
    "AQXEI": "Andijon Qishloq Xo'jaligi va Ekologiya Instituti (AQXEI)",
    "CHU": "Collegium Humanum Varshava Universiteti Andijon (CHU)",
    "ShardaU": "Sharda University Andijon (ShardaU)",
    "UEP": "University of Economic and Pedagogy Andijon (UEP)",
    "NUUz": "O'zbekiston Milliy Universiteti (NUUz)",
    "TDTU": "Toshkent Davlat Tibbiyot Universiteti (TDTU)",
    "TATU": "Toshkent Axborot Texnologiyalari Universiteti (TATU)",
    "TDIU": "Toshkent Davlat Iqtisodiyot Universiteti (TDIU)",
    "ToshDTU": "Islom Karimov nomidagi Toshkent DTU (ToshDTU)",
    "TDPU": "Toshkent Davlat Pedagogika Universiteti (TDPU)",
    "TDYuU": "Toshkent Davlat Yuridik Universiteti (TDYuU)",
    "TTESI": "Toshkent To'qimachilik va Engil Sanoat Instituti (TTESI)",
    "TQTI": "Toshkent Kimyo Texnologiya Instituti (TQTI)",
    "TMI": "Toshkent Moliya Instituti (TMI)",
    "TDSHI": "Toshkent Davlat Sharqshunoslik Instituti (TDSHI)",
    "OzDSMI": "O'zbekiston Davlat San'at va Madaniyat Instituti (OzDSMI)",
    "OzMU": "O'zbekiston Milliy Musiqa Universiteti (OzMU)",
    "ToshDAU": "Toshkent Davlat Agrar Universiteti (ToshDAU)",
    "OzDJTI": "O'zbekiston Davlat Jismoniy Tarbiya Instituti (OzDJTI)",
    "WIUT": "Westminster Xalqaro Universiteti (WIUT)",
    "Inha": "Inha University Tashkent (Inha)",
    "Turin": "Turin Politexnika Universiteti Toshkent (Turin)",
    "MDU": "Lomonosov nomidagi MDU Toshkent filiali (MDU)",
    "RIEU": "Rossiya Iqtisodiyot Universiteti Toshkent filiali (RIEU)",
    "KXU": "Kimyo Xalqaro Universiteti (KXU)",
    "SRIU": "Silk Road International University (SRIU)",
}

# === NARXLAR ===
NARXLAR = {
    "referat": {
        "10-30 bet": "100 000 so'm",
        "30-50 bet": "150 000 so'm",
        "50-80 bet": "200 000 so'm",
        "80-120 bet": "250 000 so'm",
        "120+ bet": "300 000 so'm+"
    },
    "diplom": {
        "10-30 bet": "500 000 so'm",
        "30-50 bet": "750 000 so'm",
        "50-80 bet": "1 000 000 so'm",
        "80-120 bet": "1 250 000 so'm",
        "120+ bet": "1 500 000 so'm+"
    },
    "konferensiya": {
        "Mahalliy": "100 000 so'm",
        "Xalqaro": "300 000 so'm"
    },
    "gost": {
        "10-30 bet": "50 000 so'm",
        "30-50 bet": "75 000 so'm",
        "50-80 bet": "100 000 so'm",
        "80-120 bet": "125 000 so'm",
        "120+ bet": "150 000 so'm+"
    },
    "magistr": {
        "50-80 bet": "1 500 000 so'm",
        "80-120 bet": "3 000 000 so'm",
        "120+ bet": "6 000 000 so'm+"
    },
    "vak_mahalliy": {
        "Small": "$100",
        "Medium": "$200",
        "Large": "$300"
    },
    "vak_xalqaro": {
        "Small": "$150",
        "Medium": "$250",
        "Large": "$300"
    },
    "scopus_q3q4": {
        "Small": "$300",
        "Medium": "$500",
        "Large": "$800"
    },
    "scopus_q1q2": {
        "Small": "$800",
        "Medium": "$1 000",
        "Large": "$1 200"
    },
    "adabiyotlar": {
        "20-40 manba": "500 000 so'm",
        "40-60 manba": "750 000 so'm",
        "60+ manba": "1 000 000 so'm"
    },
    "biostatistika": {
        "Simple / Oddiy / Простой": "600 000 so'm",
        "Medium / O'rta / Средний": "900 000 so'm",
        "Complex / Murakkab / Сложный": "1 200 000 so'm"
    },
    "meta_analiz": {
        "Simple / Oddiy / Простой": "2 000 000 so'm",
        "Medium / O'rta / Средний": "3 000 000 so'm",
        "Complex / Murakkab / Сложный": "4 000 000 so'm"
    },
    "data_analytics": {
        "Simple / Oddiy / Простой": "1 500 000 so'm",
        "Medium / O'rta / Средний": "2 500 000 so'm",
        "Complex / Murakkab / Сложный": "3 500 000 so'm"
    },
}

MUDDAT_FOIZ = {
    "1 hafta": "+50%",
    "2 hafta": "+40%",
    "1 oy": "+30%",
    "2 oy": "+20%",
    "3 oy": "+15%",
    "6 oy": "Standart narx",
    "12 oy": "-10%",
    "18 oy": "-12%",
    "24 oy": "-15%",
}

def btn(rows):
    return InlineKeyboardMarkup([[InlineKeyboardButton(t, callback_data=t) for t in row] for row in rows])

def til(ctx):
    return ctx.user_data.get("til", "uz")

START_MATNI = {
    "uz": """👋 *Salom! Ilmiy ishlar bo'yicha professional ko'mak markaziga xush kelibsiz!*

🎓 Bu yerda siz yetuk mutaxassislar yordamida barcha turdagi akademik ishlar uchun mukammal ko'mak olasiz.

━━━━━━━━━━━━━━━
📚 *BIZNING XIZMATLARIMIZ:*

📝 *ENTRY — Boshlang'ich darajadagi ishlar*
• Referat va kurs ishlari — 100 000 so'mdan
• Diplom ishlari — 500 000 so'mdan
• Konferensiya maqolalari — 100 000 so'mdan
• GOST formatlash — 50 000 so'mdan

📘 *MIDDLE — O'rta daraja*
• Magistrlik dissertatsiyasi — 1 500 000 so'mdan
• VAK/RINTS maqolalar — $100 dan
• Scopus Q3-Q4 — $300 dan
• Adabiyotlar sharhi — 500 000 so'mdan
• Biostatistika — 600 000 so'mdan

🏆 *PREMIUM — Yuqori daraja*
• Scopus Q1-Q2 — $800 dan
• Meta-analiz — 2 000 000 so'mdan
• Data analytics — 1 500 000 so'mdan
• Grant ariza — kelishiladi
• PhD dissertatsiya — $2 000 dan
• Doktorlik dissertatsiya — $5 000 dan

💎 *VIP — Maxsus xizmatlar*
• Monografiya — 3 000 000 so'mdan
• Patent (kafolat bilan) — 7 000 000 so'mdan

⚖️ *YURIDIK YORDAM*
• Talaba va magistrlarning o'quv jarayonidagi huquqiy masalalar
• Ilmiy faoliyat bilan bog'liq nizolar
• Muassasa bilan huquqiy muloqot

━━━━━━━━━━━━━━━
⏰ *Muddat bo'yicha narx:*
• Tezkor (1-2 hafta): +30–50% qo'shimcha
• Standart (6 oy): asosiy narx
• Uzoq muddat (24 oy): −15% chegirma

✅ *Kafolatlar:* Sifat, maxfiylik, o'z vaqtida topshirish

📞 Savol bo'lsa: {menejer} | {tel}
━━━━━━━━━━━━━━━

🌐 *Tilni tanlang:*""",

    "ru": """👋 *Добро пожаловать в профессиональный центр помощи в научных работах!*

🎓 Здесь вы получите квалифицированную помощь в подготовке академических работ любого уровня.

━━━━━━━━━━━━━━━
📚 *НАШИ УСЛУГИ:*

📝 *ENTRY — Базовый уровень*
• Рефераты и курсовые — от 100 000 сум
• Дипломные работы — от 500 000 сум
• Статьи конференций — от 100 000 сум
• Оформление по ГОСТ — от 50 000 сум

📘 *MIDDLE — Средний уровень*
• Магистерская диссертация — от 1 500 000 сум
• Статьи ВАК/РИНЦ — от $100
• Scopus Q3-Q4 — от $300
• Обзор литературы — от 500 000 сум
• Биостатистика — от 600 000 сум

🏆 *PREMIUM — Высокий уровень*
• Scopus Q1-Q2 — от $800
• Мета-анализ — от 2 000 000 сум
• Аналитика данных — от 1 500 000 сум
• Грантовая заявка — по договорённости
• Диссертация PhD — от $2 000
• Докторская диссертация — от $5 000

💎 *VIP — Специальные услуги*
• Монография — от 3 000 000 сум
• Патент (с гарантией) — от 7 000 000 сум

⚖️ *ЮРИДИЧЕСКАЯ ПОМОЩЬ*
• Правовые вопросы в учебном процессе
• Споры, связанные с научной деятельностью
• Правовое взаимодействие с учреждением

━━━━━━━━━━━━━━━
⏰ *Стоимость по срокам:*
• Срочно (1–2 нед.): +30–50% надбавка
• Стандарт (6 мес.): базовая цена
• Долгосрочно (24 мес.): −15% скидка

✅ *Гарантии:* Качество, конфиденциальность, соблюдение сроков

📞 По вопросам: {menejer} | {tel}
━━━━━━━━━━━━━━━

🌐 *Выберите язык:*""",

    "en": """👋 *Welcome to the Professional Academic Assistance Center!*

🎓 Here you will receive expert help with academic works of any level.

━━━━━━━━━━━━━━━
📚 *OUR SERVICES:*

📝 *ENTRY — Basic level*
• Essays & Course works — from 100 000 UZS
• Bachelor's thesis — from 500 000 UZS
• Conference papers — from 100 000 UZS
• GOST formatting — from 50 000 UZS

📘 *MIDDLE — Intermediate level*
• Master's dissertation — from 1 500 000 UZS
• VAK/RINC articles — from $100
• Scopus Q3-Q4 — from $300
• Literature review — from 500 000 UZS
• Biostatistics — from 600 000 UZS

🏆 *PREMIUM — Advanced level*
• Scopus Q1-Q2 — from $800
• Meta-analysis — from 2 000 000 UZS
• Data analytics — from 1 500 000 UZS
• Grant application — negotiable
• PhD dissertation — from $2 000
• Doctoral dissertation — from $5 000

💎 *VIP — Special services*
• Monograph — from 3 000 000 UZS
• Patent (with guarantee) — from 7 000 000 UZS

⚖️ *LEGAL ASSISTANCE*
• Legal issues in the study process
• Disputes related to scientific activities
• Legal interaction with institutions

━━━━━━━━━━━━━━━
⏰ *Price by deadline:*
• Urgent (1–2 weeks): +30–50% surcharge
• Standard (6 months): base price
• Long-term (24 months): −15% discount

✅ *Guarantees:* Quality, confidentiality, on-time delivery

📞 Contact: {menejer} | {tel}
━━━━━━━━━━━━━━━

🌐 *Choose language:*"""
}

XIZMAT_TURI_MATNI = {
    "uz": """📋 *Xizmat turini tanlang:*

📝 *Entry* — Referat, Diplom, Konferensiya, GOST
📘 *Middle* — Magistr, VAK, Scopus Q3-Q4
🏆 *Premium* — PhD, Scopus Q1-Q2, Meta-analiz
💎 *VIP* — Monografiya, Patent
⚖️ *Yuridik yordam* — Huquqiy masalalar""",
    "ru": """📋 *Выберите тип услуги:*

📝 *Entry* — Реферат, Диплом, Конференция, ГОСТ
📘 *Middle* — Магистр, ВАК, Scopus Q3-Q4
🏆 *Premium* — PhD, Scopus Q1-Q2, Мета-анализ
💎 *VIP* — Монография, Патент
⚖️ *Юридическая помощь* — Правовые вопросы""",
    "en": """📋 *Choose service type:*

📝 *Entry* — Essay, Thesis, Conference, GOST
📘 *Middle* — Master's, VAK, Scopus Q3-Q4
🏆 *Premium* — PhD, Scopus Q1-Q2, Meta-analysis
💎 *VIP* — Monograph, Patent
⚖️ *Legal assistance* — Legal issues"""
}

ENTRY_KARTOCHKALAR = {
    "uz": [
        {
            "matn": "📝 *Referat / Kurs ishi*\n\n📏 Hajm: 10 betdan 120+ betgacha\n💰 Narx: 100 000 — 300 000 so'm\n\n_Standart akademik talablarga to'liq mos holda tayyorlanadi_",
            "tugma": "✅ Referat / Kurs ishi",
            "key": "referat"
        },
        {
            "matn": "🎓 *Diplom ishi*\n\n📏 Hajm: 10 betdan 120+ betgacha\n💰 Narx: 500 000 — 1 500 000 so'm\n\n_Davlat standartlari va universitet talablariga mos_",
            "tugma": "✅ Diplom ishi",
            "key": "diplom"
        },
        {
            "matn": "📊 *Konferensiya maqolasi*\n\n🏛 Mahalliy: 100 000 so'm\n🌍 Xalqaro: 300 000 so'm\n\n_GOST va xalqaro standartlarga mos formatlash bilan_",
            "tugma": "✅ Konferensiya maqolasi",
            "key": "konferensiya"
        },
        {
            "matn": "📋 *GOST formatlash*\n\n📏 Hajm: 10 betdan 120+ betgacha\n💰 Narx: 50 000 — 150 000 so'm\n\n_Rasmiy talablarga to'liq muvofiqlashtirish_",
            "tugma": "✅ GOST formatlash",
            "key": "gost"
        },
    ],
    "ru": [
        {
            "matn": "📝 *Реферат / Курсовая работа*\n\n📏 Объём: от 10 до 120+ страниц\n💰 Цена: 100 000 — 300 000 сум\n\n_Полное соответствие академическим стандартам_",
            "tugma": "✅ Реферат / Курсовая",
            "key": "referat"
        },
        {
            "matn": "🎓 *Дипломная работа*\n\n📏 Объём: от 10 до 120+ страниц\n💰 Цена: 500 000 — 1 500 000 сум\n\n_По государственным и университетским стандартам_",
            "tugma": "✅ Дипломная работа",
            "key": "diplom"
        },
        {
            "matn": "📊 *Статья для конференции*\n\n🏛 Местная: 100 000 сум\n🌍 Международная: 300 000 сум\n\n_С форматированием по ГОСТ и международным стандартам_",
            "tugma": "✅ Статья конференции",
            "key": "konferensiya"
        },
        {
            "matn": "📋 *Оформление по ГОСТ*\n\n📏 Объём: от 10 до 120+ страниц\n💰 Цена: 50 000 — 150 000 сум\n\n_Полное приведение к официальным требованиям_",
            "tugma": "✅ Оформление ГОСТ",
            "key": "gost"
        },
    ],
    "en": [
        {
            "matn": "📝 *Essay / Course work*\n\n📏 Volume: 10 to 120+ pages\n💰 Price: 100 000 — 300 000 UZS\n\n_Full compliance with academic standards_",
            "tugma": "✅ Essay / Course work",
            "key": "referat"
        },
        {
            "matn": "🎓 *Bachelor's thesis*\n\n📏 Volume: 10 to 120+ pages\n💰 Price: 500 000 — 1 500 000 UZS\n\n_According to state and university standards_",
            "tugma": "✅ Bachelor's thesis",
            "key": "diplom"
        },
        {
            "matn": "📊 *Conference paper*\n\n🏛 Local: 100 000 UZS\n🌍 International: 300 000 UZS\n\n_With GOST and international standard formatting_",
            "tugma": "✅ Conference paper",
            "key": "konferensiya"
        },
        {
            "matn": "📋 *GOST formatting*\n\n📏 Volume: 10 to 120+ pages\n💰 Price: 50 000 — 150 000 UZS\n\n_Full compliance with official requirements_",
            "tugma": "✅ GOST formatting",
            "key": "gost"
        },
    ],
}

MIDDLE_KARTOCHKALAR = {
    "uz": [
        {"matn": "📘 *Magistrlik dissertatsiyasi*\n\n📏 Hajm: 50 betdan 120+ betgacha\n💰 Narx: 1 500 000 — 6 000 000 so'm\n\n_Ilmiy standartlarga to'liq mos, rahbar talablari inobatga olinadi_", "tugma": "✅ Magistrlik dissertatsiyasi", "key": "magistr"},
        {"matn": "📑 *VAK/RINTS maqolasi (mahalliy)*\n\n📏 Hajm: material va jurnalga qarab\n💰 Narx: $100 — $300\n\n_Mahalliy akkreditatsiyalangan jurnallar uchun_", "tugma": "✅ VAK mahalliy", "key": "vak_mahalliy"},
        {"matn": "📑 *VAK/RINTS maqolasi (xalqaro)*\n\n📏 Hajm: material va jurnalga qarab\n💰 Narx: $150 — $300\n\n_Xalqaro indekslanadigan jurnallar uchun_", "tugma": "✅ VAK xalqaro", "key": "vak_xalqaro"},
        {"matn": "🔬 *Scopus Q3-Q4 maqolasi*\n\n⏰ Muddat: 6 oydan 24 oygacha\n💰 Narx: $300 — $800\n\n_Hajm va jurnalga qarab narx belgilanadi_", "tugma": "✅ Scopus Q3-Q4", "key": "scopus_q3q4"},
        {"matn": "📚 *Adabiyotlar sharhi*\n\n📏 Hajm: 20 manbadan 60+ manbacha\n💰 Narx: 500 000 — 1 000 000 so'm\n\n_Ilmiy manbalar to'liq tahlili va sharhi_", "tugma": "✅ Adabiyotlar sharhi", "key": "adabiyotlar"},
        {"matn": "📊 *Biostatistika*\n\n💰 Narx: 600 000 — 1 200 000 so'm\n\n_Tibbiy, biologik va ijtimoiy tadqiqotlar uchun_", "tugma": "✅ Biostatistika", "key": "biostatistika"},
    ],
    "ru": [
        {"matn": "📘 *Магистерская диссертация*\n\n📏 Объём: от 50 до 120+ страниц\n💰 Цена: 1 500 000 — 6 000 000 сум\n\n_С учётом требований научного руководителя_", "tugma": "✅ Магистерская", "key": "magistr"},
        {"matn": "📑 *Статья ВАК/РИНЦ (местный)*\n\n📏 Зависит от объёма и журнала\n💰 Цена: $100 — $300\n\n_Для местных аккредитованных журналов_", "tugma": "✅ ВАК местный", "key": "vak_mahalliy"},
        {"matn": "📑 *Статья ВАК/РИНЦ (международный)*\n\n📏 Зависит от объёма и журнала\n💰 Цена: $150 — $300\n\n_Для международных индексируемых журналов_", "tugma": "✅ ВАК международный", "key": "vak_xalqaro"},
        {"matn": "🔬 *Статья Scopus Q3-Q4*\n\n⏰ Срок: от 6 до 24 месяцев\n💰 Цена: $300 — $800\n\n_Цена зависит от журнала и объёма_", "tugma": "✅ Scopus Q3-Q4", "key": "scopus_q3q4"},
        {"matn": "📚 *Обзор литературы*\n\n📏 Объём: от 20 до 60+ источников\n💰 Цена: 500 000 — 1 000 000 сум\n\n_Полный анализ и обзор научных источников_", "tugma": "✅ Обзор литературы", "key": "adabiyotlar"},
        {"matn": "📊 *Биостатистика*\n\n💰 Цена: 600 000 — 1 200 000 сум\n\n_Для медицинских и социальных исследований_", "tugma": "✅ Биостатистика", "key": "biostatistika"},
    ],
    "en": [
        {"matn": "📘 *Master's dissertation*\n\n📏 Volume: 50 to 120+ pages\n💰 Price: 1 500 000 — 6 000 000 UZS\n\n_Considering supervisor requirements_", "tugma": "✅ Master's dissertation", "key": "magistr"},
        {"matn": "📑 *VAK/RINC article (local)*\n\n📏 Depends on volume and journal\n💰 Price: $100 — $300\n\n_For locally accredited journals_", "tugma": "✅ VAK local", "key": "vak_mahalliy"},
        {"matn": "📑 *VAK/RINC article (international)*\n\n📏 Depends on volume and journal\n💰 Price: $150 — $300\n\n_For internationally indexed journals_", "tugma": "✅ VAK international", "key": "vak_xalqaro"},
        {"matn": "🔬 *Scopus Q3-Q4 article*\n\n⏰ Deadline: 6 to 24 months\n💰 Price: $300 — $800\n\n_Price depends on journal and volume_", "tugma": "✅ Scopus Q3-Q4", "key": "scopus_q3q4"},
        {"matn": "📚 *Literature review*\n\n📏 Volume: 20 to 60+ sources\n💰 Price: 500 000 — 1 000 000 UZS\n\n_Full analysis and review of scientific sources_", "tugma": "✅ Literature review", "key": "adabiyotlar"},
        {"matn": "📊 *Biostatistics*\n\n💰 Price: 600 000 — 1 200 000 UZS\n\n_For medical and social research_", "tugma": "✅ Biostatistics", "key": "biostatistika"},
    ],
}

PREMIUM_KARTOCHKALAR = {
    "uz": [
        {"matn": "⭐ *Scopus Q1-Q2 maqolasi*\n\n⏰ Muddat: 6 oydan 24 oygacha\n💰 Narx: $800 — $1 200\n\n_Hajm va jurnalga qarab narx belgilanadi. Eng nufuzli xalqaro jurnallar uchun_", "tugma": "✅ Scopus Q1-Q2", "key": "scopus_q1q2"},
        {"matn": "🔍 *Meta-analiz / Tizimli tahlil*\n\n💰 Narx: 2 000 000 — 4 000 000 so'm\n\n_Ilmiy tadqiqotlar sintezi va to'liq tizimli tahlil_", "tugma": "✅ Meta-analiz", "key": "meta_analiz"},
        {"matn": "📈 *Data analytics*\n\n💰 Narx: 1 500 000 — 3 500 000 so'm\n\n_Ma'lumotlar tahlili, vizualizatsiya va interpretatsiya_", "tugma": "✅ Data analytics", "key": "data_analytics"},
        {"matn": "📝 *Grant ariza*\n\n💰 Narx: Kelishiladi\n\n_Xalqaro va mahalliy grantlar uchun professional ariza tayyorlash_", "tugma": "✅ Grant ariza", "key": "grant"},
        {"matn": "🏆 *PhD dissertatsiyasi (Fan nomzodligi)*\n\n⏰ Muddat va narx:\n• 12 oygacha: $3 500 va undan yuqori\n• 12–18 oy: $2 500 — $3 000\n• 18 oydan ko'p: $2 000 dan boshlanadi\n\n_Menejer bilan batafsil muhokama qilinadi_", "tugma": "✅ PhD dissertatsiyasi", "key": "phd"},
        {"matn": "🎖 *Doktorlik dissertatsiyasi (DSc)*\n\n💰 Narx: $5 000 dan boshlanadi\n\n_Muddat va hajmga qarab narx belgilanadi. Menejer bilan batafsil muhokama qilinadi_", "tugma": "✅ Doktorlik dissertatsiyasi", "key": "doktorlik"},
    ],
    "ru": [
        {"matn": "⭐ *Статья Scopus Q1-Q2*\n\n⏰ Срок: от 6 до 24 месяцев\n💰 Цена: $800 — $1 200\n\n_Цена зависит от журнала и объёма. Самые престижные международные журналы_", "tugma": "✅ Scopus Q1-Q2", "key": "scopus_q1q2"},
        {"matn": "🔍 *Мета-анализ / Системный анализ*\n\n💰 Цена: 2 000 000 — 4 000 000 сум\n\n_Синтез научных исследований и системный анализ_", "tugma": "✅ Мета-анализ", "key": "meta_analiz"},
        {"matn": "📈 *Аналитика данных*\n\n💰 Цена: 1 500 000 — 3 500 000 сум\n\n_Анализ данных, визуализация и интерпретация_", "tugma": "✅ Data analytics", "key": "data_analytics"},
        {"matn": "📝 *Грантовая заявка*\n\n💰 Цена: По договорённости\n\n_Профессиональная подготовка заявок на международные и местные гранты_", "tugma": "✅ Грантовая заявка", "key": "grant"},
        {"matn": "🏆 *Диссертация PhD (Кандидатская)*\n\n⏰ Сроки и цены:\n• До 12 мес.: от $3 500\n• 12–18 мес.: $2 500 — $3 000\n• Более 18 мес.: от $2 000\n\n_Детали обсуждаются с менеджером_", "tugma": "✅ Диссертация PhD", "key": "phd"},
        {"matn": "🎖 *Докторская диссертация (DSc)*\n\n💰 Цена: от $5 000\n\n_Цена зависит от срока и объёма. Детали обсуждаются с менеджером_", "tugma": "✅ Докторская", "key": "doktorlik"},
    ],
    "en": [
        {"matn": "⭐ *Scopus Q1-Q2 article*\n\n⏰ Deadline: 6 to 24 months\n💰 Price: $800 — $1 200\n\n_Price depends on journal and volume. Top international journals_", "tugma": "✅ Scopus Q1-Q2", "key": "scopus_q1q2"},
        {"matn": "🔍 *Meta-analysis / Systematic analysis*\n\n💰 Price: 2 000 000 — 4 000 000 UZS\n\n_Synthesis of scientific research and systematic analysis_", "tugma": "✅ Meta-analysis", "key": "meta_analiz"},
        {"matn": "📈 *Data analytics*\n\n💰 Price: 1 500 000 — 3 500 000 UZS\n\n_Data analysis, visualization and interpretation_", "tugma": "✅ Data analytics", "key": "data_analytics"},
        {"matn": "📝 *Grant application*\n\n💰 Price: Negotiable\n\n_Professional preparation of grant applications_", "tugma": "✅ Grant application", "key": "grant"},
        {"matn": "🏆 *PhD dissertation*\n\n⏰ Deadlines and prices:\n• Up to 12 months: from $3 500\n• 12–18 months: $2 500 — $3 000\n• Over 18 months: from $2 000\n\n_Details discussed with manager_", "tugma": "✅ PhD dissertation", "key": "phd"},
        {"matn": "🎖 *Doctoral dissertation (DSc)*\n\n💰 Price: from $5 000\n\n_Price depends on deadline and volume. Details discussed with manager_", "tugma": "✅ Doctoral dissertation", "key": "doktorlik"},
    ],
}

VIP_KARTOCHKALAR = {
    "uz": [
        {"matn": "📖 *Monografiya*\n\n💰 Narx: 3 000 000 — 7 000 000 so'm\n\n_To'liq ilmiy asar, barcha standartlarga muvofiq_", "tugma": "✅ Monografiya", "key": "monografiya"},
        {"matn": "💡 *Patent*\n\n💰 Narx: 7 000 000 so'mdan\n\n_Xizmatga davlat boji ham kiritilgan. Ixtironing hujjatlashtirilishi va bahslashtirib bo'lmasligi kafolati (сопровождение и гарантия неоспариваемости)_", "tugma": "✅ Patent", "key": "patent"},
    ],
    "ru": [
        {"matn": "📖 *Монография*\n\n💰 Цена: 3 000 000 — 7 000 000 сум\n\n_Полный научный труд, соответствующий всем стандартам_", "tugma": "✅ Монография", "key": "monografiya"},
        {"matn": "💡 *Патент*\n\n💰 Цена: от 7 000 000 сум\n\n_Включает госпошлину. Сопровождение и гарантия неоспариваемости_", "tugma": "✅ Патент", "key": "patent"},
    ],
    "en": [
        {"matn": "📖 *Monograph*\n\n💰 Price: 3 000 000 — 7 000 000 UZS\n\n_Complete scientific work meeting all standards_", "tugma": "✅ Monograph", "key": "monografiya"},
        {"matn": "💡 *Patent*\n\n💰 Price: from 7 000 000 UZS\n\n_Includes state fee. Support and guarantee of non-contestability_", "tugma": "✅ Patent", "key": "patent"},
    ],
}

MUDDAT_TUGMALAR = {
    "uz": [["1 hafta", "2 hafta"], ["1 oy", "2 oy"], ["3 oy", "6 oy"], ["12 oy", "18 oy"], ["24 oy"]],
    "ru": [["1 неделя", "2 недели"], ["1 месяц", "2 месяца"], ["3 месяца", "6 месяцев"], ["12 месяцев", "18 месяцев"], ["24 месяца"]],
    "en": [["1 week", "2 weeks"], ["1 month", "2 months"], ["3 months", "6 months"], ["12 months", "18 months"], ["24 months"]],
}

MUDDAT_MAP = {
    "1 hafta": "1 hafta", "2 hafta": "2 hafta", "1 oy": "1 oy", "2 oy": "2 oy",
    "3 oy": "3 oy", "6 oy": "6 oy", "12 oy": "12 oy", "18 oy": "18 oy", "24 oy": "24 oy",
    "1 неделя": "1 hafta", "2 недели": "2 hafta", "1 месяц": "1 oy", "2 месяца": "2 oy",
    "3 месяца": "3 oy", "6 месяцев": "6 oy", "12 месяцев": "12 oy", "18 месяцев": "18 oy", "24 месяца": "24 oy",
    "1 week": "1 hafta", "2 weeks": "2 hafta", "1 month": "1 oy", "2 months": "2 oy",
    "3 months": "3 oy", "6 months": "6 oy", "12 months": "12 oy", "18 months": "18 oy", "24 months": "24 oy",
}

def ortga_btn(t):
    ortga = {"uz": "🔙 Ortga", "ru": "🔙 Назад", "en": "🔙 Back"}
    return ortga.get(t, "🔙 Ortga")

def m(ctx, key):
    t = til(ctx)
    matnlar = {
        "uz": {
            "til_tanlang": "Iltimos, tilni tanlang 👆",
            "hajm": "📏 *Hajm va narxni tanlang:*\n\n",
            "tema": "✏️ *Ishingizning mavzusini kiriting:*\n\n📌 _Masalan: «Raqamlashtirish iqtisodiyotga ta'siri»_",
            "tema_xato": "⚠️ *Iltimos, mavzuni to'liqroq kiriting!*",
            "muddat": "⏰ *Ish muddatini tanlang:*\n\n💡 _Muddat qanchalik qisqa bo'lsa, narxga qo'shimcha foiz qo'shiladi. Uzoq muddatda chegirma beriladi._",
            "talablar": "📋 *Qo'shimcha ma'lumotlarni kiriting:*\n\n🏛 Universitetingiz nomi\n📚 Kurs / yil / mutaxassislik\n📝 Rasmiylashtirish talablari _(GOST, APA, MLA...)_\n🌐 Ish tili _(O'zbek, Rus, Ingliz)_\n📍 Shahringiz",
            "talablar_xato": "⚠️ *Iltimos, ma'lumotlarni to'liqroq kiriting!*",
            "kontakt": "📞 *Telefon raqam yoki Telegram username kiriting:*",
            "tolov": "💳 *To'lov usulini tanlang:*",
            "uzcard": "💳 *UzCard orqali to'lov:*\n\n🔢 Karta: `6262 5700 7026 5220`\n👤 Egasi: *QARAYEV ULUGBEK*\n\n💰 Miqdor: *{narx}*\n\n📸 *To'lovdan so'ng chek rasmini yuboring!*",
            "visa": "💳 *Visa orqali to'lov:*\n\n🔢 Karta: `4278 3100 2613 3181`\n👤 Egasi: *QARAYEV ULUGBEK*\n\n💰 Miqdor: *{narx}*\n\n📸 *To'lovdan so'ng chek rasmini yuboring!*",
            "usdt": "💰 *USDT (TRC20) orqali to'lov:*\n\n🔢 Manzil:\n`TUv1qZ1Cxmh5aao877J4xB43MTXz5w6Y`\n\n💵 Miqdor: *{narx}*\n\n📸 *To'lovdan so'ng chek rasmini yuboring!*",
            "chek_sorovi": "🧾 *Chek rasmini yuboring:*\n\n📸 Rasm _(foto chek)_\n📱 Skrinshot\n📄 Fayl",
            "chek_xato": "⚠️ *Iltimos, chekni rasm yoki fayl sifatida yuboring!*",
            "rahmat": "✅ *Buyurtmangiz qabul qilindi!*\n\n⏳ Tez orada mutaxassisimiz siz bilan bog'lanadi\n\n📞 Admin: @Karaevmladshii\n☎️ Tel: +998946267555\n\n🙏 *Bizga ishonganingiz uchun rahmat!*",
            "menejer": "📞 *Menejer bilan bog'lanish:*\n\nTelegram: @Karaevmladshii\nTel: +998946267555\n\nMenejerimiz siz bilan tez orada bog'lanadi!",
            "yuridik": "⚖️ *Yuridik yordam xizmati*\n\nBiz quyidagi masalalar bo'yicha yordam beramiz:\n\n• Talaba va magistrlarning o'quv jarayonidagi huquqiy masalalar\n• Ilmiy faoliyat bilan bog'liq nizolar\n• O'quv muassasasi bilan huquqiy muloqot\n• Akademik huquqlar himoyasi\n\n📞 Menejer: @Karaevmladshii\n☎️ Tel: +998946267555\n\nMuammoingizni bizga yozing — mutaxassisimiz yordam beradi!",
            "bekor": "❌ *Bekor qilindi*\n\n/start — qaytadan boshlash",
            "tushunmadim": "❓ *Tushunmadim*\n\n/start — qaytadan boshlash",
            "entry_sarlavha": "📝 *Entry xizmatlari:*\n\nQuyidagilardan birini tanlang 👇",
            "middle_sarlavha": "📘 *Middle xizmatlari:*\n\nQuyidagilardan birini tanlang 👇",
            "premium_sarlavha": "🏆 *Premium xizmatlari:*\n\nQuyidagilardan birini tanlang 👇",
            "vip_sarlavha": "💎 *VIP xizmatlari:*\n\nQuyidagilardan birini tanlang 👇",
        },
        "ru": {
            "til_tanlang": "Пожалуйста, выберите язык 👆",
            "hajm": "📏 *Выберите объём и цену:*\n\n",
            "tema": "✏️ *Введите тему работы:*\n\n📌 _Например: «Влияние цифровизации на экономику»_",
            "tema_xato": "⚠️ *Пожалуйста, введите тему полнее!*",
            "muddat": "⏰ *Выберите срок выполнения:*\n\n💡 _Чем короче срок — тем выше надбавка. При длительном сроке предоставляется скидка._",
            "talablar": "📋 *Введите дополнительную информацию:*\n\n🏛 Название университета\n📚 Курс / год / специальность\n📝 Требования к оформлению _(ГОСТ, APA, MLA...)_\n🌐 Язык работы _(Узбекский, Русский, Английский)_\n📍 Ваш город",
            "talablar_xato": "⚠️ *Пожалуйста, введите информацию полнее!*",
            "kontakt": "📞 *Введите номер телефона или Telegram username:*",
            "tolov": "💳 *Выберите способ оплаты:*",
            "uzcard": "💳 *Оплата через UzCard:*\n\n🔢 Карта: `6262 5700 7026 5220`\n👤 Владелец: *QARAYEV ULUGBEK*\n\n💰 Сумма: *{narx}*\n\n📸 *После оплаты отправьте чек!*",
            "visa": "💳 *Оплата через Visa:*\n\n🔢 Карта: `4278 3100 2613 3181`\n👤 Владелец: *QARAYEV ULUGBEK*\n\n💰 Сумма: *{narx}*\n\n📸 *После оплаты отправьте чек!*",
            "usdt": "💰 *Оплата через USDT (TRC20):*\n\n🔢 Адрес:\n`TUv1qZ1Cxmh5aao877J4xB43MTXz5w6Y`\n\n💵 Сумма: *{narx}*\n\n📸 *После оплаты отправьте чек!*",
            "chek_sorovi": "🧾 *Отправьте чек об оплате:*\n\n📸 Фото\n📄 Файл",
            "chek_xato": "⚠️ *Пожалуйста, отправьте чек в виде фото или файла!*",
            "rahmat": "✅ *Ваш заказ принят!*\n\n⏳ Наш специалист свяжется с вами\n\n📞 Админ: @Karaevmladshii\n☎️ Тел: +998946267555\n\n🙏 *Спасибо, что доверились нам!*",
            "menejer": "📞 *Связаться с менеджером:*\n\nTelegram: @Karaevmladshii\nТел: +998946267555\n\nНаш менеджер свяжется с вами в ближайшее время!",
            "yuridik": "⚖️ *Юридическая помощь*\n\nМы помогаем по следующим вопросам:\n\n• Правовые вопросы в учебном процессе студентов и магистрантов\n• Споры, связанные с научной деятельностью\n• Правовое взаимодействие с учебным заведением\n• Защита академических прав\n\n📞 Менеджер: @Karaevmladshii\n☎️ Тел: +998946267555\n\nОпишите вашу проблему — наш специалист поможет!",
            "bekor": "❌ *Отменено*\n\n/start — начать заново",
            "tushunmadim": "❓ *Не понял*\n\n/start — начать заново",
            "entry_sarlavha": "📝 *Услуги Entry:*\n\nВыберите одну из них 👇",
            "middle_sarlavha": "📘 *Услуги Middle:*\n\nВыберите одну из них 👇",
            "premium_sarlavha": "🏆 *Услуги Premium:*\n\nВыберите одну из них 👇",
            "vip_sarlavha": "💎 *Услуги VIP:*\n\nВыберите одну из них 👇",
        },
        "en": {
            "til_tanlang": "Please choose a language 👆",
            "hajm": "📏 *Choose volume and price:*\n\n",
            "tema": "✏️ *Enter your topic:*\n\n📌 _Example: «Impact of digitalization on economy»_",
            "tema_xato": "⚠️ *Please enter the topic in more detail!*",
            "muddat": "⏰ *Choose deadline:*\n\n💡 _The shorter the deadline — the higher the surcharge. Long-term orders get a discount._",
            "talablar": "📋 *Enter additional information:*\n\n🏛 University name\n📚 Course / year / specialization\n📝 Formatting requirements _(GOST, APA, MLA...)_\n🌐 Language _(Uzbek, Russian, English)_\n📍 Your city",
            "talablar_xato": "⚠️ *Please enter the information in more detail!*",
            "kontakt": "📞 *Enter your phone number or Telegram username:*",
            "tolov": "💳 *Choose payment method:*",
            "uzcard": "💳 *Payment via UzCard:*\n\n🔢 Card: `6262 5700 7026 5220`\n👤 Owner: *QARAYEV ULUGBEK*\n\n💰 Amount: *{narx}*\n\n📸 *After payment, send receipt!*",
            "visa": "💳 *Payment via Visa:*\n\n🔢 Card: `4278 3100 2613 3181`\n👤 Owner: *QARAYEV ULUGBEK*\n\n💰 Amount: *{narx}*\n\n📸 *After payment, send receipt!*",
            "usdt": "💰 *Payment via USDT (TRC20):*\n\n🔢 Address:\n`TUv1qZ1Cxmh5aao877J4xB43MTXz5w6Y`\n\n💵 Amount: *{narx}*\n\n📸 *After payment, send receipt!*",
            "chek_sorovi": "🧾 *Send your payment receipt:*\n\n📸 Photo\n📄 File",
            "chek_xato": "⚠️ *Please send receipt as photo or file!*",
            "rahmat": "✅ *Your order received!*\n\n⏳ Our specialist will contact you\n\n📞 Admin: @Karaevmladshii\n☎️ Tel: +998946267555\n\n🙏 *Thank you for choosing us!*",
            "menejer": "📞 *Contact manager:*\n\nTelegram: @Karaevmladshii\nTel: +998946267555\n\nOur manager will contact you soon!",
            "yuridik": "⚖️ *Legal assistance*\n\nWe help with:\n\n• Legal issues in students' and master's study process\n• Disputes related to scientific activities\n• Legal interaction with educational institutions\n• Academic rights protection\n\n📞 Manager: @Karaevmladshii\n☎️ Tel: +998946267555\n\nDescribe your problem — our specialist will help!",
            "bekor": "❌ *Cancelled*\n\n/start — start again",
            "tushunmadim": "❓ *I didn't understand*\n\n/start — start again",
            "entry_sarlavha": "📝 *Entry services:*\n\nChoose one 👇",
            "middle_sarlavha": "📘 *Middle services:*\n\nChoose one 👇",
            "premium_sarlavha": "🏆 *Premium services:*\n\nChoose one 👇",
            "vip_sarlavha": "💎 *VIP services:*\n\nChoose one 👇",
        },
    }
    return matnlar.get(t, matnlar["uz"]).get(key, "")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    if context.args:
        referal = context.args[0]
        univer_nomi = UNIVERSITETLAR.get(referal, f"Noma'lum ({referal})")
        context.user_data["referal"] = referal
        context.user_data["universitet"] = univer_nomi
    else:
        context.user_data["referal"] = "Bevosita"
        context.user_data["universitet"] = "Bevosita"

    keyboard = btn([["🇺🇿 O'zbek", "🇷🇺 Русский", "🇬🇧 English"]])
    matn = "🌐 *Tilni tanlang / Выберите язык / Choose language:*"
    if update.message:
        await update.message.reply_text(matn, reply_markup=keyboard, parse_mode="Markdown")
    else:
        await update.callback_query.message.reply_text(matn, reply_markup=keyboard, parse_mode="Markdown")
    return TIL_TANLASH

async def til_tanlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if "O'zbek" in q.data:
        context.user_data["til"] = "uz"
    elif "Русский" in q.data:
        context.user_data["til"] = "ru"
    elif "English" in q.data:
        context.user_data["til"] = "en"
    else:
        await q.message.reply_text(m(context, "til_tanlang"))
        return TIL_TANLASH
    t = til(context)
    keyboard = btn([["📝 Entry", "📘 Middle"], ["🏆 Premium", "💎 VIP"], ["⚖️ Yuridik yordam" if t=="uz" else "⚖️ Юридическая помощь" if t=="ru" else "⚖️ Legal assistance"]])
    await q.message.edit_text(XIZMAT_TURI_MATNI[t], reply_markup=keyboard, parse_mode="Markdown")
    return XIZMAT_TURI

async def xizmat_turi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    t = til(context)
    ortga = ortga_btn(t)
    data = q.data

    if ortga in data:
        # Ortga — til tanlashga qaytish
        keyboard = btn([["🇺🇿 O'zbek", "🇷🇺 Русский", "🇬🇧 English"]])
        matn = "👋 *Salom! / Привет! / Hello!*\n\n🌐 *Tilni tanlang / Выберите язык / Choose language:*"
        await q.message.edit_text(matn, reply_markup=keyboard, parse_mode="Markdown")
        return TIL_TANLASH

    if "Entry" in data:
        context.user_data["xizmat_turi"] = "Entry"
        kartochkalar = ENTRY_KARTOCHKALAR[t]
        sarlavha = m(context, "entry_sarlavha")
    elif "Middle" in data:
        context.user_data["xizmat_turi"] = "Middle"
        kartochkalar = MIDDLE_KARTOCHKALAR[t]
        sarlavha = m(context, "middle_sarlavha")
    elif "Premium" in data:
        context.user_data["xizmat_turi"] = "Premium"
        kartochkalar = PREMIUM_KARTOCHKALAR[t]
        sarlavha = m(context, "premium_sarlavha")
    elif "VIP" in data:
        context.user_data["xizmat_turi"] = "VIP"
        kartochkalar = VIP_KARTOCHKALAR[t]
        sarlavha = m(context, "vip_sarlavha")
    elif "Yuridik" in data or "Юридическая" in data or "Legal" in data:
        await q.message.edit_text(m(context, "yuridik"), parse_mode="Markdown",
            reply_markup=btn([[ortga]]))
        return XIZMAT_TURI
    else:
        return XIZMAT_TURI

    await q.message.edit_text(sarlavha, parse_mode="Markdown")
    for k in kartochkalar:
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(k["tugma"], callback_data=f"xizmat_{k['key']}")]])
        await q.message.reply_text(k["matn"], reply_markup=keyboard, parse_mode="Markdown")
    await q.message.reply_text("─" * 20, reply_markup=btn([[ortga]]))

    tur = context.user_data.get("xizmat_turi")
    if tur == "Entry":
        return ENTRY_XIZMAT
    elif tur == "Middle":
        return MIDDLE_XIZMAT
    else:
        return PREMIUM_XIZMAT

async def xizmat_tanlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    t = til(context)
    ortga = ortga_btn(t)

    if ortga in data:
        # Ortga — 4 ta xizmat turi ga qaytish (Entry/Middle/Premium/VIP)
        t2 = til(context)
        tur = context.user_data.get("xizmat_turi", "Entry")
        if tur == "Entry":
            kartochkalar = ENTRY_KARTOCHKALAR[t2]
            sarlavha = m(context, "entry_sarlavha")
            next_state = ENTRY_XIZMAT
        elif tur == "Middle":
            kartochkalar = MIDDLE_KARTOCHKALAR[t2]
            sarlavha = m(context, "middle_sarlavha")
            next_state = MIDDLE_XIZMAT
        elif tur == "Premium":
            kartochkalar = PREMIUM_KARTOCHKALAR[t2]
            sarlavha = m(context, "premium_sarlavha")
            next_state = PREMIUM_XIZMAT
        else:
            kartochkalar = VIP_KARTOCHKALAR[t2]
            sarlavha = m(context, "vip_sarlavha")
            next_state = PREMIUM_XIZMAT
        ortga2 = ortga_btn(t2)
        await q.message.edit_text(sarlavha, parse_mode="Markdown")
        for k in kartochkalar:
            keyboard2 = InlineKeyboardMarkup([[InlineKeyboardButton(k["tugma"], callback_data=f"xizmat_{k['key']}")]])
            await q.message.reply_text(k["matn"], reply_markup=keyboard2, parse_mode="Markdown")
        await q.message.reply_text("─" * 20, reply_markup=btn([[ortga2]]))
        return next_state

    if not data.startswith("xizmat_"):
        return ENTRY_XIZMAT

    key = data.replace("xizmat_", "")

    NOMLAR = {
        "referat": {"uz": "Referat / Kurs ishi", "ru": "Реферат / Курсовая", "en": "Essay / Course work"},
        "diplom": {"uz": "Diplom ishi", "ru": "Дипломная работа", "en": "Bachelor's thesis"},
        "konferensiya": {"uz": "Konferensiya maqolasi", "ru": "Статья конференции", "en": "Conference paper"},
        "gost": {"uz": "GOST formatlash", "ru": "Оформление ГОСТ", "en": "GOST formatting"},
        "magistr": {"uz": "Magistrlik dissertatsiyasi", "ru": "Магистерская диссертация", "en": "Master's dissertation"},
        "vak_mahalliy": {"uz": "VAK/RINTS (mahalliy)", "ru": "ВАК/РИНЦ (местный)", "en": "VAK/RINC (local)"},
        "vak_xalqaro": {"uz": "VAK/RINTS (xalqaro)", "ru": "ВАК/РИНЦ (международный)", "en": "VAK/RINC (international)"},
        "scopus_q3q4": {"uz": "Scopus Q3-Q4", "ru": "Scopus Q3-Q4", "en": "Scopus Q3-Q4"},
        "scopus_q1q2": {"uz": "Scopus Q1-Q2", "ru": "Scopus Q1-Q2", "en": "Scopus Q1-Q2"},
        "adabiyotlar": {"uz": "Adabiyotlar sharhi", "ru": "Обзор литературы", "en": "Literature review"},
        "biostatistika": {"uz": "Biostatistika", "ru": "Биостатистика", "en": "Biostatistics"},
        "meta_analiz": {"uz": "Meta-analiz", "ru": "Мета-анализ", "en": "Meta-analysis"},
        "data_analytics": {"uz": "Data analytics", "ru": "Аналитика данных", "en": "Data analytics"},
        "grant": {"uz": "Grant ariza", "ru": "Грантовая заявка", "en": "Grant application"},
        "monografiya": {"uz": "Monografiya", "ru": "Монография", "en": "Monograph"},
        "patent": {"uz": "Patent", "ru": "Патент", "en": "Patent"},
    }

    if key in ["phd", "doktorlik"]:
        nom = {"phd": {"uz": "PhD dissertatsiyasi", "ru": "Диссертация PhD", "en": "PhD dissertation"},
               "doktorlik": {"uz": "Doktorlik dissertatsiyasi (DSc)", "ru": "Докторская диссертация (DSc)", "en": "Doctoral dissertation (DSc)"}}[key][t]
        context.user_data["xizmat"] = nom
        context.user_data["hajm_narx"] = f"{nom} | Menejer bilan kelishiladi"
        context.user_data["narx"] = "Kelishiladi"
        izoh = {
            "phd": {
                "uz": "🏆 *PhD dissertatsiyasi (Fan nomzodligi)*\n\n⏰ *Muddat va narx:*\n• 12 oygacha: $3 500 va undan yuqori\n• 12–18 oy: $2 500 — $3 000\n• 18 oydan ko'p: $2 000 dan boshlanadi\n\n📌 _Narx va muddat individual ravishda menejer bilan kelishiladi_\n\n📞 Bog'lanish uchun quyidagi tugmani bosing:",
                "ru": "🏆 *Диссертация PhD (Кандидатская)*\n\n⏰ *Сроки и цены:*\n• До 12 мес.: от $3 500\n• 12–18 мес.: $2 500 — $3 000\n• Более 18 мес.: от $2 000\n\n📌 _Цена и срок обсуждаются индивидуально с менеджером_\n\n📞 Нажмите кнопку для связи:",
                "en": "🏆 *PhD Dissertation*\n\n⏰ *Deadlines and prices:*\n• Up to 12 months: from $3 500\n• 12–18 months: $2 500 — $3 000\n• Over 18 months: from $2 000\n\n📌 _Price and deadline are discussed individually with manager_\n\n📞 Press button to contact:"
            },
            "doktorlik": {
                "uz": "🎖 *Doktorlik dissertatsiyasi (DSc)*\n\n💰 Narx: $5 000 dan boshlanadi\n\n📌 _Muddat va hajmga qarab narx belgilanadi. Individual ravishda menejer bilan kelishiladi_\n\n📞 Bog'lanish uchun quyidagi tugmani bosing:",
                "ru": "🎖 *Докторская диссертация (DSc)*\n\n💰 Цена: от $5 000\n\n📌 _Цена зависит от срока и объёма. Обсуждается индивидуально с менеджером_\n\n📞 Нажмите кнопку для связи:",
                "en": "🎖 *Doctoral Dissertation (DSc)*\n\n💰 Price: from $5 000\n\n📌 _Price depends on deadline and volume. Discussed individually with manager_\n\n📞 Press button to contact:"
            }
        }[key][t]
        menejer_btn = {
            "uz": "📞 Menejer bilan bog'lanish",
            "ru": "📞 Связаться с менеджером",
            "en": "📞 Contact manager"
        }[t]
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(menejer_btn, url=f"https://t.me/Karaevmladshii")],
            [InlineKeyboardButton(ortga, callback_data=ortga)]
        ])
        await q.message.reply_text(izoh, reply_markup=keyboard, parse_mode="Markdown")
        return PREMIUM_XIZMAT

    if key in ["grant", "monografiya", "patent"]:
        narxlar_fixed = {
            "grant": {"uz": "Kelishiladi", "ru": "По договорённости", "en": "Negotiable"},
            "monografiya": {"uz": "3 000 000 — 7 000 000 so'm", "ru": "3 000 000 — 7 000 000 сум", "en": "3 000 000 — 7 000 000 UZS"},
            "patent": {"uz": "7 000 000 so'mdan (davlat boji bilan)", "ru": "от 7 000 000 сум (включая госпошлину)", "en": "from 7 000 000 UZS (including state fee)"},
        }
        nom = NOMLAR[key][t]
        narx = narxlar_fixed[key][t]
        context.user_data["xizmat"] = nom
        context.user_data["hajm_narx"] = f"{nom} | {narx}"
        context.user_data["narx"] = narx
        await q.message.reply_text(
            f"✅ *{nom}* tanlandi!\n💰 {narx}\n\n" + m(context, "tema"),
            parse_mode="Markdown"
        )
        return TEMA

    if key in NARXLAR:
        nom = NOMLAR.get(key, {}).get(t, key)
        context.user_data["xizmat"] = nom
        context.user_data["xizmat_key"] = key
        narxlar = NARXLAR[key]
        matn = m(context, "hajm")
        for h, n in narxlar.items():
            matn += f"• *{h}* — _{n}_\n"
        keyboard = btn([[h] for h in narxlar.keys()] + [[ortga]])
        await q.message.reply_text(matn, reply_markup=keyboard, parse_mode="Markdown")
        return HAJM_TANLASH

    return ENTRY_XIZMAT

async def hajm_tanlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    t = til(context)
    ortga = ortga_btn(t)

    if ortga in data:
        return await start(update, context)

    xizmat_key = context.user_data.get("xizmat_key", "")
    xizmat_nom = context.user_data.get("xizmat", "")

    if xizmat_key in NARXLAR and data in NARXLAR[xizmat_key]:
        narx = NARXLAR[xizmat_key][data]
        context.user_data["hajm_narx"] = f"{data} | {narx}"
        context.user_data["narx"] = narx
        await q.message.edit_text(
            f"✅ *{xizmat_nom}*\n📏 {data} — 💰 *{narx}*\n\n" + m(context, "tema"),
            parse_mode="Markdown"
        )
        return TEMA

    return HAJM_TANLASH

async def tema(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matn = update.message.text.strip()
    t = til(context)
    if len(matn) < 3:
        await update.message.reply_text(m(context, "tema_xato"), parse_mode="Markdown")
        return TEMA
    context.user_data["tema"] = matn
    muddat_btn = MUDDAT_TUGMALAR[t] + [[ortga_btn(t)]]
    keyboard = btn(muddat_btn)
    await update.message.reply_text(m(context, "muddat"), reply_markup=keyboard, parse_mode="Markdown")
    return MUDDAT

async def muddat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    t = til(context)
    ortga = ortga_btn(t)

    if ortga in q.data:
        return await start(update, context)

    muddat_uz = MUDDAT_MAP.get(q.data, q.data)
    foiz = MUDDAT_FOIZ.get(muddat_uz, "Standart")
    context.user_data["muddat"] = q.data
    context.user_data["muddat_foiz"] = foiz

    await q.message.edit_text(
        f"⏰ *Muddat:* {q.data} — 💡 *{foiz}*\n\n" + m(context, "talablar"),
        parse_mode="Markdown"
    )
    return TALABLAR

async def talablar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matn = update.message.text.strip()
    t = til(context)
    if len(matn) < 5:
        await update.message.reply_text(m(context, "talablar_xato"), parse_mode="Markdown")
        return TALABLAR
    context.user_data["talablar"] = matn
    await update.message.reply_text(m(context, "kontakt"), parse_mode="Markdown")
    return KONTAKT

async def kontakt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["kontakt"] = update.message.text
    t = til(context)
    keyboard = btn([["💳 UzCard", "💳 Visa"], ["💰 USDT (TRC20)"]])
    await update.message.reply_text(m(context, "tolov"), reply_markup=keyboard, parse_mode="Markdown")
    return TOLOV_TURI

async def tolov_turi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    narx = context.user_data.get("narx", "-")
    t = til(context)
    if "UzCard" in q.data:
        context.user_data["tolov"] = "UzCard"
        javob = m(context, "uzcard").format(narx=narx)
    elif "Visa" in q.data:
        context.user_data["tolov"] = "Visa"
        javob = m(context, "visa").format(narx=narx)
    elif "USDT" in q.data:
        context.user_data["tolov"] = "USDT"
        javob = m(context, "usdt").format(narx=narx)
    else:
        return TOLOV_TURI
    await q.message.edit_text(javob, parse_mode="Markdown")
    await q.message.reply_text(m(context, "chek_sorovi"), parse_mode="Markdown")
    return CHEK

async def chek(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = til(context)
    if not (update.message.photo or update.message.document):
        await update.message.reply_text(m(context, "chek_xato"), parse_mode="Markdown")
        return CHEK

    user = update.effective_user
    data = context.user_data

    admin_matn = (
        f"🔔 *YANGI BUYURTMA!*\n\n"
        f"👤 Mijoz: {user.full_name}\n"
        f"🆔 ID: `{user.id}`\n"
        f"📱 Username: @{user.username or 'yoq'}\n"
        f"🌐 Til: {t.upper()}\n\n"
        f"📚 Xizmat: *{data.get('xizmat', '-')}*\n"
        f"📏 Hajm/Narx: {data.get('hajm_narx', '-')}\n"
        f"✏️ Mavzu: _{data.get('tema', '-')}_\n"
        f"⏰ Muddat: {data.get('muddat', '-')} ({data.get('muddat_foiz', '-')})\n"
        f"📋 Talablar: {data.get('talablar', '-')}\n"
        f"📞 Kontakt: {data.get('kontakt', '-')}\n"
        f"💳 To'lov: {data.get('tolov', '-')}\n"
        f"🏛 Universitet: {data.get('universitet', '-')}\n"
        f"🔗 Referal: {data.get('referal', '-')}\n"
        f"✅ Chek: *Yuborildi!*"
    )

    await update.message.reply_text(m(context, "rahmat"), parse_mode="Markdown")

    # Make.com webhook — faqat ma'lumot yuboriladi, Telegram xabar yuborilmaydi
    try:
        import httpx
        async with httpx.AsyncClient() as client:
            await client.post(
                "https://hook.eu1.make.com/oaxswgwoj74hfk69l32yhhm8495jrxn4",
                json={
                    "full_name": user.full_name,
                    "telegram_id": str(user.id),
                    "username": f"@{user.username or 'yoq'}",
                    "til": t,
                    "xizmat": data.get("xizmat", "-"),
                    "hajm_narx": data.get("hajm_narx", "-"),
                    "tema": data.get("tema", "-"),
                    "muddat": data.get("muddat", "-"),
                    "muddat_foiz": data.get("muddat_foiz", "-"),
                    "talablar": data.get("talablar", "-"),
                    "kontakt": data.get("kontakt", "-"),
                    "tolov": data.get("tolov", "-"),
                    "referal": data.get("referal", "Bevosita"),
                    "universitet": data.get("universitet", "-"),
                },
                timeout=10
            )
    except:
        pass

    await context.bot.send_message(ADMIN_ID, admin_matn, parse_mode="Markdown")

    if update.message.photo:
        await context.bot.send_photo(ADMIN_ID, update.message.photo[-1].file_id, caption="📸 Chek rasmi")
    elif update.message.document:
        await context.bot.send_document(ADMIN_ID, update.message.document.file_id, caption="📄 Chek fayli")

    return ConversationHandler.END

async def bekor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = til(context)
    context.user_data.clear()
    await update.message.reply_text(m(context, "bekor"), parse_mode="Markdown")
    return ConversationHandler.END

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    keyboard = btn([["🇺🇿 O'zbek", "🇷🇺 Русский", "🇬🇧 English"]])
    await update.message.reply_text(
        "🔄 Bot qayta ishga tushdi!\n\n🌐 Tilni tanlang / Выберите язык / Choose language:",
        reply_markup=keyboard, parse_mode="Markdown"
    )
    return TIL_TANLASH

async def noaniq_buyruq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = btn([["🇺🇿 O'zbek", "🇷🇺 Русский", "🇬🇧 English"]])
    await update.message.reply_text(
        "❓ Noto'g'ri buyruq.\n\n/start — boshlash uchun",
        reply_markup=keyboard, parse_mode="Markdown"
    )
    return TIL_TANLASH

async def noaniq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(m(context, "tushunmadim"), parse_mode="Markdown")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            TIL_TANLASH: [CallbackQueryHandler(til_tanlash)],
            XIZMAT_TURI: [CallbackQueryHandler(xizmat_turi)],
            ENTRY_XIZMAT: [CallbackQueryHandler(xizmat_tanlash)],
            MIDDLE_XIZMAT: [CallbackQueryHandler(xizmat_tanlash)],
            PREMIUM_XIZMAT: [CallbackQueryHandler(xizmat_tanlash)],
            HAJM_TANLASH: [CallbackQueryHandler(hajm_tanlash)],
            TEMA: [MessageHandler(filters.TEXT & ~filters.COMMAND, tema)],
            MUDDAT: [CallbackQueryHandler(muddat)],
            TALABLAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, talablar)],
            KONTAKT: [MessageHandler(filters.TEXT & ~filters.COMMAND, kontakt)],
            TOLOV_TURI: [CallbackQueryHandler(tolov_turi)],
            CHEK: [MessageHandler(filters.PHOTO | filters.Document.ALL, chek)],
        },
        fallbacks=[
            CommandHandler("bekor", bekor),
            CommandHandler("start", start),
            CommandHandler("reset", reset),
            MessageHandler(filters.COMMAND, noaniq_buyruq),
        ],
    )
    app.add_handler(conv)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, noaniq))
    print("Bot ishga tushdi!")
    app.run_polling()

if __name__ == "__main__":
    main()
