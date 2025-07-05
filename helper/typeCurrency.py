import requests
from datetime import datetime
from decimal import Decimal, InvalidOperation

currencyType = (
    ('AED', 'UAE Dirham'),
    ('AFN', 'Afghani'),
    ('ALL', 'Lek'),
    ('AMD', 'Armenian Dram'),
    ('ANG', 'Netherlands Antillean Guilder'),
    ('AOA', 'Kwanza'),
    ('ARS', 'Argentine Peso'),
    ('AUD', 'Australian Dollar'),
    ('AWG', 'Aruban Florin'),
    ('AZN', 'Azerbaijanian Manat'),
    ('BAM', 'Convertible Mark'),
    ('BBD', 'Barbados Dollar'),
    ('BDT', 'Taka'),
    ('BGN', 'Bulgarian Lev'),
    ('BHD', 'Bahraini Dinar'),
    ('BIF', 'Burundi Franc'),
    ('BMD', 'Bermudian Dollar'),
    ('BND', 'Brunei Dollar'),
    ('BOB', 'Boliviano'),
    ('BRL', 'Brazilian Real'),
    ('BSD', 'Bahamian Dollar'),
    ('BTN', 'Ngultrum'),
    ('BWP', 'Pula'),
    ('BYN', 'Belarusian Ruble'),
    ('BZD', 'Belize Dollar'),
    ('CAD', 'Canadian Dollar'),
    ('CDF', 'Congolese Franc'),
    ('CHF', 'Swiss Franc'),
    ('CLP', 'Chilean Peso'),
    ('CNY', 'Yuan Renminbi'),
    ('COP', 'Colombian Peso'),
    ('CRC', 'Costa Rican Colon'),
    ('CUC', 'Peso Convertible'),
    ('CUP', 'Cuban Peso'),
    ('CVE', 'Cabo Verde Escudo'),
    ('CZK', 'Czech Koruna'),
    ('DJF', 'Djibouti Franc'),
    ('DKK', 'Danish Krone'),
    ('DOP', 'Dominican Peso'),
    ('DZD', 'Algerian Dinar'),
    ('EGP', 'Egyptian Pound'),
    ('ERN', 'Nakfa'),
    ('ETB', 'Ethiopian Birr'),
    ('EUR', 'Euro'),
    ('FJD', 'Fiji Dollar'),
    ('FKP', 'Falkland Islands Pound'),
    ('FOK', 'Faroese Króna'),
    ('GBP', 'Pound Sterling'),
    ('GEL', 'Lari'),
    ('GGP', 'Guernsey Pound'),
    ('GHS', 'Ghana Cedi'),
    ('GIP', 'Gibraltar Pound'),
    ('GMD', 'Dalasi'),
    ('GNF', 'Guinean Franc'),
    ('GTQ', 'Quetzal'),
    ('GYD', 'Guyana Dollar'),
    ('HKD', 'Hong Kong Dollar'),
    ('HNL', 'Lempira'),
    ('HRK', 'Croatian Kuna'),
    ('HTG', 'Gourde'),
    ('HUF', 'Forint'),
    ('IDR', 'Rupiah'),
    ('ILS', 'New Israeli Sheqel'),
    ('IMP', 'Isle of Man Pound'),
    ('INR', 'Indian Rupee'),
    ('IQD', 'Iraqi Dinar'),
    ('IRR', 'Iranian Rial'),
    ('ISK', 'Iceland Krona'),
    ('JEP', 'Jersey Pound'),
    ('JMD', 'Jamaican Dollar'),
    ('JOD', 'Jordanian Dinar'),
    ('JPY', 'Yen'),
    ('KES', 'Kenyan Shilling'),
    ('KGS', 'Som'),
    ('KHR', 'Riel'),
    ('KID', 'Kiribati Dollar'),
    ('KMF', 'Comorian Franc'),
    ('KRW', 'Won'),
    ('KWD', 'Kuwaiti Dinar'),
    ('KYD', 'Cayman Islands Dollar'),
    ('KZT', 'Tenge'),
    ('LAK', 'Lao Kip'),
    ('LBP', 'Lebanese Pound'),
    ('LKR', 'Sri Lanka Rupee'),
    ('LRD', 'Liberian Dollar'),
    ('LSL', 'Loti'),
    ('LYD', 'Libyan Dinar'),
    ('MAD', 'Moroccan Dirham'),
    ('MDL', 'Moldovan Leu'),
    ('MGA', 'Malagasy Ariary'),
    ('MKD', 'Denar'),
    ('MMK', 'Kyat'),
    ('MNT', 'Tugrik'),
    ('MOP', 'Pataca'),
    ('MRU', 'Ouguiya'),
    ('MUR', 'Mauritius Rupee'),
    ('MVR', 'Rufiyaa'),
    ('MWK', 'Malawi Kwacha'),
    ('MXN', 'Mexican Peso'),
    ('MYR', 'Malaysian Ringgit'),
    ('MZN', 'Mozambique Metical'),
    ('NAD', 'Namibia Dollar'),
    ('NGN', 'Naira'),
    ('NIO', 'Cordoba Oro'),
    ('NOK', 'Norwegian Krone'),
    ('NPR', 'Nepalese Rupee'),
    ('NZD', 'New Zealand Dollar'),
    ('OMR', 'Rial Omani'),
    ('PAB', 'Balboa'),
    ('PEN', 'Sol'),
    ('PGK', 'Kina'),
    ('PHP', 'Philippine Peso'),
    ('PKR', 'Pakistan Rupee'),
    ('PLN', 'Zloty'),
    ('PYG', 'Guarani'),
    ('QAR', 'Qatari Rial'),
    ('RON', 'Romanian Leu'),
    ('RSD', 'Serbian Dinar'),
    ('RUB', 'Russian Ruble'),
    ('RWF', 'Rwanda Franc'),
    ('SAR', 'Saudi Riyal'),
    ('SBD', 'Solomon Islands Dollar'),
    ('SCR', 'Seychelles Rupee'),
    ('SDG', 'Sudanese Pound'),
    ('SEK', 'Swedish Krona'),
    ('SGD', 'Singapore Dollar'),
    ('SHP', 'Saint Helena Pound'),
    ('SLL', 'Leone'),
    ('SOS', 'Somali Shilling'),
    ('SRD', 'Surinam Dollar'),
    ('SSP', 'South Sudanese Pound'),
    ('STN', 'Dobra'),
    ('SYP', 'Syrian Pound'),
    ('SZL', 'Lilangeni'),
    ('THB', 'Baht'),
    ('TJS', 'Somoni'),
    ('TMT', 'Turkmenistan New Manat'),
    ('TND', 'Tunisian Dinar'),
    ('TOP', 'Pa’anga'),
    ('TRY', 'Turkish Lira'),
    ('TTD', 'Trinidad and Tobago Dollar'),
    ('TVD', 'Tuvaluan Dollar'),
    ('TWD', 'New Taiwan Dollar'),
    ('TZS', 'Tanzanian Shilling'),
    ('UAH', 'Hryvnia'),
    ('UGX', 'Uganda Shilling'),
    ('USD', 'US Dollar'),
    ('UYU', 'Peso Uruguayo'),
    ('UZS', 'Uzbekistan Sum'),
    ('VES', 'Bolívar Soberano'),
    ('VND', 'Dong'),
    ('VUV', 'Vatu'),
    ('WST', 'Tala'),
    ('XAF', 'CFA Franc BEAC'),
    ('XCD', 'East Caribbean Dollar'),
    ('XOF', 'CFA Franc BCEAO'),
    ('XPF', 'CFP Franc'),
    ('YER', 'Yemeni Rial'),
    ('ZAR', 'Rand'),
    ('ZMW', 'Zambian Kwacha'),
    ('ZWL', 'Zimbabwe Dollar'),
)

