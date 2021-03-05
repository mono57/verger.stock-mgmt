import math
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db.models.base import ModelState
from django_extensions.db.models import TimeStampedModel

User = get_user_model()


class Room(TimeStampedModel):
    name = models.CharField(
        max_length=150,
        verbose_name="Nom de la salle")

    class Meta:
        verbose_name = 'Salle'
        verbose_name_plural = 'Salles'

    def __str__(self):
        return self.name


class PartitionFormulla(TimeStampedModel):
    cooking_type = models.CharField(
        max_length=100,
        verbose_name='Type de préparation'
    )
    portions_name = models.CharField(
        max_length=50, verbose_name='Nom de portion', default='')
    input = models.IntegerField(
        default=1, verbose_name="Quantité en kg ou litre")
    output = models.IntegerField(
        verbose_name='Nombre de portions ou consos pour 1 kg ou litre')

    class Meta:
        verbose_name = 'Formule de partition'
        verbose_name_plural = 'Formules de partition'

    def __str__(self):
        return self.cooking_type + '(' + str(self.input) + 'Kg/L -> ' + str(self.output) + ' Portion(s))'

    def compute_stock_quantity(self, buying_qty):
        stock_quantity = buying_qty * (self.output / float(self.input))
        decimal_part = int(str(stock_quantity-int(stock_quantity))[2:3])

        # print("Stock qtté: ", stock_quantity, type(stock_quantity))
        # print("Decimal part: ", decimal_part, type(decimal_part))

        if decimal_part <= 5:
            stock_quantity = math.floor(stock_quantity)
        else:
            stock_quantity = math.ceil(stock_quantity)
        # print("Stock qtté: ", stock_quantity, type(stock_quantity))
        return int(stock_quantity)


class ProductType(TimeStampedModel):
    name = models.CharField(
        max_length=250,
        verbose_name="Type de produit")

    def __str__(self) -> str:
        return self.name


class Product(TimeStampedModel):
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
        verbose_name="Categorie du produit")

    partition = models.ManyToManyField(
        PartitionFormulla,
        blank=True,
        verbose_name='Type de préparation qu\'on peut faire avec ce produit',
        help_text='Appuyez sur Shift pour selectionner plusieurs')

    product_type = models.ForeignKey(
        ProductType,
        blank=True,
        on_delete=models.DO_NOTHING,
        null=True,
        verbose_name="Type de produit"
    )

    @property
    def is_portionable(self):
        return self.ProductCategory.PORTIONABLE == self.category

    class Meta:
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits'

    def __str__(self):
        return self.name


class Portion(TimeStampedModel):
    stock_store = models.IntegerField(default=0)
    store = models.IntegerField(default=0)
    partition = models.OneToOneField(
        PartitionFormulla,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name='portion')

    def __str__(self):
        return 'Portion pour {}'.format(self.partition.portions_name)


class PriceManager(models.Manager):
    def get_price_by_room(self, room):
        qs = self.get_queryset()
        return qs.filter(room=room).first()


class Price(TimeStampedModel):
    price = models.IntegerField()
    room = models.ForeignKey(
        Room, on_delete=models.DO_NOTHING, related_name='room_prices')
    content_type = models.ForeignKey(
        ContentType, null=True, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    # dish = models.ForeignKey(
    #     Dish, on_delete=models.DO_NOTHING, related_name='dish_prices')

    objects = PriceManager()

    class Meta:
        verbose_name = 'Prix'
        verbose_name_plural = 'Prix'

    def __str__(self):
        return str(self.price)


class Dish(TimeStampedModel):
    name = models.CharField(
        max_length=250,
        verbose_name="Nom du plat")

    partition = models.ForeignKey(
        PartitionFormulla,
        null=True,
        on_delete=models.CASCADE,
        related_name='dishs',
        verbose_name='Formule de partition')
    prices = GenericRelation(Price)

    class Meta:
        verbose_name = 'Plat'
        verbose_name_plural = 'Plats'

    def __str__(self):
        return self.name

    def get_price_by_room(self, room):
        qs = Price.objects.filter()


class Drink(TimeStampedModel):
    name = models.CharField(max_length=100, verbose_name='Nom de la boisson')
    prices = GenericRelation(Price)

    class Meta:
        verbose_name = 'Boisson'
        verbose_name_plural = 'Boissons'

    def __str__(self):
        return self.name


class Invoice(TimeStampedModel):
    paymaster = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='invoices',
        verbose_name='Caissier',)

    table_number = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Numéro de la table")

    room = models.ForeignKey(
        Room, null=True, on_delete=models.CASCADE, verbose_name='Salle')

    total_price = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Montant')

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
        return "{:06d}".format(self.pk)


class InvoiceEntry(TimeStampedModel):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.DO_NOTHING,
        related_name='invoices')

    content_type = models.ForeignKey(
        ContentType,
        null=True,
        on_delete=models.CASCADE)
    content_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'content_id')
    quantity = models.IntegerField(verbose_name='Quantité achetée')
    price = models.IntegerField()


class Buying(TimeStampedModel):
    date = models.DateField(default=timezone.now, blank=True)
    total_amount = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Montant total de l\'achat')

    def format_total_amount(self):
        return str(self.total_amount) + ' F CFA' if self.total_amount else None

    class Meta:
        verbose_name = 'Achat'
        verbose_name_plural = 'Achats'


class BuyingEntry(TimeStampedModel):
    buying = models.ForeignKey(
        Buying, on_delete=models.DO_NOTHING, related_name='entries')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(
        verbose_name='Prix d\'achat', blank=True, null=True)
    quantity = models.IntegerField(verbose_name='Quantité achetée')
    partition = models.ForeignKey(
        PartitionFormulla,
        help_text='Choisir la formule de partition a appliquée sur ce cette quantité',
        blank=True,
        null=True,
        on_delete=models.CASCADE)


class Transfert(TimeStampedModel):
    portion = models.ForeignKey(Portion, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=0)
