import json, hashlib, random, string
from django.shortcuts import render, redirect, get_object_or_404
from bank.models import Currency, Transaction
from django.http import JsonResponse
from helper import typeCurrency
from django.contrib import messages
from decimal import Decimal
from django.contrib.auth.models import User
# Create your views here.
TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates"),'
)

# Mapping index ke kode dan nama
CURRENCY_TYPE_MAP = {i: {"code": code, "name": name, "label": f"{code} - {name}"} for i, (code, name) in enumerate(typeCurrency.currencyType)}

def generate_unique_code(length=8):
    while True:
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        code = hashlib.md5(random_string.encode()).hexdigest()[:length]
        if not Transaction.objects.filter(code_transactions=code).exists():
            return code


def transferViews(request):
    tipeCurrencyIndex = list(
        Currency.objects.filter(user=request.user).values_list('currency_type', flat=True)
    )

    # Ambil kode berdasarkan index dari mapping
    tipeCurrencyCode = [
        CURRENCY_TYPE_MAP.get(index, {}).get('code') for index in tipeCurrencyIndex
    ]

    # Buang None (jika ada index yang tidak ditemukan)
    tipeCurrencyCode = [code for code in tipeCurrencyCode if code is not None]

    context = {
        'tipeCurrency': tipeCurrencyCode
    }
    return render(request, 'transferTunai.html', context)

CURRENCY_TYPE = [
    (i, f"{code} - {name}") for i, (code, name) in enumerate(typeCurrency.currencyType)
]

def get_currency_code_from_index(index):
    try:
        return typeCurrency.currencyType[int(index)][0]
    except (IndexError, ValueError):
        return "UNKNOWN"


def transferStore(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        no_rekening = data.get('no_rekening', '').strip()
        print(f"Rekening AJAX diterima: {no_rekening}")

        try:
            currency = Currency.objects.select_related('user').get(no_rekening=no_rekening)

            currency_type_info = CURRENCY_TYPE_MAP.get(currency.currency_type, {"code": "UNKNOWN", "name": "Unknown", "label": "UNKNOWN"})

            result = {
                'found': True,
                'user': {
                    'username': currency.user.username,
                    'first_name': currency.user.first_name,
                    'last_name': currency.user.last_name,
                },
                'currency': {
                    'no_rekening': currency.no_rekening,
                    'currency_type_index': currency.currency_type,
                    'currency_type_code': currency_type_info['code'],
                    'currency_type_name': currency_type_info['name'],
                    'currency_type_label': currency_type_info['label'],  # e.g., "IDR - Rupiah"
                }
            }
            return JsonResponse(result)
        except Currency.DoesNotExist:
            return JsonResponse({'found': False})
        
def transferStored(request):
    if request.method == 'POST':
        user = request.user
        usernamePenerima = request.POST.get('usernameCurrencys')
        no_rekening = request.POST.get('noRekening')
        nominal_tunai = request.POST.get('nominalTunai')
        currency_type_number = request.POST.get('currencyTypeNumber')

        # Validasi user penerima
        try:
            user_penerima = User.objects.get(username=usernamePenerima)
        except User.DoesNotExist:
            messages.error(request, "Username penerima tidak ditemukan.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        print(f"[DEBUG] User login     : {user.username}")
        print(f"[DEBUG] No Rekening    : {no_rekening}")
        print(f"[DEBUG] Nominal Tunai  : {nominal_tunai}")
        print(f"[DEBUG] Currency Type  : {currency_type_number}")

        # Konversi nominal_tunai menjadi Decimal
        try:
            nominal = Decimal(nominal_tunai)
            print(f"[DEBUG] Nominal Decimal: {nominal}")
        except:
            print("[ERROR] Nominal tidak valid.")
            messages.error(request, "Nominal tidak valid.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        # Validasi rekening penerima
        try:
            currency_receiver = Currency.objects.get(
                user=user_penerima,
                no_rekening=no_rekening
            )
            print(f"[DEBUG] Receiver ditemukan: {currency_receiver.user.username}")
        except Currency.DoesNotExist:
            print("[ERROR] Rekening penerima tidak ditemukan.")
            messages.error(request, "Rekening tujuan tidak ditemukan.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        # Validasi rekening pengirim
        try:
            currency_sender = Currency.objects.get(user=user)
            print(f"[DEBUG] Sender ditemukan: saldo = {currency_sender.saldo}")
            if currency_sender.jenis_rekening == "mencurigakan":
                print("Pengirim ini mencurigakan")
        except Currency.DoesNotExist:
            print("[ERROR] Rekening pengirim tidak ditemukan.")
            messages.error(request, "Rekening Anda tidak ditemukan.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        # Ambil kode mata uang pengirim dan penerima
        sender_currency_code = get_currency_code_from_index(currency_sender.currency_type)
        receiver_currency_code = get_currency_code_from_index(currency_receiver.currency_type)

        print(f"[DEBUG] Sender Currency Type   : {sender_currency_code}")
        print(f"[DEBUG] Receiver Currency Type : {receiver_currency_code}")

        # Konversi nominal dengan tipe data Decimal
        hasil = typeCurrency.convert_currency(nominal, sender_currency_code, receiver_currency_code)

        if hasil is not None:
            currency_result = hasil
            print(f"Hasil Konversi: {currency_result} {receiver_currency_code}")
        else:
            print("Konversi gagal. Coba periksa koneksi internet atau mata uang yang digunakan.")
            messages.error(request, "Konversi gagal.")
            return redirect('transferTunai')

        # Cek saldo cukup
        if currency_sender.saldo < nominal:
            print("[ERROR] Saldo tidak cukup.")
            messages.error(request, "Saldo Anda tidak cukup.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        # Proses transfer
        currency_sender.saldo -= nominal
        currency_receiver.saldo += currency_result
        currency_sender.save()
        currency_receiver.save()

        print(f"[DEBUG] Saldo setelah transfer - Sender: {currency_sender.saldo}, Receiver: {currency_receiver.saldo}")

        # Buat transaksi
        kode_transaksi = generate_unique_code()
        transaksi = Transaction.objects.create(
            user=user,
            code_transactions=kode_transaksi,
            nominal=nominal,
            receiver_currency = currency_result,
            jenis_transaksi=1,  # Transfer Tunai
            status=1,           # Berhasil
        )
        transaksi.currency.add(currency_receiver)

        print(f"[SUCCESS] Transaksi berhasil dibuat dengan kode: {kode_transaksi}")
        messages.success(request, "Transfer tunai berhasil.")
        return redirect('transferTunai')
    
def tarikViews(request):
    saldo = Currency.objects.filter(user=request.user).order_by('-created').first()
    context = {
        'saldo': saldo
    }
    return render(request, 'tarikTunai.html', context)
