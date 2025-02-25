# notifications/views.py
from django.http import JsonResponse
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from .models import Notification


class MarkAllReadView(LoginRequiredMixin, View):
    def post(self, request):
        Notification.objects.filter(user=request.user).update(is_read=True)
        return JsonResponse({'success': True})


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'list.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')


class MarkAsReadView(LoginRequiredMixin, View):
    def post(self, request, pk):
        notification = Notification.objects.get(pk=pk, user=request.user)
        notification.is_read = True
        notification.save()
        return redirect('notifications:list')
