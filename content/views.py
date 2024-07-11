from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from content.forms import (
    ContentTypeForm,
    TaskForm,
    TaskSearchForm,
)
from content.models import ContentType, Task


@login_required
def index(request: HttpRequest) -> HttpResponse:
    """View function for the home page."""
    content_types_num = ContentType.objects.count()
    staff_num = get_user_model().objects.count()
    tasks_num = Task.objects.count()
    context = {
        "content_types_num": content_types_num,
        "staff_num": staff_num,
        "tasks_num": tasks_num,
    }
    return render(request, "content/index.html", context=context)


@login_required
def update_task_staff(request: HttpRequest, pk: int) -> HttpResponse:
    task = Task.objects.prefetch_related("staff").get(id=pk)
    if request.user in task.staff.all():
        task.staff.remove(request.user)
    else:
        task.staff.add(request.user)

    return redirect(reverse("content:task-list"), pk)


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


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("content:task-list")
