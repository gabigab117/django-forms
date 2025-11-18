# Django Forms vs ModelForms

Ce projet Django illustre la différence entre **Form** et **ModelForm** à travers deux applications :

## Les deux approches

### 1. ModelForm (app `shop`)

**Fichier :** [shop/forms.py](shop/forms.py)

```python
class ProductForm(forms.ModelForm):
    # Champ custom qui n'existe PAS dans le modèle Product
    notify_on_low_stock = forms.BooleanField(
        required=False,
        label='Recevoir une notification si le stock est bas',
        help_text='Cochez cette case pour être notifié quand le stock passe sous 10 unités',
    )

    class Meta:
        model = Product
        fields = ['name', 'price', 'stock']

        # Personnalisation des labels
        labels = {
            'name': 'Nom du produit',
        }

        # Personnalisation des widgets avec CSS et attributs HTML
        widgets = {
            'name': forms.Textarea(attrs={
                'class': 'form-control product-input',
                'placeholder': 'e.g., Wireless Headphones',
                'style': 'border: 2px solid #4CAF50; padding: 8px; border-radius: 4px;',
            }),
        }

    def __init__(self, *args, **kwargs):
        """Personnalisation dynamique des champs"""
        super().__init__(*args, **kwargs)
        # Modification du label au moment de l'initialisation
        self.fields['price'].label = 'Prix (€)'
```

**Avantages :**
- Génération automatique des champs depuis le modèle
- Méthode `save()` intégrée pour créer/modifier les instances
- Validation automatique basée sur le modèle
- **Personnalisable** : ajout de champs custom, modification des widgets et labels
- Moins de code à écrire pour les cas standard

**Personnalisations démontrées :**
- **Champ additionnel** : `notify_on_low_stock` n'existe pas dans le modèle mais disponible dans le formulaire
- **Labels personnalisés** : via `Meta.labels` ou dans `__init__()` pour personnalisation dynamique
- **Widgets custom** : modification du rendu HTML avec classes CSS, placeholders et styles inline

**Utilisation typique :** Formulaires CRUD (Create, Read, Update, Delete) directement liés à un modèle de base de données, même avec personnalisations avancées.

### 2. Form (app `sav`)

**Fichier :** [sav/forms.py](sav/forms.py)

```python
class ReclamationForm(forms.Form):
    email = forms.EmailField(max_length=254, label="Votre email")
    message = forms.CharField(label="Votre réclamation", widget=forms.Textarea)

    def save(self):
        # Création manuelle de l'instance
        reclamation = Reclamation.objects.create(
            email=self.cleaned_data['email'],
            message=self.cleaned_data['message']
        )
        return reclamation
```

**Avantages :**
- Contrôle total sur les champs et leur validation
- Peut combiner plusieurs modèles ou ne pas être lié à un modèle
- Permet des traitements personnalisés avant sauvegarde
- Idéal pour les formulaires complexes (recherche, filtres, etc.)

**Utilisation typique :** Formulaires de contact, recherche, filtres, ou formulaires nécessitant une logique métier complexe.

### Exemple concret : Réutilisation du même formulaire

L'application `sav` démontre la **flexibilité des forms.Form** en réutilisant `ReclamationForm` pour deux usages différents :

1. **`/sav/add/`** ([views.py:7-16](sav/views.py#L7-L16)) : Sauvegarde en base de données
   ```python
   form.save()  # Crée une instance Reclamation en DB
   ```

2. **`/sav/contact/`** ([views.py:19-51](sav/views.py#L19-L51)) : Envoi d'email sans sauvegarde
   ```python
   # Même formulaire, usage différent
   email = form.cleaned_data['email']
   message = form.cleaned_data['message']
   send_mail(...)  # Envoie uniquement un email
   ```

Ce pattern illustre qu'un **forms.Form n'est pas lié à la persistance** - vous décidez quoi faire avec les données validées.

## Démarrage rapide

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Appliquer les migrations
python manage.py migrate

# Lancer le serveur
python manage.py runserver
```

**URLs disponibles :**
- Ajouter un produit (ModelForm) : `http://localhost:8000/shop/add/`
- Ajouter une réclamation (Form avec save) : `http://localhost:8000/sav/add/`
- Contact (Form avec email) : `http://localhost:8000/sav/contact/`
- Interface admin : `http://localhost:8000/admin/`

## Conclusion

**Choisissez ModelForm** quand votre formulaire correspond exactement à un modèle et que vous voulez créer/modifier des instances.

**Choisissez Form** quand vous avez besoin de flexibilité, de logique personnalisée, ou que votre formulaire ne correspond pas directement à un modèle unique.
