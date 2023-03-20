from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.views import generic

from .models import User, Listing, Comment, Watchlist, Category, Bid, Winner
from .forms import ListingForm, CommentForm, BidForm

##My own first attempt to work with a class based view
######################################################

class AllListings(generic.ListView):
    """Generic class-based view listing all listings from all users"""
    model = Listing
    template_name = "auctions/index.html"
    redirect_field_name = 'index'

##Views to display site content
###############################

def listing(request, listing_id):
    """ View for an individual listing, displayed on its own unique page
        according to its primary key. Rendered context and conditionals in 
        auctions/listing.html will dictate the state-specific messages 
        presented to the user."""

    chosen_listing = get_object_or_404(Listing, pk=listing_id)
    comments = Comment.objects.filter(listing=chosen_listing)
    user = request.user
    context = {"listing": chosen_listing, "user":user, "comments":comments,}

    try:
        #Page visited and user has watchlist
        watchlist = Watchlist.objects.filter(user=user, listing=chosen_listing)  
        context ["watchlist"] = watchlist
        
    except:
        pass
    
    try:
        #Page visited and a bid already exists
        bid = Bid.objects.get(listing=chosen_listing)
        bidder = bid.user
        context["bidder"] = bidder 

    except:
        pass
    
    try:
        #Listing is inactive and there is a winner
        winner1 = Winner.objects.get(listing=chosen_listing)
        #Name of the winner passed into context
        winners_name = winner1.winner
        context['message'] = winners_name 
        context['winner'] = winner1
    except:
        pass

    return render(request, "auctions/listing.html", context)

def categories(request):
    """View to display categories list."""

    categories = Category.objects.all()
    return render(request, "auctions/categories.html", { "categories": categories })

def category_by_type(request,category):
    """View to display Listings according to each category"""

    category_name = get_object_or_404(Category, category=category)
    listings = Listing.objects.filter(category=category_name)
    context = { "category": category_name, "listings": listings }
    return render(request, "auctions/category_listing.html", context)

##Views to allow user to change listing data
############################################

@login_required
def make_bid(request, listing_id):
    """View to allow authenticated user to bid on an item"""
    
    listing = get_object_or_404(Listing, pk=listing_id)
    user = request.user
    bid_form = BidForm(request.POST)

    #if the pages is requested, form provided
    if request.method == 'GET':
        context = { "bid_form": bid_form, "listing": listing, 
        "user": user }
        return render(request, "auctions/make_bid.html", context)
    
    #otherwise user is already on page and submits form
    if bid_form.is_valid():
        new_bid = bid_form.cleaned_data["amount"]
        current_price = listing.initial_price
            
        if new_bid > current_price:
            #new bid object is created
            bid_form.save(commit=False)
            listing.initial_price = new_bid
            listing.save()
            previous_bid = Bid.objects.filter(listing=listing)

            if previous_bid:
            #replaces previous bid if there is one.
                previous_bid.delete()

            #Bid object is created to relate the relevant User, Bid and Listing objects
            highest_bid = Bid()
            highest_bid.user = user
            highest_bid.listing = listing
            highest_bid.amount = new_bid 
            highest_bid.save() 

            return redirect('listing', listing_id)
        
        else:
            context = { "bid_form": bid_form, "listing": listing, 
            "user": user, "error": "Please ensure your new bid is higher than the current one."}
            return render(request, "auctions/make_bid.html", context)

def terminate(request, listing_id):
    
    """View to allow the owner of a listing to end the listing
    (make it inactive). Outcome 1; listing is terminated with bids,
    created winner object is saved to database. Outcome 2; 
    listing terminated, without bids and no winner object saved."""

    winner = Winner()
    chosen_listing = Listing.objects.get(pk=listing_id)
    user = request.user
    request.user == chosen_listing.user
    chosen_listing.active = False
    chosen_listing.save()
    context = { "listing": chosen_listing, "user": user,}

    try:    
        #listing terminated with bids
            highest_bid = Bid.objects.get(listing=chosen_listing)  
            context["bidder"] = highest_bid.user  
            winner.owner = request.user
            winner.winner = highest_bid.user
            winner.listing = chosen_listing 
            winner.highest_bid = highest_bid.amount
            winner.save()
            new_winner = Winner.objects.get(listing=chosen_listing)
            winners_name = new_winner.winner
            context['message'] = winners_name 
            context['winner'] = new_winner
            
            return render(request, "auctions/listing.html", context)

    except:
        #listing terminated without bids
            return render(request, "auctions/listing.html", context)


