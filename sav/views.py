from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
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


def contact_view(request):
    """
    Vue de contact qui utilise ReclamationForm pour envoyer un email.

    Contrairement à add_reclamation qui sauvegarde en base de données,
    cette vue utilise le même formulaire mais envoie uniquement un email.

    Ceci démontre la flexibilité des forms.Form qui peuvent être réutilisés
    pour différents usages sans être liés à la persistance en base de données.
    """
    if request.method == 'POST':
        form = ReclamationForm(request.POST)
        if form.is_valid():
            # Récupérer les données du formulaire
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Envoyer l'email
            send_mail(
                subject=f'Message de contact de {email}',
                message=message,
                from_email=email,
                recipient_list=['admin@example.com'],
                fail_silently=False,
            )

            # Ajouter un message de succès
            messages.success(request, 'Votre message a été envoyé avec succès!')
            return redirect('contact')
    else:
        form = ReclamationForm()

    return render(request, 'sav/contact.html', {'form': form})
