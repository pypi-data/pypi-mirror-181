from django.contrib import admin
from django.shortcuts import render


@admin.action(description='Сравнить')
def compare(modeladmin, request, queryset):
    original = queryset.values_list()
    turn90 = list(zip(*original[::-1]))  # поворачиваем данные на 90
    headers = [field._verbose_name if field._verbose_name else field.name for field in modeladmin.model._meta.fields]
    turn90 = [list(item) for item in turn90]  # кортежи  в списке т.к нужно изменять
    headers.reverse()
    [item.insert(0, headers.pop()) for item in turn90]  # добавляем заголовки

    opts = modeladmin.opts
    opts.app_label = modeladmin.model._meta.app_label
    context = dict(
        opts=opts,
        app_label=opts.app_label,
        list_objs_compare=turn90,
        cl=dict(opts=opts),
        **modeladmin.admin_site.each_context(request)
    )

    return render(request, 'list_compare.html', context)
