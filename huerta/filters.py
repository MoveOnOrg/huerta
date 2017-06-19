from django.contrib.admin.filters import AllValuesFieldListFilter
from django.db.models import Q
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _

class DropdownFilter(AllValuesFieldListFilter):
    template = 'admin/dropdown_filter.html'

class CollapsedListFilter(AllValuesFieldListFilter):
    template = 'admin/collapsed_filter.html'

    def queryset(self, request, queryset):
        """
        This handles multi-value options as comma-separated lists
        and null options are OR'd with the other selected options.
        """
        modified_query = {}
        null_keys = {}
        for key, value in self.used_parameters.items():
            if isinstance(value, str):
                modified_key = ('%s__in' % key).replace('__exact','')
                modified_value = value.split(',')
                modified_query[modified_key] = modified_value
            elif isinstance(value, bool) and '__isnull' in key:
                null_keys[key] = value
            else:
                modified_query[key] = value

        if not modified_query and not null_keys:
            # Nothing was modified, use default queryset
            return queryset
        elif not null_keys:
            # Query modified without null keys
            return queryset.filter(**modified_query)
        else:
            # Query modified with OR'd null key/value pairs
            final_query = Q(**modified_query) if modified_query else None
            for null_key, null_value in null_keys.items():
                if final_query is None:
                    final_query = Q(**{null_key:null_value})
                else:
                    final_query = final_query | Q(**{null_key:null_value})
                return queryset.filter(final_query)

    def choices(self, cl):
        # copied over from parent class EXCEPT splits value
        # hacky -- we should put this in __init__ but lazy
        # we need it for {{spec.parameter_name}} in template
        self.parameter_name = self.lookup_kwarg
        yield {
            'parameter_name': self.parameter_name,
            'selected': (self.lookup_val is None
                and self.lookup_val_isnull is None),
            'query_string': cl.get_query_string({},
                [self.lookup_kwarg, self.lookup_kwarg_isnull]),
            'display': _('All'),
            'value': '',
        }
        include_none = False
        for val in self.lookup_choices:
            pk_val = str(val)
            display_val = str(val)
            if isinstance(val, tuple):
                #remote_field case
                pk_val = str(val[0])
                display_val = val[1]
            if val is None:
                include_none = True
                continue
            display_val = smart_text(display_val)
            val_choice_list = [] if self.lookup_val is None else self.lookup_val.split(',')
            selected = (pk_val in val_choice_list) #DIFF
            remove = [self.lookup_kwarg_isnull]
            change = {}
            # ugly matrix of when to remove the val when selected
            # vs when to append it to the existing? list
            if val_choice_list:
                if selected:
                    # choice should be to remove it
                    val_choice_list.remove(pk_val)
                    if len(val_choice_list) == 0:
                        remove.append(self.lookup_kwarg)
                    else:
                        change[self.lookup_kwarg] = ','.join(val_choice_list)
                else:
                    val_choice_list.append(pk_val)
                    change[self.lookup_kwarg] = ','.join(val_choice_list)
            else:
                change[self.lookup_kwarg] = pk_val
            yield {
                'parameter_name': self.parameter_name,
                'selected': selected,
                'query_string': cl.get_query_string(change, remove),
                'display': display_val,
                'multiselect': True,
                'value': pk_val,
            }
        if include_none:
            yield {
                'parameter_name': self.parameter_name,
                'selected': bool(self.lookup_val_isnull),
                'query_string': cl.get_query_string({
                    self.lookup_kwarg_isnull: 'True',
                }, [self.lookup_kwarg]),
                'display': self.empty_value_display,
                'multiselect': True,
                'value': 'EMPTY',
            }

    def selected_choices(self, cl):
        self.parameter_name = self.lookup_kwarg
        if self.lookup_val is None and self.lookup_val_isnull is None:
            yield {
                'parameter_name': self.parameter_name,
                'selected': (self.lookup_val is None
                    and self.lookup_val_isnull is None),
                'query_string': cl.get_query_string({},
                    [self.lookup_kwarg, self.lookup_kwarg_isnull]),
                'display': _('All'),
                'value': '',
            }
        include_none = False
        for val in self.lookup_choices:
            pk_val = str(val)
            display_val = str(val)
            if isinstance(val, tuple):
                #remote_field case
                pk_val = str(val[0])
                display_val = val[1]
            if val is None:
                include_none = True
                continue
            display_val = smart_text(display_val)
            val_choice_list = [] if self.lookup_val is None else self.lookup_val.split(',')
            selected = (pk_val in val_choice_list) #DIFF
            remove = [self.lookup_kwarg_isnull]
            change = {}
            # ugly matrix of when to remove the val when selected
            # vs when to append it to the existing? list
            if val_choice_list:
                if selected:
                    # choice should be to remove it
                    val_choice_list.remove(pk_val)
                    if len(val_choice_list) == 0:
                        remove.append(self.lookup_kwarg)
                    else:
                        change[self.lookup_kwarg] = ','.join(val_choice_list)
                else:
                    val_choice_list.append(pk_val)
                    change[self.lookup_kwarg] = ','.join(val_choice_list)
            else:
                change[self.lookup_kwarg] = pk_val
            if selected:
                yield {
                    'parameter_name': self.parameter_name,
                    'selected': selected,
                    'query_string': cl.get_query_string(change, remove),
                    'display': display_val,
                    'multiselect': True,
                    'value': pk_val,
                }
        if include_none and bool(self.lookup_val_isnull):
            yield {
                'parameter_name': self.parameter_name,
                'selected': bool(self.lookup_val_isnull),
                'query_string': cl.get_query_string({
                    self.lookup_kwarg_isnull: 'True',
                }, [self.lookup_kwarg]),
                'display': self.empty_value_display,
                'multiselect': True,
                'value': 'EMPTY'
            }

