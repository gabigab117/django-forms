from django.shortcuts import render, redirect
from .forms import ReclamationForm


def add_reclamation(request):
    if request.method == 'POST':
        form = ReclamationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_reclamation')
    else:
        form = ReclamationForm()

    return render(request, 'sav/add_reclamation.html', {'form': form})
