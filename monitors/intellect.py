import sys
import logging

from intellect.Intellect import Intellect
from intellect.Intellect import Callable
from intellect.examples.testing import ClassA


class MyIntellect(Intellect):

    @Callable
    def bar(self):
        self.log("<<< called MyIntellect's bar method as it was decorated as Callable >>>")

if __name__ == "__main__":

    try:
        logger = logging.getLogger('intellect')
        #logger.setLevel(logging.DEBUG)
        logger.setLevel(logging.ERROR)
        consoleHandler = logging.StreamHandler(stream=sys.stdout)
        consoleHandler.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s%(message)s'))
        logger.addHandler(consoleHandler)

        myIntellect = MyIntellect()
        print("passo")

        policy_a = myIntellect.learn(Intellect.local_file_uri("intellect/policies/test_a.policy"))
        print("policy loaded")
        #print(policy_a)
        #myIntellect.reason(["test_a"])

        a = ClassA(property0="cpu", property1=10, property2={"a": 1, "b": 2})
        b = ClassA(property0="network", property1=11)
        c = ClassA(property0="cpu", property1=12)

        print("Learn instance a")
        myIntellect.learn(a)
        print("Learn instance b")
        myIntellect.learn(b)
        print("Learn instance c")
        myIntellect.learn(c)

        print("Reasoning...")
        myIntellect.reason(["test_a"])

        print(myIntellect.knowledge)

    except Exception as e:
        print(e.message)
