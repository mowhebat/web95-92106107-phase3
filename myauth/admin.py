from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from myauth.models import MyUser
from django.contrib.auth import tokens


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    username = forms.CharField( error_messages = {'required': 'username needed'} )
    first_name = forms.CharField( error_messages = {'required': 'first name needed'} )
    last_name = forms.CharField( error_messages = {'required': 'last name needed'} )
    email = forms.CharField(error_messages={'required': 'email needed'})
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].error_messages = {'required': 'password needed'}
        self.fields['password2'].error_messages = {'required': 'please enter your password again'}

    class Meta:
        model = MyUser
        fields = ('username', 'email', 'first_name', 'last_name', )

    def clean_username(self):
        # Get the username
        username = self.cleaned_data.get('username')
        if MyUser.objects.filter(username=self.cleaned_data['username']).exists():
            raise forms.ValidationError('username already exists')
        else:
            return username

    def clean_email(self):
        # Get the username
        email = self.cleaned_data.get('email')
        if MyUser.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError('email already exists')
        else:
            return email

    def clean_password1(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise forms.ValidationError("too short password")
        return password1

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('username', 'email', 'first_name', 'last_name',  'password', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'email','first_name', 'last_name', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'password1', 'password2')}
        ),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    filter_horizontal = ()


    actions = ['make_admin']


    def make_admin(self, request, queryset):
        queryset.update(is_admin=True)

    make_admin.short_description = "Mark selected users as admin"

# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)

class UserLogForm(forms.Form):

    username = forms.CharField(label='username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserLogForm, self).__init__(*args, **kwargs)
        self.fields['username'].error_messages = {'required': 'username needed'}
        self.fields['password'].error_messages = {'required': 'password needed'}


    def clean_username(self):

        # Get the username
        username = self.cleaned_data.get('username')

        if MyUser.objects.filter(username=username).exists():
            return username
        else:
            raise forms.ValidationError("username not found")


    def clean_password(self):

        # Get the username and password
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get("password")

        if MyUser.objects.filter(username=username, password=password).exists():
            return password
        else:
            raise forms.ValidationError("wrong password")