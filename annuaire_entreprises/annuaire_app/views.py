from django.shortcuts import render, get_object_or_404, redirect
from .models import Entreprise
from .forms import EntrepriseForm, CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm

@login_required
def home(request):
    return render(request, 'home.html')

# Liste des entreprises
def liste_entreprises(request):
    entreprises = Entreprise.objects.all()
    return render(request, 'list.html', {'entreprises': entreprises})

# Détails d'une entreprise
def details_entreprise(request, id):
    entreprise = get_object_or_404(Entreprise, id=id)
    return render(request, 'detail.html', {'entreprise': entreprise})

# Ajouter une entreprise
def ajouter_entreprise(request):
    if request.method == 'POST':
        form = EntrepriseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_entreprises')
    else:
        form = EntrepriseForm()
    return render(request, 'form.html', {'form': form})

# Modifier une entreprise
@login_required
def modifier_entreprise(request, entreprise_id):
    entreprise = get_object_or_404(Entreprise, id=entreprise_id)

    if entreprise.owner != request.user:
        messages.error(request, "Vous n'avez pas la permission de modifier cette entreprise.")
        return render(request, 'annuaire_app/modifier_entreprise.html', {'form': None})

    if request.method == 'POST':
        form = EntrepriseForm(request.POST, instance=entreprise)
        if form.is_valid():
            form.save()
            messages.success(request, "Entreprise mise à jour avec succès.")
            return redirect('liste_entreprises')
    else:
        form = EntrepriseForm(instance=entreprise)

    return render(request, 'annuaire_app/modifier_entreprise.html', {'form': form})

# Supprimer une entreprise
@login_required
def supprimer_entreprise(request, id):
    entreprise = get_object_or_404(Entreprise, id=id)
    if entreprise.owner != request.user:
        messages.error(request, "Vous n'avez pas la permission de suprimer cette entreprise.")
    else:
        entreprise.delete()
    return redirect('liste_entreprises')

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save to DB yet
            email = form.cleaned_data.get('email')
            user.email = email  # Set email explicitly
            
            # Debug information
            print(f"Before save - Username: {user.username}, Email: {email}")
            
            # Save the user
            user.save()
            
            # Verify the save
            saved_user = User.objects.get(username=user.username)
            print(f"After save - Username: {saved_user.username}, Email: {saved_user.email}")
            
            # Log the user in
            login(request, user)
            messages.success(request, "Compte créé avec succès!")
            return redirect('home')
        else:
            print(f"Form errors: {form.errors}")
            for field, errors in form.errors.items():
                messages.error(request, f"{field}: {', '.join(errors)}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get('email')
        print(f"Attempting password reset for email: {email}")
        User = get_user_model()
        
        # Debug: Print all users and their emails
        all_users = User.objects.all()
        print("All users in database:")
        for u in all_users:
            print(f"Username: {u.username}, Email: {u.email}")
        
        # Try to find user by email or username
        try:
            # First try to find by email
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            try:
                # If not found by email, try to find by username
                user = User.objects.get(username=email)
                # If found by username, update their email
                user.email = email
                user.save()
                print(f"Updated email for user {user.username} to {email}")
            except User.DoesNotExist:
                print(f"No user found with email or username: {email}")
                messages.error(request, "Aucun compte n'est associé à cette adresse email.")
                return render(request, 'registration/password_reset_form.html')
        
        print(f"Found user: {user.username}, Email: {user.email}")
        # Generate token and uid
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Create reset link
        reset_link = request.build_absolute_uri(f'/reset-password/{uid}/{token}/')
        print(f"Generated reset link: {reset_link}")
        
        # Send email
        subject = "Réinitialisation de votre mot de passe"
        message = render_to_string('registration/password_reset_email.html', {
            'user': user,
            'reset_link': reset_link,
        })
        
        try:
            send_mail(
                subject,
                message,
                None,  # Will use EMAIL_HOST_USER from settings
                [email],
                fail_silently=False,
            )
            print(f"Password reset email sent to {email}")
            messages.success(request, 'Un email a été envoyé avec les instructions pour réinitialiser votre mot de passe.')
            return redirect('password_reset_done')
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            messages.error(request, "Une erreur s'est produite lors de l'envoi de l'email. Veuillez réessayer plus tard.")
    
    return render(request, 'registration/password_reset_form.html')

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Votre mot de passe a été réinitialisé avec succès.')
                return redirect('password_reset_complete')
        else:
            form = SetPasswordForm(user)
        return render(request, 'registration/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, 'Le lien de réinitialisation est invalide ou a expiré.')
        return redirect('password_reset')

def password_reset_done(request):
    return render(request, 'registration/password_reset_done.html')

def password_reset_complete(request):
    return render(request, 'registration/password_reset_complete.html')
