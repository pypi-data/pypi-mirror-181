import logging

from django.utils.translation import gettext as _
from django.views.generic import View
from django.http import JsonResponse

from requests import HTTPError, ConnectionError, Timeout
from .keycloak import create_user

logger = logging.getLogger(__name__)


class SyncUserAPI(View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")

        if not email:
            return JsonResponse({"message": _("Email is required")}, status=400)

        try:
            create_user(email=email)
        except (HTTPError, ConnectionError, Timeout):
            logger.exception("Error creating the user %s", email)
            return JsonResponse({"message": _("Error creating the user")}, status=500)

        return JsonResponse({"message": _("User synced successfully"),}, status=200)


class SyncUserBulkAPI(View):
    def post(self, request, *args, **kwargs):
        emails = request.POST.get("emails")

        if not emails:
            return JsonResponse({"message": _("Emails are required")}, status=400)

        for email in emails:
            try:
                create_user(email=email)
            except (HTTPError, ConnectionError, Timeout):
                logger.exception("Error creating the user %s", email)
                return JsonResponse({"message": _("Error creating the user")}, status=500)

        return JsonResponse({"message": _("Users synced successfully"),}, status=200)
