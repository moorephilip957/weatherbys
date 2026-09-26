from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Prefetch
from django.utils import timezone
from datetime import timedelta

from .forms import TicketForm
from .models import Ticket, TicketMessage
from kyc.decorator import kyc_required

@login_required
def create_ticket(request):
    # Get user's recent tickets for sidebar
    recent_tickets = Ticket.objects.filter(
        user=request.user
    ).order_by('-created_at')[:5]

    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.name = request.user.get_full_name() or request.user.first_name
            ticket.email = request.user.email
            ticket.save()

            # Create initial message
            TicketMessage.objects.create(
                ticket=ticket,
                sender="user",
                content=ticket.message,
            )

            return redirect("support:ticket_success", reference_id=ticket.reference_id)

        messages.error(request, "Please correct the errors below.")

    else:
        form = TicketForm()

    return render(request, "customers/support/create_ticket.html", {
        "form": form,
        "recent_tickets": recent_tickets,
    })


@login_required
# @kyc_required
def ticket_success(request, reference_id):
    ticket = get_object_or_404(
        Ticket,
        reference_id=reference_id,
        user=request.user  # ← Only show tickets belonging to this user
    )
    return render(request, "customers/support/ticket_success.html", {"ticket": ticket})


@login_required
# @kyc_required
def ticket_list(request):
    # Base queryset
    tickets = Ticket.objects.filter(user=request.user)

    status = request.GET.get("status")
    search = request.GET.get("search", "")

    if status and status != "all":
        tickets = tickets.filter(status=status)

    if search:
        tickets = tickets.filter(
            Q(subject__icontains=search) |
            Q(reference_id__icontains=search) |
            Q(message__icontains=search)
        )

    # Prefetch last message for each ticket (for preview)
    tickets = tickets.prefetch_related(
        Prefetch(
            'messages',
            queryset=TicketMessage.objects.order_by('-created_at')[:1],
            to_attr='last_message_list'
        )
    ).order_by("-updated_at")

    # Summary counts (unfiltered)
    all_user_tickets = Ticket.objects.filter(user=request.user)
    total_count = all_user_tickets.count()
    open_count = all_user_tickets.filter(status="open").count()
    in_progress_count = all_user_tickets.filter(status="in_progress").count()
    resolved_count = all_user_tickets.filter(status="resolved").count()
    closed_count = all_user_tickets.filter(status="closed").count()

    return render(request, "customers/support/ticket_list.html", {
        "tickets": tickets,
        "status": status,
        "search": search,
        "total_count": total_count,
        "open_count": open_count,
        "in_progress_count": in_progress_count,
        "resolved_count": resolved_count,
        "closed_count": closed_count,
    })


@login_required
# @kyc_required
def ticket_detail(request, reference_id):
    ticket = get_object_or_404(Ticket, reference_id=reference_id, user=request.user)
    
    # Fetch messages chronologically
    ticket_messages = ticket.messages.all().order_by("created_at")
    
    if request.method == "POST":
        content = request.POST.get("message")
        attachment = request.FILES.get("attachment")

        if content or attachment:
            TicketMessage.objects.create(
                ticket=ticket,
                sender="user",
                content=content,
                attachment=attachment
            )
            ticket.status = "in_progress"
            ticket.save()
            messages.success(request, "Your message has been sent.")
            return redirect("support:ticket_detail", reference_id=ticket.reference_id)
        else:
            messages.error(request, "Please enter a message or attach a file.")

    now = timezone.now()
    return render(request, "customers/support/ticket_detail.html", {
        "ticket": ticket,
        "ticket_messages": ticket_messages,
        "today_date": now.date().isoformat(),
        "yesterday_date": (now.date() - timedelta(days=1)).isoformat(),
    })