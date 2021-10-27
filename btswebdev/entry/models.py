from django.db import models
from report.models import Report


# Create your models here.
# Entry model is mapped to the database 
class Entry(models.Model):
	entry_id = models.BigAutoField(primary_key=True)
	entry_title = models.TextField(max_length=100) # the title of the entry with a text limit of 100
	entry_content = models.TextField(max_length=500) # the actual content of the entry field with a text limit of 500
	entry_date = models.DateTimeField(auto_now=True) # the time that the entry was created
	report_id = models.ForeignKey(Report, on_delete=models.CASCADE)

	def get_absolute_url(self):
		return f"entry/{self.entry_id}"



class EntryImage(models.Model):
	entry_image_id = models.BigAutoField(primary_key=True)
	entry_image_desc = models.TextField(null=True, blank=True, max_length=200)
	entry_image_file = models.ImageField(upload_to="images/")
	entry_id = models.ForeignKey(Entry, on_delete=models.CASCADE)

	def get_absolute_url(self):
		return f"image/{self.entry_image_id}"


