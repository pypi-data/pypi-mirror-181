from functools import wraps


def try_and_get_bool(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        try:
            view_func(*args, **kwargs)
            return True
        except:
            return False
    return wrapped_view


def try_and_get_data(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except:
            pass
    return wrapped_view
