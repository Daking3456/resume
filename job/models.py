from django.db import models
from django.utils.text import slugify
from django.conf import settings

class Address(models.Model):
	"""
	Author: Daking Rai (daking.rai@infodevelopers.com.np)
	Date: July 04, 2018
	Description: Address model that is used by company.
	"""
	city = models.CharField(max_length=200, null=True)
	country = models.CharField(max_length=200, null=True)
	zip_code = models.CharField(max_length=200, null=True)
	address1 = models.CharField(max_length=200, null=True)
	address2 = models.CharField(max_length=200, null=True)

	class Meta:
		db_table = 'addresses'
		verbose_name_plural = 'addresses'

	def __str__(self):
		return ('{},{}'.format(self.city,self.country))


class Company(models.Model):
    """
    Author: Daking Rai (daking.rai@infodevelopers.com.np)
    Date: July 04, 2018
    """
    name = models.CharField(max_length=150)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    website = models.CharField(max_length=300, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = 'company'
        verbose_name_plural = 'companies'

    def __str__(self):
        return ('{}'.format(self.name))

    def save(self, **kwargs):
        slug_str = "%s" % (self.name)
        self.slug = slugify(self, slug_str)
        super(Company, self).save(**kwargs)

class Job(models.Model):
    """
    Author: Daking Rai (daking.rai@infodevelopers.com.np)
    Date: July 05, 2018
    """
    title = models.CharField(max_length=250)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    responsibilities = models.TextField(null=True, blank=True)
    qualification = models.TextField(null=True, blank=True)
    education = models.CharField(max_length=500, null=True, blank=True)
    salary = models.IntegerField(null=True, blank=True)
    no_opening = models.IntegerField(null= True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    status = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    tags = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'job'
        verbose_name_plural = 'jobs'

    def __str__(self):
        return ('{}'.format(self.title))

    def save(self, **kwargs):
        slug_str = "%s %s %s" % (self.title, self.company.name,self.created_at)
        self.slug = slugify(self, slug_str)
        super(Job, self).save(**kwargs)



