import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    filters, ContextTypes, ConversationHandler
)

BOT_TOKEN = "8852741001:AAFZxKwuXDpgk9YAf6Fc5sMdIeH2v6uCKg8"
ADMIN_ID = 5846813939

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

(
    TIL_TANLASH, XIZMAT_TURI, ENTRY_XIZMAT, MIDDLE_XIZMAT,
    PREMIUM_XIZMAT, HAJM_TANLASH, TEMA, MUDDAT,
    TALABLAR, KONTAKT, TOLOV_TURI, CHEK,
) = range(12)

NARXLAR = {
    "referat": {"10-30 bet": "100 000 so'm", "30-50 bet": "150 000 so'm", "50-80 bet": "200 000 so'm", "80-120 bet": "250 000 so'm", "120+ bet": "300 000 so'm+"},
    "diplom": {"10-30 bet": "500 000 so'm", "30-50 bet": "750 000 so'm", "50-80 bet": "1 000 000 so'm", "80-120 bet": "1 250 000 so'm", "120+ bet": "1 500 000 so'm+"},
    "konferensiya": {"Mahalliy": "100 000 so'm", "Xalqaro": "300 000 so'm"},
    "gost": {"10-30 bet": "50 000 so'm", "30-50 bet": "75 000 so'm", "50-80 bet": "100 000 so'm", "80-120 bet": "125 000 so'm", "120+ bet": "150 000 so'm+"},
    "magistr": {"50-80 bet": "1 500 000 so'm", "80-120 bet": "3 000 000 so'm", "120+ bet": "6 000 000 so'm+"},
    "oak_mahalliy": {"5-10 bet": "1 100 000 so'm", "10-20 bet": "1 500 000 so'm", "20+ bet": "2 000 000 so'm"},
    "oak_xalqaro": {"5-10 bet": "2 600 000 so'm", "10-20 bet": "3 000 000 so'm", "20+ bet": "3 600 000 so'm"},
    "scopus_q3q4": {"Kichik": "$400", "O'rta": "$500", "Katta": "$600"},
    "adabiyotlar": {"20-40 manba": "500 000 so'm", "40-60 manba": "750 000 so'm", "60+ manba": "1 000 000 so'm"},
    "biostatistika": {"Oddiy": "600 000 so'm", "O'rta": "900 000 so'm", "Murakkab": "1 200 000 so'm"},
    "phd": {"100-150 bet": "$1 500", "150-200 bet": "$2 500", "200+ bet": "$3 500"},
    "scopus_q1q2": {"Kichik": "$800", "O'rta": "$1 100", "Katta": "$1 500"},
    "meta_analiz": {"Oddiy": "2 000 000 so'm", "O'rta": "3 000 000 so'm", "Murakkab": "4 000 000 so'm"},
    "data_analytics": {"Oddiy": "1 500 000 so'm", "O'rta": "2 500 000 so'm", "Murakkab": "3 500 000 so'm"},
}

