import datetime
from haystack import indexes
from job.models import Job

class JobIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	title = indexes.EdgeNgramField(model_attr='title')

	company = indexes.EdgeNgramField(model_attr='company')
	responsibilities = indexes.CharField(model_attr='responsibilities')

	industry = indexes.CharField(model_attr='job_field', faceted=True)
	type_of_job = indexes.CharField(model_attr='type_of_job', faceted=True)
	contract_type = indexes.CharField(model_attr='contract_type', faceted=True)
	level_of_job = indexes.CharField(model_attr='level_of_job', faceted=True)
	experience = indexes.CharField(model_attr='experience', faceted=True)
	
	description = indexes.CharField(model_attr='description')
	requirements = indexes.CharField(model_attr='requirements')
	tags = indexes.EdgeNgramField(model_attr='tags')
	

	content_auto = indexes.EdgeNgramField(model_attr='title')


	def get_model(self):
		return Job

	def index_queryset(self, using=None):
		"""Used when the entire index for model is updated."""
		return self.get_model().objects.all()

	def prepare_type_of_job(self, obj):
		return obj.get_type_of_job_display()

	def prepare_contract_type(self, obj):
		return obj.get_contract_type_display()

	def prepare_level_of_job(self, obj):
		return obj.get_level_of_job_display()

	def prepare_experience(self, obj):
		return obj.get_experience_display()
