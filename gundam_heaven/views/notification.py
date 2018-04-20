from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect

from gundam_heaven.models import Notification



class NotificationListView(LoginRequiredMixin, ListView):
    template_name = 'gundam_heaven/notification_list.html'
    model = Notification
    context_object_name = 'notifications'
    login_url = reverse_lazy('gundam_heaven:login')
    paginate_by = 3

    def get_queryset(self):
        qs = super().get_queryset()
        type = self.request.GET.get('type', 1)
        return qs.filter(owner=self.request.user, type=int(type))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        type = self.request.GET.get('type', '1')
        context['type'] = type
        context['unread_amt'] = self.get_queryset().count()
        return context

@login_required(login_url=reverse_lazy('gundam_heaven:login'))
@require_POST
def read_notification(request):
    notification = get_object_or_404(Notification, id=request.POST['noti_id'])
    notification.has_read = True
    notification.save()
    return redirect(request.POST['forward'])



