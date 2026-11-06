
import sqlite3

# Підключення до бази даних
conn = sqlite3.connect("sales.db")
cursor = conn.cursor()

# Створення таблиць
cursor.execute("""
CREATE TABLE IF NOT EXISTS Salesmen (
    id INTEGER PRIMARY KEY,
    name TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Customers (
    id INTEGER PRIMARY KEY,
    name TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Sales (
    id INTEGER PRIMARY KEY,
    salesman_id INTEGER,
    customer_id INTEGER,
    amount REAL,
    FOREIGN KEY (salesman_id) REFERENCES Salesmen(id),
    FOREIGN KEY (customer_id) REFERENCES Customers(id)
)
""")

# Додавання продавців
cursor.executemany("""
INSERT OR IGNORE INTO Salesmen VALUES (?, ?)
""", [
    (1, "Іван"),
    (2, "Марія"),
    (3, "Олег")
])

# Додавання покупців
cursor.executemany("""
INSERT OR IGNORE INTO Customers VALUES (?, ?)
""", [
    (1, "Анна"),
    (2, "Петро"),
    (3, "Олена")
])

# Додавання продажів
cursor.executemany("""
INSERT OR IGNORE INTO Sales VALUES (?, ?, ?, ?)
""", [
    (1, 1, 1, 500),
    (2, 1, 2, 1200),
    (3, 2, 1, 800),
    (4, 2, 3, 2000),
    (5, 3, 2, 300),
    (6, 3, 3, 1500)
])

conn.commit()


# Функція для виконання запитів
def show(title, query, params=()):
    print("\n" + title)
    cursor.execute(query, params)
    for row in cursor.fetchall():
        print(row)


# 1. Усі угоди
show("1. Усі угоди",
     "SELECT * FROM Sales")

# 2. Угоди конкретного продавця
show("2. Угоди продавця Іван",
     "SELECT * FROM Sales WHERE salesman_id = ?", (1,))

# 3. Максимальна угода
show("3. Максимальна угода",
     "SELECT * FROM Sales ORDER BY amount DESC LIMIT 1")

# 4. Мінімальна угода
show("4. Мінімальна угода",
     "SELECT * FROM Sales ORDER BY amount ASC LIMIT 1")

# 5. Максимальна угода продавця
show("5. Максимальна угода Івана",
     "SELECT MAX(amount) FROM Sales WHERE salesman_id = ?", (1,))

# 6. Мінімальна угода продавця
show("6. Мінімальна угода Івана",
     "SELECT MIN(amount) FROM Sales WHERE salesman_id = ?", (1,))

# 7. Максимальна угода покупця
show("7. Максимальна покупка Анни",
     "SELECT MAX(amount) FROM Sales WHERE customer_id = ?", (1,))

# 8. Мінімальна угода покупця
show("8. Мінімальна покупка Анни",
     "SELECT MIN(amount) FROM Sales WHERE customer_id = ?", (1,))

# 9. Продавець з максимальною сумою продажів
show("9. Найкращий продавець",
     """
     SELECT Salesmen.name, SUM(Sales.amount)
     FROM Sales
     JOIN Salesmen ON Sales.salesman_id = Salesmen.id
     GROUP BY Salesmen.id
     ORDER BY SUM(Sales.amount) DESC
     LIMIT 1
     """)

# 10. Продавець з мінімальною сумою продажів
show("10. Продавець з мінімальними продажами",
     """
     SELECT Salesmen.name, SUM(Sales.amount)
     FROM Sales
     JOIN Salesmen ON Sales.salesman_id = Salesmen.id
     GROUP BY Salesmen.id
     ORDER BY SUM(Sales.amount) ASC
     LIMIT 1
     """)

# 11. Покупець з максимальною сумою покупок
show("11. Найкращий покупець",
     """
     SELECT Customers.name, SUM(Sales.amount)
     FROM Sales
     JOIN Customers ON Sales.customer_id = Customers.id
     GROUP BY Customers.id
     ORDER BY SUM(Sales.amount) DESC
     LIMIT 1
     """)

# 12. Середня сума покупки покупця
show("12. Середня покупка Анни",
     "SELECT AVG(amount) FROM Sales WHERE customer_id = ?", (1,))

# 13. Середня сума продажу продавця
show("13. Середній продаж Івана",
     "SELECT AVG(amount) FROM Sales WHERE salesman_id = ?", (1,))

# Закриття бази
conn.close()
