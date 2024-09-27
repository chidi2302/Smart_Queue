from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate,logout
#from django.contrib.auth.models import User
from .forms import SignUpForm, LoginForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from queue_app.models import CustomUser 
from django.utils import timezone
from django.core.mail import send_mail
from .models import Service, Booking
import uuid
from datetime import timedelta

# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def about(request):
    return render(request, 'about.html')

@login_required
def atm_queue(request):
    return render(request, 'atm-queue.html')

@login_required
def contact(request):
    return render(request, 'contact.html')

@login_required
def features(request):
    return render(request, 'features.html')

@login_required
def deposit_queue(request):
    return render(request, 'deposit-queue.html')

@login_required
def general_inquiries(request):
    return render(request, 'general_inquiries.html')

@login_required
def how_it_works(request):
    return render(request, 'how-it-works.html')

@login_required
def services(request):
    return render(request, 'services.html')

@login_required
def withdrawal_queue(request):
    return render(request, 'withdrawal-queue.html')

@login_required
def book_slot(request):
    return render(request, 'book_slot.html', {'services':services})



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user}!')
            login(request, user)
            return redirect('login')  # Redirect to home after signup
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirect to home after login
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def home(request):
    return render(request, 'index.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login after logout

def book_slot(request):
    if request.method == 'POST':
        service_id = request.POST.get('service')
        date = request.POST.get('date')  # Get selected date from the form
        time = request.POST.get('time')  # Get selected time from the form
        date_time = f"{date} {time}:00"  # Combine date and time for full datetime

        # Check if the user has already booked this service today
        today = timezone.now().date()
        has_booked_today = Booking.objects.filter(
            user=request.user,
            service_id=service_id,
            date_time__date=today
        ).exists()

        if has_booked_today:
            messages.error(request, 'You can only book this service once per day.')
            return redirect('book_slot')

        # Check if the time slot is full (maximum of 3 bookings)
        bookings_count = Booking.objects.filter(date_time=date_time, service_id=service_id).count()
        if bookings_count >= 3:  # Change this number to adjust the limit
            messages.error(request, 'Time slot is full. Please choose another time.')
            return redirect('book_slot')

        # Create a unique queue number
        queue_number = str(uuid.uuid4())[:8]

        # Create the booking
        booking = Booking(user=request.user, service_id=service_id, date_time=date_time, queue_number=queue_number)
        booking.save()

        # Send confirmation email
        '''send_mail(
            'Booking Confirmation',
            f'Your booking is confirmed. Queue Number: {queue_number}',
            'from@example.com',
            [request.user.email],
            fail_silently=False,
        )'''

        messages.success(request, 'Successfully booked! Queue Number: {}'.format(queue_number))
        return redirect('book_slot')

    # Create time slots from 7 AM to 3 PM
    time_slots = []
    for hour in range(7, 16):  # 7 AM (7) to 3 PM (15)
        time_slots.append(f"{hour}:00")
        #time_slots.append(f"{hour}:00")

    services = Service.objects.all()  # Fetch services from the database
    return render(request, 'book_slot.html', {'services': services, 'time_slots': time_slots})


def view_available_queues(request):
    today = timezone.now().date()
    services = Service.objects.all()
    available_slots = []

    # Check each hour from 7:00 to 15:00
    for hour in range(7, 16):  # 7:00 to 15:00
        time_slot = timezone.datetime(today.year, today.month, today.day, hour, 0, 0)
        # Check if this time slot is available for any service
        if not Booking.objects.filter(date_time=time_slot).exists():
            for service in services:
                available_slots.append({'time': time_slot, 'service': service})

    return render(request, 'available_queues.html', {'available_slots': available_slots})


###  Create a View for Real-Time Queuing Status
def view_real_time_queuing_status(request):
    # Get today's date
    today = timezone.now().date()

    # Get all services
    services = Service.objects.all()
    queuing_status = []

    for service in services:
        # Count how many bookings exist for this service today
        total_bookings = Booking.objects.filter(service=service, date_time__date=today).count()
        
        # Assume a max of 10 bookings per service for the current time
        max_bookings_per_service = 10
        
        # Calculate available slots
        available_slots = max_bookings_per_service - total_bookings
        
        queuing_status.append({
            'service': service,
            'total_bookings': total_bookings,
            'available_slots': available_slots,
        })

    # Render the template with the queuing status data
    return render(request, 'real_time_queuing_status.html', {'queuing_status': queuing_status})

