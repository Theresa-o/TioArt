from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

class Auction(models.Model):
    title = models.CharField(max_length=25)
    description = models.TextField()
    starting_bid = models.IntegerField(null=False, blank=False)
    image_url = models.URLField(verbose_name="URL", max_length=255, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, max_length=12, null=True, blank=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def no_of_bids(self):
        return self.bidding.all().count()

    def last_bid(self):
        if self.no_of_bids() > 0:
            return self.bidding.aggregate(Max('new_bid'))['new_bid__max']
        else:
            return self.starting_bid

    def winner(self):
        if self.no_of_bids() > 0:
            return self.bidding.get(new_bid=self.last_bid()).user
        else:
            return None

    class Meta:
        ordering = ['-created_at']

class Bids(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bidding', null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='bidding')
    new_bid = models.IntegerField()
    done_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.new_bid)

    class Meta:
        ordering = ['auction', '-new_bid']

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Auction, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}'s watchlist"
    

class Comment(models.Model):
    auction = models.ForeignKey(Auction, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    description = models.TextField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return '%s, - %s' % {self.auction.title, self.name}

    class Meta:
        ordering = ['-created_at']
