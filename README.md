# 「要求内容」の要件定義書

## 1. 目的
このシステムの目的は、ECサイトの基盤となるウェブアプリケーションをAWSのサービス（RDS、EC2、CloudFormation）を用いて構築し、以下の機能を提供することです。
- トップページの表示
- 商品一覧の表示
- カート一覧の表示
- 注文決定の処理
- 注文履歴の表示
- 在庫管理の実施

## 2. ファイル・フォルダ構成

```
project-root/
├── README.md
├── cloudformation/
│   ├── main.yaml
├── src/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── models.py
│   │   ├── controllers/
│   │   │   ├── __init__.py
│   │   │   ├── cart_controller.py
│   │   │   ├── orders_controller.py
│   │   │   └── products_controller.py
│   │   └── templates/
│   │       ├── index.html
│   │       ├── product_list.html
│   │       ├── cart_list.html
│   │       ├── order_confirm.html
│   │       └── order_history.html
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_cart.py
│   │   ├── test_orders.py
│   │   └── test_products.py
├── scripts/
│   ├── init_script.sh
└── requirements.txt
```

- `README.md`：プロジェクトの概要とセットアップ手順。
- `cloudformation/`：CloudFormationテンプレートを格納するディレクトリ。
  - `main.yaml`：EC2インスタンス、RDSインスタンス、およびその他必要なリソースを定義するCloudFormationテンプレート。
- `src/`：アプリケーションのソースコードを格納するディレクトリ。
  - `app/`：アプリケーションのメインフォルダ。
    - `__init__.py`：アプリケーションの初期化ファイル。
    - `routes.py`：Flaskルーティング情報。
    - `models.py`：データモデル定義。
    - `controllers/`：各機能ごとのコントローラーファイル。
      - `cart_controller.py`：カート機能のコントローラ。
      - `orders_controller.py`：注文機能のコントローラ。
      - `products_controller.py`：商品機能のコントローラ。
    - `templates/`：HTMLテンプレートファイルを格納するディレクトリ。
      - `index.html`：トップページ。
      - `product_list.html`：商品一覧ページ。
      - `cart_list.html`：カート一覧ページ。
      - `order_confirm.html`：注文確定ページ。
      - `order_history.html`：注文履歴ページ。
- `tests/`：テストコードを格納するディレクトリ。
  - `test_cart.py`：カート機能のテストケース。
  - `test_orders.py`：注文機能のテストケース。
  - `test_products.py`：商品機能のテストケース。
- `scripts/`：各種スクリプトを格納するディレクトリ。
  - `init_script.sh`：EC2インスタンス起動時に実行されるスクリプト。
- `requirements.txt`：Pythonパッケージの依存関係リスト。

各ファイルの詳細な内容は以下の通りです。

### `cloudformation/main.yaml`
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  EC2Instance:
    Type: 'AWS::EC2::Instance'
    Properties:
      InstanceType: 't2.micro'
      ImageId: 'ami-0abcdef1234567890'
      UserData:
        Fn::Base64: !Sub |
          #!/bin/bash
          cd /home/ec2-user
          yum install -y python3
          pip3 install -r requirements.txt
          python3 src/app/__init__.py
  RDSInstance:
    Type: 'AWS::RDS::DBInstance'
    Properties:
      DBInstanceClass: 'db.t2.micro'
      Engine: 'MySQL'
      MasterUsername: !Ref DBUsername
      MasterUserPassword: !Ref DBPassword
      AllocatedStorage: 20
Parameters:
  DBUsername:
    Type: String
    NoEcho: true
  DBPassword:
    Type: String
    NoEcho: true
Outputs:
  EC2InstanceId:
    Description: 'InstanceId of the newly created EC2 instance'
    Value: !Ref EC2Instance
  RDSInstanceEndpoint:
    Description: 'Endpoint of the RDS instance'
    Value: !GetAtt 
      - RDSInstance
      - Endpoint.Address
```

### `src/app/routes.py`
```python
from flask import Flask, render_template
from .controllers import cart_controller, orders_controller, products_controller

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/products')
def products():
    return products_controller.get_products()

@app.route('/cart')
def cart():
    return cart_controller.get_cart()

@app.route('/orders')
def orders():
    return orders_controller.get_orders()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
```

### `src/app/controllers/cart_controller.py`
```python
from flask import render_template

def get_cart():
    # カート情報を取得するロジック
    return render_template('cart_list.html', cart_items=[])
```

### `src/app/controllers/orders_controller.py`
```python
from flask import render_template

def get_orders():
    # 注文履歴を取得するロジック
    return render_template('order_history.html', orders=[])
```

### `src/app/controllers/products_controller.py`
```python
from flask import render_template

def get_products():
    # 商品情報を取得するロジック
    return render_template('product_list.html', products=[])
```

### `scripts/init_script.sh`
```bash
#!/bin/bash
cd /home/ec2-user
yum install -y python3
pip3 install Flask
pip3 install -r requirements.txt
python3 src/app/__init__.py
```

### `requirements.txt`
```
Flask
```

### `src/tests/test_cart.py`
```python
import unittest
from app.controllers import cart_controller

class TestCartController(unittest.TestCase):
    def test_get_cart(self):
        response = cart_controller.get_cart()
        self.assertIn('<html>', response)

if __name__ == '__main__':
    unittest.main()
```

### `src/tests/test_orders.py`
```python
import unittest
from app.controllers import orders_controller

class TestOrdersController(unittest.TestCase):
    def test_get_orders(self):
        response = orders_controller.get_orders()
        self.assertIn('<html>', response)

if __name__ == '__main__':
    unittest.main()
```

### `src/tests/test_products.py`
```python
import unittest
from app.controllers import products_controller

class TestProductsController(unittest.TestCase):
    def test_get_products(self):
        response = products_controller.get_products()
        self.assertIn('<html>', response)

if __name__ == '__main__':
    unittest.main()
```

---

この要件定義書は、オブジェクト指向の原則に従い、各機能をモジュール化し、テストフレームワークを用いて動作検証ができるように設計されています。