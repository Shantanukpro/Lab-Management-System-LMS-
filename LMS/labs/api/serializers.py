from rest_framework import serializers
from labs.models import Lab, PC

class PCSerializer(serializers.ModelSerializer):
    class Meta:
        model = PC
        fields = [
            'id','lab','asset_tag','hostname','serial_number','ip_address','mac_address',
            'manufacturer','model','cpu','cpu_cores','ram_mb','storage_gb',
            'os_name','os_version','purchased_on','warranty_until',
            'is_defective','defective_reason','last_checked_at','created_at','updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class LabSerializer(serializers.ModelSerializer):
    pc_count = serializers.IntegerField(source='pc_set.count', read_only=True)
    pcs = PCSerializer(many=True, source='pc_set', read_only=True)

    class Meta:
        model = Lab
        fields = [
            'id','lab_code','name','location','description','lab_head',
            'created_at','updated_at','pc_count','pcs'
        ]
        read_only_fields = ['id','created_at','updated_at','pc_count','pcs']