# PROGRAM CURRENCY
class CurrencyConverter:
    def __init__(self):
        # Misalnya kamu punya currencyType seperti: [('IDR', 'Rupiah'), ('USD', 'US Dollar'), ...]
        self.currency_types = dict(currencyType)
        self.api_url = "https://api.exchangerate-api.com/v4/latest/"

    def get_exchange_rate(self, from_currency, to_currency):
        if from_currency == to_currency:
            return Decimal('1.0')
        try:
            response = requests.get(f"{self.api_url}{from_currency}")
            response.raise_for_status()
            data = response.json()
            rate = data.get("rates", {}).get(to_currency)
            if rate is not None:
                return Decimal(str(rate))
            else:
                print(f"[ERROR] Kurs {from_currency} ke {to_currency} tidak tersedia.")
                return None
        except Exception as e:
            print(f"[ERROR] Gagal mengambil kurs: {e}")
            return None

    def convert_currency(self, amount, from_currency, to_currency):
        try:
            # Pastikan amount berupa Decimal
            if not isinstance(amount, Decimal):
                amount = Decimal(str(amount))
        except InvalidOperation:
            print(f"[ERROR] Nilai amount tidak valid: {amount}")
            return None

        rate = self.get_exchange_rate(from_currency, to_currency)
        if rate is None:
            return None

        try:
            result = amount * rate
            return result
        except Exception as e:
            print(f"[ERROR] Gagal menghitung konversi: {e}")
            return None

# Fungsi utilitas agar bisa dipanggil dari file luar
def convert_currency(amount, from_currency, to_currency):
    converter = CurrencyConverter()
    return converter.convert_currency(amount, from_currency, to_currency)
