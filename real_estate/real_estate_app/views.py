from django.shortcuts import render, redirect
from .models import Listing, Realtor, Contact
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.



def index(request):

	if request.method == "POST":
		keywords = request.POST.get("keywords")
		city = request.POST.get("city")
		state = request.POST.get("state")
		bedroom = request.POST.get("bedrooms")
		price = request.POST.get("price")
		
		listings = Listing.objects.all()
		
		if "keywords" in request.POST:
			listings = listings.filter(title__icontains=keywords)
			
			if not listings:
				listings = Listing.objects.all()
				listings = listings.filter(description__icontains=keywords)
			
			
		if "city" in request.POST:
			listings = listings.filter(city__icontains=city)
			
		if "state" in request.POST:
			listings = listings.filter(state=state)
			
		if "bedrooms" in request.POST:
			listings = listings.filter(bedroom__lte=bedroom)
			
		if "price" in request.POST:
			listings = listings.filter(price__gte=price)
			
		context = {"listings":listings}
		
		return render(request, "real_estate_app/search.html", context)
		
	listings = Listing.objects.all().order_by("-d_time")[0:3]
	
	context = {"listings":listings}
	
	return render(request, "real_estate_app/index.html", context)
	
	
	
def search(request):
	if request.method == "POST":
		keywords = request.POST.get("keywords")
		city = request.POST.get("city")
		state = request.POST.get("state")
		bedroom = request.POST.get("bedrooms")
		price = request.POST.get("price")
		
		listings = Listing.objects.all()
		
		if "keywords" in request.POST:
			listings = listings.filter(title__icontains=keywords)
			
			if not listings:
				listings = Listing.objects.all()
				listings = listings.filter(description__icontains=keywords)
			
			
		if "city" in request.POST:
			listings = listings.filter(city__icontains=city)
			
		if "state" in request.POST:
			listings = listings.filter(state=state)
			
		if "bedrooms" in request.POST:
			listings = listings.filter(bedroom__lte=bedroom)
			
		if "price" in request.POST:
			listings = listings.filter(price__gte=price)
			
		context = {"listings":listings}
		
		return render(request, "real_estate_app/search.html", context)
		
	
	
def listings(request):

	listings = Listing.objects.order_by("-d_time")
	page = request.GET.get('page')

	paginator = Paginator(listings, 6) 

	try:
		listings = paginator.page(page)
		
	except PageNotAnInteger:
	
		# If page is not an integer, deliver first page.
		listings = paginator.page(1)
		
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		listings = paginator.page(paginator.num_pages)
		
		
	context = {
		"listings":listings
	}
	return render(request, "real_estate_app/listings.html", context)
	
	
def listing(request, pk):
	listing_item = Listing.objects.get(pk=pk)
	context = {"listing":listing_item}
	return render(request, "real_estate_app/listing.html", context)
	
	
	
def about(request):
	realtors = Realtor.objects.all().order_by("hired_date")
	
	try:
		mvp = Realtor.objects.filter(is_mvp=True)[0]
		
	except IndexError:
		mvp = None
		pass
	context = {"realtors":realtors, "mvp":mvp}
	return render(request, "real_estate_app/about.html", context)
	
	

def dashboard(request):
	contacts = Contact.objects.order_by("-date_created").filter(user_id=request.user.id)
	context = {"contacts":contacts}
	return render(request, "real_estate_app/dashboard.html", context)
	
	
def register(request):
	if request.method == "POST":
		first_name = request.POST.get("first_name", None)
		last_name = request.POST.get("last_name", None)
		user_name = request.POST.get("username", None)
		email = request.POST.get("email", None)
		password = request.POST.get("password", None)
		password2 = request.POST.get("password2", None)
		
		if User.objects.filter(username=user_name).exists():
			messages.error(request, "Username already exists")
			return redirect("register")
			
		if User.objects.filter(email=email).exists():
			messages.error(request, "Email already exists")
			return redirect("register")
			
		if password != password2:
			messages.error(request, "The passwords do not match")
			return redirect("register")
			
		if len(password) < 7:
			messages.error(request, "Password is too short")
			return redirect("register")
			
		user = User.objects.create_user(first_name=first_name, last_name=last_name, username=user_name, email=email, password=password)
		user.save()
		messages.success(request, "Registration Successful!")
		return redirect("login")
	return render(request, "real_estate_app/register.html")
	
	
	
def login(request):
	if request.method == "POST":
		username = request.POST.get("username", None)
		password = request.POST.get("password", None)
		
		user = auth.authenticate(username=username, password=password)
		
		if user is not None:
			auth.login(request, user)
			messages.success(request, "Login was successful!")
			return redirect("dashboard")
		else:
			messages.error(request, "Authentication failed")
			return redirect("login")
	return render(request, "real_estate_app/login.html")
	

def logout(request):
	auth.logout(request)
	messages.success(request, "Logout was successful!")
	return redirect("index")
	
	
def contact(request):
	if request.method == "POST":
		listing = request.POST.get("listing")
		listing_id = request.POST.get("listing_id")
		name = request.POST.get("name")
		email = request.POST.get("email")
		phone = request.POST.get("phone")
		message = request.POST.get("message")
		realtor_email = request.POST.get("realtor_email")
		realtor_id = request.POST.get("realtor_id")
		listing_id = request.POST.get("listing_id")
		user_id = request.POST.get("user_id")
		
		
		if request.user.is_authenticated:
			has_inquired = Contact.objects.filter(user_id=user_id, listing_id=listing_id).exists()
			
		if has_inquired:
			messages.error(request, "You have already sent an inquiry message on this property")
			return redirect("listing", pk=listing_id)
		
		contact = Contact(listing=listing, listing_id=listing_id, user_id=user_id, 
		name=name, email=email, phone=phone, message=message)
		
		subject = 'Property Enquiry'
		message = "There is a new property enquiry. Login to read more"
		email_from = settings.EMAIL_HOST_USER
		recipient_list = ['collinsanele@gmail.com',]
		
		try:
			send_mail( subject, message, email_from, recipient_list )
			
		except Exception as e:
			messages.error(request, "An error occured while sending this message")
			return redirect("listing", pk=listing_id)
		
		contact.save()
		messages.success(request, "Message Sent")
		return redirect("listing", pk=listing_id)
		
		
		

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
