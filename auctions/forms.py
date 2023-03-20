from django.forms import ModelForm, Textarea
from .models import Listing, Comment, Bid

class ListingForm(ModelForm):
    
    class Meta: 
        #specify which model the form is for and desired fields
        model = Listing
        fields = ['title', 'summary', 'category', 'image', 'initial_price']

class CommentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        #Use super to change inherited attributes > change widget for 'text' field to a Bootstrap class
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'form-control'})
    
    class Meta:
        model = Comment
        fields = ['text']
        labels = { 'text': ('Your Comment:')}
        widgets = { 'text': Textarea(attrs={'rows': 5, 'cols': 8}) }

class BidForm(ModelForm):

    class Meta:
        model = Bid 
        fields = ['amount']
        labels = { 'amount': ('Bid Amount: £')}
   