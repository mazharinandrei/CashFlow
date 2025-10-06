class CreatedByViewMixin:
    """
    Миксин для view с формами пользовательских объектов.
    Фильтрует queryset'ы по created_by=self.request.user.
    Добавляет created_by=self.request.user к сохранению объекта.
    """

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        for field_name, field in form.fields.items():
            queryset = getattr(field, 'queryset', None)

            if queryset is None:
                continue

            model = queryset.model

            if hasattr(model, 'created_by'):
                form.fields[field_name].queryset = queryset.filter(created_by=self.request.user)

        return form