# Kartochkalar — har bir xizmat alohida xabar
ENTRY_KARTOCHKALAR = {
    "uz": [
        {
            "matn": "📄 *Referat / Kurs ishi*\n\n📏 Hajm: 10 betdan 120+ betgacha\n💰 Narx: 100 000 — 300 000 so'm\n\n_Sifatli va o'z vaqtida tayyorlanadi_",
            "tugma": "✅ Referat / Kurs ishi tanlash",
            "key": "referat"
        },
        {
            "matn": "🎓 *Diplom ishi*\n\n📏 Hajm: 10 betdan 120+ betgacha\n💰 Narx: 500 000 — 1 500 000 so'm\n\n_Davlat standartlariga mos tayyorlanadi_",
            "tugma": "✅ Diplom ishi tanlash",
            "key": "diplom"
        },
        {
            "matn": "📊 *Konferensiya maqolasi*\n\n🏛 Mahalliy: 100 000 so'm\n🌍 Xalqaro: 300 000 so'm\n\n_GOST va xalqaro standartlarga mos_",
            "tugma": "✅ Konferensiya maqolasi tanlash",
            "key": "konferensiya"
        },
        {
            "matn": "📋 *GOST formatlash*\n\n📏 Hajm: 10 betdan 120+ betgacha\n💰 Narx: 50 000 — 150 000 so'm\n\n_Rasmiy talablarga to'liq mos_",
            "tugma": "✅ GOST formatlash tanlash",
            "key": "gost"
        },
    ],
    "ru": [
        {
            "matn": "📄 *Реферат / Курсовая*\n\n📏 Объём: от 10 до 120+ страниц\n💰 Цена: 100 000 — 300 000 сум\n\n_Качественно и в срок_",
            "tugma": "✅ Выбрать Реферат / Курсовую",
            "key": "referat"
        },
        {
            "matn": "🎓 *Дипломная работа*\n\n📏 Объём: от 10 до 120+ страниц\n💰 Цена: 500 000 — 1 500 000 сум\n\n_По государственным стандартам_",
            "tugma": "✅ Выбрать Дипломную работу",
            "key": "diplom"
        },
        {
            "matn": "📊 *Статья для конференции*\n\n🏛 Местная: 100 000 сум\n🌍 Международная: 300 000 сум\n\n_По ГОСТ и международным стандартам_",
            "tugma": "✅ Выбрать статью конференции",
            "key": "konferensiya"
        },
        {
            "matn": "📋 *Оформление по ГОСТ*\n\n📏 Объём: от 10 до 120+ страниц\n💰 Цена: 50 000 — 150 000 сум\n\n_Полное соответствие требованиям_",
            "tugma": "✅ Выбрать оформление ГОСТ",
            "key": "gost"
        },
    ],
    "en": [
        {
            "matn": "📄 *Essay / Course work*\n\n📏 Volume: 10 to 120+ pages\n💰 Price: 100 000 — 300 000 UZS\n\n_Quality and on time_",
            "tugma": "✅ Choose Essay / Course work",
            "key": "referat"
        },
        {
            "matn": "🎓 *Thesis*\n\n📏 Volume: 10 to 120+ pages\n💰 Price: 500 000 — 1 500 000 UZS\n\n_According to state standards_",
            "tugma": "✅ Choose Thesis",
            "key": "diplom"
        },
        {
            "matn": "📊 *Conference paper*\n\n🏛 Local: 100 000 UZS\n🌍 International: 300 000 UZS\n\n_GOST and international standards_",
            "tugma": "✅ Choose Conference paper",
            "key": "konferensiya"
        },
        {
            "matn": "📋 *GOST formatting*\n\n📏 Volume: 10 to 120+ pages\n💰 Price: 50 000 — 150 000 UZS\n\n_Full compliance with requirements_",
            "tugma": "✅ Choose GOST formatting",
            "key": "gost"
        },
    ],
}

MIDDLE_KARTOCHKALAR = {
    "uz": [
        {"matn": "📘 *Magistr dissertatsiyasi*\n\n📏 Hajm: 50 betdan 120+ betgacha\n💰 Narx: 1 500 000 — 6 000 000 so'm\n\n_Ilmiy standartlarga to'liq mos_", "tugma": "✅ Magistr dissertatsiyasi tanlash", "key": "magistr"},
        {"matn": "📑 *OAK maqolasi (mahalliy)*\n\n📏 Hajm: 5 betdan 20+ betgacha\n💰 Narx: 1 100 000 — 2 000 000 so'm\n\n_Mahalliy jurnallar uchun_", "tugma": "✅ OAK mahalliy tanlash", "key": "oak_mahalliy"},
        {"matn": "📑 *OAK maqolasi (xalqaro)*\n\n📏 Hajm: 5 betdan 20+ betgacha\n💰 Narx: 2 600 000 — 3 600 000 so'm\n\n_Xalqaro jurnallar uchun_", "tugma": "✅ OAK xalqaro tanlash", "key": "oak_xalqaro"},
        {"matn": "🔬 *Scopus Q3-Q4 maqolasi*\n\n💰 Narx: $400 — $600\n\n_Scopus indekslangan jurnallar uchun_", "tugma": "✅ Scopus Q3-Q4 tanlash", "key": "scopus_q3q4"},
        {"matn": "📚 *Adabiyotlar sharhi*\n\n📏 Hajm: 20 manbadan 60+ manbacha\n💰 Narx: 500 000 — 1 000 000 so'm\n\n_Ilmiy manbalar tahlili_", "tugma": "✅ Adabiyotlar sharhi tanlash", "key": "adabiyotlar"},
        {"matn": "📊 *Biostatistika*\n\n💰 Narx: 600 000 — 1 200 000 so'm\n\n_Tibbiy va biologik tadqiqotlar uchun_", "tugma": "✅ Biostatistika tanlash", "key": "biostatistika"},
    ],
    "ru": [
        {"matn": "📘 *Магистерская диссертация*\n\n📏 Объём: от 50 до 120+ страниц\n💰 Цена: 1 500 000 — 6 000 000 сум\n\n_По научным стандартам_", "tugma": "✅ Выбрать Магистерскую", "key": "magistr"},
        {"matn": "📑 *Статья ВАК (местный)*\n\n📏 Объём: от 5 до 20+ страниц\n💰 Цена: 1 100 000 — 2 000 000 сум\n\n_Для местных журналов_", "tugma": "✅ Выбрать ВАК местный", "key": "oak_mahalliy"},
        {"matn": "📑 *Статья ВАК (международный)*\n\n📏 Объём: от 5 до 20+ страниц\n💰 Цена: 2 600 000 — 3 600 000 сум\n\n_Для международных журналов_", "tugma": "✅ Выбрать ВАК международный", "key": "oak_xalqaro"},
        {"matn": "🔬 *Статья Scopus Q3-Q4*\n\n💰 Цена: $400 — $600\n\n_Для журналов Scopus_", "tugma": "✅ Выбрать Scopus Q3-Q4", "key": "scopus_q3q4"},
        {"matn": "📚 *Обзор литературы*\n\n📏 Объём: от 20 до 60+ источников\n💰 Цена: 500 000 — 1 000 000 сум\n\n_Анализ научных источников_", "tugma": "✅ Выбрать Обзор литературы", "key": "adabiyotlar"},
        {"matn": "📊 *Биостатистика*\n\n💰 Цена: 600 000 — 1 200 000 сум\n\n_Для медицинских исследований_", "tugma": "✅ Выбрать Биостатистику", "key": "biostatistika"},
    ],
    "en": [
        {"matn": "📘 *Master's dissertation*\n\n📏 Volume: 50 to 120+ pages\n💰 Price: 1 500 000 — 6 000 000 UZS\n\n_Academic standards_", "tugma": "✅ Choose Master's dissertation", "key": "magistr"},
        {"matn": "📑 *VAK article (local)*\n\n📏 Volume: 5 to 20+ pages\n💰 Price: 1 100 000 — 2 000 000 UZS\n\n_For local journals_", "tugma": "✅ Choose VAK local", "key": "oak_mahalliy"},
        {"matn": "📑 *VAK article (international)*\n\n📏 Volume: 5 to 20+ pages\n💰 Price: 2 600 000 — 3 600 000 UZS\n\n_For international journals_", "tugma": "✅ Choose VAK international", "key": "oak_xalqaro"},
        {"matn": "🔬 *Scopus Q3-Q4 article*\n\n💰 Price: $400 — $600\n\n_For Scopus indexed journals_", "tugma": "✅ Choose Scopus Q3-Q4", "key": "scopus_q3q4"},
        {"matn": "📚 *Literature review*\n\n📏 Volume: 20 to 60+ sources\n💰 Price: 500 000 — 1 000 000 UZS\n\n_Scientific sources analysis_", "tugma": "✅ Choose Literature review", "key": "adabiyotlar"},
        {"matn": "📊 *Biostatistics*\n\n💰 Price: 600 000 — 1 200 000 UZS\n\n_For medical research_", "tugma": "✅ Choose Biostatistics", "key": "biostatistika"},
    ],
}

