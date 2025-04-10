from django.db import models

class GeneratedWebsite(models.Model):
    business_type = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    html_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Feedback(models.Model):
    user_email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_email