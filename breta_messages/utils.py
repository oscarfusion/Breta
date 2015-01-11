from django.utils.timezone import make_aware, get_current_timezone
import datetime


def filter_queryset(iterable):
    qs = sorted(list(iterable), key=lambda x: x.sent_at or make_aware(
        datetime.datetime(datetime.MINYEAR, 1, 1),
        get_current_timezone()
    ))
    res = []
    while qs:
        obj = qs.pop(0)
        res.insert(0, obj)
        pos = res.index(obj) + 1
        replies_to_curr = [y for y in qs if y.reply_to == obj]
        for i, x in enumerate(replies_to_curr):
            res.insert(pos + i, x)
            qs.remove(x)
    return res
