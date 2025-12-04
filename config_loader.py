import configparser
from flask import Flask


def load_config(app: Flask, conf_path: str):
    parser = configparser.ConfigParser()
    parser.read(conf_path, encoding='utf-8')

    mysql = parser['mysql']
    app.config.update(
        DB_HOST=mysql.get('host', '127.0.0.1'),
        DB_PORT=mysql.getint('port', 3306),
        DB_USER=mysql.get('user', 'vehicles'),
        DB_PASSWORD=mysql.get('password', '123'),
        DB_NAME=mysql.get('database', 'vehicles'),
    )
    return app
