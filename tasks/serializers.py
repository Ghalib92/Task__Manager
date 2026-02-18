from . models import Projects, Task, UserProfile
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


# User Profile Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'bio', 'date_of_birth', 'phone_number', 'gender', 
            'city', 'country', 'address',
            'job_title', 'company', 'career',
            'hobbies', 'skills',
            'website', 'linkedin', 'github',
            'profile_picture', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


# User Serializer (includes profile)
class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']


# User Registration Serializer (with optional profile data)
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    # Optional profile fields during registration
    bio = serializers.CharField(required=False, allow_blank=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    gender = serializers.ChoiceField(choices=UserProfile.GENDER_CHOICES, required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)
    country = serializers.CharField(required=False, allow_blank=True)
    job_title = serializers.CharField(required=False, allow_blank=True)
    company = serializers.CharField(required=False, allow_blank=True)
    career = serializers.CharField(required=False, allow_blank=True)
    hobbies = serializers.CharField(required=False, allow_blank=True)
    skills = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = (
            'username', 'password', 'password2', 'email', 'first_name', 'last_name',
            # Profile fields
            'bio', 'date_of_birth', 'phone_number', 'gender', 
            'city', 'country', 'job_title', 'company', 'career', 
            'hobbies', 'skills'
        )
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        # Extract profile data
        profile_data = {
            'bio': validated_data.pop('bio', ''),
            'date_of_birth': validated_data.pop('date_of_birth', None),
            'phone_number': validated_data.pop('phone_number', ''),
            'gender': validated_data.pop('gender', ''),
            'city': validated_data.pop('city', ''),
            'country': validated_data.pop('country', ''),
            'job_title': validated_data.pop('job_title', ''),
            'company': validated_data.pop('company', ''),
            'career': validated_data.pop('career', ''),
            'hobbies': validated_data.pop('hobbies', ''),
            'skills': validated_data.pop('skills', ''),
        }
        
        # Remove password2 as it's not a User model field
        validated_data.pop('password2')
        
        # Create user
        user = User.objects.create_user(**validated_data)
        
        # Update profile (automatically created by signal)
        profile = user.profile
        for key, value in profile_data.items():
            if value:  # Only update if value provided
                setattr(profile, key, value)
        profile.save()
        
        return user


class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ['id', 'name']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'project', 'title', 'details', 'description', 'start_date', 'due_date', 'priority', 'completed']