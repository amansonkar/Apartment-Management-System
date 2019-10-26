from django import forms
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
#from .models import UserProfile

class SignupForm(forms.Form):
    door_number = forms.CharField(max_length=30)
    mobile_number = forms.CharField(max_length=30)
    email_id = forms.EmailField(max_length=30)

    def clean(self):
        cleaned_data = super(SignupForm,self).clean()
        print(cleaned_data)
        print('is the cleaned data')
        door_number = self.cleaned_data.get('door_number')
        mobile_number = self.cleaned_data.get('mobile_number')
        email_id = self.cleaned_data.get('email_id')
        if not door_number and not mobile_number and not email_id:
            raise forms.ValidationError('All Field are Required')
        return cleaned_data
class RegistrationForm(forms.Form):
    # email = forms.EmailField(required=True)
    username = forms.CharField(max_length=20)
    password1 = forms.CharField(max_length=30)
    password2 = forms.CharField(max_length=30)
    # class Meta:
    #     model = UserProfile
    #     fields = (
    #         'username',
    #         'password1',
    #         'password2'
    #     )

    def clean(self):
        cleaned_data = super(RegistrationForm,self).clean()
        print(cleaned_data)
        print('is the cleaned data')
        username = self.cleaned_data.get('username')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not password1 and not username and not password2:
            raise forms.ValidationError('All Field are Required')
        return cleaned_data

    # def save(self, commit=True):
    #     user = super(RegistrationForm, self).save(commit=False)
    #     email = self.cleaned_data['email']
    #     if commit:
    #         user.save()
    #     else:
    #         raise forms.ValidationError(("This username has already existed."))

    #     return user

# class EditProfileForm(UserChangeForm):

#     class Meta:
#         model = UserProfile
#         fields = (
#             'email',
#             'first_name',
#             'last_name',
#         )

class ContactForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    message = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(),
        help_text='Write here your message!'
    )
    source = forms.CharField(       # A hidden input for internal use
        max_length=50,              # tell from which page the user sent the message
        widget=forms.HiddenInput()
    )

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        message = cleaned_data.get('message')
        if not name and not email and not message:
            raise forms.ValidationError('You have to write something!')

# class regForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('first_name','last_name','username','password')
#         widgets = {
#         'password':forms.PasswordInput(attrs={'type':'password'})
#         }

# class regform1(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ('mobile_number',)