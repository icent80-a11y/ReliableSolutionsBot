# -*- coding: utf-8 -*-

"""
Форматтеры для вывода результатов расчетов
"""

from config.tariffs import MARKETPLACE_TARIFFS, SERVICE_TARIFFS

def format_calculation_result(result: dict, marketplace: str, orders_count: int, selected_services: list) -> str:
    """
    Форматирование результата расчета для вывода пользователю
    
    Args:
        result: Результат расчета из калькулятора
        marketplace: Название маркетплейса
        orders_count: Количество заказов
        selected_services: Список выбранных услуг
    
    Returns:
        str: Отформатированный текст результата
    """
    
    marketplace_names = {
        'wildberries': '🛍 Wildberries',
        'ozon': '📦 Ozon',
        'yandex': '🟡 Яндекс Маркет'
    }
    
    marketplace_display = marketplace_names.get(marketplace, marketplace)
    
    text = f"""
💰 <b>Результат расчета стоимости</b>

<b>📊 Параметры расчета:</b>
• Маркетплейс: {marketplace_display}
• Количество заказов в месяц: {orders_count:,}

<b>🛠 Выбранные услуги:</b>
"""
    
    # Детализация по услугам
    total_services_cost = 0
    for service_code, service_data in result['services'].items():
        service_name = service_data['name']
        service_cost = service_data['cost']
        rate = service_data['rate']
        rate_type = service_data['rate_type']
        
        total_services_cost += service_cost
        
        # Форматирование тарифа
        if rate_type == 'per_order':
            rate_text = f"{rate} руб/заказ"
        elif rate_type == 'monthly':
            rate_text = f"{rate} руб/месяц"
        elif rate_type == 'per_item':
            rate_text = f"{rate} руб/товар"
        elif rate_type == 'per_m3_day':
            rate_text = f"{rate} руб/м³/день"
        else:
            rate_text = f"{rate}"
        
        text += f"  • {service_name}: {service_cost:,.0f} руб ({rate_text})\n"
    
    # Итоговые суммы
    text += f"""
<b>💸 Расчет стоимости:</b>
• Услуги фулфилмента: {total_services_cost:,.0f} руб/мес
• Комиссии маркетплейса: {result['marketplace_commission']:,.0f} руб/мес

<b>🎯 ИТОГО: {result['total_cost']:,.0f} руб/мес</b>
<b>📈 Стоимость за заказ: {result['cost_per_order']:.0f} руб</b>

<b>💡 Дополнительная информация:</b>
"""
    
    # Добавляем информацию о скидках
    volume_discount = _get_volume_discount_info(orders_count)
    if volume_discount:
        text += f"• {volume_discount}\n"
    
    # Информация о маркетплейсе
    marketplace_info = MARKETPLACE_TARIFFS.get(marketplace, {})
    commission_rate = marketplace_info.get('commission_rate', 0) * 100
    text += f"• Комиссия {marketplace_display}: {commission_rate}%\n"
    
    text += """
<b>⚡ Что дальше?</b>
• Подайте заявку для получения персонального предложения
• Наш менеджер свяжется с вами в течение 2 часов
• Обсудим детали и запустим сотрудничество

<i>* Расчет является примерным. Точная стоимость определяется после анализа ваших потребностей.</i>
"""
    
    return text

def _get_volume_discount_info(orders_count: int) -> str:
    """Получение информации о скидке за объем"""
    if orders_count >= 10000:
        return "🎉 Скидка за объем: 15% (от 10,000 заказов)"
    elif orders_count >= 5000:
        return "🎉 Скидка за объем: 10% (от 5,000 заказов)"
    elif orders_count >= 1000:
        return "🎉 Скидка за объем: 5% (от 1,000 заказов)"
    else:
        return ""

def format_currency(amount: float) -> str:
    """Форматирование денежных сумм"""
    return f"{amount:,.0f} руб"

def format_service_description(service_code: str) -> str:
    """Получение описания услуги"""
    service_info = SERVICE_TARIFFS.get(service_code, {})
    
    name = service_info.get('name', service_code)
    description = service_info.get('description', '')
    features = service_info.get('features', [])
    
    text = f"<b>{name}</b>\n\n{description}\n\n<b>Особенности:</b>\n"
    
    for feature in features:
        text += f"• {feature}\n"
    
    return text

def format_marketplace_info(marketplace: str) -> str:
    """Форматирование информации о маркетплейсе"""
    marketplace_info = MARKETPLACE_TARIFFS.get(marketplace, {})
    
    name = marketplace_info.get('name', marketplace)
    commission = marketplace_info.get('commission_rate', 0) * 100
    avg_order = marketplace_info.get('average_order_value', 0)
    features = marketplace_info.get('features', [])
    
    text = f"""
<b>{name}</b>

<b>Условия работы:</b>
• Комиссия: {commission}%
• Средний чек: {avg_order} руб

<b>Особенности интеграции:</b>
"""
    
    for feature in features:
        text += f"• {feature}\n"
    
    return text
