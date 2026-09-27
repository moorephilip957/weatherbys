from django.shortcuts import render,redirect
import time

def home_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('staff:staff_dashboard')
        else:
            return redirect('customer:dashboard')
    return render(request, 'frontend2/index.html')

def personal_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('staff:staff_dashboard')
        else:
            return redirect('customer:dashboard')
    return render(request, 'frontend2/personal.html')

def corperate_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('staff:staff_dashboard')
        else:
            return redirect('customer:dashboard')
    return render(request, 'frontend2/corperate.html')

def insurance_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('staff:staff_dashboard')
        else:
            return redirect('customer:dashboard')
    return render(request, 'frontend/insurance.html')

def mortgages_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('staff:staff_dashboard')
        else:
            return redirect('customer:dashboard')
    return render(request, 'frontend/mortgages.html')

def savings_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('staff:staff_dashboard')
        else:
            return redirect('customer:dashboard')
    return render(request, 'frontend2/savings.html')

def loans_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('staff:staff_dashboard')
        else:
            return redirect('customer:dashboard')
    return render(request, 'frontend2/loans.html')

def cards_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('staff:staff_dashboard')
        else:
            return redirect('customer:dashboard')
    return render(request, 'frontend2/cards.html')

def about_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('staff:staff_dashboard')
        else:
            return redirect('customer:dashboard')
    return render(request, 'frontend2/about.html')

def contact_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('staff:staff_dashboard')
        else:
            return redirect('customer:dashboard')
    return render(request, 'frontend2/contact.html')

def terms_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('staff:staff_dashboard')
        else:
            return redirect('customer:dashboard')
    return render(request, 'frontend2/terms.html')

def privacy_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('staff:staff_dashboard')
        else:
            return redirect('customer:dashboard')
    return render(request, 'frontend2/privacy.html')