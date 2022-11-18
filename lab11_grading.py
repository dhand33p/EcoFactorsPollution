import re
import sys
import requests
import threading
from importlib import import_module

EPSILON = 1e-3
TIMEOUT = 30
LAB = "lab11"
RPC_URL = "https://dsci.isi.edu/api/rpc"


def rpc_call(filename, funcname, args):
    query = {
        "filename": filename,
        "funcname": funcname,
        "args": args
    }
    return requests.get(RPC_URL, params=query).json()


all_tests = {
    "find_weather": {
        ("Los Angeles", ): ((rpc_call("lab11_solution", "find_weather", "Los Angeles"), ), (2.5, )),
        ("San Francisco", ): ((rpc_call("lab11_solution", "find_weather", "San Francisco"), ), (2.5, )),
        ("New York", ): ((rpc_call("lab11_solution", "find_weather", "New York"), ), (2.5, )),
        ("Seattle", ): ((rpc_call("lab11_solution", "find_weather", "Seattle"), ), (2.5, )),
    },
    "find_food": {
        ("USC", ): (rpc_call("lab11_solution", "find_food", "USC"), (0.9, 0.8, 0.8)),
        ("UCLA", ): (rpc_call("lab11_solution", "find_food", "UCLA"), (0.9, 0.8, 0.8)),
        ("Caltech", ): (rpc_call("lab11_solution", "find_food", "Caltech"), (0.9, 0.8, 0.8)),
        ("UCI", ): (rpc_call("lab11_solution", "find_food", "UCI"), (0.9, 0.8, 0.8)),
    },
    "find_tweet": {
        ("USCmoves", ): (rpc_call("lab11_solution", "find_tweet", "USCmoves"), (0.9, 0.8, 0.8)),
        ("elonmusk", ): (rpc_call("lab11_solution", "find_tweet", "elonmusk"), (0.9, 0.8, 0.8)),
        ("YosemiteNPS", ): (rpc_call("lab11_solution", "find_tweet", "YosemiteNPS"), (0.9, 0.8, 0.8)),
        ("YellowstoneNPS", ): (rpc_call("lab11_solution", "find_tweet", "YellowstoneNPS"), (0.9, 0.8, 0.8)),
    },
}


class ThreadWithResult(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        def function():
            self.result = target(*args, **kwargs)
        super().__init__(group=group, target=function, name=name, daemon=daemon)


def print_tuple(tp, always_parentheses=False):
    content_str = ', '.join([repr(x) for x in tp])
    if always_parentheses or len(tp) > 1:
        return '(' + content_str + ')'
    else:
        return content_str


def check_filename(filename):
    if filename != f"{LAB}_firstname_lastname.py":
        if filename.islower():
            if re.match(LAB + r"_.*\.py", filename):
                return True, ""
            else:
                return False, f'The filename should starts with "{LAB}_", ends with ".py", the provided filename is: {filename}'
        else:
            return False, f"The filename should be in lower case, the provided filename is: {filename}"
    else:
        return False, f"Please rename the file using your real name, the provided filename is: {filename}"


def check_match(actual_outputs, expected_outputs, scores, prefix=''):
    earned_score = 0
    msgs = []
    if len(actual_outputs) == len(expected_outputs):
        for i in range(len(expected_outputs)):
            prefix_i = f"{prefix}[{i}]"
            actual = actual_outputs[i]
            expected = expected_outputs[i]
            score = scores[i]
            try:
                if isinstance(expected, list) or isinstance(expected, tuple):
                    es, ms = check_match(actual, expected, score, prefix_i)
                    earned_score += es
                    msgs += ms
                elif isinstance(expected, set):
                    if actual in expected:
                        earned_score += score
                    else:
                        expected_list = list(expected)
                        msgs.append(f"output index {prefix_i}, your output: {repr(actual)}, expected output: {repr(expected_list[0])} or {repr(expected_list[1])}")
                else:
                    if actual == expected or (isinstance(expected, float) and abs(actual - expected) < EPSILON):
                        earned_score += score
                    else:
                        msgs.append(f"output index {prefix_i}, your output: {repr(actual)}, expected output: {repr(expected)}")
            except TypeError:
                msgs.append(f"output index {prefix_i}, your output: {repr(actual)}, type: {type(actual)}; expected output: {repr(expected)}, type: {type(expected)}")
    else:
        prefix_msg = '' if prefix == '' else f"output index {prefix}, "
        msgs.append(f"{prefix_msg}your output has: {len(actual_outputs)} value(s), expected output has: {len(expected_outputs)} value(s)")
    return earned_score, msgs


def run_tests(filename):
    msgs = []
    module_name = filename.replace(".py", "")
    t = ThreadWithResult(target=import_module, args=(module_name, ), daemon=True)
    t.start()
    t.join(TIMEOUT)
    if t.is_alive():
        msgs.append(f"Error: When importing your solution, it didn't finish in {TIMEOUT} seconds. Did you use input() in your solution?")
        return 0, msgs

    solution = getattr(t, "result", None)
    if solution is None:
        msgs.append("Error: When importing your solution, it raised above exception:")
        return 0, msgs

    total_score = 0
    for fn_name, fn_tests in all_tests.items():
        fn = getattr(solution, fn_name, None)
        if fn is None:
            msgs.append(f"Error: Your solution does not contain function: {fn_name}")
            continue

        for args, outputs_score in fn_tests.items():
            expected_outputs, scores = outputs_score

            t = ThreadWithResult(target=fn, args=args, daemon=True)
            t.start()
            t.join(TIMEOUT)
            if t.is_alive():
                msgs.append(f"Error: In test case: {fn_name}{print_tuple(args, True)}, your function didn't finish in {TIMEOUT} seconds. Did you use proper data strcture like dict, set? Did you use input() in your function?")
                continue

            if not hasattr(t, "result"):
                msgs.append(f"Error: In test case: {fn_name}{print_tuple(args, True)}, your function raised above exception:")
                continue

            actual_outputs = t.result
            if not (isinstance(actual_outputs, tuple) or isinstance(actual_outputs, list)):
                actual_outputs = (actual_outputs, )

            es, ms = check_match(actual_outputs, expected_outputs, scores)
            total_score += es
            msgs += [f"Error: In test case: {fn_name}{print_tuple(args, True)}, {m}" for m in ms]

    return total_score, msgs


if __name__ == "__main__":
    filename = sys.argv[1]
    is_valid, msg = check_filename(filename)
    if is_valid:
        total_score, msgs = run_tests(filename)
        if len(msgs) > 0:
            print("\n".join(msgs))
    else:
        print(msg)
        total_score = 0
    print(f"Your score for {LAB.capitalize()} Assignment: {total_score:.1f}")
