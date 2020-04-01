from django.shortcuts import render, redirect
from .models import Goat
from .forms import GoatForm

def list_goats(request):
    goats = Goat.objects.all()
    return render(request, 'goats.html', {'goats': goats})

def create_goat(request):
    form = GoatForm(request.POST or None)

    if form.is_valid():
        form.save()
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
