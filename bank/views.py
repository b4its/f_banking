import json, hashlib, random, string
from django.shortcuts import render, redirect, get_object_or_404
from bank.models import Currency, Transaction
from account.models import Profile
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

        # Konversi nominal_tunai menjadi Decimal
        try:
            nominal = Decimal(nominal_tunai)
        except:
            messages.error(request, "Nominal tidak valid.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        # Validasi rekening penerima
        try:
            currency_receiver = Currency.objects.get(
                user=user_penerima,
                no_rekening=no_rekening
            )
        except Currency.DoesNotExist:
            messages.error(request, "Rekening tujuan tidak ditemukan.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        # Validasi rekening pengirim
        try:
            currency_sender = Currency.objects.get(user=user)
        except Currency.DoesNotExist:
            messages.error(request, "Rekening Anda tidak ditemukan.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        # Deteksi potensi fraud
        fraud_detected = False

        # 1. Cek NIK & KK dari Profile pengirim dan penerima
        try:
            profile_sender = Profile.objects.get(user=user)
            profile_receiver = Profile.objects.get(user=user_penerima)
            if not profile_sender.nik or not profile_sender.kk:
                print("[FRAUD] NIK atau KK pengirim tidak ditemukan.")
                fraud_detected = True
            if not profile_receiver.nik or not profile_receiver.kk:
                print("[FRAUD] NIK atau KK penerima tidak ditemukan.")
                fraud_detected = True
        except Profile.DoesNotExist:
            print("[FRAUD] Profil pengirim atau penerima tidak ditemukan.")
            fraud_detected = True

        # 2. Cek jenis rekening mencurigakan
        if currency_sender.jenis_rekening.lower() == "mencurigakan":
            print(f"[FRAUD] Jenis rekening pengirim mencurigakan: {currency_sender.jenis_rekening}")
            fraud_detected = True
        if currency_receiver.jenis_rekening.lower() == "mencurigakan":
            print(f"[FRAUD] Jenis rekening penerima mencurigakan: {currency_receiver.jenis_rekening}")
            fraud_detected = True

        # 3. Cek status aktif
        if not currency_sender.status_aktif:
            print("[FRAUD] Rekening pengirim tidak aktif.")
            fraud_detected = True
        if not currency_receiver.status_aktif:
            print("[FRAUD] Rekening penerima tidak aktif.")
            fraud_detected = True

        # Ambil kode mata uang
        sender_currency_code = typeCurrency.get_currency_code_from_index(currency_sender.currency_type)
        receiver_currency_code = typeCurrency.get_currency_code_from_index(currency_receiver.currency_type)

        # Konversi mata uang
        hasil = typeCurrency.convert_currency(nominal, sender_currency_code, receiver_currency_code)

        if hasil is None:
            messages.error(request, "Konversi gagal.")
            return redirect('transferTunai')

        currency_result = hasil

        # Cek saldo
        if currency_sender.saldo < nominal:
            messages.error(request, "Saldo Anda tidak cukup.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        # Proses transfer saldo
        currency_sender.saldo -= nominal
        currency_receiver.saldo += currency_result
        currency_sender.save()
        currency_receiver.save()

        # Buat transaksi dengan status FRAUD jika terdeteksi
        kode_transaksi = generate_unique_code()
        transaksi = Transaction.objects.create(
            user=user,
            code_transactions=kode_transaksi,
            nominal=nominal,
            receiver_currency=currency_result,
            jenis_transaksi=0,
            status=2 if fraud_detected else 1,
        )
        transaksi.currency.add(currency_receiver)

        if fraud_detected:
            print(f"[FRAUD DETECTED] Transaksi kode {kode_transaksi} ditandai sebagai mencurigakan.")
        else:
            print(f"[INFO] Transaksi kode {kode_transaksi} aman.")

        messages.success(request, f"Transfer Tunai Sebesar {receiver_currency_code} {typeCurrency.format_currency(currency_result)}")
        return redirect('transferTunai')

def tarikViews(request):
    saldo = Currency.objects.filter(user=request.user).order_by('-created').first()
    context = {
        'saldo': saldo
    }
    return render(request, 'tarikTunai.html', context)
