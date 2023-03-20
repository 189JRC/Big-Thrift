from django.contrib import admin
from .models import Listing, User, Comment, Watchlist, Bid, Category, Winner


admin.site.register(Listing)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Watchlist)
admin.site.register(Bid)
admin.site.register(Category)
admin.site.register(Winner)