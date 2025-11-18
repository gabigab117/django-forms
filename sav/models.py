from django.db import models


class Reclamation(models.Model):
    """
    Modèle pour gérer les réclamations clients.
    """
    email = models.EmailField(max_length=254, verbose_name="Email du client")
    message = models.TextField(verbose_name="Message de réclamation")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    class Meta:
        verbose_name = "Réclamation"
        verbose_name_plural = "Réclamations"
        ordering = ['-date_created']

    def __str__(self):
        return f"Réclamation de {self.email} - {self.date_created.strftime('%d/%m/%Y')}"
