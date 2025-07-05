from helper import typeCurrency
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
CURRENCY_TYPE = [
    (i, f"{code} - {name}") for i, (code, name) in enumerate(typeCurrency.currencyType)
]

TRANSACTIONS_TYPE = (
        (0, 'Transfer Tunai'),
        (1, 'Pembayaran'),
        (2, 'Tarik Tunai'),
)

STATUS_TRANSACTIONS = (
        (0, 'Tidak Diketahui'),
        (1, 'Aman'),
        (2, 'Mencurigakan'),
)

class Currency(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='users_currency')
    no_rekening = models.CharField(max_length=255, blank=False, null=False)
    saldo = models.DecimalField(max_digits=15, decimal_places=2)  # Ganti dari CharField
    currency_type = models.IntegerField(choices=CURRENCY_TYPE, default=63) # default IDR currency
    jenis_rekening = models.CharField(max_length=255, blank=False, null=False)
    status_aktif = models.BooleanField(default=True) 
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"saldo: {self.saldo}, nomor: {self.no_rekening}, {self.user.username}"  # Ganti dari self.name yang tidak ada

    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'Currencies'  # Ganti 'Categories' agar sesuai konteks

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_transaction')
    code_transactions = models.CharField(max_length=255, blank=False, null=False)
    currency = models.ManyToManyField(Currency, related_name='users_currency_transaction')
    nominal = models.DecimalField(max_digits=15, decimal_places=2, null = True)  # Ganti dari CharField
    receiver_currency = models.DecimalField(max_digits=15, decimal_places=2, null = True)  # Ganti dari CharField
    jenis_transaksi = models.IntegerField(choices=TRANSACTIONS_TYPE, default=1)
    status = models.IntegerField(choices=STATUS_TRANSACTIONS, default=1)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        currencies = ", ".join([
            f"{c.user.username} - {c.no_rekening}" for c in self.currency.all()
        ])
        return f"Transaksi oleh {self.user.username} {self.nominal:,.2f} ({self.get_jenis_transaksi_display()}) ke {currencies} | {self.receiver_currency} "

    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'Transactions'  # Ganti 'Categories' agar sesuai konteks