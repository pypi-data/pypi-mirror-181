from pagarme_integration.utils.handle_errors import (
    handle_error_pagarme,
    handle_error_insert_orders,
)
from pagarme_integration.schemas.orders import OrderSchema
from pagarme_integration.classes.config import Config

from jsonschema import validate

from abc import abstractmethod

import requests
import json


class Order(OrderSchema):
    def __init__(self, id, status, customer, items, charges, payments) -> None:
        if id:
            self.id = id
        if status:
            self.status = status
        if customer:
            self.customer = customer
        self.items = items
        if payments:
            self.payments = payments
        if charges:
            self.charges = charges

    @abstractmethod
    def mount_obj(content: dict):
        return Order(
            id=content.get("id"),
            status=content.get("status"),
            customer=content.get("customer"),
            items=content.get("items"),
            payments=content.get("payments"),
            charges=content.get("charges"),
        ).__dict__

    @classmethod
    def get_orders(cls, customer_id):
        response = []
        if customer_id:
            url = Config.get_url() + f"/orders?customer_id={customer_id}"
        else:
            url = Config.get_url() + "/orders"
        content = json.loads(
            requests.get(
                url,
                auth=Config.get_auth(),
                headers=Config.get_header(),
            ).text
        )
        content_validated = handle_error_pagarme(content)
        contents = content_validated.get("data")
        validate(instance=contents, schema=cls.validate_list())
        [response.append(Order.mount_obj(content)) for content in contents]
        return response

    @classmethod
    def get_order(cls, pk):
        url = Config.get_url() + f"/orders/{pk}"
        content = json.loads(
            requests.get(
                url,
                auth=Config.get_auth(),
                headers=Config.get_header(),
            ).text
        )
        content_validated = handle_error_pagarme(content)
        validate(instance=content_validated, schema=cls.validate_get())
        return Order.mount_obj(content_validated)

    @classmethod
    def insert_order(cls, payload):
        url = Config.get_url() + "/orders/"
        header = Config.get_header()
        header["Content-Type"] = "application/json"
        content = json.loads(
            requests.post(
                url,
                auth=Config.get_auth(),
                headers=header,
                json=payload,
            ).text
        )
        content_validated = handle_error_pagarme(content)
        handle_error_insert_orders(
            content=content_validated.get("charges")[0]
            .get("last_transaction")
            .get("gateway_response")
        )
        return Order.mount_obj(content_validated)

    @classmethod
    def cancel_charge(cls, charge_id):
        url = Config.get_url() + f"/charges/{charge_id}"
        header = Config.get_header()
        response = requests.delete(url, auth=Config.get_auth(), headers=header)
        handle_error_pagarme(response.json())

    @classmethod
    def cancel_order(cls, order_id):
        order = cls.get_order(order_id)
        cancelled_charges = []
        for charge in order.get("charges"):
            if charge.get("status") == "paid" or charge.get("status") == "pending":
                cls.cancel_charge(charge.get("id"))
                cancelled_charges.append(charge.get("id"))
        return cancelled_charges
