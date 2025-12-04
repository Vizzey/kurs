from functools import wraps
from typing import Callable, Iterable
from flask import flash, redirect, request, session, url_for

UserDict = dict[str, str | list[str]]


def current_user() -> UserDict | None:
    return session.get('user')


def _redirect_to_login():
    return redirect(url_for('auth.login', next=request.path))


def login_required(view: Callable):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not current_user():
            flash('Требуется авторизация.', 'warning')
            return _redirect_to_login()
        return view(*args, **kwargs)

    return wrapper


def permission_required(permission: str):
    def decorator(view: Callable):
        @wraps(view)
        def wrapper(*args, **kwargs):
            user = current_user()
            if not user:
                flash('Требуется авторизация.', 'warning')
                return _redirect_to_login()
            permissions: Iterable[str] = user.get('permissions', [])  # type: ignore[assignment]
            if permission not in permissions:
                flash('Недостаточно прав для выбранного действия.', 'error')
                return redirect(url_for('menu'))
            return view(*args, **kwargs)

        return wrapper

    return decorator
