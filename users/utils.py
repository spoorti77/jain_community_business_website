from django.http import JsonResponse
import random

def send_otp(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        otp = str(random.randint(100000, 999999))

        # Store OTP in session or temp model for verification
        request.session['otp'] = otp
        request.session['phone_number'] = phone_number

        # Just print the OTP to console (for dev use)
        print(f"Generated OTP for {phone_number}: {otp}")

        # OR return it in response temporarily (remove in production)
        return JsonResponse({'status': 'success', 'otp': otp, 'message': 'OTP generated (debug mode)'})
