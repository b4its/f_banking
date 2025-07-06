from django.shortcuts import render
from bank.models import Currency
from helper import typeCurrency
# Create your views here.
TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates"),'
)

def dashboards(request):
    saldo = Currency.objects.filter(user=request.user).order_by('-created').first()
    context = {
        'saldo': f"{typeCurrency.get_currency_code_from_index(saldo.currency_type)} {typeCurrency.format_currency(saldo.saldo)}"
    }
    return render(request, 'dashboard.html', context)
