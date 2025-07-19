from django.db import models
from django.utils import timezone


# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    posted_at = models.DateTimeField(default=timezone.now)
    due_at = models.DateTimeField(null=True, blank=True)
    likes = models.IntegerField(default=0)

    def is_overdue(self, dt):
        if self.due_at is None:
            return False
        return self.due_at < dt

# コメントモデル
class Comment(models.Model):
    text = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"Comment on '{self.task.title}' at {self.created_at.strftime('%Y-%m-%d %H:%M')}"
