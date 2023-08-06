from notifications import views
from django.urls import path

from . import views


urlpatterns = [
    path("sync-users/", views.SyncUserAPI.as_view(), name="sync-users"),
    path("sync-users-bulk/", views.SyncUserBulkAPI.as_view(), name="sync-users-bulk"),
]