PREMIUM_KARTOCHKALAR = {
    "uz": [
        {"matn": "🏆 *PhD dissertatsiyasi*\n\n📏 Hajm: 100 betdan 200+ betgacha\n💰 Narx: $1 500 — $3 500\n\n_Eng yuqori ilmiy daraja uchun_", "tugma": "✅ PhD dissertatsiyasi tanlash", "key": "phd"},
        {"matn": "⭐ *Scopus Q1-Q2 maqolasi*\n\n💰 Narx: $800 — $1 500\n\n_Eng nufuzli xalqaro jurnallar uchun_", "tugma": "✅ Scopus Q1-Q2 tanlash", "key": "scopus_q1q2"},
        {"matn": "🔍 *Meta-analiz*\n\n💰 Narx: 2 000 000 — 4 000 000 so'm\n\n_Ilmiy tadqiqotlar sintezi_", "tugma": "✅ Meta-analiz tanlash", "key": "meta_analiz"},
        {"matn": "📈 *Data analytics*\n\n💰 Narx: 1 500 000 — 3 500 000 so'm\n\n_Ma'lumotlar tahlili va vizualizatsiya_", "tugma": "✅ Data analytics tanlash", "key": "data_analytics"},
        {"matn": "📝 *Grant ariza*\n\n💰 Narx: Kelishiladi\n\n_Xalqaro grantlar uchun professional ariza_", "tugma": "✅ Grant ariza tanlash", "key": "grant"},
    ],
    "ru": [
        {"matn": "🏆 *Диссертация PhD*\n\n📏 Объём: от 100 до 200+ страниц\n💰 Цена: $1 500 — $3 500\n\n_Для высшей научной степени_", "tugma": "✅ Выбрать PhD диссертацию", "key": "phd"},
        {"matn": "⭐ *Статья Scopus Q1-Q2*\n\n💰 Цена: $800 — $1 500\n\n_Для престижных международных журналов_", "tugma": "✅ Выбрать Scopus Q1-Q2", "key": "scopus_q1q2"},
        {"matn": "🔍 *Мета-анализ*\n\n💰 Цена: 2 000 000 — 4 000 000 сум\n\n_Синтез научных исследований_", "tugma": "✅ Выбрать Мета-анализ", "key": "meta_analiz"},
        {"matn": "📈 *Аналитика данных*\n\n💰 Цена: 1 500 000 — 3 500 000 сум\n\n_Анализ и визуализация данных_", "tugma": "✅ Выбрать Data analytics", "key": "data_analytics"},
        {"matn": "📝 *Грантовая заявка*\n\n💰 Цена: По договорённости\n\n_Профессиональная заявка на гранты_", "tugma": "✅ Выбрать Грантовую заявку", "key": "grant"},
    ],
    "en": [
        {"matn": "🏆 *PhD dissertation*\n\n📏 Volume: 100 to 200+ pages\n💰 Price: $1 500 — $3 500\n\n_For the highest academic degree_", "tugma": "✅ Choose PhD dissertation", "key": "phd"},
        {"matn": "⭐ *Scopus Q1-Q2 article*\n\n💰 Price: $800 — $1 500\n\n_For prestigious international journals_", "tugma": "✅ Choose Scopus Q1-Q2", "key": "scopus_q1q2"},
        {"matn": "🔍 *Meta-analysis*\n\n💰 Price: 2 000 000 — 4 000 000 UZS\n\n_Synthesis of scientific research_", "tugma": "✅ Choose Meta-analysis", "key": "meta_analiz"},
        {"matn": "📈 *Data analytics*\n\n💰 Price: 1 500 000 — 3 500 000 UZS\n\n_Data analysis and visualization_", "tugma": "✅ Choose Data analytics", "key": "data_analytics"},
        {"matn": "📝 *Grant application*\n\n💰 Price: Negotiable\n\n_Professional grant application_", "tugma": "✅ Choose Grant application", "key": "grant"},
    ],
}

