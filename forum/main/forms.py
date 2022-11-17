from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.forms import TextInput

from .models import AbsUser, Request, Category


class RegisterUserForm(forms.ModelForm):
    surname = forms.CharField(label='Фамилия',
                              validators=[RegexValidator('^[а-яА-Я- ]+$',
                                                         message='только кирилица и тире')],
                              error_messages={
                                  'required': 'Обязательное поле',
                              })
    name = forms.CharField(label='Имя',
                           validators=[RegexValidator('^[а-яА-Я- ]+$',
                                                      message='только кирилица и тире')],
                           error_messages={
                               'required': 'Обязательное поле',
                           })
    patronymic = forms.CharField(label='Отчество',
                                 validators=[RegexValidator('^[а-яА-Я- ]+$',
                                                            message='только кирилица и тире')],
                                 error_messages={
                                     'required': 'Обязательное поле',
                                 })
    username = forms.CharField(label='Логин',
                               validators=[RegexValidator('^[a-zA-z-]+$',
                                                          message='только латиница и тире')],
                               error_messages={
                                   'required': 'Обязательное поле',
                                   'unique': 'Данный логин занят'
                               })
    email = forms.EmailField(label='Почта',
                             error_messages={
                                 'required': 'Обязательное поле',
                                 'invalid': 'Не правильный формат',
                                 'unique': 'Адрес занят'
                             })
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput,
                               error_messages={
                                   'required': 'Обязательное поле',
                               })
    password2 = forms.CharField(label='Пароль (повторно)',
                                widget=forms.PasswordInput,
                                error_messages={
                                    'required': 'Обязательное поле',
                                })
    personal_data = forms.BooleanField(required=True, label='Согласие на обработку данных',
                                       error_messages={
                                           'required': 'Обязательно поле'
                                       })

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise ValidationError({
                'password2': ValidationError('Пароли не совпадают', code='pass_error')
            })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user

    class Meta:
        model = AbsUser
        fields = ('surname', 'name', 'patronymic', 'username', 'email', 'password', 'password2', 'personal_data')


class CreateRequestForm(forms.ModelForm):
    photo = forms.ImageField(label='Фото',)

    class Meta:
        model = Request
        fields = ('name', 'description', 'category', 'photo')
        enctype = "multipart/form-data"


class RequestForm(forms.ModelForm):
    def clean(self):
        status = self.cleaned_data.get('status')
        comment = self.cleaned_data.get('comment')
        photo2 = self.cleaned_data.get('photo2')
        if self.instance.status != 'new':
            raise forms.ValidationError({'status': 'Статус можно сменить только у нового заказа'})
        if status == 'work' and not comment:
            raise forms.ValidationError({'comment': 'Нужно ввести комментарий'})
        if status == 'completed' and not photo2:
            raise forms.ValidationError({'photo2': 'Нужно загрузить фото'})
