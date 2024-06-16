from apps.mailer.views import mailing_admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = [
    path("", include("apps.core.urls")),
    path("", include("apps.booking.urls")),
    path("tickets/", include("apps.tickets.urls")),
    path("payments/", include("apps.payments.urls")),
    # path("amo/", include("apps.amo.urls")),
    path("mailer/", include("apps.mailer.urls")),
    path("api/mailing-admin/", mailing_admin, name="mailing-admin"),
    path("api/mailing-admin/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("users/", include("apps.accounts.urls")),
]
