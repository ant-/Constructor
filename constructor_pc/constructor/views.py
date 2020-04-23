from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.views import generic
from constructor import models


def home(request):
    template = 'home.html'
    return render(request, template)


def parts_view(request):
    if request.GET:
        return render(request, 'product_list.html')
    return render(request, 'parts.html')


class ProdListView(generic.ListView):
    model = models.Product
    template_name = 'product_list.html'
    paginate_by = 15
    category = int()

    def get_queryset(self):
        return models.Product.objects.filter(category_id=self.category)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['count'] = models.Product.objects.filter(category_id=self.category).count()
        context_data['is_manager'] = self.request.user.groups.filter(name='Manager').exists()
        return context_data

    def get(self, request, *args, **kwargs):
        # breakpoint()
        for key in request.GET:
            if key.isdigit():
                self.category = key
                return super().get(request, args, kwargs)


class DetailView(generic.DetailView):
    model = models.Product
    template_name = 'detail.html'
