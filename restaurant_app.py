from flask import Flask, render_template, redirect, url_for, request, abort, session
import secrets

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.order_model import Base, Order

engine = create_engine("sqlite:///orders.db", echo=True)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
db_session = DBSession()

#.\venv\Scripts\activate
#py restaurant_app.py

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

@app.route("/<int:table_number>")
def main_menu(table_number):

    session["table_number"] = table_number
    return render_template("main_menu.html", order_summary_ref = url_for('order', table_number=table_number))

@app.route("/order/<int:table_number>", methods=["POST"])
def order(table_number):

    order = request.form["order_summary"]
    customer_name = request.form["customer_name"]
    
    itemized_order = [item.strip() for item in order.strip().split("\r\n") if item.strip()]
    order_items_str = ", ".join(itemized_order)

    new_order = Order(
        customer_name=customer_name,
        order_items=order_items_str,
        table_number=table_number
    )
    
    try:
        db_session.add(new_order)
        db_session.commit()
    except:
        print("Error saving order")

    order_details = {
        "customer_name": customer_name,
        "order_items": itemized_order,
        "table_number": table_number
    }
    
    return render_template("order_summary.html", orders=order_details)
    
@app.route("/kitchen/")
def kitchen():

    orders = db_session.query(Order).all()
    
    kitchen_orders = []
    for order in orders:
        JSON_order = {
            "id": order.id,
            "customer_name": order.customer_name,
            "order_items": order.order_items.split(", "),  
            "table_number": order.table_number
        }
        kitchen_orders.append(JSON_order)
        
    return render_template("kitchen.html", orders=kitchen_orders)

@app.route("/delete/<int:order_id>")
def delete_order(order_id):
    try:
        order_to_delete = db_session.query(Order).filter_by(id=order_id).first()
        if order_to_delete:
            db_session.delete(order_to_delete)
            db_session.commit()
        else:
            abort(404)
    except:
        print("There was a problem deleting that task")

    return redirect(url_for("kitchen"))


if __name__ == "__main__":
    app.run(debug=True)