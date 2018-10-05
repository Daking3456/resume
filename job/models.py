from django.db import models
from django.utils.text import slugify
from django.conf import settings
from accounts.models import Company, User
from django.urls.base import reverse



class Field(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self):
        return ('{}'.format(self.name))

class Job(models.Model):
    """
    Author: Daking Rai (daking.rai@infodevelopers.com.np)
    Date: July 05, 2018
   
    fulltime parttime contract Internship student_work
    """
    title = models.CharField(max_length=250)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    job_field = models.ForeignKey(Field, on_delete=models.CASCADE)
    type_of_job = models.CharField(max_length=100)      #  facitated
    contract_type = models.IntegerField()               #  facitated
    level_of_job = models.CharField()                   ## senior mid associate etry   facitated

    description = models.TextField(null=True, blank=True)
    responsibilities = models.TextField(null=True, blank=True)
    skills_qualification = models.TextField()
    requirements = models.TextField(null=True, blank=True)
    
    experience = models.CharField() 
    no_opening = models.IntegerField(null= True, blank=True)

    deadline = models.DateTimeField()

    benifits = models.TextField(null=True, blank=True)
    salary = models.IntegerField(null=True, blank=True)
  

    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    tags = models.CharField(max_length=200, null=True, blank=True)


    class Meta:
        db_table = 'job'
        verbose_name_plural = 'jobs'

    def __str__(self):
        return ('{}'.format(self.title))

    def save(self, **kwargs):
        slug_str = "%s %s %s" % (self.title, self.company.user.username,self.created_at)
        self.slug = slugify(self, slug_str)
        super(Job, self).save(**kwargs)
    def get_absolute_url(self):
        return reverse('job_detail',kwargs={'slug': self.slug})



class Applicant (models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    job = models.ForeignKey(Job, on_delete= models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to="uploads/resume/%Y/%m/%d/")
    date_applied = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ('{}{}'.format(self.applicant.username, self.job.title))


class TempResume(models.Model):
    temp_resume = models.FileField(upload_to="uploads/temp/resume/%Y/%m/%d/")

class ParsedResume(models.Model):
    applied_for = models.TextField(null=True, blank=True)
    personal_info = models.TextField(null=True, blank=True)
    education = models.TextField(null=True, blank=True)
    experience = models.TextField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)


