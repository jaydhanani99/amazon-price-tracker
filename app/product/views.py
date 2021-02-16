from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Product
from product import serializers

from django.http import HttpResponse
from django.views.generic import View
import subprocess

class ProductViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Manage products in database"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all()

    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        """Return objects for current authenticated user only"""

        return self.queryset.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        """Create a new Product"""

        serializer.save(user=self.request.user)


class ExecutePythonFileView(View):
    def get(self, request):
        # Execute script
        subprocess.call(['python', 'track_product.py'])
        # Return response
        return HttpResponse("Executed!")