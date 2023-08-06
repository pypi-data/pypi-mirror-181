from pagarme_integration.schemas.payments import PaymentSchema
from pagarme_integration.schemas.charges import ChargeSchema
from pagarme_integration.schemas.items import ItemSchema
from pagarme_integration.schemas.customers import CustomerSchema


class OrderSchema:
    __insert = {
        "type": "object",
        "properties": {
            "customer": CustomerSchema.validate_insert(),
            "items": {"type": "array", "items": ItemSchema.validate_insert()},
            "payments": {"type": "array", "items": PaymentSchema.validate_get()},
        },
        "required": ["customer", "items", "payments"],
    }

    __get = {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "items": {"type": "array", "items": ItemSchema.validate_get()},
            "charges": {"type": "array", "items": ChargeSchema.validate_get()},
        },
        "required": ["id", "items", "charges"],
    }

    __list = {
        "type": "array",
        "items": __get,
    }

    @classmethod
    def validate_insert(cls):
        return cls.__insert

    @classmethod
    def validate_get(cls):
        return cls.__get

    @classmethod
    def validate_list(cls):
        return cls.__list
