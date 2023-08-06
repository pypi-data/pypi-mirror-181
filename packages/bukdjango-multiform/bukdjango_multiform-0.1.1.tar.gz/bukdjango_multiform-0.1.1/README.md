# multiform

Multiple forms processing in one View.

```python
from bukdjango_multiform.views import MultiFormTemplateView

from django.http import HttpResponse, HttpResponseForbidden
from .forms import Form1, Form2
    

def logged_in(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return HttpResponseForbidden(b'loginplease')


class MyMultiFormTemplateView(MultiFormTemplateView):
    template_name = 'index.html'
    multiform_field_name = 'html_field_name'
    multiforms = {
        # template context name for `Form`
        'form1_ctx': {
            'class': Form1,
            # pass view attr as keyword argument to form
            'attrs': ('request',),
            # pass view kwargs as keyword argument to form
            'kwargs': ('some_kwarg',),
        },
        'form2_ctx': {
            'class': Form2,
            # check if form can be processed
            'checks': (logged_in,),
            # save form if valid
            'save': True,
        }
    }
    
    # pass additional kwargs to `Form1`
    def get_kwargs_form1_ctx(self, **kwargs):
        kwargs.update({
            'request': None,
            'some_kwarg': None,
        })
        return kwargs
    
    def handle_valid_form2_ctx(self, form):
        return HttpResponse(b'VALID!form2_ctx')

    def handle_invalid_form2_ctx(self, form):
        return HttpResponse(b'INVALID!form2_ctx')

    def handle_valid_form1_ctx(self, form):
        return HttpResponse(b'VALID!form1_ctx')

    def handle_invalid_form1_ctx(self, form):
        return HttpResponse(b'INVALID!form1_ctx')


    class MyMultiFormTemplateView2(MyMultiFormTemplateView):
        template_name = 'index.html'
        # when subclassing all forms are collected
        # similiar to how `django.forms.Form` fields work
        multiforms = {
            'form4_ctx': {
                'class': Form2,
            },
            # delete form` from context
            'form2_ctx': None,
        }

```