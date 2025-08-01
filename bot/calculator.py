# -*- coding: utf-8 -*-

from config.tariffs import MARKETPLACE_TARIFFS, SERVICE_TARIFFS

class FulfillmentCalculator:
    """Калькулятор стоимости услуг фулфилмента"""
    
    def __init__(self):
        self.marketplace_tariffs = MARKETPLACE_TARIFFS
        self.service_tariffs = SERVICE_TARIFFS
    
    def calculate(self, marketplace: str, orders_count: int, selected_services: list) -> dict:
        """
        Основной метод расчета стоимости
        
        Args:
            marketplace: Выбранный маркетплейс
            orders_count: Количество заказов в месяц
            selected_services: Список выбранных услуг
        
        Returns:
            dict: Результат расчета с детализацией
        """
        result = {
            'marketplace': marketplace,
            'orders_count': orders_count,
            'services': {},
            'marketplace_commission': 0,
            'total_service_cost': 0,
            'total_cost': 0,
            'cost_per_order': 0
        }
        
        # Расчет комиссии маркетплейса
        marketplace_tariff = self.marketplace_tariffs.get(marketplace, {})
        base_commission = marketplace_tariff.get('commission_rate', 0.1)
        
        # Применяем скидки за объем
        volume_discount = self._calculate_volume_discount(orders_count)
        commission_rate = base_commission * (1 - volume_discount)
        
        # Примерная стоимость заказа для расчета комиссии
        average_order_value = marketplace_tariff.get('average_order_value', 1000)
        result['marketplace_commission'] = orders_count * average_order_value * commission_rate
        
        # Расчет стоимости выбранных услуг
        total_service_cost = 0
        service_details = {}
        
        for service in selected_services:
            service_tariff = self.service_tariffs.get(service, {})
            service_cost = self._calculate_service_cost(service, orders_count, service_tariff)
            
            service_details[service] = {
                'name': service_tariff.get('name', service),
                'cost': service_cost,
                'rate': service_tariff.get('rate', 0),
                'rate_type': service_tariff.get('rate_type', 'per_order')
            }
            
            total_service_cost += service_cost
        
        result['services'] = service_details
        result['total_service_cost'] = total_service_cost
        result['total_cost'] = result['marketplace_commission'] + total_service_cost
        result['cost_per_order'] = result['total_cost'] / orders_count if orders_count > 0 else 0
        
        return result
    
    def _calculate_volume_discount(self, orders_count: int) -> float:
        """Расчет скидки за объем заказов"""
        if orders_count >= 10000:
            return 0.15  # 15% скидка
        elif orders_count >= 5000:
            return 0.10  # 10% скидка
        elif orders_count >= 1000:
            return 0.05  # 5% скидка
        else:
            return 0.0   # Без скидки
    
    def _calculate_service_cost(self, service: str, orders_count: int, service_tariff: dict) -> float:
        """Расчет стоимости конкретной услуги"""
        rate = service_tariff.get('rate', 0)
        rate_type = service_tariff.get('rate_type', 'per_order')
        
        if rate_type == 'per_order':
            return rate * orders_count
        elif rate_type == 'monthly':
            return rate
        elif rate_type == 'percentage':
            # Процент от оборота (примерная оценка)
            average_order_value = 1000
            return rate * orders_count * average_order_value
        else:
            return 0
    
    def get_marketplace_info(self, marketplace: str) -> dict:
        """Получение информации о маркетплейсе"""
        return self.marketplace_tariffs.get(marketplace, {})
    
    def get_service_info(self, service: str) -> dict:
        """Получение информации об услуге"""
        return self.service_tariffs.get(service, {})
