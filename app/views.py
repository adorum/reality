from django.views.generic import ListView
from app.models import RealityPost


class RealityPostList(ListView):
    model = RealityPost
    paginate_by = 30
    queryset = RealityPost.objects.order_by('-date_updated', '-date_created')
    template_name = 'app/realitypost_list.html'
