from django import forms
from django.http import HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.views.generic import TemplateView


class NewMultiForm(type):

    def __new__(mcs, name, bases, attrs):
        new_class = super().__new__(mcs, name, bases, attrs)

        multiforms = {}
        for base in reversed(new_class.__mro__):
            if hasattr(base, 'multiforms'):
                multiforms.update(base.multiforms)
                for k, v in base.multiforms.items():
                    if v is None and k in multiforms:
                        multiforms.pop(k)

        if multiforms:
            field_name = attrs.get('multiform_field_name', 'formtype')
            for k, v in multiforms.items():
                multiforms[k]['class'] = type(
                    v['class'].__name__,
                    (v['class'],),
                    {field_name: forms.CharField(
                        widget=forms.HiddenInput(),
                        initial=k,
                    )}
                )

        new_class.multiforms = multiforms

        return new_class


# todo before post we should decorate
# todo for ex. login required or other checks per form
class MultiFormMixin(metaclass=NewMultiForm):

    multiforms = {}
    multiform_field_name = 'formtype'

    def kwargs_getattr(self, name):
        return f'get_kwargs_{name}'

    @property
    def invalid_handle(self):
        return getattr(
            self, f'handle_invalid_{self.form_name}', None
        )

    @property
    def valid_handle(self):
        return getattr(
            self, f'handle_valid_{self.form_name}', None
        )

    @cached_property
    def form_name(self):
        return self.request.POST.get(
            self.multiform_field_name
        )

    @cached_property
    def form_class(self):
        return self.multiforms.get(
            self.form_name
        )['class']

    @cached_property
    def form_params(self):
        return self.multiforms.get(
            self.form_name
        )

    @cached_property
    def form_checks(self):
        return self.multiforms.get(
            self.form_name
        ).get('checks', None)

    @cached_property
    def form_save(self):
        return self.multiforms.get(
            self.form_name
        ).get('save', False)

    def get_form_kwargs(self, name, params, **kwargs):
        if attrs := params.get('attrs'):
            for attr in attrs:
                kwargs[attr] = getattr(self, attr)
        if kws := params.get('kwargs'):
            for kw in kws:
                kwargs[kw] = self.kwargs[kw]
        if func := getattr(self, self.kwargs_getattr(name), None):
            kwargs.update(func(**kwargs))
        return kwargs

    def post(self, request, *args, **kwargs):

        if not self.form_params:
            return HttpResponseBadRequest()

        if self.form_checks:
            for check in self.form_checks:
                if response := check(
                    request, *args, **kwargs,
                ):
                    return response

        form = self.form_class(
            **self.get_form_kwargs(
                name=self.form_name,
                params=self.form_params,
                data=request.POST,
                files=request.FILES,
            )
        )

        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        if handler := self.valid_handle:
            return handler(form=form)
        if self.form_save:
            form.save()
        return self.post_response(form)

    def form_invalid(self, form):
        if handler := self.invalid_handle:
            return handler(form=form)
        return self.post_response(form)


class MultiFormTemplateView(MultiFormMixin, TemplateView):

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        for k, v in self.multiforms.items():
            if not kwargs.get(k):
                ctx[k] = v['class'](
                    **self.get_form_kwargs(
                        name=k, params=v,
                    )
                )
        return ctx

    def post_response(self, form):
        return self.render_to_response(
            context=self.get_context_data(**{
                self.form_name: form,
            })
        )
