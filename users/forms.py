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