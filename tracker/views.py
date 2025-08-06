from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from .forms import ExpenseForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from datetime import date
from django.contrib.auth import login

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created. Welcome!")
            return redirect("dashboard")
    else:
        form = UserRegisterForm()
    return render(request, "tracker/register.html", {"form": form})

# views.py
from django.db.models import Sum
from datetime import date

@login_required
def dashboard(request):
    today = date.today()
    month_start = today.replace(day=1)
    monthly_expenses = Expense.objects.filter(
        user=request.user,
        date__gte=month_start,
        date__lte=today
    )
    total_spent = monthly_expenses.aggregate(total=Sum("amount"))["total"] or 0

    # build breakdown as floats
    breakdown_qs = (
        monthly_expenses
        .values("category")
        .annotate(sum=Sum("amount"))
    )
    breakdown = {item["category"]: float(item["sum"]) for item in breakdown_qs}

    context = {
        "total_spent": total_spent,
        "breakdown": breakdown,
        "monthly_expenses": monthly_expenses[:5],
    }
    return render(request, "tracker/dashboard.html", context)

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    return render(request, "tracker/expense_list.html", {"expenses": expenses})

@login_required
def expense_create(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            exp = form.save(commit=False)
            exp.user = request.user
            exp.save()
            messages.success(request, "Expense added.")
            return redirect("expense_list")
    else:
        form = ExpenseForm()
    return render(request, "tracker/expense_form.html", {"form": form, "title": "Add Expense"})

@login_required
def expense_edit(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense updated.")
            return redirect("expense_list")
    else:
        form = ExpenseForm(instance=expense)
    return render(request, "tracker/expense_form.html", {"form": form, "title": "Edit Expense"})

@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == "POST":
        expense.delete()
        messages.success(request, "Expense deleted.")
        return redirect("expense_list")
    return render(request, "tracker/expense_confirm_delete.html", {"expense": expense})
