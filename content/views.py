from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic

from content.forms import (
    ContentTypeForm,
    TaskForm,
    TaskSearchForm,
)
from content.models import ContentType, Task


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = "content/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["staff_num"] = get_user_model().objects.count()
        context["tasks_num"] = Task.objects.count()
        context["content_types_num"] = ContentType.objects.count()
        return context


class ContentTypeListView(LoginRequiredMixin, generic.ListView):
    model = ContentType
    template_name = "content/content_type_list.html"
    context_object_name = "content_type_list"
    paginate_by = 5


class ContentTypeCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = ContentTypeForm
    template_name = "content/content_type_form.html"
    success_url = reverse_lazy("content:content-type-list")


class ContentTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = ContentType
    form_class = ContentTypeForm
    template_name = "content/content_type_form.html"
    success_url = reverse_lazy("content:content-type-list")


class ContentTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = ContentType
    template_name = "content/content_type_confirm_delete.html"
    success_url = reverse_lazy("content:content-type-list")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = (Task.objects.select_related("content_type")
                    .prefetch_related("staff"))
        name = self.request.GET.get("name")
        if name:
            return queryset.filter(
                Q(name__icontains=name) | Q(staff__username__icontains=name)
            )
        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = (Task.objects.select_related("content_type")
                .prefetch_related("staff"))


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = TaskForm
    template_name = "content/task_form.html"
    success_url = reverse_lazy("content:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "content/task_form.html"
    success_url = reverse_lazy("content:task-list")


class UpdateTaskStaffView(LoginRequiredMixin, generic.RedirectView):
    pattern_name = "content:task-list"

    def get_redirect_url(self, *args, **kwargs):
        queryset = Task.objects.prefetch_related("staff")
        task = get_object_or_404(queryset, id=kwargs["pk"])
        if self.request.user in task.staff.all():
            task.staff.remove(self.request.user)
        else:
            task.staff.add(self.request.user)
        return super().get_redirect_url()


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("content:task-list")
