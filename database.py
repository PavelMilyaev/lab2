import sqlite3
import os
from datetime import datetime

# Получаем путь к БД из переменной окружения или используем локальный путь
DB_NAME = os.getenv('DB_PATH', 'clothing_calculations.db')


def init_db():
    """Инициализация базы данных"""
    # Создаем директорию, если её нет
    db_dir = os.path.dirname(DB_NAME)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS calculations
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       date
                       TEXT
                       NOT
                       NULL,
                       items
                       TEXT
                       NOT
                       NULL,
                       total_fabric
                       REAL
                       NOT
                       NULL,
                       total_sewing_cost
                       REAL
                       NOT
                       NULL,
                       total_material_cost
                       REAL
                       NOT
                       NULL,
                       grand_total
                       REAL
                       NOT
                       NULL
                   )
                   ''')
    conn.commit()
    conn.close()


def save_calculation(items, total_fabric, total_sewing, total_materials, grand_total):
    """Сохранение расчёта в БД"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
                   INSERT INTO calculations (date, items, total_fabric, total_sewing_cost, total_material_cost,
                                             grand_total)
                   VALUES (?, ?, ?, ?, ?, ?)
                   ''',
                   (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), items, total_fabric, total_sewing, total_materials,
                    grand_total))
    conn.commit()
    conn.close()


def get_history():
    """Получение истории расчётов"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM calculations ORDER BY date DESC')
    data = cursor.fetchall()
    conn.close()
    return data