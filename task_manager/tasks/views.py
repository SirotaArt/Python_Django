from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required  # ← ДОБАВИЛИ
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render  # ← ДОБАВИЛИ render
from django.db.models import Q
from .models import Task, Category
from .forms import TaskForm

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 5
    
    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        
        # Фильтрация по статусу
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Фильтрация по категории
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        
        # Фильтрация по приоритету
        priority = self.request.GET.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
        
        # Поиск
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.status = 'completed'
    task.save()
    return redirect('task_list')

#Функция дашборда
@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)
    
    # Статистика
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='completed').count()
    pending_tasks = tasks.filter(status='pending').count()
    high_priority_tasks = tasks.filter(priority='high').count()
    
    # Просроченные задачи
    overdue_tasks = 0
    for task in tasks.filter(status='pending'):
        if task.is_overdue():
            overdue_tasks += 1
    
    # Процент выполнения
    completion_rate = 0
    if total_tasks > 0:
        completion_rate = int((completed_tasks / total_tasks) * 100)
    
    # Последние 3 задачи
    recent_tasks = tasks.order_by('-created_at')[:3]
    
    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'high_priority_tasks': high_priority_tasks,
        'overdue_tasks': overdue_tasks,
        'completion_rate': completion_rate,
        'recent_tasks': recent_tasks,
    }
    
    return render(request, 'tasks/dashboard.html', context)