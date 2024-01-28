from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal
import random
from .forms import CoinFlipForm  
from mainpage.models import User
from django.utils import timezone
from mainpage.models import BetHistory


@login_required(login_url='login')
def coin_flip(request):
    user = User.objects.get(user=request.user)
    main_account = User.objects.get(username='admin')
    multiplier = Decimal(2)

    form = CoinFlipForm()
    if request.method == "POST":
        form = CoinFlipForm(request.POST)
        if form.is_valid():
            bet_amount = form.cleaned_data['bet_amount']
            bet_side = form.cleaned_data['bet_side']


            if user.money >= bet_amount:
                user.money -= bet_amount
                user.save()
                
                coin_result = random.choice(['Heads', 'Tails'])
                if coin_result == bet_side:
                    BetHistory.objects.create(
                        user=user,
                        game='Coin Flip',
                        bet_amount=bet_amount,
                        win_amount=bet_amount * multiplier,
                        timestamp=timezone.now(),
                    )
                    user.money += (bet_amount * multiplier)
                    user.save()

                    main_account.money -= (bet_amount * multiplier)
                    main_account.save()
                    messages.success(request, f'You won {round(bet_amount*multiplier,2)}€! {coin_result}')
                    
                else:
                    BetHistory.objects.create(
                        user=user,
                        game='Coin Flip',
                        bet_amount=bet_amount,
                        win_amount=Decimal(0),
                        timestamp=timezone.now(),
                    )
                    messages.error(request, f'You lose! {coin_result}')
                    main_account.money += bet_amount
                    main_account.save()
                    user.save()


            else:
                messages.error(request, "You don't have enough money")

    context = {
        'form': form
    }

    return render(request, 'coinflip/play_coin_flip.html', context)


