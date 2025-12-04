import os
from flask import Flask, render_template, redirect, url_for, session
from config_loader import load_config
from blueprints.query import query_bp
from blueprints.reports import reports_bp
from blueprints.auth import auth_bp, login_required, permission_required, current_user


def _run_startup_sql():
    import re
    import pymysql

    conf_path = os.path.join('config', 'app.conf')
    sql_path = os.path.join('initdb', 'newdb.sql')
    if not os.path.exists(sql_path):
        return
    kv = {}
    try:
        with open(conf_path, 'r', encoding='utf-8') as f:
            for line in f:
                s = line.strip()
                if not s or s.startswith('#') or s.startswith('[') or '=' not in s:
                    continue
                k, v = s.split('=', 1)
                kv[k.strip()] = v.strip()
    except FileNotFoundError:
        pass

    host = kv.get('DB_HOST') or kv.get('host') or '127.0.0.1'
    port = int(kv.get('DB_PORT') or kv.get('port') or 3306)
    user = kv.get('DB_ADMIN_USER') or kv.get('user') or 'root'
    password = kv.get('DB_ADMIN_PASSWORD') or kv.get('password') or ''

    with open(sql_path, 'r', encoding='utf-8') as f:
        sql_text = f.read()

    if 'DELIMITER' in sql_text.upper():
        raise RuntimeError('newdb.sql содержит DELIMITER — такой файл этой мини-функцией не выполняется')

    sql_text = re.sub(r'/\*.*?\*/', '', sql_text, flags=re.S)  # /* ... */
    lines = []
    for line in sql_text.splitlines():
        line = line.split('--')[0].strip()                     # -- ...
        if line:
            lines.append(line)
    cleaned = '\n'.join(lines)
    statements = [s.strip() for s in cleaned.split(';') if s.strip()]

    conn = pymysql.connect(
        host=host, port=port, user=user, password=password,
        autocommit=True, charset='utf8mb4'
    )
    try:
        with conn.cursor() as cur:
            for s in statements:
                cur.execute(s)
    finally:
        conn.close()


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

    load_config(app, os.path.join('config', 'app.conf'))
    app.config.setdefault('REPORTS_CONFIG_PATH', os.path.join(app.root_path, 'config', 'reports.json'))

    app.register_blueprint(auth_bp)
    app.register_blueprint(query_bp)
    app.register_blueprint(reports_bp)

    MENU_ITEMS = [
        {
            'title': 'Параметризованные запросы',
            'subtitle': 'Готовые выборки и поисковые формы',
            'endpoint': 'query.index',
            'icon': '🚗',
            'permissions': ['queries']
        },
        {
            'title': 'Отчёты',
            'subtitle': 'Сводные показатели компании',
            'endpoint': 'reports.entrypoint',
            'icon': '📊',
            'permissions': ['reports_view', 'reports_create']
        },
        {
            'title': 'Администрирование',
            'subtitle': 'Пользователи и роли',
            'endpoint': 'admin',
            'icon': '🛠️',
            'permissions': ['admin']
        },
        {
            'title': 'Выход',
            'subtitle': 'Завершить смену',
            'endpoint': 'auth.logout',
            'icon': '🏁',
            'permissions': []
        },
    ]

    @app.route('/')
    @login_required
    def menu():
        user = current_user()
        permissions = set(user.get('permissions', [])) if user else set()
        items = [
            {
                'title': item['title'],
                'subtitle': item.get('subtitle'),
                'icon': item.get('icon'),
                'url': url_for(item['endpoint'])
            }
            for item in MENU_ITEMS
            if not item.get('permissions') or permissions.intersection(item['permissions'])
        ]
        return render_template('menu.html', menu_items=items)

    @app.route('/admin')
    @permission_required('admin')
    def admin():
        return render_template('admin.html')

    @app.route('/exit')
    def exit_page():
        session.clear()
        return redirect(url_for('auth.login'))

    return app


# _run_startup_sql()

app = create_app()
wsgi_app = app.wsgi_app

if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)
