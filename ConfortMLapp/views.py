from django.shortcuts import render, redirect
from .forms import ContactForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import  Shop, Categorie
from .forms import UserLoginForm, UserRegisterForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import  Cart, CartItem, Order
from .forms import UserLoginForm, UserRegisterForm
from django.http import HttpResponseRedirect
import os
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.core.files import File
from io import BytesIO
from django.contrib.staticfiles import finders
from django.core.files.base import ContentFile



def index(request):
    return render(request, 'index.html')

def shop(request):
    return render(request, 'shop.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def blog_view(request):
    return render(request, 'blog.html')

def login_view(request):
    return render(request, 'login.html')

def condition(request):
    return render(request, 'condition.html')

def create_login_view(request):
    return render(request, 'create_login.html')

def politique(request):
    return render(request, 'politique.html')

def thankyou_view(request):
    return render(request, 'thankyou.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact')  # Rediriger pour éviter de soumettre à nouveau le formulaire si la page est actualisée

    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form, 'success': 'POST' in request.method and form.is_valid()})

def shop(request):
    categories = Categorie.objects.all()
    return render(request, 'shop.html', {'categories': categories})

def shop_categorie(request, category_id):
    category = get_object_or_404(Categorie, id=category_id)
    products = Shop.objects.filter(categorie=category)
    return render(request, 'shop_categorie.html', {'category': category, 'products': products})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return render(request, 'registration/login.html', {'form': form, 'error_message': "Vous n'avez pas de compte, Veuillez vous inscrire !"})

            user = authenticate(username=user.username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return render(request, 'registration/login.html', {'form': form, 'error_message': "La combinaison e-mail/mot de passe est incorrecte."})

    else:
        form = UserLoginForm()

    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Shop, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    # Récupérer l'URL précédente pour rediriger l'utilisateur
    referer = request.META.get('HTTP_REFERER', 'shop')  # 'shop' est l'URL de fallback si le referer est absent
    return HttpResponseRedirect(referer)
@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def increase_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')

@login_required
def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('view_cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('view_cart')


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()
    total_price = sum(item.total_price() for item in cart_items)

    if request.method == 'POST':
        customer_phone = request.POST.get('customer_phone')
        customer_address = request.POST.get('customer_address')

        # Generate a unique invoice number
        last_order = Order.objects.order_by('-id').first()
        if last_order:
            next_order_number = last_order.id + 1
        else:
            next_order_number = 1

        # Initialiser le document PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(letter), rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
        elements = []

        # Chemin du logo
        logo_path = finders.find('images/cm.png')

        # Ajouter le logo et le titre avec numéro de facture
        if logo_path:
            logo = Image(logo_path)
            logo.drawHeight = 150
            logo.drawWidth = 150
            elements.append(logo)
            elements.append(Spacer(1, 12))  # Ajouter un espace après le logo

        styles = getSampleStyleSheet()

        # Titre de la facture avec numéro de facture
        title = Paragraph(f"Facture de commande N°{next_order_number}", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 24))  # Ajouter un espace après le titre

        # Tableau des produits
        data = [
            ["Client", "Téléphone", "Adresse", "Produit", "Quantité", "Prix Total"]
        ]

        for item in cart_items:
            data.append([
                request.user.username,
                customer_phone,
                customer_address,
                item.product.name,
                item.quantity,
                f"{item.total_price()} FCFA"
            ])

        # Calculer la somme des prix totaux
        total_amount = sum(item.total_price() for item in cart_items)

        # Ajouter la ligne de total à la fin du tableau
        data.append(["", "", "", "", "Total", f"{total_amount} FCFA"])

        # Style du tableau
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#007BFF')),  # Couleur de fond pour l'en-tête (bleu)
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Couleur du texte pour l'en-tête
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alignement du texte au centre
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alignement vertical au centre
            ('GRID', (0, 0), (-1, -1), 1, colors.white),  # Bordures du tableau
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Police en gras pour l'en-tête
            ('FONTSIZE', (0, 0), (-1, 0), 14),  # Taille de police pour l'en-tête
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Police normale pour le contenu
            ('FONTSIZE', (0, 1), (-1, -1), 12),  # Taille de police pour le contenu
            ('BOX', (0, 0), (-1, -1), 2, colors.white),  # Bordure extérieure
            ('INNERGRID', (0, 0), (-1, -1), 1, colors.white),  # Bordure intérieure
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),  # Couleurs alternées des lignes
            ('TOPPADDING', (0, 0), (-1, 0), 12),  # Padding en haut pour l'en-tête
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding en bas pour l'en-tête
            ('TOPPADDING', (0, 1), (-1, -1), 10),  # Padding en haut pour le contenu
            ('BOTTOMPADDING', (0, 1), (-1, -1), 10),  # Padding en bas pour le contenu
            ('LEFTPADDING', (0, 0), (-1, -1), 8),  # Padding à gauche
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),  # Padding à droite
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.white),  # Ligne en dessous de l'en-tête
            ('LINEABOVE', (0, -1), (-1, -1), 2, colors.white),  # Ligne au-dessus de la dernière ligne
            ('TEXTCOLOR', (-1, -1), (-1, -1), colors.HexColor('#007BFF')),  # Couleur bleue pour le total
        ])

        # Création du tableau avec largeurs de colonnes définies
        col_widths = [120, 120, 150, 200, 80, 100]   # Réduites par rapport à l'exemple précédent
        table = Table(data, colWidths=col_widths)
        table.setStyle(style)

        # Ajout du tableau aux éléments
        elements.append(table)

        # Ajouter un espace entre le tableau et le pied de page
        elements.append(Spacer(1, 180))  # Ajustez la valeur selon votre besoin

        # Pied de page
        footer_data = [
            ["", "Confort Mali, Merci pour votre achat !"],
            ["", "Téléphone : +223 74-61-12-35 | Adresse : Titibougou, Mali | Email : confortmali@gmail.com"]
        ]

        footer_table = Table(footer_data, colWidths=[10, 10])
        footer_table.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5)
        ]))
        elements.append(footer_table)

        # Construction du PDF
        doc.build(elements)

        # Enregistrer le PDF dans chaque commande et vider le panier
        for item in cart_items:
            order = Order.objects.create(
                shop=item.product,
                quantity=item.quantity,
                total_price=item.total_price(),
                customer_name=request.user.username,
                customer_phone=customer_phone,
                customer_address=customer_address,
                payment_status=False,
                user=request.user
            )
            buffer.seek(0)
            order.invoice_pdf.save(f'facture_{order.id}.pdf', File(buffer), save=True)

        cart.items.all().delete()  # Vider le panier après validation
        return redirect('order_confirmation_authenticated')

    return render(request, 'checkout_authenticated.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

@login_required
def order_confirmation_authenticated(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    return render(request, 'order_confirmation_authenticated.html', {'orders': orders})