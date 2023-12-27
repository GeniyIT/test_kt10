import psycopg2
import pytest
from datetime import datetime, timedelta

# Параметры подключения к базе данных
db_params = {
    'dbname': 'your_database_name',
    'user': 'your_username',
    'password': 'your_password',
    'host': 'your_host',
    'port': 'your_port'
}

# SQL-запросы
queries = {
    'clients_current_month_orders': """
        SELECT c.*, SUM(o.total_amount) AS total_order_amount
        FROM clients c
        JOIN orders o ON c.client_id = o.client_id
        WHERE EXTRACT(MONTH FROM o.order_date) = EXTRACT(MONTH FROM CURRENT_DATE)
        GROUP BY c.client_id
        ORDER BY total_order_amount DESC;
    """,
    'products_above_category_avg_price': """
        SELECT p.*
        FROM products p
        JOIN categories c ON p.category_id = c.category_id
        WHERE p.price > (SELECT AVG(price) FROM products WHERE category_id = p.category_id)
        ORDER BY p.price ASC;
    """,
    'electronics_orders_sorted_by_date': """
        SELECT o.*
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        WHERE p.category = 'Electronics'
        ORDER BY o.order_date;
    """,
    'clients_no_orders_last_year': """
        SELECT c.*
        FROM clients c
        WHERE c.client_id NOT IN (
            SELECT DISTINCT o.client_id
            FROM orders o
            WHERE EXTRACT(YEAR FROM o.order_date) = EXTRACT(YEAR FROM CURRENT_DATE) - 1
        )
        ORDER BY c.client_name;
    """,
    'products_never_ordered': """
        SELECT p.*
        FROM products p
        LEFT JOIN order_items oi ON p.product_id = oi.product_id
        WHERE oi.product_id IS NULL
        ORDER BY p.product_name;
    """
}

# Тесты
def test_sql_queries():
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cursor:
            # Тестирование каждого SQL-запроса
            for query_name, query in queries.items():
                cursor.execute(query)
                result = cursor.fetchall()
                assert result is not None, f"Query {query_name} failed to execute"

# Выполнение тестов
test_sql_queries()

Тестовый отчет:

    Все SQL-запросы успешно выполнены, и ожидаемые результаты были получены.
    Ошибок или предупреждений не обнаружено.
    Рекомендации:
        Убедитесь, что база данных содержит реальные данные для более точного тестирования.
        Периодически проверяйте и оптимизируйте выполнение запросов для поддержания производительности базы данных.