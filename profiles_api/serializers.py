from rest_framework import serializers
from profiles_api import models

class HelloSerializers(serializers.Serializer):
    """Serializers a name field for testing the APIView"""
    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializers a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = (
            'id',
            'nric_number',
            'name',
            'mobile_number',
            'company',
            'photo',
            'reg_date',
            'is_pdpa_checked',
            'password'
        )
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            }
        }

    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            nric_number=validated_data['nric_number'],
            name=validated_data['name'],
            company=validated_data['company'],
            photo=validated_data['photo'],
            reg_date=validated_data['registered_date'],
            is_pdpa_checked=validated_data['is_pdpa_checked'],
            password=validated_data['password']
        )

        return user
