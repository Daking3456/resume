import datetime
from haystack import indexes
from haystack.fields import CharField
from job.models import Job


class JobIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    title = indexes.EdgeNgramField(model_attr='title')
    # responsibilities = indexes.CharField(model_attr='responsibilities')
    # qualification = indexes.CharField(model_attr='qualification')
    # education = indexes.CharField(model_attr='education')
    # description = indexes.CharField(model_attr='description')
    # requirements = indexes.CharField(model_attr='requirements')
    # type_of_job = indexes.CharField(model_attr='type_of_job')
    

    def get_model(self):
        return Job

    # def index_queryset(self, using=None):
    #     "Used when the entire index for model is updated."
    #     return self.get_model().objects.filter(created_at__lte=datetime.datetime.now())

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
        created_at__lte=datetime.datetime.now())