@login_required
def new_listing(request):

    """View to allow authenticated user to make listings.
    2 outcomes depend on whether 'POST' request has been
    made or not."""

    if request.method == 'POST':
        listing_form = ListingForm(request.POST)

        if listing_form.is_valid():
            new_item = listing_form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            messages.success(request, ("Your listing was successfully added."))
            return HttpResponseRedirect(reverse("index"))

    listing_form = ListingForm(request.POST)
    context = {"form": listing_form}
    return render(request, "auctions/new_listing.html", context)

##Comment related views
#########################

@login_required
def create_comment(request, listing_id):

    "View to allow authenticate user to comment on a Listing"

    listing = get_object_or_404(Listing, pk=listing_id)

    #On first visit to page, pass comment form and listing
    if request.method == 'GET':
        context = { 'form': CommentForm(), 'listing': listing }
        return render(request, 'auctions/create_comment.html', context)
    
    #On submission of form with POST request, Create new comment object
    else:
        try:
            form = CommentForm(request.POST)
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.listing = listing  
            new_comment.save()
            return redirect('listing', new_comment.listing.id)

        except ValueError:

            context = { 'form':CommentForm(), 'error':'Error: please review form or contact administrator.'}
            return render(request, 'auctions/create_comment.html', context)

@login_required
def update_comment(request, comment_id): 

    """View to allow authenticated user to update their own comments. 
    Will remain open after listing is made inactive
    and new comments are disabled in 'auctions/listing.html'."""

    comment = get_object_or_404(Comment,id=comment_id, user=request.user)

    #Render first template of page with prefilled CommentForm on request
    if request.method == 'GET':
        form = CommentForm(instance=comment)
        context = {"comment": comment, "form": form}
        return render(request, 'auctions/update_comment.html', context)

    else:
    #User is already on page and trying to submit form with POST request.
        try:
            #Retrieve values from form and save to update existing comment.
            form = CommentForm(request.POST, instance=comment)
            form.save() 
            return redirect('listing', comment.listing.id)
            
            #Issues with form data will be captured by except statement.
        except ValueError:
            context = { "comment": comment, "form":form, "error":"Error: issue with form data"}
            return render(request, "auctions/update_comment.html", context)

@login_required
def delete_comment(request, comment_id):
    """View to allow user to delete their own comments.
    Will remain open after listing is made inactive
    and new comments are disabled in 'auctions/listing.html'."""

    comment = get_object_or_404(Comment, pk=comment_id, user=request.user)
    comment.delete()
    return redirect('listing', comment.listing.id)


##Watchlist related views
#########################

@login_required
def watchlist(request):

    """View to allow a user to see their own watchlist page"""

    user = request.user
    watchlist = Watchlist.objects.filter(user=user)
    context = { "watchlist": watchlist, "user": user }
    return render(request, "auctions/watchlist.html", context)

@login_required 
def add_to_watchlist(request, listing_id):

    """View to allow a user to add items to their own watchlist"""

    user = request.user 
    listing = Listing.objects.filter(id=listing_id).first()
    #watchlist = Watchlist.objects.filter(user=user).first()
    Watchlist.objects.create(user=user, listing=listing)
    #watchlist.save()
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))

@login_required 
def remove_from_watchlist(request, listing_id):

    """View to allow a user to remove items from their own watchlist"""
    
    user = request.user 
    listings = Listing.objects.filter(id=listing_id).first()
    watch = Watchlist.objects.filter(user = user, listing=listings).first()
    watch.delete()
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))

##User Authentication
#####################

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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

@login_required
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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")