VIP_KARTOCHKALAR = {
    "uz": [
        {"matn": "📖 *Monografiya*\n\n💰 Narx: 3 000 000 — 7 000 000 so'm\n\n_To'liq ilmiy asar_", "tugma": "✅ Monografiya tanlash", "key": "monografiya"},
        {"matn": "💡 *Patent*\n\n💰 Narx: 1 000 000 — 2 500 000 so'm\n\n_Ixtiro va yangiliklar uchun_", "tugma": "✅ Patent tanlash", "key": "patent"},
    ],
    "ru": [
        {"matn": "📖 *Монография*\n\n💰 Цена: 3 000 000 — 7 000 000 сум\n\n_Полный научный труд_", "tugma": "✅ Выбрать Монографию", "key": "monografiya"},
        {"matn": "💡 *Патент*\n\n💰 Цена: 1 000 000 — 2 500 000 сум\n\n_Для изобретений и новшеств_", "tugma": "✅ Выбрать Патент", "key": "patent"},
    ],
    "en": [
        {"matn": "📖 *Monograph*\n\n💰 Price: 3 000 000 — 7 000 000 UZS\n\n_Complete scientific work_", "tugma": "✅ Choose Monograph", "key": "monografiya"},
        {"matn": "💡 *Patent*\n\n💰 Price: 1 000 000 — 2 500 000 UZS\n\n_For inventions and innovations_", "tugma": "✅ Choose Patent", "key": "patent"},
    ],
}

def til(ctx):
    return ctx.user_data.get("til", "uz")

