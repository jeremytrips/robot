import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Singleton:

    def __init__(self, decorated):
        self._decorated = decorated

    def get(self):
        try:
            return self._instance
        except:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through get() method.')


@Singleton
class Logger:

    def __init__(self):
        self._warn_once = []
        self._log_once = []

    def log(self, *args):
        logs = "\033[K" + bcolors.HEADER + "[ROBOT:LOG] "
        for log in args:
            logs += str(log)
        logs += bcolors.ENDC + "\n"
        sys.stdout.write(logs)

    def warn(self, *args):
        logs = "\033[K" + bcolors.WARNING + "[ROBOT:WARN] "
        for log in args:
            logs += str(log)
        logs += bcolors.ENDC + "\n"
        sys.stdout.write(logs)
    
    def error(self, *args):
        logs = "\033[K" + bcolors.FAIL + "[EMULATOR:WARN] "
        for log in args:
            logs += str(log)
        logs += bcolors.ENDC + "\n"
        sys.stdout.write(logs)
        input("Touch any key to quit")
        sys.exit()

    def log_once(self, *args):
        logs = "\033[K" + bcolors.HEADER + "[ROBOT:LOG] "
        for log in args:
            logs += str(log)
        logs += bcolors.ENDC + "\n"
        if logs not in self._log_once:
            self._log_once.append(logs)
            sys.stdout.write(logs)

    def warn_once(self, *args):
        logs = "\033[K" + bcolors.WARNING + "[ROBOT:WARN] "
        for log in args:
            logs += str(log)
        logs += bcolors.ENDC + "\n"
        if logs not in self._warn_once:
            self._warn_once.append(logs)
            sys.stdout.write(logs)

LOG = Logger.get().log
WARN = Logger.get().warn
WARN_ONCE = Logger.get().warn_once
ERROR = Logger.get().error
