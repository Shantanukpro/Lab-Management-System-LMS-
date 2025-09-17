from rest_framework import serializers
from labs.models import Lab, PC

class PCSerializer(serializers.ModelSerializer):
    class Meta:
        model = PC
        fields = '__all__'   # all fields of PC

class LabSerializer(serializers.ModelSerializer):
    pcs = PCSerializer(many=True, read_only=True, source='pc_set')  

    class Meta:
        model = Lab
        fields = '__all__'
