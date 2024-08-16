from flask import render_template, jsonify
from ..models import db, Product

def get_products():
    """
    商品一覧を取得し、テンプレートにレンダリングする
    """
    products = Product.query.all()
    return render_template('product_list.html', products=products)

def get_product(product_id):
    """
    指定されたIDの商品詳細を取得する
    """
    product = Product.query.get(product_id)
    if product:
        return jsonify(product.to_dict())
    return jsonify({"error": "Product not found"}), 404

def create_product(data):
    """
    新しい商品を作成する
    """
    new_product = Product(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        stock=data['stock']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201

def update_product(product_id, data):
    """
    指定されたIDの商品情報を更新する
    """
    product = Product.query.get(product_id)
    if product:
        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.price = data.get('price', product.price)
        product.stock = data.get('stock', product.stock)
        db.session.commit()
        return jsonify(product.to_dict())
    return jsonify({"error": "Product not found"}), 404

def delete_product(product_id):
    """
    指定されたIDの商品を削除する
    """
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"})
    return jsonify({"error": "Product not found"}), 404

def check_stock(product_id):
    """
    指定されたIDの商品の在庫状況を確認する
    """
    product = Product.query.get(product_id)
    if product:
        return jsonify({"product_id": product_id, "stock": product.stock})
    return jsonify({"error": "Product not found"}), 404
