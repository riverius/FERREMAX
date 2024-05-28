from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from .models import Usuario
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import LoginForm, RegisterForm, UserProfileForm
from django.http import JsonResponse
from django.contrib.auth.models import User
import requests, sys, os
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q, Count, Value
from django.db.models.functions import Concat
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import random

def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')

def contacto(request):
    return render(request, 'contacto.html')

def footer(request):
    return render(request, 'footer.html')

def catalogo(request):
    return render(request, 'catalogo.html')

def login_view(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')
        if not identifier or not password:
            return JsonResponse({'valid': False, 'error_message': 'Por favor, complete todos los campos.'})
        user = User.objects.filter(Q(email=identifier) | Q(username=identifier)).first()
        if user is not None:
            if user.check_password(password):
                login(request, user)
                return JsonResponse({'valid': True, 'success_message': 'Inicio de sesión exitoso.'})
            else:
                return JsonResponse({'valid': False, 'error_message': 'Contraseña no válida.'})
        else:
            return JsonResponse({'valid': False, 'error_message': 'Correo electrónico o usuario no válido.'})

    return JsonResponse({'valid': False, 'error_message': 'Método de solicitud no válido.'})

def logout_view(request):
    logout(request)
    return redirect('home')

#Transbank
from transbank.error.transbank_error import TransbankError
from transbank.error.transaction_commit_error import TransactionCommitError
from transbank.webpay.webpay_plus.transaction import Transaction
import random
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_http_methods(["POST"])
def webpay_plus_create(request):
    print("Webpay Plus Transaction.create")
    buy_order = str(random.randrange(1000000, 99999999))
    session_id = str(random.randrange(1000000, 99999999))
    amount = request.POST.get('amount')
    element_type = request.POST.get('element_type')
    return_url = request.build_absolute_uri(reverse('webpay-plus-commit'))

    create_request = {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": amount,
        "return_url": return_url
    }

    response = (Transaction()).create(buy_order, session_id, amount, return_url)

    print(response)

    return render(request, 'webpay/plus/create.html', {
        'request': create_request,
        'response': response,
        'amount': amount,
        'element_type': element_type
    })

@csrf_exempt
@require_http_methods(["GET"])
def webpay_plus_commit(request):
    token = request.GET.get('token_ws') or request.GET.get('TBK_TOKEN')
    print("commit for token: {}".format(token))
    try:
        response = (Transaction()).commit(token=token)
        print("response: {}".format(response))
    except TransactionCommitError as e:
        print("Error al confirmar la transacción: {}".format(e))
        return render(request, 'webpay/plus/error.html', {'message': str(e)})

    return render(request, 'webpay/plus/commit.html', {'token': token, 'response': response})

def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'valid': False, 'error_message': 'El nombre de usuario ya está en uso.'})

        if User.objects.filter(email=email).exists():
            return JsonResponse({'valid': False, 'error_message': 'El correo electrónico ya está registrado.'})

        if password != confirm_password:
            return JsonResponse({'valid': False, 'error_message': 'Las contraseñas no coinciden.'})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        login(request, user)

        return JsonResponse({'valid': True, 'success_message': 'Registro exitoso. Inicie sesión para continuar.'})

    return JsonResponse({'valid': False, 'error_message': 'Método de solicitud no válido.'})
