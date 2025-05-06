def create_customer(connection, customer_data: dict) -> int:
    """
    Универсальная вставка записи в таблицу oc_customer без явного перечисления столбцов.
    """
    fields = ", ".join(customer_data.keys())
    placeholders = ", ".join(["%s"] * len(customer_data))
    values = tuple(customer_data.values())

    query = f"INSERT INTO oc_customer ({fields}) VALUES ({placeholders})"

    with connection.cursor() as cursor:
        cursor.execute(query, values)
        connection.commit()
        return cursor.lastrowid


def get_customer_by_email(connection, email: str) -> dict | None:
    """
    Получает информацию о клиенте по его email.
    """
    query = "SELECT * FROM oc_customer WHERE email = %s"

    with connection.cursor() as cursor:
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        return result


def get_customer_by_id(connection, customer_id: int) -> dict | None:
    """
    Получает информацию о клиенте по его ID.
    """
    query = "SELECT * FROM oc_customer WHERE customer_id = %s"

    with connection.cursor() as cursor:
        cursor.execute(query, (customer_id,))
        result = cursor.fetchone()
        return result


def delete_customer_by_id(connection, customer_id: int) -> int:
    """
    Удаляет клиента по его ID.
    """
    query = "DELETE FROM oc_customer WHERE customer_id = %s"

    with connection.cursor() as cursor:
        cursor.execute(query, (customer_id,))
        connection.commit()
        return cursor.rowcount


def update_customer(connection, customer_id: int, updated_data: dict) -> int:
    """
    Обновляет данные клиента по его ID.
    """
    if not updated_data:
        return 0

    set_clause = ", ".join([f"{key} = %s" for key in updated_data])
    values = list(updated_data.values()) + [customer_id]

    query = f"UPDATE oc_customer SET {set_clause} WHERE customer_id = %s"

    with connection.cursor() as cursor:
        cursor.execute(query, values)
        connection.commit()
        return cursor.rowcount
