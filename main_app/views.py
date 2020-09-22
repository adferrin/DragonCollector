from django.shortcuts import render, redirect

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DeleteView, ListView

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Toy, Dragon 
from .forms import FeedingForm



# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

@login_required
def dragons_index(request):
    dragons = Dragon.objects.filter(user=request.user)
    return render(request, 'dragons/index.html', { 'dragons': dragons })

@login_required
def dragons_detail(request, dragon_id):
    dragon = Dragon.objects.get(id=dragon_id)
    toys_dragon_doesnt_have = Toy.objects.exclude(id__in = dragon.toys.all().values_list('id'))
    feeding_form = FeedingForm()
    return render(request, 'dragons/detail.html', {
        'dragon': dragon, 
        'feeding_form': feeding_form,
        'toys': toys_dragon_doesnt_have 
    })

@login_required
def add_feeding(request, dragon_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        # don't save the form to the db until it
        # has the cat_id assigned
        new_feeding = form.save(commit=False)
        new_feeding.dragon_id = dragon_id
        new_feeding.save()
    return redirect('detail', dragon_id=dragon_id)

@login_required    
def assoc_toy(request, dragon_id, toy_id):
    Dragon.objects.get(id=dragon_id).toys.add(toy_id)
    return redirect('detail', dragon_id=dragon_id)

def toys_index(request):
    toys = Toy.objects.all()
    return render(request, 'toys/index.html', { 'toys': toys })

def toys_detail(request, toy_id):
    toy = Toy.objects.get(id=toy_id)
    return render(request, 'toys/detail.html', { 'toy': toy })

class DragonCreate(LoginRequiredMixin, CreateView):
    model = Dragon
    fields = ['name', 'breed', 'description', 'age']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class DragonUpdate(LoginRequiredMixin, UpdateView):
    model = Dragon
    fields = ['breed', 'description', 'age']

class DragonDelete(LoginRequiredMixin, DeleteView):
    model = Dragon
    success_url = '/dragons/'


class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = '__all__'

class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = '__all__'

class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys/'