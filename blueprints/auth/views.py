from flask import flash, redirect, render_template, request, session, url_for

from . import auth_bp

USERS: dict[str, dict[str, object]] = {
    'dispatcher': {'password': 'disp123', 'role': 'диспетчер', 'permissions': ['queries']},
    'manager': {
        'password': 'boss123',
        'role': 'начальник',
        'permissions': ['queries', 'reports_view'],
    },
    'admin': {
        'password': 'admin123',
        'role': 'администратор',
        'permissions': ['queries', 'reports_view', 'reports_create', 'admin'],
    },
}


def _find_user(login: str):
    normalized = login.lower()
    for username, data in USERS.items():
        if username.lower() == normalized:
            return username, data
    return None, None


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_value = (request.form.get('login') or '').strip()
        password_value = request.form.get('password') or ''

        if not login_value or not password_value:
            flash('Введите логин и пароль.', 'error')
            return render_template('auth/login.html', login_value=login_value)

        username, data = _find_user(login_value)
        if not data:
            flash('Пользователь с таким логином не найден.', 'error')
            return render_template('auth/login.html', login_value=login_value)
        if password_value != data['password']:
            flash('Неверный пароль. Попробуйте снова.', 'error')
            return render_template('auth/login.html', login_value=login_value)

        session['user'] = {
            'login': username,
            'role': data['role'],
            'permissions': data['permissions'],
        }
        flash('Успешная авторизация.', 'success')
        next_url = request.args.get('next') or url_for('menu')
        return redirect(next_url)

    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('auth.login'))
