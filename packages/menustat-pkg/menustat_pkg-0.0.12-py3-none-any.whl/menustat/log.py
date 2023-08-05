"""logger settings and functions."""
import io
import logging

logger = logging.getLogger("menustat")

logging.basicConfig(filename="menustat.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger.setLevel(logging.DEBUG)


def writelog(func, comm, *arg):
    """Get the input, output, and position of the function wrapped.
    """
    try:
        mdf = [getattr(arg[0], s) for s in dir(arg[0]) if s == "nutr_df"]
        mdf = [df for df in mdf if not df.empty]
        buffer = io.StringIO()
        mdf_info = mdf[0].columns.values#.info(verbose=True, buf=buffer)
        s = buffer.getvalue()
        logger.info("\n%s %s %s\nnutr_df\nrowcount: %s\ncols:  %s\n\nhead:\n%s\n\ntail:\n%s",
                func.__name__, func.__code__.co_firstlineno, comm, len(mdf[0].index),
                                        mdf_info, mdf[0].head(), mdf[0].tail())
    except (IndexError, AttributeError) as err:
        logger.info("ERROR: %s\n funcdata: %s %s %s", err, func.__name__,
                                            func.__code__.co_firstlineno, comm)


def wrap(pre, post):
    """Wrapper function for logging"""
    def decorate(func):
        def call(*args, **kwargs):
            pre(func, "START", *args)
            result = func(*args, **kwargs)
            post(func, "END", *args)
            return result
        return call
    return decorate
