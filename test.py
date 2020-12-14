from pubsub import pub
import time
import threading

class A(object):
    """
    docstring
    """
    def __init__(self):
        print("From A()")
        for i in range(10):
            print(i)
            time.sleep(0.5)
        print("\nSending message")
        pub.sendMessage('ir_sensor', pub="b", value=125)


class B(object):
    """
    docstring
    """
    def __init__(self):
        pub.subscribe(self.test, 'ir_sensor')
        self.a = None
        threading.Thread(target=self._a()).start()

    def _a(self):
        self.a = A()

    def test(self, pub, value):
        print(pub)
        print(value)

if __name__=="__main__":
    import sys
    for i in range(5):
        a = "hello\n"
        a += str(i)
        sys.stdout.write("\x1b[1A\x1b[2k")
        print(a, file=sys.stdout)
        time.sleep(1)