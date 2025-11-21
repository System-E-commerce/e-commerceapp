from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Client(models.Model):
	utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)
	adresse = models.CharField(max_length=255, blank=True)
	telephone = models.CharField(max_length=50, blank=True)

	def __str__(self):
		return self.utilisateur.username


class Categorie(models.Model):
	nom = models.CharField(max_length=100)
	description = models.TextField(blank=True)

	def __str__(self):
		return self.nom


class Produit(models.Model):
	nom = models.CharField(max_length=200)
	prix = models.PositiveIntegerField()
	description = models.TextField(blank=True)
	stock = models.IntegerField(default=0)
	categorie = models.ForeignKey(Categorie, null=True, blank=True, on_delete=models.SET_NULL)
	image = models.CharField(max_length=255, blank=True)
	vendeur = models.ForeignKey('vendeur.Vendeur', on_delete=models.CASCADE)
	dateAjout = models.DateTimeField(default=timezone.now)
	STATUT_CHOICES = [("ACTIF", "Actif"), ("DESACTIVE", "Désactivé")]
	statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default="ACTIF")

	def __str__(self):
		return self.nom


class Panier(models.Model):
	client = models.ForeignKey(Client, on_delete=models.CASCADE)
	dateCreation = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f"Panier {self.id} - {self.client.utilisateur.username}"


class PanierProduit(models.Model):
	panier = models.ForeignKey(Panier, on_delete=models.CASCADE, related_name='items')
	produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
	quantite = models.PositiveIntegerField(default=1)

	class Meta:
		unique_together = (('panier', 'produit'),)

	def __str__(self):
		return f"{self.produit.nom} x{self.quantite}"


class Commande(models.Model):
	client = models.ForeignKey(Client, on_delete=models.CASCADE)
	vendeur = models.ForeignKey('vendeur.Vendeur', on_delete=models.CASCADE)
	dateCommande = models.DateTimeField(default=timezone.now)
	STATUT_CHOICES = [
		("EN_ATTENTE", "En attente"),
		("VALIDE", "Validée"),
		("ANNULEE", "Annulée"),
	]
	statut = models.CharField(max_length=12, choices=STATUT_CHOICES, default="EN_ATTENTE")

	def __str__(self):
		return f"Commande {self.id} - {self.client.utilisateur.username} -> {self.vendeur.utilisateur.username}"


class CommandeProduit(models.Model):
	commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='items')
	produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
	quantite = models.PositiveIntegerField()

	class Meta:
		unique_together = (('commande', 'produit'),)

	def __str__(self):
		return f"{self.produit.nom} x{self.quantite}"


class Paiement(models.Model):
	commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
	montant = models.PositiveIntegerField()
	MODE_CHOICES = [("mobile_money", "Mobile Money"), ("carte", "Carte"), ("paypal", "PayPal")]
	modePaiement = models.CharField(max_length=20, choices=MODE_CHOICES)
	STATUT_PAIEMENT = [("EN_ATTENTE", "En attente"), ("VALIDE", "Validé"), ("ECHLOUE", "Échoué")]
	statutPaiement = models.CharField(max_length=12, choices=STATUT_PAIEMENT, default="EN_ATTENTE")
	datePaiement = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f"Paiement {self.id} - {self.commande.id} - {self.montant}"

