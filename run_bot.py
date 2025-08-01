#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
import sys

# Устанавливаем токен напрямую для тестирования
os.environ["TELEGRAM_BOT_TOKEN"] = "7635966483:AAEPV4tBUNZhqyH3iWq_Pg6JyO3-udTITdc"

from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler
from bot.handlers import (
    start, help_command, company_info, services_info, advantages,
    button_callback, handle_calculator_start, handle_marketplace_choice,
    handle_orders_count, handle_services_choice, handle_calculation_result,
    handle_application_start, handle_application_name, handle_application_contact,
    handle_application_description, handle_application_complete
)
from bot.states import (
    MARKETPLACE_CHOICE, ORDERS_COUNT, SERVICES_CHOICE, CALCULATION_RESULT,
    APPLICATION_NAME, APPLICATION_CONTACT, APPLICATION_DESCRIPTION
)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Основная функция запуска бота"""
    # Получаем токен бота из переменных окружения
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    
    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN не найден в переменных окружения!")
        return
    
    logger.info(f"Запуск бота с токеном: {bot_token[:20]}...")
    
    # Создаем приложение
    application = Application.builder().token(bot_token).build()
    
    # Создаем ConversationHandler для калькулятора
    calculator_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(handle_calculator_start, pattern="^calculator$")],
        states={
            MARKETPLACE_CHOICE: [CallbackQueryHandler(handle_marketplace_choice, pattern="^marketplace_")],
            ORDERS_COUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_orders_count)],
            SERVICES_CHOICE: [CallbackQueryHandler(handle_services_choice, pattern="^service_")],
            CALCULATION_RESULT: [CallbackQueryHandler(handle_calculation_result, pattern="^calc_")]
        },
        fallbacks=[CommandHandler('start', start)]
    )
    
    # Создаем ConversationHandler для подачи заявки
    application_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(handle_application_start, pattern="^application$")],
        states={
            APPLICATION_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_application_name)],
            APPLICATION_CONTACT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_application_contact)],
            APPLICATION_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_application_description)]
        },
        fallbacks=[CommandHandler('start', start)]
    )
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(calculator_handler)
    application.add_handler(application_handler)
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Запускаем бота
    logger.info("🚀 Запуск Telegram-бота Надежные-решения.рф")
    logger.info("✅ Бот готов к работе! Найдите его в Telegram и отправьте /start")
    
    try:
        application.run_polling(allowed_updates=['message', 'callback_query'])
    except Exception as e:
        logger.error(f"Ошибка запуска бота: {e}")

if __name__ == '__main__':
    main()