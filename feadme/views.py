from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from forms import ProfileForm


@login_required
def profile_edit(request):
    data = request.POST or None
    profile_form = ProfileForm(data, instance=request.user)
    if profile_form.is_valid():
        profile_form.save()
        messages.success(request, "Profile saved")
    elif not data is None:
        messages.error(request, "Profile could not be saved, because of invalid data")
    return render(request, "profiles/edit.html", {'form': profile_form})
