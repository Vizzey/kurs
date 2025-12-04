# blueprints/query/views.py
from flask import render_template, request, current_app, flash, redirect, url_for

from . import query_bp, provider
from models.db import DBContextManager
from blueprints.auth import permission_required


@query_bp.before_request
def ensure_authorized():
    # Перевод неавторизованных пользователей на страницу входа
    check = permission_required('queries')(lambda: None)
    return check()


@query_bp.route('/')
@permission_required('queries')
def index():
    return render_template('query_form.html')


@query_bp.route('/all')
@permission_required('queries')
def list_all_products():
    sql = provider.get('products')
    with DBContextManager(current_app.config) as db:
        rows = db.select(sql)
    return render_template('query_results.html',
                          items=rows,
                          criteria={'name': 'Все', 'min': '-', 'max': '-'})


@query_bp.route('/run', methods=['POST'])
@permission_required('queries')
def run_query():
    name = (request.form.get('name') or '').strip()
    min_price = (request.form.get('min_price') or '').strip()
    max_price = (request.form.get('max_price') or '').strip()
    try:
        min_v = float(min_price) if min_price else 0.0
        max_v = float(max_price) if max_price else 10**9
        if min_v < 0 or max_v < 0 or min_v > max_v:
            raise ValueError('Неверно задан диапазон цен.')
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(url_for('query.index'))

    sql = provider.get('search_products')
    params = {'name': f"%{name}%" if name else None,
              'min_price': min_v, 'max_price': max_v}
    with DBContextManager(current_app.config) as db:
        rows = db.select(sql, params)
    return render_template('query_results.html',
                           items=rows,
                           criteria={'name': name, 'min': min_v, 'max': max_v})


@query_bp.route('/simple/1')
@permission_required('queries')
def simple_1():
    sql = provider.get('simple_1_hired_march2020')
    with DBContextManager(current_app.config) as db:
        rows = db.select(sql)
    return render_template('query_results.html', items=rows, criteria={'q': 'сотрудники март 2020'})


@query_bp.route('/simple/2')
@permission_required('queries')
def simple_2():
    sql = provider.get('simple_2_hired_last10')
    with DBContextManager(current_app.config) as db:
        rows = db.select(sql)
    return render_template('query_results.html', items=rows, criteria={'q': 'приняты за 10 дней'})


@query_bp.route('/simple/3')
@permission_required('queries')
def simple_3():
    series = (request.args.get('series') or 'HT').strip()
    sql = provider.get('simple_3_plates_by_series')
    with DBContextManager(current_app.config) as db:
        rows = db.select(sql, {'series': series})
    return render_template('query_results.html', items=rows, criteria={'series': series})


@query_bp.route('/simple/4')
@permission_required('queries')
def simple_4():
    sql = provider.get('simple_4_ttn_count_march2020')
    with DBContextManager(current_app.config) as db:
        rows = db.select(sql)
    return render_template('query_results.html', items=rows, criteria={'q': 'TTN март 2020'})


@query_bp.route('/simple/5')
@permission_required('queries')
def simple_5():
    sql = provider.get('simple_5_total_weight_2020')
    with DBContextManager(current_app.config) as db:
        rows = db.select(sql)
    return render_template('query_results.html', items=rows, criteria={'q': 'вес по клиентам 2020'})


@query_bp.route('/simple/6')
@permission_required('queries')
def simple_6():
    sql = provider.get('simple_6_youngest_birthdate')
    with DBContextManager(current_app.config) as db:
        rows = db.select(sql)
    return render_template('query_results.html', items=rows, criteria={'q': 'самый молодой'})


@query_bp.route('/hard/1')
@permission_required('queries')
def hard_1():
    sql = provider.get('hard_1_report_ttn')
    with DBContextManager(current_app.config) as db:
        rows = db.select(sql)
    return render_template('query_results.html', items=rows, criteria={'q': 'отчёт ТТН'})


@query_bp.route('/hard/2')
@permission_required('queries')
def hard_2():
    contract = (request.args.get('contract') or 'C-1001').strip()
    sql = provider.get('hard_2_staff_for_client_contract_march2020')
    with DBContextManager(current_app.config) as db:
        rows = db.select(sql, {'contract': contract})
    return render_template('query_results.html', items=rows, criteria={'contract': contract})


@query_bp.route('/hard/3')
@permission_required('queries')
def hard_3():
    sql = provider.get('hard_3_max_weight_client_march2020')
    with DBContextManager(current_app.config) as db:
        rows = db.select(sql)
    return render_template('query_results.html', items=rows, criteria={'q': 'клиент макс вес март 2020'})


@query_bp.route('/hard/4')
@permission_required('queries')
def hard_4():
    sql = provider.get('hard_4_staff_never_issued')
    with DBContextManager(current_app.config) as db:
        rows = db.select(sql)
    return render_template('query_results.html', items=rows, criteria={'q': 'не оформляли ТТН'})


@query_bp.route('/hard/5')
@permission_required('queries')
def hard_5():
    sql = provider.get('hard_5_staff_not_march2020')
    with DBContextManager(current_app.config) as db:
        rows = db.select(sql)
    return render_template('query_results.html', items=rows, criteria={'q': 'не оформляли в марте 2020'})


@query_bp.route('/hard/6')
@permission_required('queries')
def hard_6():
    sql = provider.get('hard_6_view_most_frequent_2020')
    with DBContextManager(current_app.config) as db:
        parts = sql.split(';')
        rows = []
        for part in parts:
            stmt = part.strip()
            if not stmt:
                continue
            if stmt.upper().startswith('SELECT'):
                rows = db.select(stmt)
            else:
                db.execute(stmt)
    return render_template('query_results.html', items=rows, criteria={'q': 'клиент чаще всех 2020'})
