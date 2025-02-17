from django.db import models
from django.contrib.auth.models import User
from polls.models import Question

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=500)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.question.question_text}"