from django.db import models
from django.contrib.auth.models import User

class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Shop(models.Model):
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='produits')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    quantity_stock = models.PositiveIntegerField(default=0)
    quantity_minimale = models.PositiveIntegerField(default=12)
    description = models.TextField()
    image = models.ImageField(upload_to='produit_images/')

    def __str__(self):
        return self.name

class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"   
        

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Shop, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.price

    def str(self):
        return f'{self.quantity} x {self.product.name}'
    
class Order(models.Model):
        shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
        quantity = models.PositiveIntegerField()
        total_price = models.DecimalField(max_digits=10, decimal_places=2)
        customer_name = models.CharField(max_length=100)
        customer_phone = models.CharField(max_length=15)
        customer_address = models.TextField()
        payment_status = models.BooleanField(default=False)
        invoice_pdf = models.FileField(upload_to='invoices/', blank=True, null=True)
        user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)  # Facultatif

        def str(self):
            return f"Order #{self.id} - {self.product.name}"