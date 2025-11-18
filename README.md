# Django Forms vs ModelForms

Ce projet Django illustre la différence entre **Form** et **ModelForm** à travers deux applications :

## Les deux approches

### 1. ModelForm (app `shop`)

**Fichier :** [shop/forms.py](shop/forms.py)

```python
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'stock']
```

**Avantages :**
- Génération automatique des champs depuis le modèle
- Méthode `save()` intégrée pour créer/modifier les instances
- Validation automatique basée sur le modèle
- Moins de code à écrire

**Utilisation typique :** Formulaires CRUD (Create, Read, Update, Delete) directement liés à un modèle de base de données.

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
