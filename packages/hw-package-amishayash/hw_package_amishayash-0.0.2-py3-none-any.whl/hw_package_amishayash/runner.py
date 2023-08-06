""" Implement your own runner to find test functions in a directory specified via commandline arguments
and to print the success stats after running them """
import os
import sys
import types
import inspect
import importlib.machinery
from contextlib import contextmanager


def function_call_log(func):
    def wrapper(*args, **kwargs):
        print(f'Calling function {func.__name__} with arguments {args} {kwargs}')
        return func(*args, **kwargs)
    return wrapper


class Runner:
    @function_call_log
    def __init__(self, path):
        self.test_files = []
        self.success = True
        self.load_test_files(path)

    @function_call_log
    def load_test_files(self, path):
        if os.path.isfile(path):
            self.test_files.append(path)
        if os.path.isdir(path):
            for f in os.listdir(path):
                self.load_test_files(path + "/" + f)

    @function_call_log
    def load_module(self, file):
        loader = importlib.machinery.SourceFileLoader("testmod", file)
        mod = types.ModuleType("testmod")
        loader.exec_module(mod)
        return mod

    @function_call_log
    def run_single_file(self, file):
        if not file.endswith('.py'):
            return
        mod = self.load_module(file)
        tests = [m for m in inspect.getmembers(mod) if inspect.isfunction(m[1]) and m[0].startswith("test_a1_")]
        for test in tests:
            (test_name, test_function) = test
            print("Running Test", test_name, end=' ')
            try:
                test_function()
                print("Successful")
            except AssertionError:
                print("Failure")
                self.success = False

    @function_call_log
    def run(self):
        for test_file in self.test_files:
            self.run_single_file(test_file)

        if self.success:
            print(f"tests succeeded")
        else:
            print(f"tests failed")


if __name__ == "__main__":
    Runner(sys.argv[1]).run()