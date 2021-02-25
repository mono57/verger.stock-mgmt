from django.db import models
from django.contrib.auth import get_user, get_user_model
from django.utils import timezone
from django.db.models.base import ModelState


User = get_user_model()


class Room(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Nom de la salle")

    class Meta:
        verbose_name = 'Salle'
        verbose_name_plural = 'Salles'

    def __str__(self):
        return self.name


class PartitionFormulla(models.Model):
    cooking_type = models.CharField(
        max_length=100,
        verbose_name='Type de préparation'
    )
    input = models.IntegerField(
        default=1, verbose_name="Quantité en kg ou litre")
    output = models.IntegerField(
        verbose_name='Nombre de portions ou consos pour 1 kg ou litre')

    class Meta:
        verbose_name = 'Formule de partition'
        verbose_name_plural = 'Formules de partition'

    def __str__(self):
        return self.cooking_type


class Product(models.Model):
    class ProductCategory(models.TextChoices):
        PORTIONABLE = "P", "Portionable"
        UNPORTIONABLE = "UP", "Non Portionable"

    name = models.CharField(
        max_length=150,
        verbose_name="Nom du produit")

    category = models.CharField(
        max_length=2,
        choices=ProductCategory.choices,
        default=ProductCategory.PORTIONABLE,
        verbose_name="Catergorie du produit")

    partition = models.ManyToManyField(
        PartitionFormulla,
        blank=True,
        verbose_name='Types de préparation qu\'on peut faire avec ce produit',
        help_text='Appuyez sur Shift pour selectionner plusieurs')

    @property
    def is_portionable(self):
        return self.ProductCategory.PORTIONABLE == self.category

    class Meta:
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits'

    def __str__(self):
        return self.name


class Portion(models.Model):
    store = models.IntegerField(default=0)
    store = models.IntegerField(default=0)
    partition = models.ForeignKey(
        PartitionFormulla, on_delete=models.DO_NOTHING)


class Dish(models.Model):
    name = models.CharField(
        max_length=250,
        verbose_name="Nom du plat")

    partition = models.ForeignKey(
        PartitionFormulla,
        null=True,
        on_delete=models.CASCADE,
        related_name='dishs',
        verbose_name='Formule de partition')

    class Meta:
        verbose_name = 'Plat'
        verbose_name_plural = 'Plats'

    def __str__(self):
        return self.name


class Price(models.Model):
    price = models.IntegerField()
    room = models.ForeignKey(
        Room, on_delete=models.DO_NOTHING, related_name='room_prices')
    dish = models.ForeignKey(
        Dish, on_delete=models.DO_NOTHING, related_name='dish_prices')

    class Meta:
        verbose_name = 'Prix'
        verbose_name_plural = 'Prix'

    def __str__(self):
        return str(self.price)


class Invoice(models.Model):
    paymaster = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='invoices',
        verbose_name='Caissier',)

    table_number = models.IntegerField(
        blank=True,
        verbose_name="Numéro de la table")

    total_price = models.IntegerField(verbose_name='Montant')

    date = models.DateField(
        default=timezone.now,
        verbose_name='Date de la facture')

    class Meta:
        verbose_name = 'Facture'
        verbose_name_plural = 'Factures'

    def __str__(self):
        return self.number

    @property
    def number(self):
        return "{:6d}".format(self.pk)


class InvoiceEntry(models.Model):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.DO_NOTHING,
        related_name='invoices')
    plat = models.ForeignKey(
        Dish,
        on_delete=models.DO_NOTHING,
        related_name='invoices_plat')

    quantity = models.IntegerField(verbose_name='Quantité achetée')
    price = models.IntegerField()


class Buying(models.Model):
    date = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = 'Achat'
        verbose_name_plural = 'Achats'


class BuyingEntry(models.Model):
    buying = models.ForeignKey(Buying, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