def m(ctx, key):
    return {
        "uz": {
            "start": "👋 *Salom, {name}!*\n\n🎓 Biz — professional akademik yozuv xizmatlarini taqdim etamiz\n\n✅ Tez\n✅ Sifatli\n✅ Maxfiy\n\n🌐 *Tilni tanlang:*",
            "xizmat_turi": "📚 *Xizmat turini tanlang:*\n\n📗 *Entry* — Referat, Diplom, Konferensiya, GOST\n📘 *Middle* — Magistr, OAK, Scopus Q3-Q4\n📙 *Premium* — PhD, Scopus Q1-Q2, Meta-analiz\n💎 *VIP* — Monografiya, Patent",
            "entry_sarlavha": "📗 *Entry xizmatlari:*\n\nQuyidagilardan birini tanlang 👇",
            "middle_sarlavha": "📘 *Middle xizmatlari:*\n\nQuyidagilardan birini tanlang 👇",
            "premium_sarlavha": "📙 *Premium xizmatlari:*\n\nQuyidagilardan birini tanlang 👇",
            "vip_sarlavha": "💎 *VIP xizmatlari:*\n\nQuyidagilardan birini tanlang 👇",
            "hajm": "📏 *Hajm va narxni tanlang:*\n\n",
            "tema": "✏️ *Ishingizning mavzusini kiriting:*\n\n📌 _Masalan: «Raqamlashtirish iqtisodiyotga ta'siri»_",
            "tema_xato": "⚠️ *Iltimos, mavzuni to'liq kiriting!*",
            "muddat": "⏰ *Ishni qachon tayyorlashimiz kerak?*",
            "muddat_btn": [["⚡ 3 kun", "📅 1 hafta"], ["📆 2 hafta", "🗓 1 oy"], ["📋 1-2 oydan ko'p"]],
            "talablar": "📋 *Qo'shimcha ma'lumotlarni kiriting:*\n\n🏛 Universitetingiz nomi\n📚 Kurs / yil\n📝 Rasmiylashtirish talablari _(GOST, APA...)_\n🌐 Ish tili _(O'zbek, Rus, Ingliz)_\n📍 Viloyatingiz",
            "talablar_xato": "⚠️ *Iltimos, ma'lumotlarni to'liq kiriting!*",
            "kontakt": "📞 *Telefon raqam yoki Telegram username kiriting:*",
            "tolov": "💳 *To'lov usulini tanlang:*",
            "uzcard": "💳 *UzCard orqali to'lov:*\n\n🔢 Karta: `6262 5700 7026 5220`\n👤 Egasi: *QARAYEV ULUGBEK*\n\n💰 Miqdor: *{narx}*\n\n📸 *To'lovdan so'ng chek rasmini yuboring!*",
            "visa": "💳 *Visa orqali to'lov:*\n\n🔢 Karta: `4278 3100 2613 3181`\n👤 Egasi: *QARAYEV ULUGBEK*\n\n💰 Miqdor: *{narx}*\n\n📸 *To'lovdan so'ng chek rasmini yuboring!*",
            "usdt": "💰 *USDT (TRC20) orqali to'lov:*\n\n🔢 Manzil:\n`TUv1qZ1Cxmh5aao877J4xB43MTXz5w6Y`\n\n💵 Miqdor: *{narx}*\n\n📸 *To'lovdan so'ng chek rasmini yuboring!*",
            "chek_sorovi": "🧾 *Chek rasmini yuboring:*\n\n📸 Rasm _(foto chek)_\n📱 Skrinshot\n📄 Fayl",
            "chek_xato": "⚠️ *Iltimos, chekni rasm yoki fayl sifatida yuboring!*",
            "rahmat": "✅ *Buyurtmangiz qabul qilindi!*\n\n⏳ Tez orada mutaxassisimiz siz bilan bog'lanadi\n\n📞 Admin: @Karaevmladshii\n☎️ Tel: +998946267555\n\n🙏 *Bizga ishonganingiz uchun rahmat!*",
            "ortga": "🔙 Ortga",
            "tushunmadim": "❓ *Tushunmadim*\n\n/start — qaytadan boshlash",
            "bekor": "❌ *Bekor qilindi*\n\n/start — qaytadan boshlash",
        },
        "ru": {
            "start": "👋 *Привет, {name}!*\n\n🎓 Мы — профессиональные академические услуги\n\n✅ Быстро\n✅ Качественно\n✅ Конфиденциально\n\n🌐 *Выберите язык:*",
            "xizmat_turi": "📚 *Выберите тип услуги:*\n\n📗 *Entry* — Реферат, Диплом, Конференция, ГОСТ\n📘 *Middle* — Магистр, ВАК, Scopus Q3-Q4\n📙 *Premium* — PhD, Scopus Q1-Q2, Мета-анализ\n💎 *VIP* — Монография, Патент",
            "entry_sarlavha": "📗 *Услуги Entry:*\n\nВыберите одну из них 👇",
            "middle_sarlavha": "📘 *Услуги Middle:*\n\nВыберите одну из них 👇",
            "premium_sarlavha": "📙 *Услуги Premium:*\n\nВыберите одну из них 👇",
            "vip_sarlavha": "💎 *Услуги VIP:*\n\nВыберите одну из них 👇",
            "hajm": "📏 *Выберите объём и цену:*\n\n",
            "tema": "✏️ *Введите тему работы:*\n\n📌 _Например: «Влияние цифровизации на экономику»_",
            "tema_xato": "⚠️ *Пожалуйста, введите тему полностью!*",
            "muddat": "⏰ *Когда нужна работа?*",
            "muddat_btn": [["⚡ 3 дня", "📅 1 неделя"], ["📆 2 недели", "🗓 1 месяц"], ["📋 Более 1-2 месяцев"]],
            "talablar": "📋 *Введите дополнительную информацию:*\n\n🏛 Название университета\n📚 Курс / год\n📝 Требования к оформлению _(ГОСТ, APA...)_\n🌐 Язык работы\n📍 Ваш регион",
            "talablar_xato": "⚠️ *Пожалуйста, введите информацию полностью!*",
            "kontakt": "📞 *Введите номер телефона или Telegram username:*",
            "tolov": "💳 *Выберите способ оплаты:*",
            "uzcard": "💳 *Оплата через UzCard:*\n\n🔢 Карта: `6262 5700 7026 5220`\n👤 Владелец: *QARAYEV ULUGBEK*\n\n💰 Сумма: *{narx}*\n\n📸 *После оплаты отправьте чек!*",
            "visa": "💳 *Оплата через Visa:*\n\n🔢 Карта: `4278 3100 2613 3181`\n👤 Владелец: *QARAYEV ULUGBEK*\n\n💰 Сумма: *{narx}*\n\n📸 *После оплаты отправьте чек!*",
            "usdt": "💰 *Оплата через USDT (TRC20):*\n\n🔢 Адрес:\n`TUv1qZ1Cxmh5aao877J4xB43MTXz5w6Y`\n\n💵 Сумма: *{narx}*\n\n📸 *После оплаты отправьте чек!*",
            "chek_sorovi": "🧾 *Отправьте чек об оплате:*\n\n📸 Фото\n📄 Файл",
            "chek_xato": "⚠️ *Пожалуйста, отправьте чек в виде фото или файла!*",
            "rahmat": "✅ *Ваш заказ принят!*\n\n⏳ Наш специалист свяжется с вами\n\n📞 Админ: @Karaevmladshii\n☎️ Тел: +998946267555\n\n🙏 *Спасибо, что доверились нам!*",
            "ortga": "🔙 Назад",
            "tushunmadim": "❓ *Не понял*\n\n/start — начать заново",
            "bekor": "❌ *Отменено*\n\n/start — начать заново",
        },
        "en": {
            "start": "👋 *Hello, {name}!*\n\n🎓 We provide professional academic writing services\n\n✅ Fast\n✅ Quality\n✅ Confidential\n\n🌐 *Choose language:*",
            "xizmat_turi": "📚 *Choose service type:*\n\n📗 *Entry* — Essay, Thesis, Conference, GOST\n📘 *Middle* — Master's, VAK, Scopus Q3-Q4\n📙 *Premium* — PhD, Scopus Q1-Q2, Meta-analysis\n💎 *VIP* — Monograph, Patent",
            "entry_sarlavha": "📗 *Entry services:*\n\nChoose one 👇",
            "middle_sarlavha": "📘 *Middle services:*\n\nChoose one 👇",
            "premium_sarlavha": "📙 *Premium services:*\n\nChoose one 👇",
            "vip_sarlavha": "💎 *VIP services:*\n\nChoose one 👇",
            "hajm": "📏 *Choose volume and price:*\n\n",
            "tema": "✏️ *Enter your topic:*\n\n📌 _Example: «Impact of digitalization on economy»_",
            "tema_xato": "⚠️ *Please enter the full topic!*",
            "muddat": "⏰ *When do you need the work?*",
            "muddat_btn": [["⚡ 3 days", "📅 1 week"], ["📆 2 weeks", "🗓 1 month"], ["📋 More than 1-2 months"]],
            "talablar": "📋 *Enter additional information:*\n\n🏛 University name\n📚 Course / year\n📝 Formatting requirements _(GOST, APA...)_\n🌐 Language\n📍 Your region",
            "talablar_xato": "⚠️ *Please enter the information completely!*",
            "kontakt": "📞 *Enter your phone or Telegram username:*",
            "tolov": "💳 *Choose payment method:*",
            "uzcard": "💳 *Payment via UzCard:*\n\n🔢 Card: `6262 5700 7026 5220`\n👤 Owner: *QARAYEV ULUGBEK*\n\n💰 Amount: *{narx}*\n\n📸 *After payment, send receipt!*",
            "visa": "💳 *Payment via Visa:*\n\n🔢 Card: `4278 3100 2613 3181`\n👤 Owner: *QARAYEV ULUGBEK*\n\n💰 Amount: *{narx}*\n\n📸 *After payment, send receipt!*",
            "usdt": "💰 *Payment via USDT (TRC20):*\n\n🔢 Address:\n`TUv1qZ1Cxmh5aao877J4xB43MTXz5w6Y`\n\n💵 Amount: *{narx}*\n\n📸 *After payment, send receipt!*",
            "chek_sorovi": "🧾 *Send your payment receipt:*\n\n📸 Photo\n📄 File",
            "chek_xato": "⚠️ *Please send receipt as photo or file!*",
            "rahmat": "✅ *Your order received!*\n\n⏳ Our specialist will contact you\n\n📞 Admin: @Karaevmladshii\n☎️ Tel: +998946267555\n\n🙏 *Thank you for choosing us!*",
            "ortga": "🔙 Back",
            "tushunmadim": "❓ *I didn't understand*\n\n/start — start again",
            "bekor": "❌ *Cancelled*\n\n/start — start again",
        },
    }[ctx.user_data.get("til", "uz")][key]

