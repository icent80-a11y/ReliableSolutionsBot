# -*- coding: utf-8 -*-

import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ContextTypes, ConversationHandler
from bot.keyboards import get_main_menu_keyboard, get_marketplace_keyboard, get_services_keyboard, get_calculation_result_keyboard, get_ai_chat_keyboard
from bot.messages import MESSAGES
from bot.calculator import FulfillmentCalculator
from bot.ai_assistant import AIAssistant
from bot.states import (
    MARKETPLACE_CHOICE, ORDERS_COUNT, SERVICES_CHOICE, CALCULATION_RESULT,
    APPLICATION_NAME, APPLICATION_CONTACT, APPLICATION_DESCRIPTION, AI_CHAT
)
from utils.formatters import format_calculation_result

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    user = update.effective_user
    welcome_text = MESSAGES['welcome'].format(name=user.first_name)
    
    keyboard = get_main_menu_keyboard()
    logo_path = "assets/logo.png"
    
    if update.callback_query:
        # Если это callback от кнопки, редактируем существующее сообщение
        await update.callback_query.edit_message_text(
            text=welcome_text,
            reply_markup=keyboard,
            parse_mode='HTML'
        )
    else:
        # Если это команда /start, отправляем логотип с приветствием
        if os.path.exists(logo_path):
            with open(logo_path, 'rb') as logo_file:
                await update.message.reply_photo(
                    photo=logo_file,
                    caption=welcome_text,
                    reply_markup=keyboard,
                    parse_mode='HTML'
                )
        else:
            await update.message.reply_text(
                text=welcome_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    await update.message.reply_text(
        text=MESSAGES['help'],
        parse_mode='HTML'
    )

async def company_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Информация о компании"""
    query = update.callback_query
    await query.answer()
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Назад в меню", callback_data="main_menu")]
    ])
    
    await query.edit_message_text(
        text=MESSAGES['company_info'],
        reply_markup=keyboard,
        parse_mode='HTML'
    )

async def services_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Информация об услугах"""
    query = update.callback_query
    await query.answer()
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Назад в меню", callback_data="main_menu")]
    ])
    
    await query.edit_message_text(
        text=MESSAGES['services_info'],
        reply_markup=keyboard,
        parse_mode='HTML'
    )

async def advantages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Преимущества работы с нами"""
    query = update.callback_query
    await query.answer()
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Назад в меню", callback_data="main_menu")]
    ])
    
    await query.edit_message_text(
        text=MESSAGES['advantages'],
        reply_markup=keyboard,
        parse_mode='HTML'
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик callback кнопок"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "main_menu":
        await start(update, context)
    elif query.data == "company_info":
        await company_info(update, context)
    elif query.data == "services":
        await services_info(update, context)
    elif query.data == "advantages":
        await advantages(update, context)
    elif query.data == "ai_chat":
        await handle_ai_chat_start(update, context)
    elif query.data == "ai_examples":
        await handle_ai_examples(update, context)
    elif query.data == "ai_ask_question":
        await handle_ai_ask_question(update, context)

# Обработчики калькулятора
async def handle_calculator_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начало работы с калькулятором"""
    query = update.callback_query
    await query.answer()
    
    keyboard = get_marketplace_keyboard()
    
    await query.edit_message_text(
        text=MESSAGES['calculator_start'],
        reply_markup=keyboard,
        parse_mode='HTML'
    )
    
    return MARKETPLACE_CHOICE

async def handle_marketplace_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка выбора маркетплейса"""
    query = update.callback_query
    await query.answer()
    
    marketplace = query.data.replace("marketplace_", "")
    context.user_data['marketplace'] = marketplace
    
    marketplace_names = {
        'wildberries': 'Wildberries',
        'ozon': 'Ozon',
        'yandex': 'Яндекс Маркет'
    }
    
    text = MESSAGES['orders_count'].format(marketplace=marketplace_names.get(marketplace, marketplace))
    
    await query.edit_message_text(
        text=text,
        parse_mode='HTML'
    )
    
    return ORDERS_COUNT

async def handle_orders_count(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка количества заказов"""
    try:
        orders_count = int(update.message.text)
        if orders_count <= 0:
            raise ValueError()
        
        context.user_data['orders_count'] = orders_count
        
        keyboard = get_services_keyboard()
        
        await update.message.reply_text(
            text=MESSAGES['services_choice'],
            reply_markup=keyboard,
            parse_mode='HTML'
        )
        
        return SERVICES_CHOICE
        
    except ValueError:
        await update.message.reply_text(
            text="❌ Пожалуйста, введите корректное количество заказов (положительное число)."
        )
        return ORDERS_COUNT

