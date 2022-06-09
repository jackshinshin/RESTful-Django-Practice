from django.contrib.auth import get_user_model, authenticate
# To easily translate the strings in any language into human-readable version
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    # Serializer for the users object
    # ModelSerializer helps save validated data to the self-defined model
    class Meta:
        model = get_user_model()
        # fields contain what a user can change via the api
        fields = ('email', 'password', 'name')
        # Ensure the password is write-only, and the number of it should be above 5
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5},
        }
    # This function will be called when django rest framework tries to create a user, passing validated data

    def create(self, validated_data):
        # This function gets called when the validation is successful
        # Overriden create function to create a new user with encrypted password and return it
        # The following function is defined in models.py in 'core' module
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        # The method is called whenever a user conduct the update action on the model this serializer represents

        # Retrieve the password and remove it from the database
        # None parameter means that the user doesn't have to provide something to update the info
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

class TokenSerializer(serializers.Serializer):
    # Serializer for the user authentication object
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )
    """
    Validation :
    1. input type
    2. authentication credentials
    """

    def validate(self, attrs):
        # Validate and authenticate the user
        # attrs : contains any field that makes up the above serializer
        email = attrs.get('email')
        password = attrs.get('password')

        # When a request is made, the context variable is sent to the serializer
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        # authentication fails
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        # Overriding the validate function requires returning "attrs" once the validation is successful
        return attrs
