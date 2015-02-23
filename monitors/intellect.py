import sys, traceback, logging

from intellect.Intellect import Intellect
from intellect.Intellect import Callable
from intellect_tests.classA import ClassA


class MyIntellect(Intellect):

    @Callable
    def bar(self):
        self.log("<<< called MyIntellect's bar method as it was decorated as Callable >>>")

if __name__ == "__main__":

    try:
        logger = logging.getLogger('intellect')
        logger.setLevel(logging.ERROR)
        consoleHandler = logging.StreamHandler(stream=sys.stdout)
        consoleHandler.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s%(message)s'))
        logger.addHandler(consoleHandler)

        myIntellect = MyIntellect()
        print("passo")

        policy_a = myIntellect.learn(Intellect.local_file_uri("intellect_tests/policies/test_a.policy"))
        print("policy loaded")
        print(policy_a)
        #myIntellect.reason(["test_a"])

        a = ClassA(property1="apple", property2=11)
        b = ClassA(property1="pear", property2=12)

        print("Learn instance a")
        myIntellect.learn(a)
        print("Learn instance b")
        myIntellect.learn(b)

        print("Reasoning...")
        myIntellect.reason(["test_a"])

        print(myIntellect.knowledge)

    except Exception as e:
        print(e.message)
