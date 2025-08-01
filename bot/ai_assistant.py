# -*- coding: utf-8 -*-

import os
import logging
from openai import OpenAI
from config.tariffs import MARKETPLACE_TARIFFS, SERVICE_TARIFFS

logger = logging.getLogger(__name__)

class AIAssistant:
    """AI-помощник для консультаций по услугам фулфилмента"""
    
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.system_prompt = self._create_system_prompt()
    
    def _create_system_prompt(self) -> str:
        """Создание системного промпта с информацией о компании"""
        
        # Собираем информацию о маркетплейсах
        marketplaces_info = []
        for mp_code, mp_data in MARKETPLACE_TARIFFS.items():
            features = ", ".join(mp_data.get('features', []))
            marketplaces_info.append(
                f"• {mp_data['name']}: комиссия {mp_data['commission_rate']*100}%, "
                f"средний чек {mp_data['average_order_value']} руб. Особенности: {features}"
            )
        
        # Собираем информацию об услугах
        services_info = []
        for service_code, service_data in SERVICE_TARIFFS.items():
            rate_info = f"{service_data['rate']} руб"
            if service_data['rate_type'] == 'per_order':
                rate_info += "/заказ"
            elif service_data['rate_type'] == 'monthly':
                rate_info += "/месяц"
            elif service_data['rate_type'] == 'per_item':
                rate_info += "/товар"
            
            features = ", ".join(service_data.get('features', []))
            services_info.append(
                f"• {service_data['name']}: {rate_info}. {service_data['description']}. Особенности: {features}"
            )
        
        return f"""Ты - AI-консультант компании "Надежные-решения.рф", специализирующейся на услугах фулфилмента для российских маркетплейсов.

ИНФОРМАЦИЯ О КОМПАНИИ:
• Работаем с 2020 года
• Более 500 довольных клиентов
• Свыше 100,000 обработанных заказов в месяц
• 99.5% точность выполнения заказов
• Склады в Москве (5,000 м²), СПб (3,000 м²), Екатеринбурге (2,000 м²), Новосибирске (2,500 м²)

МАРКЕТПЛЕЙСЫ:
{chr(10).join(marketplaces_info)}

УСЛУГИ ФУЛФИЛМЕНТА:
{chr(10).join(services_info)}

СКИДКИ ЗА ОБЪЕМ:
• От 1,000 заказов/месяц: 5% скидка
• От 5,000 заказов/месяц: 10% скидка  
• От 10,000 заказов/месяц: 15% скидка

КОНТАКТЫ:
• Сайт: надежные-решения.рф
• Email: info@надежные-решения.рф
• Телефон: +7 (495) 123-45-67
• Режим работы: Пн-Пт 9:00-18:00 (МСК)

ИНСТРУКЦИИ:
1. Отвечай на русском языке профессионально и дружелюбно
2. Предоставляй конкретную информацию о тарифах и услугах
3. Помогай рассчитать примерную стоимость
4. Предлагай подходящие решения под потребности клиента
5. Всегда предлагай использовать калькулятор бота или подать заявку для точного расчета
6. Если не знаешь ответ - честно говори об этом и предлагай связаться с менеджером
7. Избегай слишком длинных ответов - будь кратким и по делу"""

    async def get_response(self, user_message: str, user_context: dict = None) -> str:
        """
        Получение ответа от AI-помощника
        
        Args:
            user_message: Сообщение пользователя
            user_context: Контекст пользователя (предыдущие расчеты и т.д.)
        
        Returns:
            str: Ответ AI-помощника
        """
        try:
            # Добавляем контекст пользователя если есть
            context_info = ""
            if user_context:
                if 'last_calculation' in user_context:
                    calc = user_context['last_calculation']
                    context_info = f"\n\nКОНТЕКСТ ПОЛЬЗОВАТЕЛЯ:\nПоследний расчет: {calc.get('marketplace', 'не указан')} маркетплейс, {calc.get('orders_count', 'не указано')} заказов/месяц, стоимость: {calc.get('total_cost', 'не рассчитана')} руб/месяц"
            
            messages = [
                {"role": "system", "content": self.system_prompt + context_info},
                {"role": "user", "content": user_message}
            ]
            
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=800,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Ошибка AI-помощника: {e}")
            return ("Извините, временные технические проблемы с AI-помощником. "
                   "Пожалуйста, воспользуйтесь калькулятором или свяжитесь с нашим менеджером: "
                   "+7 (495) 123-45-67")

    def is_question_about_services(self, message: str) -> bool:
        """Проверка, является ли сообщение вопросом об услугах"""
        service_keywords = [
            'фулфилмент', 'склад', 'хранение', 'упаковка', 'отправка', 'доставка',
            'возврат', 'маркировка', 'wildberries', 'ozon', 'яндекс', 'маркет',
            'стоимость', 'цена', 'тариф', 'сколько', 'услуг', 'фото', 'качество',
            'аналитика', 'комиссия', 'расчет', 'калькулятор'
        ]
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in service_keywords)