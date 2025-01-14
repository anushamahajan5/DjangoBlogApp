from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.db import IntegrityError

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                # Save the user instance
                user = form.save()
                # Create the profile instance
                Profile.objects.create(
                    user=user,
                    linkedin=request.POST.get('linkedin', ''),
                    instagram=request.POST.get('instagram', ''),
                    facebook=request.POST.get('facebook', ''),
                    twitter=request.POST.get('twitter', ''),
                )
                messages.success(request, 'Your account has been created! You can now log in.')
                return redirect('login')
            except IntegrityError:
                messages.error(request, 'A profile for this user already exists. Please try again with a different username or email.')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'users/profile.html')

@login_required
def profile_update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "u_form": u_form,
        "p_form": p_form
    }
    return render(request, 'users/profile_update.html', context)