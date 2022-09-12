from django.contrib import admin
from .models import Auction, Watchlist, Bids, Comment, Category

# Register your models here.
admin.site.register(Auction)
admin.site.register(Watchlist)
admin.site.register(Bids)
admin.site.register(Comment)
admin.site.register(Category)