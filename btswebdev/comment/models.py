from django.db import models
from entry.models import Entry
from django.contrib.auth.models import User


class Comment(models.Model):
	comment_id = models.BigAutoField(primary_key=True)
	comment_text = models.TextField(max_length=300)
	comment_date = models.DateTimeField(auto_now=True)
	entry_id = models.ForeignKey(Entry, on_delete=models.CASCADE)
	staff_id = models.ForeignKey(User, on_delete=models.CASCADE)

class CommentImage(models.Model):
	comment_image_id = models.BigAutoField(primary_key=True)
	comment_image_desc = models.TextField(null=True, blank=True, max_length=200)
	comment_image_file = models.ImageField(upload_to="images/")
	comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE)

	def get_absolute_url(self):
		return f"image/{self.comment_image_id}"