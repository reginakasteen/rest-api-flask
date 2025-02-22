from flask import Blueprint, jsonify, request
from flask_jwt_extended import current_user, jwt_required
from marshmallow import ValidationError

from app.db import Expense, db
from app.schemas import expense_schema, expenses_schema

bp = Blueprint("expense", __name__, url_prefix="/expenses")

@bp.route('/', methods=["POST"])
@jwt_required()
def create_expense():

    """
    Add new expense
    ---
    tags:
        - expenses
    parameters: 
        - name: expense
          in: body
          description: Expense data
          required: true
          schema:
            $ref: '#/definitions/ExpenseIn'
    """

    json_data = request.json
    try:
        data = expense_schema.load(json_data)
    except ValidationError as error:
        return error.messages, 422

    new_expense = Expense(title=data["title"], amount=data["amount"], user_id=current_user.id)
    db.session.add(new_expense)
    db.session.commit()
    return jsonify(expense_schema.dump(new_expense)), 201 

@bp.route('/', methods=["GET"])
@jwt_required()
def get_expenses():

    """
    Get list of all expenses
    ---
    tags:
        - expenses
    responses:
      200: 
        description: Expenses list
        schema:
            type: array
            items: 
                $ref: "#/definitions/ExpenseOut"

    """
    return jsonify(expenses_schema.dump(current_user.expenses))

@bp.route('/<int:id>', methods=["GET"])
@jwt_required()
def get_expense(id):
    """
    Looking for an item by ID
    ---
    tags:
        - expenses
    produces:
        - application/json
    parameters:
    - name: id
      in: path
      description: Expense ID
      required: true
      type: number
    responses:
        200:
            description: Found item
            schema:
                $ref: '#/definitions/ExpenseOut'
        404:
            description: No items found by ID
            schema:
                $ref: '#/definitions/NotFound'
    """


    expense = db.get_or_404(Expense, id)
    if expense.user_id != current_user.id:
        return jsonify(error="Access denied"), 401
    return jsonify(expense_schema.dump(expense))


@bp.route('/<int:id>', methods=["DELETE"])
@jwt_required()
def delete_expense(id):

    """
    Delete expense by ID
    ---
    tags:
        - expenses
    produces:
        - application/json
    parameters:
    - name: id
      in: path
      description: Expense ID
      required: true
      type: number
    responses:
        204:
            description: Expense deleted successfully
        404:
            description: No items found by ID
            schema:
                $ref: '#/definitions/NotFound'
    """

    expense = db.get_or_404(Expense, id)
    if expense.user_id != current_user.id:
        return jsonify(error="Access denied"), 401

    db.session.delete(expense)
    db.session.commit()
    return "", 204
    

@bp.route('/<int:id>', methods=["PATCH"])
@jwt_required()
def update_expense(id):

    """
    Update expense data by ID
    ---
    tags:
        - expenses
    produces:
        - application/json
    parameters:
    - name: id
      in: path
      description: Expense ID
      required: true
      type: number
    - name: expense
      in: body
      description: Data for update
      required: true
      schema:
        $ref: '#/definitions/ExpenseIn'
    responses:
        200:
            description: Updated expense
            schema:
                $ref: '#/definitions/ExpenseOut'
        404:
            description: No items found by ID
            schema:
                $ref: '#/definitions/NotFound'
    """

    expense = db.get_or_404(Expense, id)
    if expense.user_id != current_user.id:
        return jsonify(error="Access denied"), 401
    json_data = request.json
    try:
        data = expense_schema.load(json_data, partial=True)
    except ValidationError as error:
        return error.messages, 422    
    expense.title = data.get("title", expense.title)
    expense.amount = data.get("amount", expense.amount)
    db.session.commit()
    return jsonify(
        [{
            "id": expense.id,
            "title": expense.title,
            "amount": expense.amount
        }]
    )



