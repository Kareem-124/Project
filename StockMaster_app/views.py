from django.shortcuts import render, redirect
from django.shortcuts import reverse
from .models import *
from .models import Prodcut
from django.contrib import messages
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
import json
import math



# This function renders the homepage
def homepage(request):
    return render(request, 'homepage.html')

# This function displays all the info about a specific USER on a page with the corresponding ID
def profile(request):
    user = check_session(request)
    context = {
        'user': user,
    }
    return render(request, 'users-profile.html', context)
# This function edit the profile info
def edit(request):
    errors = User.objects.editValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/dashboard/profile')
    else:
        selected = User.objects.get(id=request.session['user'])
        selected.f_name = request.POST['f_name']
        selected.l_name = request.POST['l_name']
        selected.s_name = request.POST['s_name']
        selected.email = request.POST['email']
        selected.save()
        return redirect('/dashboard/profile')
#This function renders the page that displays all products in the database
def prodcuts(request):
    products = Prodcut.objects.all()
    context = {
        'products' : products
    }
    return render(request, 'products-page.html', context)

################## Registration and Loging ################
#This function renders the sign up page upon button click
def signup_page(request):
    return render(request, 'pages-register2.html')

#This function for registration process
def register(request):
    errors = User.objects.regValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/signup')
    else:
        User.objects.create(
        f_name= request.POST['f_name'], 
        l_name= request.POST['l_name'], 
        s_name= request.POST['s_name'], 
        email=request.POST['email'], 
        password=request.POST['password'])
        return render(request, 'pages-login-2.html')

#This function renders the Log In page upon button click
def signin_page(request):
    return render(request, 'pages-login-2.html')

#This function for loging process
def login(request):
    errors = User.objects.loginValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return render(request, 'pages-login-2.html')
    else:
        user = User.objects.get(email = request.POST['email'])
        request.session['user'] = user.id
        request.session['username'] = user.f_name
        print('user')
        return redirect('/dashboard')
    
# ------------------ KAREEM SECTION START ---------------------------
#Page : Order Page
def order_page(request):
    user = check_session(request)
    context = {
        'user' : user
    }
    return render(request,'orders_page.html',context)

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

#Process: Order list
def order_list_process(request):

    try:
        if is_ajax(request = request) and request.method == "POST":
            # Check if the barcode is exist
            user = check_session(request)
            product = Prodcut.objects.filter(p_barcode=request.POST['barcode'], user = user).first()
            order_list_products = Order_list.objects.all()
            total_order_list = 0
            if order_list_products:
                for item in order_list_products:
                    total_order_list += item.qty_sell

            total_available = products_objects_total_qty(product.p_name,user)
            print(total_available - total_order_list)
            order_list_qty = request.POST['product_qty'] 
            if (total_available-total_order_list) < int(order_list_qty):
                return JsonResponse({'message': 'qty_Exceeded'})
            order_list_price = request.POST['product_price'] 
            barcode = product.p_barcode

            Order_list.objects.create(p_price=order_list_price,
                                    qty_sell=order_list_qty,
                                    products=product.p_name,
                                    p_barcode = barcode)
            return JsonResponse({'message': 'Success'})
    except:
        return JsonResponse({'message': 'Invalid request '})


def get_order_list(request):
    order_list = Order_list.objects.all().values('id','p_price', 'qty_sell', 'products', 'p_barcode')
    return JsonResponse({"order_list":list(order_list)})

# Process: Delete
def remove_order_list(request,order_id):
    order_list = Order_list.objects.get(id=order_id)
    order_list.delete()
    return JsonResponse({'message': 'Success'})

# ------------------ KAREEM SECTION START ---------------------------


#This function renders the "add new product" form
def add_product(request):
    return render(request, 'add_product.html')

