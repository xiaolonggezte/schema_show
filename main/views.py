# coding:utf8
from django.shortcuts import render

# Create your views here.


def schema_show(request, filename):
    # filename = '/Users/xiaolong/' + filename
    filename = '/mnt/tango/log/cd.byted.org/json_schema/' + filename
    with open(filename, 'r') as f:
        msg = f.read()
    type = 1
    context = {}
    msg, raw_data = msg.split('原始数据\n:', 1)
    msg = msg.split('错误信息:', 1)[1]
    if msg.find('Failed') != -1:
        type = 1
        ex, msg = msg.split('Failed', 1)
        validator, msg = msg.split('validating', 1)[1].split('in schema', 1)
        schema_index, msg = msg.split(':\n', 1)
        schema, msg = msg.split('\nOn instance', 1)
        key, value = msg.split(':', 1)
        context.update(
            error_type=type,
            ex=ex,
            validator=validator,
            schema_index=schema_index,
            schema=schema,
            key=key,
            value=value,
            raw_data=raw_data,
        )
    else:
        type = 2
        ex, msg = msg.split('Unknown type ', 1)[1].split('for validator with schema:\n', 1)
        schema, instance = msg.split('\nWhile checking instance:', 1)
        context.update(
            ex=ex,
            schema=schema,
            instance=instance,
            raw_data=raw_data,
        )

    return render(request, 'main/show.html', context=context)