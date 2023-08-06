from . import assertions, runner

__all__ = ["assertions", "runner"]

if __name__ == "__main__":
    Runner(sys.argv[1]).run()