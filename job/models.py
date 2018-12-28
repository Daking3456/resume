from django.db import models
from django.utils.text import slugify
from accounts.models import Company, User
from django.urls.base import reverse


class Field(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.name)


class Job(models.Model):
    """
    Author: Daking Rai (daking.rai@infodevelopers.com.np)
    Date: July 05, 2018
    """

    LEVEL_CHOICES = (
        (1, "Senior Level"),
        (2, "Mid Level"),
        (3, "Associate Level"),
        (4, "Entry Level"),
        )

    TYPE_CHOICES = (
        (1, "Full Time"),
        (2, "Part Time"),
        (3, "Internship"),
        (4, "Contract"),
        (5, "Student Work"),
        )

    CONTRACT_CHOICES = (
        (1, "Permanent"),
        (2, "Temporary"),
     
        )

    EXPERIENCE_CHOICES = (
        (1, "0-1 Years"),
        (2, "1-3 Years"),
        (3, "3-5 Years"),
        (4, "5+ "),
        )

    title = models.CharField(max_length=250)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    job_field = models.ForeignKey(Field, on_delete=models.CASCADE)
    type_of_job = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)
    contract_type = models.PositiveSmallIntegerField(choices=CONTRACT_CHOICES)
    level_of_job = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES)

    description = models.TextField(null=True, blank=True)
    responsibilities = models.TextField(null=True, blank=True)
    skills_qualification = models.TextField()
    requirements = models.TextField(null=True, blank=True)
    
    experience = models.PositiveSmallIntegerField(choices=EXPERIENCE_CHOICES) 
    no_opening = models.IntegerField(null=True, blank=True)

    benefits = models.TextField(null=True, blank=True)
    salary = models.PositiveIntegerField(null=True, blank=True)
  
    deadline = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    tags = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'job'
        verbose_name_plural = 'jobs'

    def __str__(self):
        return '{}'.format(self.title)

    def save(self, **kwargs):
        slug_str = "%s %s %s" % (self.title, self.company.user.username, self.created_at)
        self.slug = slugify(self, slug_str)
        super(Job, self).save(**kwargs)

    def get_absolute_url(self):
        return reverse('job_detail', kwargs={'slug': self.slug})


class Applicant (models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to="uploads/resume/%Y/%m/%d/")
    date_applied = models.DateTimeField(auto_now_add=True)
    resume_score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '{}{}'.format(self.applicant.username, self.job.title)


class TempResume(models.Model):
    temp_resume = models.FileField(upload_to="uploads/temp/resume/%Y/%m/%d/")


class ParsedResume(models.Model):
    applied_for = models.TextField(null=True, blank=True)
    personal_info = models.TextField(null=True, blank=True)
    education = models.TextField(null=True, blank=True)
    experience = models.TextField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    grad_degree = models.NullBooleanField(null=True, blank=True)
    undergrad_degree = models.NullBooleanField(null=True, blank=True)
    total_experience = models.TextField(null=True, blank=True)
    skills_present = models.TextField(null=True, blank=True)
    resume_score = models.IntegerField(null=True, blank=True)
