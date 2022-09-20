import os
import json
import sys
import traceback
import zmq
from debugger import execute as debug
from run_anchors import execute as explain

anchor = sys.argv[0]
examples = [
    './Examples/adult',
    './Examples/amazon',
    './Examples/bmi',
    './Examples/flights',
    './Examples/opendata',
    './Examples/physicians',
    './Examples/tweets',
    ]

iterations = [
    200
]

baselines = [
    'transform',
]

if anchor == 'on':
    baselines.append('anchors')

for b in baselines:
    if b == 'anchors':
        for e in examples:
            explain(os.path.join(e.strip(),'config.json'))
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
