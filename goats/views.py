from django.shortcuts import render, redirect
from .models import Goat, GoatToUser
from .forms import GoatForm
import logging

logger = logging.getLogger(__name__)


def list_goats(request):

    logger.error(request.user)
    # goats = Goat.objects.filter(owner=request.user)
    # logger.error(goats)

    goats = GoatToUser.objects.filter(owner_id=request.user)
    goats_in_list = []
    for goat in goats:
        # if goat.owner_id == request.user.id:
        goats_in_list.append(goat.goat)

    # goats.delete()
    return render(request, 'goats.html', {'goats': goats_in_list})


def create_goat(request):
    form = GoatForm(request.POST or None)

    if form.is_valid():
        goat = form.save().id
        user = request.user.id
        gturelationship = GoatToUser(goat_id=goat, owner_id=user)
        gturelationship.save()

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


def update_goat_is_inside(request, id):
    goat = Goat.objects.get(id=id)

    if goat.is_inside:
        goat.is_inside = False
    else:
        goat.is_inside = True

    goat.save()
    return redirect('list_goats')
