from django.shortcuts import render
from bank.models import Currency
# Create your views here.
TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates"),'
)

def dashboards(request):
    saldo = Currency.objects.filter(user=request.user).order_by('-created').first()
    context = {
        'saldo': saldo
    }
    return render(request, 'dashboard.html', context)
