from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.template import context
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import AuctionForm, BidForm, CommentForm
from .models import Category, User, Auction, Watchlist, Bids, Comment

def index(request):
    listings = Auction.objects.filter(is_active = True)
    return render(request, "auctions/index.html", {'listings': listings})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, 'Invalid username and/or password.')
            return render(request, "auctions/login.html")
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.error(request, 'Passwords must match.')
            return render(request, "auctions/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.error(request, 'Username already taken.')
            return render(request, "auctions/register.html")
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    if request.method == 'POST':
        createForm = AuctionForm(request.POST, request.FILES)
        if createForm.is_valid():
            create = createForm.save(commit=False)
            create.creator = request.user
            create.save()
            messages.success(request, "Listing successfully created" )
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, 'auctions/create-listing.html', {'createForm': createForm})
    else:
        createForm = AuctionForm()
        context = {'createForm': createForm, 'creator': request.user}  
        return render(request, 'auctions/create-listing.html', context)

def listing_detail(request, listing_id):
    try:
        listing = get_object_or_404(Auction, pk=listing_id)
    except Auction.DoesNotExist:
        messages.error(request, "This is not available") 
        return HttpResponseRedirect(reverse("index"))

    bid_form= BidForm()     

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.auction = listing
            new_comment.save()

            return redirect('listing_detail', listing_id=listing_id)

        else:
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    context = {'listing': listing,
                'bid_form': bid_form,
                'comment_form': comment_form
                } 

    return render(request, 'auctions/details.html', context)

@login_required
def make_bid(request, listing_id):
    listing = Auction.objects.get(pk=listing_id)
    bid_item = Bids.objects.filter(auction=listing).order_by('-new_bid').first()

    if request.method == 'POST':
        bid_form = BidForm(request.POST, listing=listing)
        if bid_form.is_valid():
            current_bid = bid_form.save(commit=False)
            current_bid.user = request.user
            current_bid.auction = listing
            current_bid.save()


            messages.success(request, 'Successfully added your bid')
            return redirect('listing_detail', listing_id=listing_id)


        else:
            context = {
                "bid_item": bid_item,
                "bid_form": bid_form,
                "listing": listing
                } 

        return render(request, 'auctions/details.html', context)
             
                
    return render(request, 'auctions/details.html', bid_form = BidForm())  

# ---------------------------------------------------------------------------------------------------------------------------

@login_required
def add_watchlist(request, listing_id):
    if request.method == 'POST':
        listing = Auction.objects.get(pk=listing_id)
        watched = Watchlist.objects.filter(user=request.user, item=listing)

        if watched.exists():
            watched.delete()
            messages.info(request, 'Successfully deleted from your watchlist')
            return redirect('index')
           
        else:
            watched, created = Watchlist.objects.get_or_create(user=request.user, item=listing)
            watched.save()
            messages.success(request, 'Successfully added to your watchlist')
            return redirect('watchlist') 

    return redirect('index')

@login_required
def watchlist(request):
    watchlist = Watchlist.objects.filter(user=request.user)
    return render(request, 'auctions/watchlist.html', {'watchlist': watchlist})  

# ---------------------------------------------------------    

def all_category(request):
    categories = Category.objects.all()

    category = request.GET.get('category')

    if category == None:
        products = Auction.objects.all().order_by('-created_at')
    else:
        products = Auction.objects.filter(is_active=True, category__name=category)

    context = {'categories':categories, 'products':products}
    return render(request, 'auctions/category.html', context)  

@login_required
def close_auction(request, listing_id):
    if request.method == 'POST' and Auction.objects.get(pk = listing_id).creator == request.user:
        Auction.objects.filter(pk=listing_id).update(is_active = False)
        messages.success(request, 'Auction successfully closed')
        return redirect('index')

