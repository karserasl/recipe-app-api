# @Author: Lam
# @Date:   31/05/2020 13:35
from django.contrib.auth import get_user_model, authenticate
# If we have output into screen, we pass through this to automatically translate the text.
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for users object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 6,
            }
        }

    def create(self, validated_data):
        """Creates new user with encrypted password and return it"""

        return get_user_model().objects.create_user(**validated_data)

    # Set the password to set_password function
    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""

        password = validated_data.pop('password', None)  # None is because we need a default value with pop.

        # Update the user on the rest validate data using the ModelSerializer's update function
        user = super().update(instance, validated_data)

        # If user provider a password
        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth object"""

    # Add the different fields
    email = serializers.CharField()
    password = serializers.CharField(
        style={
            'input_type': 'password'
        },
        trim_whitespace=False,  # Can have whitespaces before/after characters in password
    )

    def validate(self, attrs):
        """Validate and Authenticate the user"""

        # Attrs are all the serializers fields in dict
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),  # Access the context of request that was made.
            username=email,
            password=password,
        )

        # Failed Authentication.
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        # Set the created user object as attribute's user
        attrs['user'] = user

        # If overwriting the validate function we must return the values at end, if successful.
        return attrs
