import logging
from django.apps import apps
from django.utils.module_loading import import_string


class DatabaseErrorHandler(logging.Handler):
    def emit(self, record):
        ErrorLog = apps.get_model('error_logs', 'ErrorLog')
        
        ErrorLog.objects.create(
            error_type=record.levelname,
            created_at=record.asctime,
            module=record.module,
            pathname=record.pathname,
            lineno=record.lineno,
            funcName=record.funcName,
            error_message=record.getMessage()
        )