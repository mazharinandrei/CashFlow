DEFAULT_USER_DATA = {
    "statuses": ["Бизнес", "Личное", "Налог"],
    "types": [
        {
            "type_name": "Пополнение",
            "categories": [
                {
                    "category_name": "Основной доход",
                    "subcategories": ["Зарплата", "Аванс", "Премия"] 
                    },
                { 
                    "category_name": "Прочее", 
                    "subcategories": ["Подарки"] 
                }
            ]
        },

        {
            "type_name": "Списание",
            "categories": [
                {
                    "category_name": "Маркетинг",
                    "subcategories": ["Avito", "Farpost"] 
                    },
                { 
                    "category_name": "Инфраструктура", 
                    "subcategories": ["VPS", "Proxy"] 
                }
            ]
        },
    ]
}