from service_objects.services import ServiceWithResult
from models_app.models import Tag


class TagListService(ServiceWithResult):

    def process(self):
        self.result = self._tags
        return self

    @property
    def _tags(self):
        return Tag.objects.all()
