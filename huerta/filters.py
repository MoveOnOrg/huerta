from django.contrib.admin.filters import AllValuesFieldListFilter
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _

class DropdownFilter(AllValuesFieldListFilter):
    template = 'admin/dropdown_filter.html'

class CollapsedListFilter(AllValuesFieldListFilter):
    template = 'admin/collapsed_filter.html'

    def queryset(self, request, queryset):
        q = dict([(('%s__in' % k).replace('__exact',''), v.split(',')) for k,v in self.used_parameters.items()])
        return queryset.filter(**q)

    def choices(self, cl):
        # copied over from parent class EXCEPT splits value
        # hacky -- we should put this in __init__ but lazy
        # we need it for {{spec.parameter_name}} in template
        self.parameter_name = self.lookup_kwarg
        yield {
            'selected': (self.lookup_val is None
                and self.lookup_val_isnull is None),
            'query_string': cl.get_query_string({},
                [self.lookup_kwarg, self.lookup_kwarg_isnull]),
            'display': _('All'),
            'value': '',
        }
        include_none = False
        for val in self.lookup_choices:
            pk_val = val
            display_val = val
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
                'selected': selected,
                'query_string': cl.get_query_string(change, remove),
                'display': display_val,
                'multiselect': True,
                'value': pk_val,
            }
        if include_none:
            yield {
                'selected': bool(self.lookup_val_isnull),
                'query_string': cl.get_query_string({
                    self.lookup_kwarg_isnull: 'True',
                }, [self.lookup_kwarg]),
                'display': self.empty_value_display,
            }

    def selected_choices(self, cl):
        self.parameter_name = self.lookup_kwarg
        if self.lookup_val is None and self.lookup_val_isnull is None:
            yield {
                'selected': (self.lookup_val is None
                    and self.lookup_val_isnull is None),
                'query_string': cl.get_query_string({},
                    [self.lookup_kwarg, self.lookup_kwarg_isnull]),
                'display': _('All'),
                'value': '',
            }
        include_none = False
        for val in self.lookup_choices:
            pk_val = val
            display_val = val
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
                    'selected': selected,
                    'query_string': cl.get_query_string(change, remove),
                    'display': display_val,
                    'multiselect': True,
                    'value': pk_val,
                }
        if include_none and bool(self.lookup_val_isnull):
            yield {
                'selected': bool(self.lookup_val_isnull),
                'query_string': cl.get_query_string({
                    self.lookup_kwarg_isnull: 'True',
                }, [self.lookup_kwarg]),
                'display': self.empty_value_display,
            }
