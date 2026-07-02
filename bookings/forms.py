from django import forms
from .models import Booking
from events.models import FoodItem

class BookingForm(forms.ModelForm):
    food_items = forms.ModelMultipleChoiceField(
        queryset=FoodItem.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Booking
        fields = ['food_items']

class BookingEditForm(forms.ModelForm):
    food_items = forms.ModelMultipleChoiceField(
        queryset=FoodItem.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Booking
        fields = ['status', 'food_items']

class PaymentForm(forms.Form):
    card_number = forms.CharField(max_length=16, min_length=16, widget=forms.TextInput(attrs={'placeholder': '1234567812345678'}))
    expiry_date = forms.CharField(max_length=5, widget=forms.TextInput(attrs={'placeholder': 'MM/YY'}))
    cvv = forms.CharField(max_length=3, min_length=3, widget=forms.TextInput(attrs={'placeholder': '123'}))
