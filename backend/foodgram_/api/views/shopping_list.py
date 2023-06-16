from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from api.services.shopping_list.delete import ShoppingListDeleteService


class ShoppingListDeleteView(APIView):

    def delete(self, request, *args, **kwargs):
        ServiceOutcome(ShoppingListDeleteService, kwargs | {"user": request.user})
        return Response({}, status=status.HTTP_204_NO_CONTENT)
