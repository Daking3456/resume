from haystack import indexes
from haystack.fields import CharField

from .models import Job


class JobIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(
        document=True, use_template=True,
        template_name='search/indexes/job_text.txt')
    title = indexes.CharField(model_attr='title')
    responsibilities = indexes.EdgeNgramField(model_attr="description", null=True)

    job_type = indexes.CharField(model_attr='job_type', faceted=True)

    # experience = indexes.CharField(model_attr='experience', faceted=True)

    salary = index.CharField(model_attr='salary', faceted=True)
    # for auto complete
    content_auto = indexes.EdgeNgramField(model_attr='title')

    # Spelling suggestions
    suggestions = indexes.FacetCharField()

    def get_model(self):
        return Job

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
