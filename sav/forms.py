from django import forms
from .models import Reclamation


class ReclamationForm(forms.Form):
    """
    Formulaire personnalisé (forms.Form) pour les réclamations.

    Contrairement au ModelForm utilisé dans l'app 'shop', ce formulaire:
    - Hérite de forms.Form (pas de forms.ModelForm)
    - Nécessite de définir manuellement tous les champs
    - Doit implémenter sa propre méthode save() pour créer l'instance
    - Nous ne sommes pas obligés de créer des instances
    - On pourrait juste récupérer des données et les envoyer par email par exemple

    Cet exemple illustre la différence entre forms.Form et forms.ModelForm.
    """
    email = forms.EmailField(
        max_length=254,
        label="Votre email"
    )
    message = forms.CharField(
        label="Votre réclamation",
        widget=forms.Textarea
    )

    def clean_message(self):
        """
        Validation personnalisée pour le champ message.
        """
        message = self.cleaned_data.get('message')
        if message and len(message) < 10:
            raise forms.ValidationError(
                "Le message doit contenir au moins 10 caractères."
            )
        return message

    def save(self):
        """
        Méthode personnalisée pour sauvegarder une réclamation.

        Contrairement au ModelForm qui a une méthode save() automatique,
        avec forms.Form nous devons créer manuellement l'instance du modèle.

        Returns:
            Reclamation: L'instance de réclamation créée
        """
        # Récupérer les données nettoyées du formulaire
        email = self.cleaned_data['email']
        message = self.cleaned_data['message']

        # Créer et sauvegarder manuellement l'instance
        reclamation = Reclamation.objects.create(
            email=email,
            message=message
        )
        # On pourrait même s'amuser à créer des instances de plusieurs modèles ici si besoin

        return reclamation
