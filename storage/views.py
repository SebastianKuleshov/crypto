from django.shortcuts import render
from .models import Storage
from .forms import StorageForm
from .mixins import SuperUserMixin
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.db import transaction as dj_transaction
# Create your views here.

# @login_required()
@permission_required('is_superuser')
# @user_passes_test(lambda u: u.is_superuser, login_url='/users/login')
def storage(request):

    form = StorageForm()    
    token_list = Storage.objects.all()
    context = {"token_list": token_list, "form": form}
    if request.method == 'POST':
        form = StorageForm(request.POST)
        token = request.POST['token']
        count = request.POST['count']
        storage = Storage.objects.filter(token=token).first()
        with dj_transaction.atomic():
            if storage is not None:
                storage.count += float(count)
                storage.save()
            else:
                form.save()
        return render(request, 'storage/storage.html', context=context)

    return render(request, 'storage/storage.html', context=context)

class StorageUpdateView(UpdateView):
    model = Storage
    form_class = StorageForm
    template_name = 'storage/update.html'
    success_url = '/storage/'

class StorageDeleteView(SuperUserMixin, DeleteView):    
    model = Storage
    template_name = 'storage/delete.html'
    success_url = '/storage'

    def get(self, *args, **kwargs):
        return self.delete(*args, **kwargs)