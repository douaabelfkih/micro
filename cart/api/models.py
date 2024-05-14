from django.db import models
from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Ajoutez d'autres champs au besoin

    def __str__(self):
        return f"Cart for user {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product_id = models.IntegerField()  # Suppose que vous stockez juste l'ID du produit
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x Product {self.product_id} in cart {self.cart.id}"