async def handle_services_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка выбора услуг"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "service_calculate":
        # Выполняем расчет
        calculator = FulfillmentCalculator()
        
        marketplace = context.user_data.get('marketplace')
        orders_count = context.user_data.get('orders_count')
        selected_services = context.user_data.get('selected_services', [])
        
        result = calculator.calculate(marketplace, orders_count, selected_services)
        context.user_data['calculation_result'] = result
        
        formatted_result = format_calculation_result(result, marketplace, orders_count, selected_services)
        keyboard = get_calculation_result_keyboard()
        
        await query.edit_message_text(
            text=formatted_result,
            reply_markup=keyboard,
            parse_mode='HTML'
        )
        
        return CALCULATION_RESULT
    
    else:
        # Добавляем/убираем услугу из выбранных
        service = query.data.replace("service_", "")
        selected_services = context.user_data.get('selected_services', [])
        
        if service in selected_services:
            selected_services.remove(service)
        else:
            selected_services.append(service)
        
        context.user_data['selected_services'] = selected_services
        
        keyboard = get_services_keyboard(selected_services)
        
        await query.edit_message_text(
            text=MESSAGES['services_choice'],
            reply_markup=keyboard,
            parse_mode='HTML'
        )
        
        return SERVICES_CHOICE

async def handle_calculation_result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка результата расчета"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "calc_new":
        # Новый расчет
        context.user_data.clear()
        keyboard = get_marketplace_keyboard()
        
        await query.edit_message_text(
            text=MESSAGES['calculator_start'],
            reply_markup=keyboard,
            parse_mode='HTML'
        )
        
        return MARKETPLACE_CHOICE
    
    elif query.data == "calc_application":
        # Переход к подаче заявки
        await query.edit_message_text(
            text=MESSAGES['application_start'],
            parse_mode='HTML'
        )
        
        return APPLICATION_NAME
    
    else:
        # Возврат в главное меню
        await start(update, context)
        return ConversationHandler.END

# Обработчики подачи заявки
async def handle_application_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начало подачи заявки"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        text=MESSAGES['application_start'],
        parse_mode='HTML'
    )
    
    return APPLICATION_NAME

async def handle_application_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка имени заявителя"""
    context.user_data['application_name'] = update.message.text
    
    await update.message.reply_text(
        text=MESSAGES['application_contact'],
        parse_mode='HTML'
    )
    
    return APPLICATION_CONTACT

async def handle_application_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка контактных данных"""
    context.user_data['application_contact'] = update.message.text
    
    await update.message.reply_text(
        text=MESSAGES['application_description'],
        parse_mode='HTML'
    )
    
    return APPLICATION_DESCRIPTION

async def handle_application_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка описания потребностей"""
    context.user_data['application_description'] = update.message.text
    
    await handle_application_complete(update, context)
    return ConversationHandler.END

async def handle_application_complete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Завершение подачи заявки"""
    # Здесь можно добавить отправку заявки администратору или сохранение в базу данных
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")]
    ])
    
    await update.message.reply_text(
        text=MESSAGES['application_complete'],
        reply_markup=keyboard,
        parse_mode='HTML'
    )

# Обработчики AI-помощника
async def handle_ai_chat_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начало работы с AI-помощником"""
    query = update.callback_query
    await query.answer()
    
    keyboard = get_ai_chat_keyboard()
    
    await query.edit_message_text(
        text=MESSAGES['ai_chat_welcome'],
        reply_markup=keyboard,
        parse_mode='HTML'
    )
    
    return AI_CHAT

async def handle_ai_examples(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Показ примеров вопросов для AI"""
    query = update.callback_query
    await query.answer()
    
    keyboard = get_ai_chat_keyboard()
    
    await query.edit_message_text(
        text=MESSAGES['ai_examples'],
        reply_markup=keyboard,
        parse_mode='HTML'
    )
    
    return AI_CHAT

async def handle_ai_ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Переход к вопросу AI"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        text="🤖 <b>Задайте свой вопрос</b>\n\nНапишите любой вопрос о наших услугах фулфилмента, и я постараюсь дать подробный ответ.",
        parse_mode='HTML'
    )
    
    return AI_CHAT

async def handle_ai_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка вопроса пользователя к AI"""
    user_message = update.message.text
    
    # Показываем, что бот печатает
    await update.message.chat.send_action(action="typing")
    
    try:
        # Инициализируем AI-помощника
        ai_assistant = AIAssistant()
        
        # Получаем контекст пользователя (последний расчет)
        user_context = {}
        if 'calculation_result' in context.user_data:
            user_context['last_calculation'] = context.user_data['calculation_result']
        
        # Получаем ответ от AI
        ai_response = await ai_assistant.get_response(user_message, user_context)
        
        # Создаем клавиатуру для продолжения
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🧮 Калькулятор", callback_data="calculator"),
                InlineKeyboardButton("📝 Подать заявку", callback_data="application")
            ],
            [
                InlineKeyboardButton("❓ Еще вопрос", callback_data="ai_ask_question"),
                InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")
            ]
        ])
        
        await update.message.reply_text(
            text=f"🤖 <b>AI-консультант отвечает:</b>\n\n{ai_response}",
            reply_markup=keyboard,
            parse_mode='HTML'
        )
        
        return AI_CHAT
        
    except Exception as e:
        logger.error(f"Ошибка AI-помощника: {e}")
        
        keyboard = get_ai_chat_keyboard()
        
        await update.message.reply_text(
            text="❌ Извините, временные технические проблемы с AI-помощником.\n\n"
                 "Попробуйте задать вопрос позже или воспользуйтесь калькулятором и подачей заявки.",
            reply_markup=keyboard,
            parse_mode='HTML'
        )
        
        return AI_CHAT