#This function handles POST data from "add new product" form and adds new PRODUCT to db:
def save_product(request):
    if request.method == 'POST':
        params = dict()
        
        params['p_name'] = request.POST.get('p_name')
        params['total_weight'] = request.POST.get('total_weight')
        params['expire_date'] = request.POST.get('expire_date')
        params['weight'] = request.POST.get('weight')
        params['qty'] = request.POST.get('qty')
        print(params['weight'])
        
        Prodcut.objects.create(**params)

    return redirect(reverse('products-page'))

#------------------------`````````Update 2 KAREEM -----------------------
# Process: process_order
def process_order(request):
    # Get the objects from the order_list
    order_list = Order_list.objects.all()
    # Add the objects in the order_list to the order Table*
    user = User.objects.get(id=request.session['user'])
    for order in order_list:
        Order.objects.create(p_price = order.p_price, qty_sell = order.qty_sell, products = order.products ,total_weight = order.total_weight, user = user)
        filtered_products = Prodcut.objects.filter(user = user , p_name = order.products )

        # total_qty = products_objects_total_qty(filtered_products)
        sell_qty = order.qty_sell

        for item in filtered_products:
            if sell_qty > item.qty:
                sell_qty -= item.qty
                item.qty = 0
                item.save()
            else:
                item.qty -= sell_qty
                sell_qty = 0
                item.save()
            print(f'{item.user} / {item.p_name} / object: {item}')
    # Delete the order_list items
    order_list_delete_all()
    return redirect('/order_page')


# Function: Delete all the records at the order_list table
def order_list_delete_all():
    Order_list.objects.all().delete()
    return

# Process: Clear order_list Items
def clear_all_order_list_process(request):
    order_list_delete_all()
    return redirect('/order_page')

# Process: Logout
def logout_process(request):
    request.session.flush()
    return redirect('/')

# Function : Check Session
def check_session(request):
    if request.session.has_key('user') == True:
        user_session = User.objects.get(id=request.session['user'])
    else:
        user_session = False
    return user_session

#--------------------------------- Kareem Update 3:-------------------------------
# Process : Delete Product from the DB
def remove_product_process(request,product_id):
    product = Prodcut.objects.get(id=product_id)
    product.delete()
    return redirect('/dashboard')

# Page: Display Orders Page
def display_orders_page(request):
    user = check_session(request)
    if user:
        orders=Order.objects.filter(user=user)
    context = {
        'orders' : orders,
        'user' : user,
    }
    return render(request,'display_orders_page.html',context)

#--------------------------------- Kareem Update 4:-------------------------------
def  products_total_qty(products):

    product_qty_dictionary = {}
    filtered_list = []
    # Iterate through the products list
    for item in products:
        # Check the 'product_qty_dictionary' dictionary if it contains that product so dose not iterate again because we already have its value
        # If this product name dose not exists bring all the products with that name
        if (str(item.p_name) in product_qty_dictionary) == False:
            total = 0
            # get all the products that have the same name as this product
            filtered_products = Prodcut.objects.filter(p_name = item.p_name)
            # Iterate through all products and get the total qty
            for product in filtered_products:
                total += product.qty
            # Add a new attribute to the product object called total_qty : value = total
            setattr(item,'total_qty',total)
            # Add this product name to 'product_qty_dictionary' dictionary and its value so next time if the same product came we don't
            # repeat this process
            product_qty_dictionary[f"{item.p_name}"] = total
            # Add the product object with the new attribute to 'filtered_list'
            filtered_list.append(item)
        # if the product already exists in dictionary get its value from the dictionary
        else:
            setattr(item,'total_qty',product_qty_dictionary[item.p_name])
            filtered_list.append(item)
    # Return the filtered list of products objects containing total_qty
    return filtered_list

#--------------------------------------- Kareem Update V5-------------------------------
def  products_objects_total_qty(product_name,user):
    total = 0
    products = Prodcut.objects.filter(p_name = product_name , user = user)
    for item in products:
        total += item.qty
    return total



