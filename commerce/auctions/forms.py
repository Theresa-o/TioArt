from .models import Auction, Bids, Comment
from django import forms
from django.forms import fields
from django.core.exceptions import ValidationError

class AuctionForm(forms.ModelForm):
    
    class Meta:
        model = Auction
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'starting_bid': forms.NumberInput(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }

class BidForm(forms.ModelForm):

    class Meta:
        model = Bids
        fields = ['new_bid']
        labels = {
            'new_bid': ('Bid'),
        }

    def __init__(self, *args, **kwargs):
        self.listing = kwargs.pop('listing', None)
        super().__init__(*args, **kwargs)


    def clean_new_bid(self):
        new_bid = self.cleaned_data['new_bid']
        starting_bid = self.listing.starting_bid   

        if new_bid <= starting_bid:
            raise forms.ValidationError("New bid must be greater than the previous bid")
                
        return new_bid


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['name', 'description']
               
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
