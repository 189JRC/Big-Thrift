from django.urls import path
from . import views
#app_name = "auctions"

urlpatterns = [

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("index", views.AllListings.as_view(), name="index"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),

    path("<int:listing_id>/comment", views.create_comment, name="create_comment"),
    path("comment/<int:comment_id>/update", views.update_comment, name="update_comment"),
    path('comment/<int:comment_id>/delete', views.delete_comment, name='delete_comment'),

    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/<int:listing_id>/add", views.add_to_watchlist, name="add_to_watchlist"),
    path("watchlist/<int:listing_id>/delete", views.remove_from_watchlist, name="remove_from_watchlist"),

    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category_by_type, name="category_by_type"),

    path("<int:listing_id>/make_bid", views.make_bid, name="make_bid"),
    path("<int:listing_id>/terminate", views.terminate, name="terminate"),

   ]