def btn(rows):
    return InlineKeyboardMarkup([[InlineKeyboardButton(t, callback_data=t) for t in row] for row in rows])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    user = update.effective_user
    keyboard = btn([["🇺🇿 O'zbek", "🇷🇺 Русский", "🇬🇧 English"]])
    matn = "👋 *Salom, {name}!*\n\n🎓 Biz — professional akademik yozuv xizmatlarini taqdim etamiz\n\n✅ Tez\n✅ Sifatli\n✅ Maxfiy\n\n🌐 *Tilni tanlang:*".format(name=user.first_name)
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
        return TIL_TANLASH
    keyboard = btn([["📗 Entry", "📘 Middle"], ["📙 Premium", "💎 VIP"]])
    await q.message.edit_text(m(context, "xizmat_turi"), reply_markup=keyboard, parse_mode="Markdown")
    return XIZMAT_TURI

async def xizmat_turi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    t = til(context)

    if "Entry" in q.data:
        context.user_data["xizmat_turi"] = "Entry"
        kartochkalar = ENTRY_KARTOCHKALAR[t]
        sarlavha = m(context, "entry_sarlavha")
    elif "Middle" in q.data:
        context.user_data["xizmat_turi"] = "Middle"
        kartochkalar = MIDDLE_KARTOCHKALAR[t]
        sarlavha = m(context, "middle_sarlavha")
    elif "Premium" in q.data:
        context.user_data["xizmat_turi"] = "Premium"
        kartochkalar = PREMIUM_KARTOCHKALAR[t]
        sarlavha = m(context, "premium_sarlavha")
    elif "VIP" in q.data:
        context.user_data["xizmat_turi"] = "VIP"
        kartochkalar = VIP_KARTOCHKALAR[t]
        sarlavha = m(context, "vip_sarlavha")
    else:
        return XIZMAT_TURI

    ortga = m(context, "ortga")
    await q.message.edit_text(sarlavha, parse_mode="Markdown")
    for k in kartochkalar:
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(k["tugma"], callback_data=f"xizmat_{k['key']}")]])
        await q.message.reply_text(k["matn"], reply_markup=keyboard, parse_mode="Markdown")
    await q.message.reply_text("─────────────────", reply_markup=btn([[ortga]]))

    if context.user_data["xizmat_turi"] == "Entry":
        return ENTRY_XIZMAT
    elif context.user_data["xizmat_turi"] == "Middle":
        return MIDDLE_XIZMAT
    else:
        return PREMIUM_XIZMAT

