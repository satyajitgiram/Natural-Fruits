from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from .models import FruitFarmingOption
from django.contrib.sites.shortcuts import get_current_site
from fruit_trading import settings
from django.views.decorators.csrf import csrf_exempt
from account.forms import CustomUserCreationForm
from .forms import UserProfileForm, UserProfilePhotoForm


# Create your views here.
def home (request):
    fruit_options = FruitFarmingOption.objects.all()
    return render(request, "index.html",  {'fruit_options': fruit_options})

def profile(request):
    return render(request, "profile.html")

def pricing(request):
    fruit_options = FruitFarmingOption.objects.all()
    return render(request, "pricing.html",  {'fruit_options': fruit_options})

@login_required
def dashboard(request):
    user = request.user
    profile_image_form = UserProfilePhotoForm(instance=user)
    transactions = Order.objects.filter(user=user).order_by('-datetime_of_payment')

    return render(request, "dashboard.html",  {'user': user, 'transactions': transactions, 'form':profile_image_form})


# Adding Payment Gateway
import razorpay
razorpay_client = razorpay.Client(auth=(settings.razorpay_id, settings.razorpay_account_id))

from .models import Order

    
@login_required
def payment(request):
    if request.method == "POST":
        try:
            user = request.user
            print(user)
            final_price = request.POST.get('amount')
            item_id = request.POST.get('item')
            item_instance = FruitFarmingOption.objects.get(id=item_id)
            print(final_price)
           
            order = Order.objects.create(user = request.user, amount = int(final_price), item = item_instance)
            # order.save()
        except Exception as e:
            print(e)
            return HttpResponse("No product in cart")

        order.amount = int(final_price)
        order.save()

        order_currency = 'INR'

        callback_url = 'http://'+ str(get_current_site(request))+"/handlerequest/"
        print(callback_url)
        notes = {'order-type': "basic order from the website", 'key':'value'}
        print("I AM HERE ")
        razorpay_order = razorpay_client.order.create(dict(amount=int(final_price)*100, currency=order_currency, notes = notes, receipt=order.order_id, payment_capture='0'))
        print("I AM HERE 2")
        print(razorpay_order['id'])
        order.razorpay_order_id = razorpay_order['id']
        order.save()
        
        return render(request, 'paymentsummaryrazorpay.html', {'order':order, 'order_id': razorpay_order['id'],'item':item_instance.title, 'orderId':order.order_id, 'final_price':int(final_price), 'razorpay_merchant_id':settings.razorpay_id, 'callback_url':callback_url})
    else:
        return HttpResponse("505 Not Found")


@csrf_exempt
def handlerequest(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            order_id = request.POST.get('razorpay_order_id','')
            signature = request.POST.get('razorpay_signature','')
            params_dict = { 
            'razorpay_order_id': order_id, 
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
            }
            try:
                order_db = Order.objects.get(razorpay_order_id=order_id)
            except:
                return HttpResponse("505 Not Found")
            order_db.razorpay_payment_id = payment_id
            order_db.razorpay_signature = signature
            order_db.save()
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result==None:
                amount = order_db.total_amount * 100   #we have to pass in paisa
                try:
                    razorpay_client.payment.capture(payment_id, amount)
                    order_db.payment_status = 1
                    order_db.save()

                    # Update user's wallet balance
                    user = order_db.user
                    user.wallet_balance += order_db.amount
                    user.save()

                    return render(request, 'paymentsuccess.html',{'id':order_db.id, 'amount':amount})
                except:
                    order_db.payment_status = 2
                    order_db.save()
                    return render(request, 'paymentfailed.html')
            else:
                order_db.payment_status = 2
                order_db.save()
                return render(request, 'paymentfailed.html')
        except:
            return HttpResponse("505 not found")



@login_required
def transactions(request):
    user = request.user
    transactions = Order.objects.filter(user=user).order_by('-datetime_of_payment')
    return render(request, "transactions.html", {'transactions': transactions})

from django.contrib import messages
@login_required
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'update_profile.html', {'form': form})


@login_required
def update_profile_photo(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfilePhotoForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile photo updated successfully.')
            return redirect('dashboard')
    else:
        form = UserProfilePhotoForm(instance=user)
    return render(request, 'dashboard.html', {'form': form})