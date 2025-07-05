from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import RegisterForm
# Create your views here.
from django.contrib import messages
from django.contrib.auth.models import User
from account.models import Profile
from bank.models import Currency
# authenticated function
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from .helpers import send_forget_password_mail
from helper import typeCurrency, cryptographyAlgorithm  # pastikan helper di-import
import random, requests, time
#Generate token

def generate_rekening():
    timestamp = int(time.time()) % 100000  # Ambil 5 digit terakhir timestamp
    rand_digits = random.randint(100, 999)  # Tambah 3 digit acak
    return f"{timestamp:05d}{rand_digits:03d}"  # Total 8 digit

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            nik = form.cleaned_data['nik']
            kk = form.cleaned_data['kk']
            currency_type = int(form.cleaned_data['currency_type'])

            print("Form Data:")
            print(f"Email: {email}")
            print(f"Username: {username}")
            print(f"First Name: {first_name}")
            print(f"Last Name: {last_name}")
            print(f"Password 1: {password1}")
            print(f"Password 2: {password2}")
            print(f"NIK: {nik}")
            print(f"KK: {kk}")
            print(f"Currency Type: {currency_type}")

            # Validasi tambahan
            if password1 != password2:
                msg = "Password dan konfirmasi tidak cocok."
                print(f"Error: {msg}")
                messages.error(request, msg)
                return redirect('register')

            if username == password1:
                msg = "Password tidak boleh sama dengan username."
                print(f"Error: {msg}")
                messages.error(request, msg)
                return redirect('register')

            if User.objects.filter(username=username).exists():
                msg = "Username sudah digunakan."
                print(f"Error: {msg}")
                messages.error(request, msg)
                return redirect('register')

            if User.objects.filter(email=email).exists():
                msg = "Email sudah digunakan."
                print(f"Error: {msg}")
                messages.error(request, msg)
                return redirect('register')
            
            import requests

            # Ambil dari form input
            form_nik = form.cleaned_data['nik']
            form_kk = form.cleaned_data['kk']

            # Buat user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
            )
            response = requests.get("http://192.168.1.7:8000/api/v1/citizen-identities")
            rekening_type = "tidak diketahui"
            encrypted = cryptographyAlgorithm.encrypt_data(112,211,404,505,404,11)
            if response.status_code == 200:
                data = response.json()
                print("Data dari Laravel:", data)

                for warga in data:
                    if warga['nik'] == form_nik and warga['kk'] == form_kk:
                        rekening_type = "aman"

                        # Contoh penggunaan enkripsi (misalnya data dari Laravel):
                        encrypted = cryptographyAlgorithm.encrypt_data(warga['nik'], warga['kk'], warga['sim'], warga['npwp'], warga['paspor'], warga['id'])
                        print("Hasil Enkripsi:", encrypted)
                        
                        break
                    else:
                        encrypted = cryptographyAlgorithm.encrypt_data(form_nik, form_kk, 404, 505, 404, 77)
                        print("Mencurigakan")

                else:
                    rekening_type = "mencurigakan"
            else:
                print("Gagal menghubungkan ke API Laravel")

            # Buat Profile
            Profile.objects.create(
                user=user,
                nama_lengkap=f"{first_name} {last_name}",
                nik=nik,
                kk=kk,
                verified_identities = encrypted,
                token=''  # kosong seperti diminta
            )
            
            Currency.objects.create(
                user=user,
                no_rekening=generate_rekening(),
                saldo=0,
                currency_type=currency_type,
                jenis_rekening= rekening_type  # default
            )


            login(request, user)
            msg = "Registrasi berhasil! Silakan login."
            print(f"Success: {msg}")
            messages.success(request, msg)
            return redirect('customerlogin')

        else:
            msg = "Data tidak valid. Periksa kembali form Anda."
            print(f"Error: {msg}")
            messages.error(request, msg)
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def customerlogin (request):
    if request.user.is_authenticated:
        messages.warning(request,'Anda sudah login, tidak bisa login lagi !')
        return redirect('dashboard')
    else:
        if request.method == 'post' or request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            customer = authenticate(request,username=username,password=password)
            if customer is not None:
                login(request,customer)
                messages.info(request,'Selamat Datang '+str(request.user)+'!')
                return redirect('dashboard')
            else:
                messages.error(request,'Username atau password kamu salah!')
                return redirect('customerlogin')

    return render(request,'login.html')

@login_required
def logout_view(request):
	logout(request)
	return redirect("customerlogin")

# def change_password(request, token):
#     try:
#         profile = Profile.objects.filter(token=token).first()
#         if request.method == "POST":
#             akun = User.objects.get(username=profile.user.username)
#             password = request.POST.get('password')
#             password2 = request.POST.get('password2')
#             if password == password2:
#                 akun.set_password(password)
#                 akun.save()
#                 messages.success(request, 'Anda telah berhasil mengatur ulang password anda !')
#                 return redirect('customerlogin')
#             else:
#                 messages.error(request, 'Mohon maaf tidak sesuai dengan sebelumnya !')
                

#         context = {
#             'user_id':profile.user.pk
#         }
#     except Profile.DoesNotExist:
#         messages.error(request, 'Limit token anda sudah habis!')
#         return redirect('lupa_password')

#     return render(request, "change_password.html",context)

# import uuid


# def lupa_password(request):

#         if request.method == "POST":
#             username = request.POST.get('username')
#             if not User.objects.filter(username = username).first():
                
#                 messages.error(request,'Username anda tidak ditemukan!')
#                 return redirect('lupa_password')
#             else:
#                 pengguna = User.objects.get(username = username)
#                 token = str(uuid.uuid4())
#                 send_forget_password_mail(pengguna.email, token)
#                 tes = Profile.objects.get(user = pengguna)
#                 tes.token = token
#                 tes.save()
#                 messages.success(request,'Kodenya telah berhasil dikirim!')
#                 return redirect('lupa_password')
        
#         return render(request, "lupa_password.html")


