from django.db import models
from solo.models import SingletonModel
# Create your models here.

report_choices = [
    ('Complete', 'Complete'),
    ('Failed', 'Failed'),
    ('Inprogress', 'Inprogress'),]

error_choices = [
    ("file_not_found","File not found"),
    ("no_file_with_unique_content","No file with unique content"),
    ("unknown_file_extension","Unknown file extension"),
    ("unknown_author","Unknown author"),
    ("threshold_not_found","Threshold not found")
]


class File(models.Model):
    file                  =    models.FileField(upload_to='documenmt/')
    author                =    models.CharField(max_length=90,null=True,blank=True)
    created_at            = models.DateTimeField(blank=True,null=True)
    word_count            = models.CharField(max_length=90)

    
    def __str__(self) -> str:
        return self.author
    


class Task(models.Model):
    author                      =    models.CharField(blank=True,max_length=100)
    files                        =    models.ManyToManyField(File, blank=True)
    year_details                   =    models.JSONField( null=True, blank=True)
    progress                    =    models.FloatField(default=0, blank=True)
    complete                    =    models.BooleanField(default=False, blank=True)
    threshold_similarity        =    models.IntegerField(default=0, blank=True)
    threshold_file              =    models.IntegerField(default=0, blank=True)
    status                      =    models.CharField(max_length=100, choices=report_choices, null=True, blank=True)
    error                       =    models.CharField(max_length=100, choices=error_choices, null=True, blank=True)
    selected_files              =    models.ManyToManyField(File, related_name='selected_files', blank=True)
    completed_file              =    models.IntegerField(default=0, blank=True)
    created_at                  =    models.DateTimeField(auto_now_add=True)
    updated_at                  =    models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self) -> str:
        return self.author
 
        

DEFAULT_SINGLETON_INSTANCE_ID = 1

class SingletonModel(models.Model):
    singleton_instance_id = DEFAULT_SINGLETON_INSTANCE_ID

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = self.singleton_instance_id
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(SingletonModel, self).delete(*args, **kwargs)

class Threshold(SingletonModel):
    min_file        =   models.IntegerField(default=5)
    similarity_score  =   models.IntegerField(default=70)
    
    def __str__(self):
        return "App Configuration"

    class Meta:
        verbose_name = "App Configuration"
        
