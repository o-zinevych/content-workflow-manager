from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Prefetch
from django.urls import reverse_lazy
from django.views import generic

from content.models import Task
from staff_manager.forms import (
    PositionForm,
    PositionSearchForm,
    StaffChangeForm,
    StaffCreationForm,
    StaffSearchForm,
)
from staff_manager.models import Position


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = PositionSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = Position.objects.all()
        name = self.request.GET.get("name")
        if name:
            return queryset.filter(name__icontains=name)
        return queryset


class PositionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Position
    queryset = Position.objects.prefetch_related("staff")


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = PositionForm
    template_name = "content/position_form.html"
    success_url = reverse_lazy("positions:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    form_class = PositionForm
    template_name = "content/position_form.html"
    success_url = reverse_lazy("positions:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("positions:position-list")


class StaffListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    paginate_by = 7

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StaffListView, self).get_context_data(**kwargs)
        staff = self.request.GET.get("staff", "")
        context["search_form"] = StaffSearchForm(initial={"staff": staff})
        return context

    def get_queryset(self):
        queryset = get_user_model().objects.prefetch_related("position")
        staff = self.request.GET.get("staff")
        if staff:
            return queryset.filter(
                Q(username__icontains=staff)
                | Q(first_name__icontains=staff)
                | Q(last_name__icontains=staff)
            )
        return queryset


class StaffDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()
    queryset = get_user_model().objects.prefetch_related(
        "position",
        Prefetch("tasks", queryset=Task.objects.filter(is_finished=False))
    )

    def get_context_data(self, **kwargs):
        context = super(StaffDetailView, self).get_context_data(**kwargs)
        staff = self.get_object()
        unfinished_tasks = staff.tasks.filter(is_finished=False)
        context["unfinished_tasks"] = unfinished_tasks
        return context


class StaffCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = StaffCreationForm
    template_name = "staff_manager/staff_form.html"
    success_url = reverse_lazy("staff:staff-list")


class StaffUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = StaffChangeForm
    template_name = "staff_manager/staff_form.html"
    success_url = reverse_lazy("staff:staff-list")


class StaffDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("staff:staff-list")
