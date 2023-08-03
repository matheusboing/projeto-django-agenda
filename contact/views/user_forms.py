from django.shortcuts import render, redirect
from contact.forms import RegisterForm, RegisterUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib import auth, messages
from django.contrib.auth.forms import AuthenticationForm

def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário registrado com sucesso')
            return redirect('contact:login')

    return render(
        request,
        'contact/register.html',
        {
            'form': form
        }
    )

def login(request):
    form = AuthenticationForm(request)

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.success(request, 'Logado com sucesso!')
            return redirect('contact:index')
        
        messages.error(request, 'Login inválido')

    return render(
        request,
        'contact/login.html',
        {
            'form': form
        }
    )

# Caso o usuário não esteja logado, irá ser redirecionado para a página de login
@login_required(login_url='contact:login')
def user_update(request):
    form = RegisterUpdateForm(instance=request.user)

    if request.method != 'POST':
        return render(
            request,
            'contact/register.html',
            {
                'form': form
            }
        )
    form = RegisterUpdateForm(data=request.POST, instance=request.user)

    if not form.is_valid():
         return render(
            request,
            'contact/register.html',
            {
                'form': form
            }
        )
    
    form.save()
    return redirect('contact:user_update')
        
@login_required(login_url='contact:login')
def logout(request):
    auth.logout(request)
    return redirect('contact:login')
