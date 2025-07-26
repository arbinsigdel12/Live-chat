from django.dispatch import receiver
from allauth.account.signals import user_signed_up, user_logged_in
from .models import Profile

@receiver(user_signed_up)
def create_profile_on_signup(request, user, **kwargs):
    Profile.objects.create(user=user)

@receiver(user_logged_in)
def ensure_profile_exists_on_login(request, user, **kwargs):
    Profile.objects.get_or_create(user=user)
