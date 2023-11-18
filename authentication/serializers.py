from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=50,min_length=8,write_only=True
    )

    class Meta:
        model = get_user_model()
        exclude = ["groups", "user_permissions"]
        extra_kwargs = {
            "is_superuser":{"write_only": True}
        }

    def validate(self,attrs):
        email = attrs.get('email',None)
        password = attrs.get("password", None)
        
        if email is None:
            raise serializers.ValidationError(
                'User Should Have email address'
            )
        if password is None:
            raise serializers.ValidationError(
                'User Should Have Password'
            )
        return attrs
    
    def create(self, validated_data):
        print(validated_data)
        return get_user_model().objects.create_user(**validated_data)