async def xizmat_tanlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    if data == m(context, "ortga"):
        return await start(update, context)

    if data.startswith("xizmat_"):
        key = data.replace("xizmat_", "")

        if key in ["grant", "monografiya", "patent"]:
            nomlar = {
                "grant": {"uz": "Grant ariza", "ru": "Грантовая заявка", "en": "Grant application"},
                "monografiya": {"uz": "Monografiya", "ru": "Монография", "en": "Monograph"},
                "patent": {"uz": "Patent", "ru": "Патент", "en": "Patent"},
            }
            narxlar = {
                "grant": "Kelishiladi",
                "monografiya": "3 000 000 — 7 000 000 so'm",
                "patent": "1 000 000 — 2 500 000 so'm",
            }
            t = til(context)
            nom = nomlar[key][t]
            context.user_data["xizmat"] = nom
            context.user_data["hajm_narx"] = f"{nom} | {narxlar[key]}"
            context.user_data["narx"] = narxlar[key]
            await q.message.reply_text(
                f"✅ *{nom}* tanlandi!\n\n" + m(context, "tema"),
                parse_mode="Markdown"
            )
            return TEMA

        if key in NARXLAR:
            nomlar = {
                "referat": {"uz": "Referat / Kurs ishi", "ru": "Реферат / Курсовая", "en": "Essay / Course work"},
                "diplom": {"uz": "Diplom ishi", "ru": "Дипломная работа", "en": "Thesis"},
                "konferensiya": {"uz": "Konferensiya maqolasi", "ru": "Статья конференции", "en": "Conference paper"},
                "gost": {"uz": "GOST formatlash", "ru": "Оформление ГОСТ", "en": "GOST formatting"},
                "magistr": {"uz": "Magistr dissertatsiyasi", "ru": "Магистерская диссертация", "en": "Master's dissertation"},
                "oak_mahalliy": {"uz": "OAK (mahalliy)", "ru": "ВАК (местный)", "en": "VAK (local)"},
                "oak_xalqaro": {"uz": "OAK (xalqaro)", "ru": "ВАК (международный)", "en": "VAK (international)"},
                "scopus_q3q4": {"uz": "Scopus Q3-Q4", "ru": "Scopus Q3-Q4", "en": "Scopus Q3-Q4"},
                "adabiyotlar": {"uz": "Adabiyotlar sharhi", "ru": "Обзор литературы", "en": "Literature review"},
                "biostatistika": {"uz": "Biostatistika", "ru": "Биостатистика", "en": "Biostatistics"},
                "phd": {"uz": "PhD dissertatsiyasi", "ru": "Диссертация PhD", "en": "PhD dissertation"},
                "scopus_q1q2": {"uz": "Scopus Q1-Q2", "ru": "Scopus Q1-Q2", "en": "Scopus Q1-Q2"},
                "meta_analiz": {"uz": "Meta-analiz", "ru": "Мета-анализ", "en": "Meta-analysis"},
                "data_analytics": {"uz": "Data analytics", "ru": "Аналитика данных", "en": "Data analytics"},
            }
            t = til(context)
            nom = nomlar[key][t]
            context.user_data["xizmat"] = nom
            context.user_data["xizmat_key"] = key
            narxlar = NARXLAR[key]
            matn = m(context, "hajm")
            for h, n in narxlar.items():
                matn += f"• *{h}* — _{n}_\n"
            ortga = m(context, "ortga")
            keyboard = btn([[h] for h in narxlar.keys()] + [[ortga]])
            await q.message.reply_text(matn, reply_markup=keyboard, parse_mode="Markdown")
            return HAJM_TANLASH

    tur = context.user_data.get("xizmat_turi", "Entry")
    if tur == "Entry":
        return ENTRY_XIZMAT
    elif tur == "Middle":
        return MIDDLE_XIZMAT
    return PREMIUM_XIZMAT

