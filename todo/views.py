from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from todo.models import Task, Comment


# Create your views here.

def index(request):
    if request.method == "POST":
        task = Task(title=request.POST["title"], due_at=make_aware(parse_datetime(request.POST["due_at"])))
        task.save()

    if request.GET.get('order') == 'due':
        tasks = Task.objects.order_by('due_at')
    else:
        tasks = Task.objects.order_by('-posted_at')

    context = {
        "tasks": tasks
    }
    return render(request, "todo/index.html", context)


def detail(request, task_id):    
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    if request.method == 'POST':
        if 'like' in request.POST:
            task.likes += 1
            task.save()
        elif 'text' in request.POST:
            comment = Comment(task=task, text=request.POST['text'])
            comment.save()

    context = {
        "task": task,
        'comments': task.comments.order_by('-posted_at')
    }
    return render(request, "todo/detail.html", context)

def update(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    if request.method == 'POST':
        task.title = request.POST['title']
        task.due_at = make_aware(parse_datetime(request.POST['due_at']))
        task.save()
        return redirect('detail', task_id=task.id)

    context = {
        'task': task
    }
    return render(request, "todo/edit.html", context)

def delete(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    task.delete()
    return redirect('index')

def close(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = True
    task.save()
    return redirect('index')
