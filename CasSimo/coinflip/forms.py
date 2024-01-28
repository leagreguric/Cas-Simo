from django import forms


class CoinFlipForm(forms.Form):
    bet_amount = forms.DecimalField(
        initial=1, min_value=1, max_value=10000, decimal_places=2,
        widget=forms.NumberInput(attrs={"class": "form-control", "style": "text-align:center", "step": 0.5})
    )

    CHOICES = [('Heads', 'Heads'), ('Tails', 'Tails')]
    bet_side = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect(attrs={"class": "coin-radio"}),
        initial='Heads',  # Set the initial value if needed
    )