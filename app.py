import os
from flask import Flask, render_template
from config_loader import load_config
from blueprints.query import query_bp


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

    app.register_blueprint(query_bp)

    @app.route('/')
    def menu():
        return render_template('menu.html')

    @app.route('/exit')
    def exit_page():
        return render_template('goodbye.html')

    return app


#_run_startup_sql()

app = create_app()
wsgi_app = app.wsgi_app

if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)
