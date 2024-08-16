from flask import render_template, request, redirect, url_for, session
from ..models import db, Product, CartItem

def get_cart():
    if 'cart' not in session:
        session['cart'] = {}
    
    cart_items = []
    total = 0
    for product_id, quantity in session['cart'].items():
        product = Product.query.get(product_id)
        if product:
            subtotal = product.price * quantity
            cart_items.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'quantity': quantity,
                'subtotal': subtotal
            })
            total += subtotal
    
    return render_template('cart_list.html', cart_items=cart_items, total=total)

def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = {}
    
    if product_id in session['cart']:
        session['cart'][product_id] += 1
    else:
        session['cart'][product_id] = 1
    
    session.modified = True
    return redirect(url_for('cart'))

def remove_from_cart(product_id):
    if 'cart' in session and product_id in session['cart']:
        del session['cart'][product_id]
        session.modified = True
    return redirect(url_for('cart'))

def update_quantity(product_id):
    quantity = int(request.form.get('quantity', 1))
    if quantity > 0:
        session['cart'][product_id] = quantity
        session.modified = True
    return redirect(url_for('cart'))

def clear_cart():
    session['cart'] = {}
    session.modified = True
    return redirect(url_for('cart'))

def checkout():
    if 'cart' not in session or not session['cart']:
        return redirect(url_for('cart'))
    
    # ここで注文処理を行う
    # 例: データベースに注文を保存し、在庫を更新する
    
    session['cart'] = {}
    session.modified = True
    return render_template('order_confirm.html')