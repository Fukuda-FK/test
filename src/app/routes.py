from flask import Flask, render_template, request, redirect, url_for
from .controllers import cart_controller, orders_controller, products_controller

app = Flask(__name__)

@app.route('/')
def home():
    """トップページを表示"""
    return render_template('index.html')

@app.route('/products')
def product_list():
    """商品一覧を表示"""
    products = products_controller.get_products()
    return render_template('product_list.html', products=products)

@app.route('/cart')
def cart_list():
    """カート一覧を表示"""
    cart_items = cart_controller.get_cart()
    return render_template('cart_list.html', cart_items=cart_items)

@app.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    """商品をカートに追加"""
    cart_controller.add_to_cart(product_id)
    return redirect(url_for('product_list'))

@app.route('/order/confirm')
def order_confirm():
    """注文確認ページを表示"""
    cart_items = cart_controller.get_cart()
    return render_template('order_confirm.html', cart_items=cart_items)

@app.route('/order/complete', methods=['POST'])
def order_complete():
    """注文を確定"""
    orders_controller.create_order()
    cart_controller.clear_cart()
    return redirect(url_for('order_history'))

@app.route('/order/history')
def order_history():
    """注文履歴を表示"""
    orders = orders_controller.get_orders()
    return render_template('order_history.html', orders=orders)

@app.route('/admin/inventory')
def inventory_management():
    """在庫管理ページを表示（管理者用）"""
    inventory = products_controller.get_inventory()
    return render_template('inventory_management.html', inventory=inventory)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
