from django.contrib import admin


class InputFilter(admin.SimpleListFilter):
    template = 'admin/input_filter.html'

    def lookups(self, request, model_admin):
        # Dummy, required to show the filter.
        return [(1, 1)]

    def choices(self, changelist):
        # Grab only the "all" option.
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, values in changelist.get_filters_params().items()
            for v in values
            if k != self.parameter_name
        )
        yield all_choice

    def get_placeholder(self):
        return self.parameter_name.replace('_', ' ').lower()
