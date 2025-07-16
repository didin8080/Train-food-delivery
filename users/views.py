from django.shortcuts import render,redirect
from. models import user_tbl

def log(request):
    return render(request,"index.html")

def reg(request):
    if request.method == 'POST':
        fnm = request.POST.get('fn')
        phnm = request.POST.get('ph')
        ema = request.POST.get('em')
        pss = request.POST.get('ps')
        obj = user_tbl.objects.create(fname=fnm,pnum=phnm,email=ema,passw=pss)
        obj.save()
        if obj:
            return render(request,"index.html")
        else:
            return render(request,"register.html")
    else:
        return render(request,"register.html")


def login(request):
    if request.method == 'POST':
        em = request.POST.get('email')
        ps = request.POST.get('password')
        obj = user_tbl.objects.filter(email=em, passw=ps).first()
        
        if obj:
            request.session.flush()  # Clears old session
            request.session['idl'] = obj.id  # Store user ID
            return redirect('home')
        else:
            msg = "Incorrect email or password"
            return render(request, "login.html", {"error": msg})
    
    return render(request, "login.html")
from django.shortcuts import render

def home(request):
    return render(request, "home.html")