class CollapsedListFilterSingle(SimpleListFilter):
    template = 'admin/collapsed_filter_single.html'
    """
        Collapsed List Filter for single select
    """     
    def selected_choices(self, cl):
        self.parameter_name = self.lookup_kwarg
        if self.lookup_val is None and self.lookup_val_isnull is None:
            yield {
                'parameter_name': self.parameter_name,
                'selected': (self.lookup_val is None
                    and self.lookup_val_isnull is None),
                'query_string': cl.get_query_string({},
                    [self.lookup_kwarg, self.lookup_kwarg_isnull]),
                'display': _('All'),
                'value': '',
            }
        include_none = False
        for val in self.lookup_choices:
            pk_val = str(val)
            display_val = str(val)
            if isinstance(val, tuple):
                #remote_field case
                pk_val = str(val[0])
                display_val = val[1]
            if val is None:
                include_none = True
                continue
            display_val = smart_text(display_val)
            val_choice_list = [] if self.lookup_val is None else self.lookup_val.split(',')
            selected = (pk_val in val_choice_list) #DIFF
            remove = [self.lookup_kwarg_isnull]
            change = {}
            # ugly matrix of when to remove the val when selected
            # vs when to append it to the existing? list
            if val_choice_list:
                if selected:
                    # choice should be to remove it
                    val_choice_list.remove(pk_val)
                    if len(val_choice_list) == 0:
                        remove.append(self.lookup_kwarg)
                    else:
                        change[self.lookup_kwarg] = ','.join(val_choice_list)
                else:
                    val_choice_list.append(pk_val)
                    change[self.lookup_kwarg] = ','.join(val_choice_list)
            else:
                change[self.lookup_kwarg] = pk_val
            if selected:
                yield {
                    'parameter_name': self.parameter_name,
                    'selected': selected,
                    'query_string': cl.get_query_string(change, remove),
                    'display': display_val,
                    'multiselect': True,
                    'value': pk_val,
                }
        if include_none and bool(self.lookup_val_isnull):
            yield {
                'parameter_name': self.parameter_name,
                'selected': bool(self.lookup_val_isnull),
                'query_string': cl.get_query_string({
                    self.lookup_kwarg_isnull: 'True',
                }, [self.lookup_kwarg]),
                'display': self.empty_value_display,
                'multiselect': True,
                'value': 'EMPTY'
            }