# ********************* THIS IS THE CALCULATION PART ***************** #
# This function displays the dashboard to the user with calculations functions:
def dashboard(request):
    current_date = timezone.now().date()
    user = check_session(request)
    if user:
        products = Prodcut.objects.filter(user=user)  # Fetch all products for the logged-in user
    context = {
        'products': products,
    }
    return render(request, 'dashboard.html', context)

# ********************* HAMADA SECTION ****************************
# This function displays the name of the user in the profile section
def display_products(request):
     
    product = Prodcut.objects.all()
    if product:
        weight = product.weight
        total_weight = product.total_weight
        quantity = total_weight / weight 
        result_floor = math.floor(quantity)
        print(weight)
        
       
        context = {
            'user': request.user, 
        }
        
        return render(request, 'display_products-page.html', context)
    else:
        # Handle the case where no product exists
        return render(request, 'display_products-page.html', {'error': 'No product found'})
    
def update_quantity(request, product_id):
    product = get_object_or_404(Prodcut, pk=product_id)
    quantity = product.total_weight - product.weight
    product.qty -= qty
    product.save()
    return JsonResponse({'quantity': quantity})

# product list (ajex) 

def product_list_process(request):
    try:
        if is_ajax(request=request) and request.method == "POST":
            # Check if the barcode is exist
            user = check_session(request)
            
            # Corrected typo in model name
            product = Prodcut.objects.filter(p_name=request.POST['p_name'], user=user).first()
            product_list_products = Product_list.objects.all()
            total_product_list = 0
            if product_list_products:
                for item in product_list_products:
                    total_product_list += item.qty
            
            # Validation: if the qty is less than 0 
            # total_available = products_objects_total_qty(Product.p_name, user)
            # product_list_qty = request.POST['product_qty'] 
            # if (total_available - total_product_list) < int(product_list_qty):
            #     return JsonResponse({'message': 'qty_Exceeded'})
            
            product_name = request.POST['p_name'] 
            product_total_weight = request.POST['total_weight'] 
            product_weight = request.POST['weight'] 
            product_qty = request.POST['product_qty'] 
            product_date = timezone.now() 

            # Corrected field names in create method
            Product_list.objects.create(p_name=product_name,
                                        total_weight=product_total_weight,
                                        weight=product_weight,
                                        qty=product_qty,  # Corrected field name
                                        date=product_date,
                                        products="kareem")
            return JsonResponse({'message': 'Success'})
    except Exception as e:
        print(e)  # Print exception for debugging
        return JsonResponse({'message': 'Invalid request'})

# to remove the prodcut from the list 
def remove_product_list(request,product_id):
    prodcut_list = Product_list.objects.get(id=product_id)
    print(prodcut_list)
    Product_list.delete()
    return JsonResponse({'message': 'Success'})
    
# To get add product to the list 
def get_product_list(request):
    prodcut_list = Product_list.objects.all().values('id','p_name', 'total_weight', 'weight', 'total_weight', 'qty', 'date')
    return JsonResponse({"prodcut_list":list(prodcut_list)}) 

def  products_objects_total_qty(product_name,user):
    total = 0
    products = Prodcut.objects.filter(p_name = product_name , user = user)
    for item in products:
        total += item.qty
    return total

# This function displays all products that exist in the db:
def all_product(request):
    user = check_session(request)
    if user:
        products = Prodcut.objects.filter(user=user) 
    context = {
        'products' : products,
        'user' : user, 
    }
    return render(request, 'all_product.html', context)

# This function searches products in the db using their barcodes:
def search(request):
    search = request.POST['search']
    products = Prodcut.objects.all() #array 
    product_list = []
    for x in products: 
        if search == x.p_name: 
            product_list.append(x)
    print(product_list)
    context = {
        'prod_search' : product_list, 
    }
    return render(request, 'all_product.html', context) 


def remove_product_list(request, product_id):
    product_list = Product_list.objects.get(id=product_id)
    
    product_list.delete()
    return JsonResponse({'message': 'Success'})



