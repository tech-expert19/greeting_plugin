from django.db import models
from django.contrib.auth import get_user_model

USER = get_user_model()


class UserGreetings(models.Model):
    user = models.ForeignKey(USER, related_name='user_greetings', on_delete=models.CASCADE)
    message = models.CharField(max_length=250, null=False, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}:{self.user.get_username()}"

    class Meta:
        ordering = ['-date_added']
        verbose_name = 'User Greeting'
        verbose_name_plural = 'User Greetings'
