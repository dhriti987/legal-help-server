from rest_framework import serializers
from .models import Expertise, Expert, Query, QueryFile

class ExpertiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expertise
        fields = "__all__"

class ExpertSerializer(serializers.ModelSerializer):
    # expertise_value = serializers.ReadOnlyField(source="expertise.name")
    expertise = ExpertiseSerializer()
    class Meta:
        model = Expert
        fields = "__all__"

class QueryFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueryFile
        fields = "__all__"

class QuerySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    catagory = ExpertiseSerializer()
    class Meta:
        model = Query
        fields = "__all__"
