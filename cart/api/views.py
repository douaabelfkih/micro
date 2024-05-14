# Dans le microservice Cart

# views.py
from django.http import HttpResponse
import requests
from django.contrib.auth.models import User
from .models import CartItem

def add_to_cart(request, product_id):
    # Obtenir les détails de l'utilisateur à partir du microservice d'authentification
    auth_service_url = 'http://127.0.0.1:8000/api/user-details/'  # Remplacer par l'URL réelle du microservice d'authentification
    auth_response = requests.get(auth_service_url, headers={'Authorization': f'Bearer {request.auth}'})
    
    if auth_response.status_code == 200:
        user_details = auth_response.json()
        username = user_details['username']
        user, _ = User.objects.get_or_create(username=username)
    else:
        return HttpResponse("Unauthorized", status=401)
    
    # Obtenir les détails du produit à partir du microservice de produits
    products_service_url = f'http://127.0.0.1:8001/product-details-page/{product_id}/'  # Remplacer par l'URL réelle du microservice de produits
    products_response = requests.get(products_service_url)
    
    if products_response.status_code == 200:
        product_details = products_response.json()
        product_name = product_details['name']
        product_stock = product_details['stock']
        
        # Enregistrer l'élément dans le panier
        cart_item = CartItem.objects.create(user=user, product_id=product_id, quantity=1)
        
        return HttpResponse("Product added to cart successfully")
    else:
        return HttpResponse("Product not found", status=404)
