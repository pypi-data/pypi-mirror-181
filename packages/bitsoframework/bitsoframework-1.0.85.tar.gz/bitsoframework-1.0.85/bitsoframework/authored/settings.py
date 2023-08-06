from django.conf import settings

from bitsoframework.utils.reflection import require

AUTH_USER_MODEL = settings.AUTH_USER_MODEL
ON_DELETE = require(f"django.db.models.{getattr(settings, 'BITSO_AUTHORED_ON_DELETE', 'CASCADE')}")
