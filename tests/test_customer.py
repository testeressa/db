import pytest
import allure
import random
import string
from datetime import datetime
from lib.db import (
    create_customer,
    get_customer_by_id,
    delete_customer_by_id,
    update_customer
)

def generate_random_string(length=6):
    return ''.join(random.choices(string.ascii_letters, k=length))

def generate_random_email():
    return f"{generate_random_string()}@example.com"

def generate_random_phone():
    return f"+79{random.randint(100000000, 999999999)}"

@pytest.fixture
def customer_data():
    return {
        "customer_group_id": 1,
        "store_id": 0,
        "language_id": 1,
        "firstname": "Test",
        "lastname": "User",
        "email": generate_random_email(),
        "telephone": generate_random_phone(),
        "password": "hashed_pass",
        "custom_field": "{}",
        "newsletter": 0,
        "ip": "192.168.0.2",
        "status": 1,
        "safe": 1,
        "token": "AAAAABBBBBCCCCDDDD",
        "code": "123123",
        "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

@allure.feature("Клиенты")
@allure.story("Создание клиента")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_customer_and_verify_by_id(connection, customer_data):
    with allure.step("Создание клиента"):
        customer_id = create_customer(connection, customer_data)

    with allure.step("Проверка клиента по ID"):
        customer = get_customer_by_id(connection, customer_id)
        assert customer is not None
        assert customer["email"] == customer_data["email"]
        assert customer["firstname"] == customer_data["firstname"]


@allure.feature("Клиенты")
@allure.story("Обновление клиента")
@allure.severity(allure.severity_level.NORMAL)
def test_update_existing_customer(connection, customer_data):
    with allure.step("Создание клиента"):
        customer_id = create_customer(connection, customer_data)

    updated_data = {
        "firstname": "Updated",
        "lastname": "User",
        "email": generate_random_email(),
        "telephone": "9999999999",
    }

    with allure.step("Обновление данных клиента"):
        update_customer(connection, customer_id, updated_data)

    with allure.step("Проверка обновлённых данных"):
        customer = get_customer_by_id(connection, customer_id)
        for key, value in updated_data.items():
            assert customer[key] == value


@allure.feature("Клиенты")
@allure.story("Негативное обновление несуществующего клиента")
@allure.severity(allure.severity_level.MINOR)
def test_update_nonexistent_customer(connection):
    fake_id = 999999
    updated_data = {
        "firstname": "Ghost",
        "lastname": "User",
        "email": "ghost@example.com",
        "telephone": "0000000000"
    }

    with allure.step("Попытка обновить клиента с несуществующим ID"):
        affected_rows = update_customer(connection, fake_id, updated_data)
        assert affected_rows == 0


@allure.feature("Клиенты")
@allure.story("Удаление клиента")
@allure.severity(allure.severity_level.CRITICAL)
def test_delete_existing_customer(connection, customer_data):
    with allure.step("Создание клиента"):
        customer_id = create_customer(connection, customer_data)

    with allure.step("Удаление клиента"):
        deleted = delete_customer_by_id(connection, customer_id)
        assert deleted == 1

    with allure.step("Проверка отсутствия клиента"):
        customer = get_customer_by_id(connection, customer_id)
        assert customer is None


@allure.feature("Клиенты")
@allure.story("Удаление несуществующего клиента")
@allure.severity(allure.severity_level.MINOR)
def test_delete_nonexistent_customer(connection):
    fake_id = 999999
    with allure.step("Попытка удалить несуществующего клиента"):
        deleted = delete_customer_by_id(connection, fake_id)
        assert deleted == 0
