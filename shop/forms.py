from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    # Champ checkbox custom qui n'existe PAS dans le modèle Product
    # Ce champ sera disponible dans le formulaire mais ne sera pas sauvegardé automatiquement
    # Pour utiliser cette valeur, on pourrait surcharger la méthode save() et accéder à
    # self.cleaned_data.get('notify_on_low_stock') pour logger, envoyer un email, etc.
    notify_on_low_stock = forms.BooleanField(
        required=False,  # Non obligatoire (checkbox peut rester non cochée)
        label='Recevoir une notification si le stock est bas',
        help_text='Cochez cette case pour être notifié quand le stock passe sous 10 unités',
        # On pourrait imagine un widget personnalisé ici aussi, donc soit dans Meta ou directement ici
        # widget=...
    )

    class Meta:
        model = Product
        fields = ['name', 'price', 'stock']

        # Exemple: personnalisation du label dans Meta
        labels = {
            'name': 'Nom du produit',
        }

        # Widget personnalisé pour 'name' avec CSS inline et attributs HTML
        widgets = {
            # TextArea n'est pas super approprié pour un CharField, mais utilisé ici pour l'exemple
            'name': forms.Textarea(attrs={
                'class': 'form-control product-input',  # Imaginons avoir ces classes CSS
                'placeholder': 'e.g., Wireless Headphones',  # Placeholder
                'style': 'border: 2px solid #4CAF50; padding: 8px; border-radius: 4px;',  # CSS inline
            }),
        }

    def __init__(self, *args, **kwargs):
        """Exemple: personnalisation du label dans __init__ (approche dynamique)"""
        super().__init__(*args, **kwargs)
        # Modifier le label de 'price' au moment de l'initialisation du formulaire
        self.fields['price'].label = 'Prix (€)'
