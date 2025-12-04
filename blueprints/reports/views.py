import json
import os
from typing import Any

from flask import (
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from blueprints.auth import current_user, login_required, permission_required
from models.db import DBContextManager

from . import reports_bp


ReportDefinition = dict[str, Any]


def _storage_path() -> str:
    return current_app.config.get(
        'REPORTS_CONFIG_PATH', os.path.join(current_app.root_path, 'config', 'reports.json')
    )


def _load_reports() -> list[ReportDefinition]:
    path = _storage_path()
    if not os.path.exists(path):
        return []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except (OSError, json.JSONDecodeError):
        pass
    return []


def _save_reports(reports: list[ReportDefinition]) -> None:
    path = _storage_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(reports, f, ensure_ascii=False, indent=2)


def _find_report(report_id: str) -> ReportDefinition | None:
    for item in _load_reports():
        if item.get('id') == report_id:
            return item
    return None


@reports_bp.before_request
def ensure_can_work_with_reports():
    user = current_user()
    if not user:
        return login_required(lambda: None)()
    perms = set(user.get('permissions', []))
    if not {'reports_view', 'reports_create'} & perms:
        flash('Недостаточно прав для раздела отчетов.', 'error')
        return redirect(url_for('menu'))


@reports_bp.route('/')
@login_required
def entrypoint():
    user = current_user() or {}
    perms = set(user.get('permissions', []))
    if 'reports_view' in perms:
        return redirect(url_for('reports.list_reports'))
    if 'reports_create' in perms:
        return redirect(url_for('reports.create_report'))
    flash('Недостаточно прав для раздела отчетов.', 'error')
    return redirect(url_for('menu'))


@reports_bp.route('/list')
@permission_required('reports_view')
def list_reports():
    reports = _load_reports()
    return render_template('reports/index.html', reports=reports)


@reports_bp.route('/view/<report_id>', methods=['GET', 'POST'])
@permission_required('reports_view')
def view_report(report_id: str):
    report = _find_report(report_id)
    if not report:
        flash('Отчет не найден.', 'error')
        return redirect(url_for('reports.list_reports'))

    parameters: list[dict[str, Any]] = report.get('params') or []
    provided = request.form if request.method == 'POST' else request.args
    params_values = {
        param['name']: (provided.get(param['name']) or param.get('default') or '')
        for param in parameters
    }

    should_execute = not parameters or request.method == 'POST' or any(provided.values())
    rows: list[dict[str, Any]] | None = None
    if should_execute:
        query = report.get('sql')
        if not query:
            flash('Для отчета не задан SQL-запрос.', 'error')
            return redirect(url_for('reports.list_reports'))
        try:
            with DBContextManager(current_app.config) as db:
                rows = db.select(query, params_values if parameters else None)
        except Exception as exc:  # pragma: no cover - defensive path
            current_app.logger.exception('Ошибка при выполнении отчета %s', report_id)
            flash(f'Не удалось выполнить отчет: {exc}', 'error')
            rows = None

    return render_template(
        'reports/view.html', report=report, params=parameters, values=params_values, rows=rows
    )


@reports_bp.route('/create', methods=['GET', 'POST'])
@permission_required('reports_create')
def create_report():
    if request.method == 'POST':
        report_id = (request.form.get('id') or '').strip()
        title = (request.form.get('title') or '').strip()
        description = (request.form.get('description') or '').strip()
        sql = (request.form.get('sql') or '').strip()
        raw_params = (request.form.get('params_json') or '').strip()

        if not report_id or not title or not sql:
            flash('Идентификатор, заголовок и SQL должны быть заполнены.', 'error')
            return render_template('reports/create.html', values=request.form)

        reports = _load_reports()
        if any(item.get('id') == report_id for item in reports):
            flash('Отчет с таким идентификатором уже существует.', 'error')
            return render_template('reports/create.html', values=request.form)

        params_list: list[dict[str, Any]] = []
        if raw_params:
            try:
                parsed = json.loads(raw_params)
                if isinstance(parsed, list):
                    params_list = [p for p in parsed if isinstance(p, dict) and 'name' in p]
                else:
                    raise ValueError
            except ValueError:
                flash('Параметры должны быть списком JSON.', 'error')
                return render_template('reports/create.html', values=request.form)

        reports.append(
            {
                'id': report_id,
                'title': title,
                'description': description,
                'sql': sql,
                'params': params_list,
            }
        )
        _save_reports(reports)
        flash('Отчет добавлен и готов к использованию.', 'success')
        return redirect(url_for('reports.view_report', report_id=report_id))

    return render_template('reports/create.html', values={})
