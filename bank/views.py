from django.shortcuts import render
from bank.models import Currency
# Create your views here.
TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates"),'
)

def transferViews(request):
    saldo = Currency.objects.filter(user=request.user).order_by('-created').first()
    context = {
        'saldo': saldo
    }
    return render(request, 'transferTunai.html', context)

def tarikViews(request):
    saldo = Currency.objects.filter(user=request.user).order_by('-created').first()
    context = {
        'saldo': saldo
    }
    return render(request, 'tarikTunai.html', context)
