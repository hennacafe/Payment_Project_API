from django.shortcuts import render
import logging
from django.http import JsonResponse
from django.conf import settings
from cryptography.fernet import Fernet
from django_ratelimit.decorators import ratelimit
from django.views.decorators.csrf import csrf_exempt
from .models import Payment

# Part D: Setup Logger
logger = logging.getLogger(__name__) 

# Part C: Rate Limiting (5 requests per minute, block=True) 
@csrf_exempt
@ratelimit(key='ip', rate='5/m', block=True)
def login_view(request):

    was_limited = getattr(request, 'limited', False)
    if was_limited:
        return JsonResponse({'status': 'Error', 'message': 'Too many requests. Please try again later.'}, status=429)

    if request.method == 'POST':
       
        logger.warning("Multiple failed login attempts detected") # 

        
        key = settings.FERNET_KEY
        cipher = Fernet(key)
        
        
        encrypted_payload = cipher.encrypt(b"4111-1111-1111-1111")
        
        # Store encrypted data in the database [cite: 465]
        Payment.objects.create(encrypted_data=encrypted_payload)
        
        return JsonResponse({'status': 'Success', 'message': 'Data encrypted and stored.'})
        
    return JsonResponse({'message': 'Send a POST request.'})
