from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/", views.create_listing, name="create_listing"),
    path("detail/<int:listing_id>/", views.listing_detail, name="listing_detail"),
    path("make_bid/<int:listing_id>", views.make_bid, name="make_bid"),
    path("add_watchlist/<int:listing_id>/", views.add_watchlist, name="add_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category", views.all_category, name="all_category"),
    path("close_auction/<int:listing_id>/", views.close_auction, name="close_auction"),
    path('__debug__/', include('debug_toolbar.urls')),
    ]


# if settings.DEBUG:
#         urlpatterns += static(settings.MEDIA_URL,
#                               document_root=settings.MEDIA_ROOT)

