from functools import wraps
from io import StringIO

def buffered(f):
    @wraps(f)
    def wrapper(self=None, buf=None, *args, **kwargs):
        write_to_str = not buf
        buf = buf or StringIO()
        f(self, buf=buf, *args, **kwargs)
        if write_to_str:
            return buf.getvalue()
    return wrapper
