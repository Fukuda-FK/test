# src/app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Flaskアプリケーションの初期化
app = Flask(__name__)

# 設定
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
    'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# データベースの初期化
db = SQLAlchemy(app)

# ルートのインポート（循環インポートを避けるため、ここで行う）
from app import routes, models

# アプリケーションの実行
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
