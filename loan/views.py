from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q, Count
from django.utils import timezone


from .forms import LoanApplicationForm
from .models import LoanApplication
from kyc.decorator import kyc_required
from account.decorator import block_blocked_users

@login_required
@kyc_required
@block_blocked_users
def apply_loan(request):
    active_loans = LoanApplication.active_loans_count(request.user)
    bank_account = request.user.bank_account

    if request.method == 'POST':
        form = LoanApplicationForm(request.POST, user=request.user)

        if form.is_valid():
            loan = form.save(commit=False)
            loan.applicant = request.user
            loan.save()

            messages.success(request, "Loan application submitted successfully!")
            return redirect('loan:loan_history')

        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = LoanApplicationForm(user=request.user)

    return render(request, 'customers/loan/apply_loan.html', {
        'form': form,
        'active_loans': active_loans,
        'bank_account': bank_account,
    })


@login_required
@kyc_required
@block_blocked_users
def loan_history(request):

    status = request.GET.get('status')

    loans = LoanApplication.objects.filter(
        applicant=request.user
    )

    if status:
        loans = loans.filter(status=status)

    loans = loans.order_by('-date_applied')

    # All user loans (unfiltered) for summary stats
    all_loans = LoanApplication.objects.filter(applicant=request.user)

    # Summary stats
    total_borrowed = all_loans.filter(
        status__in=['approved', 'disbursed', 'repaid']
    ).aggregate(total=Sum('amount'))['total'] or 0

    active_loans = all_loans.filter(
        status__in=['approved', 'disbursed']
    )
    active_count = active_loans.count()

    # Next payment: earliest due_date among active loans
    next_payment_loan = active_loans.order_by('due_date').first()
    next_payment_amount = next_payment_loan.monthly_payment if next_payment_loan else 0
    next_payment_date = next_payment_loan.due_date if next_payment_loan else None

    # Status counts for filter tabs
    pending_count = all_loans.filter(status__in=['pending', 'processing']).count()
    active_count_filter = all_loans.filter(status__in=['approved', 'disbursed']).count()
    repaid_count = all_loans.filter(status='repaid').count()
    rejected_count = all_loans.filter(status='rejected').count()
    total_count = all_loans.count()

    # Overdue loans (disbursed but past due date)
    overdue_count = all_loans.filter(
        status='disbursed',
        due_date__lt=timezone.now().date()
    ).count()

    context = {
        'loans': loans,
        'status': status,
        'total_borrowed': total_borrowed,
        'active_count': active_count,
        'next_payment_amount': next_payment_amount,
        'next_payment_date': next_payment_date,
        'pending_count': pending_count,
        'active_count_filter': active_count_filter,
        'repaid_count': repaid_count,
        'rejected_count': rejected_count,
        'overdue_count': overdue_count,
        'total_count': total_count,
    }

    return render(request, 'customers/loan/loan_history.html', context)