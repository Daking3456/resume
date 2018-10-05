import datetime
from haystack import indexes
from job.models import Job

class JobIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	title = indexes.EdgeNgramField(model_attr='title')

	company = indexes.EdgeNgramField(model_attr='company')
	responsibilities = indexes.CharField(model_attr='responsibilities')
	qualification = indexes.CharField(model_attr='qualification')
	education = indexes.CharField(model_attr='education')
	
	description = indexes.CharField(model_attr='description')
	requirements = indexes.CharField(model_attr='requirements')
	type_of_job = indexes.CharField(model_attr='type_of_job', faceted=True)
	type_job = indexes.EdgeNgramField(model_attr='type_of_job')
	job_field = indexes.EdgeNgramField(model_attr='job_field')
	tags = indexes.CharField(model_attr='tags')
	# content_auto = indexes.EdgeNgramField(model_attr='title')


	def get_model(self):
		return Job

	def index_queryset(self, using=None):
		"""Used when the entire index for model is updated."""
		return self.get_model().objects.all()