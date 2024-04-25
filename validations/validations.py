import base64
import re
import os
from datetime import datetime
from flask import current_app


def is_empty(input_str):
    current_app.logger.info("valida  %s", str(input_str))
    if input_str is None:
        return True

    if isinstance(input_str, str):
        cleaned_str = input_str.strip()
        if not cleaned_str:
            return True

    return False


def formato_iso():
    return "YYYY-MM-DD HH:MM:SS.mmmmmm"


def obtener_password(passw, correo):
    return passw.strip() + base64.b64encode(
        correo.strip().split("@")[0].encode()
    ).decode("utf-8")


def es_correo_valido(correo):
    expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    validacion = re.match(expresion_regular, correo) is not None
    current_app.logger.info("valida email %s, es %s", str(correo), str(validacion))
    return validacion


def obtener_fecha_actual():
    return datetime.now()
