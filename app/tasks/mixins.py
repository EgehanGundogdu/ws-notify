from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import ImproperlyConfigured


class FormViewsButtonLabelContextMixin:
    def get_context_data(self, **kwargs):
        if getattr(self, "button_label_text", None) is None:
            raise ImproperlyConfigured(
                f"button_label_text not provided for {self.__class__.__name__}"
            )
        if not isinstance(self.button_label_text, str):
            raise ImproperlyConfigured(f"button_label_text value must be str.")
        context = super().get_context_data(**kwargs)
        context["button_text"] = self.button_label_text
        return context


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self) -> bool:
        return self.request.user.is_staff