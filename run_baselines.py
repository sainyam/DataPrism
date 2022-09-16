import os
import json
import sys
import traceback
import zmq
from debugger import execute as debug
from run_anchors import execute as explain

examples = []


experiments = open("./SIGMOD_conjunctions_2/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_conjunctions_4/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_conjunctions_8/list.txt",'r')
examples += experiments.readlines()
experiments.close()


experiments = open("./SIGMOD_conjunctions_16/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_conjunctions_32/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_conjunctions_missing_2/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_conjunctions_missing_4/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_conjunctions_missing_8/list.txt",'r')
examples += experiments.readlines()
experiments.close()


experiments = open("./SIGMOD_conjunctions_missing_16/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_conjunctions_missing_32/list.txt",'r')
examples += experiments.readlines()
experiments.close()


experiments = open("./SIGMOD_disjunctions_2/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_disjunctions_4/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_disjunctions_8/list.txt",'r')
examples += experiments.readlines()
experiments.close()


experiments = open("./SIGMOD_disjunctions_16/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_disjunctions_32/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_disjunctions_missing_2/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_disjunctions_missing_4/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_disjunctions_missing_8/list.txt",'r')
examples += experiments.readlines()
experiments.close()


experiments = open("./SIGMOD_disjunctions_missing_16/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_disjunctions_missing_32/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_single_2/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_single_4/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_single_8/list.txt",'r')
examples += experiments.readlines()
experiments.close()


experiments = open("./SIGMOD_single_16/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_single_32/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_single_missing_2/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_single_missing_4/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_single_missing_8/list.txt",'r')
examples += experiments.readlines()
experiments.close()


experiments = open("./SIGMOD_single_missing_16/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_single_missing_32/list.txt",'r')
examples += experiments.readlines()
experiments.close()

iterations = [
    200
]

baselines = [
    'transform',
    'anchors'
]
for b in baselines:
    if b == 'anchors':
        for e in examples:
            explain(b, os.path.join(e.strip(),'config.json'))
    else:
        os.system("python worker_%s.py & disown" % b )
        try:
            for e in examples:
                for i in iterations:
                    debug(b, os.path.join(e.strip(),'config.json'), i, remove='corr|functional|conformance')
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
        finally:
            context = zmq.Context()
            sender = context.socket(zmq.PUSH)
            sender.bind("tcp://{0}:{1}".format("*", '5557'))
            receiver = context.socket(zmq.PULL)
            receiver.bind("tcp://{0}:{1}".format("*", '5558'))
            poller = zmq.Poller()
            poller.register(receiver, zmq.POLLIN)

            sender.send_string('kill')

            poller.unregister(receiver)
            receiver.close()
            sender.close()
            context.term()