async def hajm_tanlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    ortga = m(context, "ortga")

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
    if len(matn) < 3:
        await update.message.reply_text(m(context, "tema_xato"), parse_mode="Markdown")
        return TEMA
    context.user_data["tema"] = matn
    keyboard = btn(m(context, "muddat_btn"))
    await update.message.reply_text(m(context, "muddat"), reply_markup=keyboard, parse_mode="Markdown")
    return MUDDAT

async def muddat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    context.user_data["muddat"] = q.data
    await q.message.edit_text(m(context, "talablar"), parse_mode="Markdown")
    return TALABLAR

async def talablar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matn = update.message.text.strip()
    if len(matn) < 5:
        await update.message.reply_text(m(context, "talablar_xato"), parse_mode="Markdown")
        return TALABLAR
    context.user_data["talablar"] = matn
    await update.message.reply_text(m(context, "kontakt"), parse_mode="Markdown")
    return KONTAKT

async def kontakt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["kontakt"] = update.message.text
    keyboard = btn([["💳 UzCard", "💳 Visa"], ["💰 USDT (TRC20)"]])
    await update.message.reply_text(m(context, "tolov"), reply_markup=keyboard, parse_mode="Markdown")
    return TOLOV_TURI

async def tolov_turi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    narx = context.user_data.get("narx", "-")
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
    if not (update.message.photo or update.message.document):
        await update.message.reply_text(m(context, "chek_xato"), parse_mode="Markdown")
        return CHEK
    user = update.effective_user
    data = context.user_data
    t = til(context)
    admin_matn = (
        f"🔔 *YANGI BUYURTMA!*\n\n"
        f"👤 Mijoz: {user.full_name}\n"
        f"🆔 ID: `{user.id}`\n"
        f"📱 Username: @{user.username or 'yoq'}\n"
        f"🌐 Til: {t.upper()}\n\n"
        f"📚 Xizmat: *{data.get('xizmat', '-')}*\n"
        f"📏 Hajm/Narx: {data.get('hajm_narx', '-')}\n"
        f"✏️ Mavzu: _{data.get('tema', '-')}_\n"
        f"⏰ Muddat: {data.get('muddat', '-')}\n"
        f"📋 Talablar: {data.get('talablar', '-')}\n"
        f"📞 Kontakt: {data.get('kontakt', '-')}\n"
        f"💳 To'lov: {data.get('tolov', '-')}\n"
        f"✅ Chek: *Yuborildi!*"
    )
    await update.message.reply_text(m(context, "rahmat"), parse_mode="Markdown")
    await context.bot.send_message(ADMIN_ID, admin_matn, parse_mode="Markdown")
    if update.message.photo:
        await context.bot.send_photo(ADMIN_ID, update.message.photo[-1].file_id, caption="📸 Chek rasmi")
    elif update.message.document:
        await context.bot.send_document(ADMIN_ID, update.message.document.file_id, caption="📄 Chek fayli")
    return ConversationHandler.END

async def bekor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = til(context)
    context.user_data.clear()
    await update.message.reply_text(
        {"uz": "❌ *Bekor qilindi*\n\n/start — qaytadan boshlash",
         "ru": "❌ *Отменено*\n\n/start — начать заново",
         "en": "❌ *Cancelled*\n\n/start — start again"}[t],
        parse_mode="Markdown"
    )
    return ConversationHandler.END

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
        fallbacks=[CommandHandler("bekor", bekor)],
    )
    app.add_handler(conv)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, noaniq))
    print("Bot ishga tushdi!")
    app.run_polling()

if __name__ == "__main__":
    main()