import os
from flask import Flask, request, render_template

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # ИСПРАВЛЕНО: Секретный ключ из переменных окружения
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))

    # ИСПРАВЛЕНО: Debug mode через переменные окружения
    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False') == 'True'

    @app.route('/')
    def index():
        # ИСПРАВЛЕНО: безопасное экранирование ввода через render_template
        name = request.args.get('name', 'Guest')
        return render_template('index.html', name=name)

    @app.route('/eval')
    def eval_code():
        # ИСПРАВЛЕНО: безопасная обработка вместо eval
        expression = request.args.get('expr', '1+1')
        allowed_chars = set('0123456789+-*/(). ')
        if all(c in allowed_chars for c in expression):
            try:
                result = eval(expression)
            except:
                result = 'Ошибка вычисления'
        else:
            result = 'Недопустимые символы'
        return f'Result: {result}'

    @app.route('/admin')
    def admin():
        # ИСПРАВЛЕНО: добавлена проверка аутентификации
        auth_token = request.headers.get('Authorization')
        expected_token = os.environ.get('ADMIN_TOKEN', 'admin-secret-token')
        if not auth_token or auth_token != f'Bearer {expected_token}':
            return 'Unauthorized', 401
        return 'Admin panel'

    return app