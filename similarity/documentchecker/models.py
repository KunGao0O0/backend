from django.db import models
from .utils import extracttext,get_doc_text
import os
from django.utils.functional import cached_property
from django.core.validators import MaxValueValidator, MinValueValidator
import spacy

nlp=spacy.load("en_core_web_lg")
nlp.max_length = 10000000

# Create your models here.

report_choices = [
    ('Complete', 'Complete'),
    ('Failed', 'Failed'),
    ('Inprogress', 'Inprogress'),]

error_choices = [
    ("1","File not found"),
    ("2","No file with unique content"),
    ("3","Unknown author"),
    ("4","Threshold not found"),
    ("5","Error in file"),
]


class File(models.Model):
    file                  = models.FileField(upload_to='documenmt/')
    author                = models.CharField(max_length=90,null=True,blank=True)
    created_at            = models.DateTimeField(blank=True,null=True)
    word_count            = models.CharField(max_length=90)
    error                 = models.JSONField()
    is_error = models.BooleanField(default=False)

    
    def __str__(self) -> str:
        return "{}-{}-{}".format(self.author,str(self.file.name) , self.created_at)
    
    @cached_property
    def text(self):
        error = False
        text  = ""
        try:
            extension = os.path.splitext(str(self.file.name))[-1].lower()
            if extension == '.docx':
                text = extracttext(self.file)
            elif extension == '.doc':
                text = get_doc_text(self.file)
        except Exception as e:
            error = True
            text = str(e)
        return text, error
    
    @cached_property
    def clean_text(self):
    #  "nlp" Object is used to create documents with linguistic annotations.
        error = False
        text, texterror = self.text
        if texterror:
            return text, texterror
        try:
            my_doc = nlp(text)
            # Create list of word tokens
            token_list = []
            for token in my_doc:
                token_list.append(token.text)
            # Create list of word tokens after removing stopwords
            filtered_sentence =[]
            for word in token_list:
                lexeme = nlp.vocab[word]
                if lexeme.is_stop == False:
                    filtered_sentence.append(word)
            filtered_text = (" ").join(filtered_sentence)
        except Exception as e:
            filtered_text = str(e)
            error = True
        return filtered_text , error


class Task(models.Model):
    authors                      =    models.JSONField(blank=True,null=True)
    files                       =    models.ManyToManyField(File, blank=True)
    year_details                =    models.JSONField( null=True, blank=True)
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

    @classmethod
    def get_solo(cls):
        obj, created = cls.objects.get_or_create(pk=cls.singleton_instance_id)
        return obj

class Threshold(SingletonModel):
    min_year = models.IntegerField(default=1)
    min_files_per_year = models.IntegerField(default=1)
    min_files = models.IntegerField(default=5)
    similarity_score = models.IntegerField(default=70 ,validators=[MaxValueValidator(100),MinValueValidator(1)])

    def __str__(self):
        return "App Configuration"

    class Meta:
        verbose_name = "App Configuration"
        
