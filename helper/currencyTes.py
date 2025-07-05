from tesCurrency import convert_currency

# Contoh konversi
amount = 500
from_currency = "IDR"
to_currency = "USD"

hasil = convert_currency(amount, from_currency, to_currency)

if hasil is not None:
    print(f"{amount} {from_currency} = {hasil:,.2f} {to_currency}")
else:
    print("Konversi gagal. Coba periksa koneksi internet atau mata uang yang digunakan.")
