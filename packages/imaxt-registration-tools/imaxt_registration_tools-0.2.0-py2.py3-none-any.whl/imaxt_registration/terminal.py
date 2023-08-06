from colored import fg, bg, attr
import multiprocessing as mp

VERBOSE = True


def set_verbose(val):
    global VERBOSE
    VERBOSE = val


def debug(*args):
    if not VERBOSE:
        return
    curr_proc = mp.current_process()
    print(f"{curr_proc.name}:{fg('blue')}", *args, attr("reset"))


def info(*args):
    if not VERBOSE:
        return
    curr_proc = mp.current_process()
    print(f"{curr_proc.name}:", *args)


def warn(*args):
    if not VERBOSE:
        return
    curr_proc = mp.current_process()
    print(f"{curr_proc.name}:{fg('magenta')}", *args, attr("reset"))


def error(*args):
    if not VERBOSE:
        return
    curr_proc = mp.current_process()
    print(f"{curr_proc.name}:{fg('white')}{bg('red')}", *args, attr("reset"))
