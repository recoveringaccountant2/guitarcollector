# from io import BufferedRandom
from django.shortcuts import render, redirect 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.mixins import LoginRequiredMixin 
from .models import Guitar, Accessory, Photo 
from .forms import RestringForm 
import uuid
import boto3
# from django.http import HttpResponse

BUCKET = 'guitarcollector2201'
S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'

# Create your views here.

class GuitarCreate(LoginRequiredMixin, CreateView):
    model = Guitar
    fields = ['name', 'brand', 'description', 'year']
    # This inherited method is called when a
    # valid guitar form is being submitted
    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  # form.instance is the guitar
        # Let the CreateView do its job as usual
        return super().form_valid(form)

class GuitarUpdate(LoginRequiredMixin, UpdateView):
    model = Guitar
    # Let's disallow the renaming of a guitar by excluding the name field
    fields = ['brand', 'description', 'year']

class GuitarDelete(LoginRequiredMixin, DeleteView):
    model = Guitar
    success_url = '/guitars/'

# Define the home view
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

@login_required
def guitars_index(request):
    # guitars = Guitar.objects.all()
    guitars = Guitar.objects.filter(user=request.user)
    return render(request, 'guitars/index.html', { 'guitars': guitars })

@login_required
def guitars_detail(request, guitar_id):
    guitar = Guitar.objects.get(id=guitar_id)
    accessories_guitar_doesnt_have = Accessory.objects.exclude(id__in = guitar.accessories.all().values_list('id'))
    restring_form = RestringForm()
    return render(request, 'guitars/detail.html', {
        'guitar': guitar, 'restring_form': restring_form,
        'accessories': accessories_guitar_doesnt_have
    })

@login_required
def add_restring(request, guitar_id):
    # create a ModelForm instance using the data in request.POST
    form = RestringForm(request.POST)
    # validate the form
    if form.is_valid():
        # don't save the form to the db until it
        # has the guitar_id assigned
        new_restring = form.save(commit=False)
        new_restring.guitar_id = guitar_id
        new_restring.save()
    return redirect('detail', guitar_id=guitar_id)

class AccessoryList(LoginRequiredMixin, ListView):
    model = Accessory

class AccessoryDetail(LoginRequiredMixin, DetailView):
    model = Accessory

class AccessoryCreate(LoginRequiredMixin, CreateView):
    model = Accessory
    fields = '__all__'

class AccessoryUpdate(LoginRequiredMixin, UpdateView):
    model = Accessory
    fields = ['name', 'description']

class AccessoryDelete(LoginRequiredMixin, DeleteView):
    model = Accessory
    success_url = '/accessories/'

@login_required
def assoc_accessory(request, guitar_id, accessory_id):
    Guitar.objects.get(id=guitar_id).accessories.add(accessory_id)
    return redirect('detail', guitar_id=guitar_id)

@login_required
def add_photo(request, guitar_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to guitar_id or guitar (if you have a guitar object)
            Photo.objects.create(url=url, guitar_id=guitar_id)
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', guitar_id=guitar_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in via code
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)