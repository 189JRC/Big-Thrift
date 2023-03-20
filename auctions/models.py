from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):

    def __str__(self):
        return f"{self.username}"

class Category(models.Model):
    """Model representing categories for listings"""
    category = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.category}"
    
    class Meta:
        ordering = ("category",)

class Listing(models.Model):
    """Model representing an item listing"""

    title = models.CharField(max_length=200)
    user = models.ForeignKey(User,  null=True, blank=True, on_delete=models.CASCADE)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of this item.")
    image = models.URLField(max_length=1000, help_text="Enter a URL for the picture of this item.")
    initial_price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    time_up = models.DateTimeField(auto_now=False, auto_now_add=True)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category, on_delete= models.SET_DEFAULT, help_text="Please select a category", default="Other")


    class Meta:
        ordering = ("-time_up",)
    
    def __str__(self):
        if self.active == True:
            status = "Active"
        else:
            status = "Inactive"
        
        return f"{self.title}: {self.id}, listed by: {self.user}. Listing is {status}" 

    def snippet(self):
        return f"{self.summary[:50]}..."

    def terminate(self):

        return self.active == False 

class Winner(models.Model):
    """Model representing the winner of an item listing"""

    owner = models.CharField(max_length=50)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    listing = models.OneToOneField(Listing, on_delete=models.CASCADE)
    highest_bid = models.IntegerField()

    def __str__(self):
        return f"{self.winner}"
        
        
           
class Bid(models.Model):
    """Model representing the highest bid for an item listing"""
    
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    time_up = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        ordering = ("-time_up", )
        
    def __str__(self):
        return f"Bid of {self.amount} made by {self.user} at {self.time_up}"

class Comment(models.Model):
    """Model to create comment objects connecting Users and Listings"""

    text = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    #1 User can have many comment objects
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    #1 Listing can have many comment objects
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE)

    def __str__(self):
        return self.text
    

class Watchlist(models.Model):
    """Model to create watchlist object for users"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} is watching {self.listing}"


