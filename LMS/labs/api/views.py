from rest_framework import viewsets
from labs.models import Lab, PC
from .serializers import LabSerializer, PCSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class LabViewSet(viewsets.ModelViewSet):
    queryset = Lab.objects.all().order_by('id')
    serializer_class = LabSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class PCViewSet(viewsets.ModelViewSet):
    queryset = PC.objects.all().order_by('id')
    serializer_class = PCSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        lab_id = self.request.query_params.get('lab', None)
        if lab_id:
            qs = qs.filter(lab_id=lab_id)
        return qs
