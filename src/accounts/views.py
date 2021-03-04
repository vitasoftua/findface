from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View


class UserTakeWebNotificationView(LoginRequiredMixin, View):
    """View to update user's field."""

    def post(self, request, *args, **kwargs):
        """Process user data."""
        user = request.user
        user.is_take_web_notification = not user.is_take_web_notification
        user.save(update_fields=['is_take_web_notification'])
        return redirect(reverse_lazy('index'))
