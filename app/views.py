from django.views.generic import ListView
from app.models import RealityPost


class RealityPostList(ListView):
    model = RealityPost
    paginate_by = 10
    queryset = RealityPost.objects.order_by('-date')
    template_name = 'app/realitypost_list.html'
