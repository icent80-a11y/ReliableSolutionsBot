# -*- coding: utf-8 -*-

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Главное меню бота"""
    keyboard = [
        [
            InlineKeyboardButton("🧮 Калькулятор стоимости", callback_data="calculator"),
            InlineKeyboardButton("📝 Подать заявку", callback_data="application")
        ],
        [
            InlineKeyboardButton("🏢 О компании", callback_data="company_info"),
            InlineKeyboardButton("🛠 Наши услуги", callback_data="services")
        ],
        [
            InlineKeyboardButton("⭐ Преимущества", callback_data="advantages"),
            InlineKeyboardButton("🤖 AI-консультант", callback_data="ai_chat")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_marketplace_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора маркетплейса"""
    keyboard = [
        [
            InlineKeyboardButton("🛍 Wildberries", callback_data="marketplace_wildberries"),
            InlineKeyboardButton("📦 Ozon", callback_data="marketplace_ozon")
        ],
        [
            InlineKeyboardButton("🟡 Яндекс Маркет", callback_data="marketplace_yandex")
        ],
        [
            InlineKeyboardButton("🔙 Назад в меню", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_services_keyboard(selected_services: list = None) -> InlineKeyboardMarkup:
    """Клавиатура выбора услуг"""
    if selected_services is None:
        selected_services = []
    
    services = [
        ('storage', '📦 Хранение товаров'),
        ('packaging', '📮 Упаковка'),
        ('shipping', '🚚 Отправка'),
        ('returns', '↩️ Обработка возвратов'),
        ('labeling', '🏷 Маркировка'),
        ('quality_control', '✅ Контроль качества'),
        ('photo', '📸 Фотосъемка товаров'),
        ('analytics', '📊 Аналитика и отчеты')
    ]
    
    keyboard = []
    
    # Добавляем услуги по 2 в ряд
    for i in range(0, len(services), 2):
        row = []
        for j in range(2):
            if i + j < len(services):
                service_code, service_name = services[i + j]
                
                # Добавляем галочку если услуга выбрана
                if service_code in selected_services:
                    service_name = f"✅ {service_name}"
                
                row.append(InlineKeyboardButton(service_name, callback_data=f"service_{service_code}"))
        
        keyboard.append(row)
    
    # Кнопка расчета (активна только если выбрана хотя бы одна услуга)
    if selected_services:
        keyboard.append([InlineKeyboardButton("💰 Рассчитать стоимость", callback_data="service_calculate")])
    
    keyboard.append([InlineKeyboardButton("🔙 Назад в меню", callback_data="main_menu")])
    
    return InlineKeyboardMarkup(keyboard)

def get_calculation_result_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для результата расчета"""
    keyboard = [
        [
            InlineKeyboardButton("🔄 Новый расчет", callback_data="calc_new"),
            InlineKeyboardButton("📝 Подать заявку", callback_data="calc_application")
        ],
        [
            InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_ai_chat_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для AI-чата"""
    keyboard = [
        [
            InlineKeyboardButton("❓ Задать вопрос", callback_data="ai_ask_question"),
            InlineKeyboardButton("💡 Примеры вопросов", callback_data="ai_examples")
        ],
        [
            InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
