from django.shortcuts import render, redirect
from .models import Goat
from .forms import GoatForm
import logging

logger = logging.getLogger(__name__)

def list_goats(request):

    logger.error(request.user)
    goats = Goat.objects.filter(owner = request.user)
    logger.error(goats)

    # goats = Goat.objects.all()
    # goats.delete()
    return render(request, 'goats.html', {'goats': goats})

def create_goat(request):
    form = GoatForm(request.POST or None)

    if form.is_valid():
        form.save()
        Goat.objects.all().order_by('id')[0].set_owner(request.user)

        return redirect('list_goats')

    return render(request, 'goats-form.html', {'form': form})

def update_goat(request, id):
    goat = Goat.objects.get(id=id)
    form = GoatForm(request.POST or None, instance=goat)

    if form.is_valid():
        form.save()
        return redirect('list_goats')

    return render(request, 'goats-form.html', {'form': form, 'goat': goat})

def delete_goat(request, id):
    goat = Goat.objects.get(id=id)

    if request.method == 'POST':
        goat.delete()
        return redirect('list_goats')

    return render(request, 'goat-delete-confirm.html', {'goat': goat})

# Create your views here.
