from haystack import indexes
from .models import Car

class CarIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    brand = indexes.CharField(model_attr='brand')
    model = indexes.CharField(model_attr='model')
    year = indexes.IntegerField(model_attr='year')
    price = indexes.DecimalField(model_attr='price')

    def get_model(self):
        return Car

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()