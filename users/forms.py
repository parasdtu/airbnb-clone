from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # does the work for below two methods
    # when working with "just" clean method
    # add error specifically to the field
    # otherwise the error is thrown for all fields
    def clean(self):
        # to validate password first get user
        # then check password
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(username=email)
            if user.check_password(password):
                # when using clean method always return cleaned data
                return self.cleaned_data
            else:
                # raise forms.ValidationError("Incorrect username or password")
                # or you can add error or a specific field
                self.add_error(
                    "password",
                    forms.ValidationError("Incorrect username or password"),
                )
        except:
            # this means that user does not exist
            # and user will have to signup
            # raise forms.ValidationError("User does not exist")
            self.add_error(
                "email",
                forms.ValidationError("User does not exist"),
            )

    # not an arbitrary name but clean_<name of the class field>
    # is used to check for any errors or format data as per requirements
    # and also if this actually exists in database

    # we alsohave to return the validated/cleaned data
    # otherwise None will be returned
    """ def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            # to get the user with the email/username
            models.User.objects.get(username=email)
            return email
        except models.User.DoesNotExist:
            # this means that user does not exist
            # and user will have to signup
            raise forms.ValidationError("User does not exist")

    def clean_password(self):
        # to validate password first get user
        # then check password
        email = self.cleaned_data.get("email")
        password= self.cleaned_data.get("password")
        try:
            user=models.User.objects.get(username=email)
            if user.check_password(password):
                return password
            else:
                raise forms.ValidationError("Incorrect username or password")
        except:
            pass
"""


# we have to return the value from the above described clean functions
# otherwise it is almost as equivalent as removing the field
# ie. will return None unless we return a value


class SignUpForm(forms.ModelForm):
    class Meta:
        # here we specify the model we want to create a form for
        # also we can specify fields acc to what we want

        # models is required
        model = models.User

        # fields are required
        fields = (
            "first_name",
            "last_name",
            "email",
        )

    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    # we don't have to use clean email anymore cuz it will be
    # cleaned by ModelForm

    # however we need to clean password cuz it is custom
    # and not defined in model

    def clean_password1(self):
        # note that you can get password from clean_password1
        # but you can not get password1 from clean_password
        # because it is declared below password and thus is not cleaned yet
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            # passwords do not match
            raise forms.ValidationError("Passwords do not match")
        else:
            # can return password and move further with signup
            return password

    """ModelForm by default has a save method, just like clean
    but we have to override it to customize saving,
    as in this case we want username to be email"""

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        """the above call saye to create the user object
        BUT do not add it to database 
        because we will do it on our own"""

        print(self.cleaned_data)
        user.username = self.cleaned_data.get("email")
        user.set_password(self.cleaned_data.get("password"))
        user.save()


# very annoying to create fields like these for all models...
# django provides ModelForm to create a form linked to a model
# it will have all required fields
class SignUpForm1(forms.Form):

    first_name = forms.CharField(max_length=80)
    last_name = forms.CharField(max_length=80)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            # if no error means user already exists
            raise forms.ValidationError("User already exists with this email")
        except models.User.DoesNotExist:
            # now this means this is a new email and user can be created
            return email

    def clean_password1(self):
        # note that you can get password from clean_password1
        # but you can not get password1 from clean_password
        # because it is declared below password and thus is not cleaned yet
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            # passwords do not match
            raise forms.ValidationError("Passwords do not match")
        else:
            # can return password and move further with signup
            return password

    def save(self):
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        user = models.User.objects.create_user(
            username=email,
            email=email,
            password=password,
        )
        user.first_name = first_name
        user.last_name = last_name
        user.save()