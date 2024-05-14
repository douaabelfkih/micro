from rest_framework import serializers
from .models import Cart

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'  # Vous pouvez personnaliser les champs à inclure dans la sérialisation
