from flask_swagger import swagger

def build_swagger(app):
    swg = swagger(app)
    swg["info"]["title"] = 'Expense control app'
    swg["info"]["version"] = '0.0.1'
    swg["definitions"] = {
        "Hello": {
            "type": "object",
            "discriminator": "helloType",
            "properties": {"message": {"type": "string"}},
            "example": {"message": "Hi"},
        },
        "ExpenseIn": {
            "type": "object",
            "descriminator": "expenseInType",
            "properties": {
                "title": {"type": "string"},
                "amount": {"type": "number"},
            },
            "example": {
                "title": "Expense title",
                "amount": 0,
            }
        },
        "ExpenseOut": {
            "allOf": [
                {"$ref": "#/definitions/ExpenseIn"},
                {
                    "type": "object",
                    "properties": {
                        "id": {"type": "number"}
                    },
                    "example": {
                        "id": 0,
                    }
                }
            ]
        },
        "NotFound": {
            "type": "object",
            "discriminator": "notFoundType",
            "properties": {"error": {"type": "string"}},
            "example": {"error": "No items found"},
        },
    }
    return swg