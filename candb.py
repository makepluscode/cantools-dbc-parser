import os
import csv
import cantools

from data import Message, Signal
from ecu import ECU


class CANDBC:
    db = None
    ecu_set, message_set, signal_set, receiver_set = set(
        []), set([]), set([]), set([])
    count_messages, count_signals, count_receivers, count_signals_path = 0, 0, 0, 0
    count_signal_abnormal = 0

    def __init__(self, file_path):
        self.db = cantools.database.load_file(file_path)

        if self.db is None:
            print('dbc file path is wrong')
            exit()

        for m in self.db.messages:
            signals = m.signals

            # message
            message = Message(m.name, m.senders, m.frame_id,
                              m.length, m.is_fd, m.is_container)
            self.message_set.add(message)
            self.count_messages = self.count_messages + 1
            print(m.senders)
            for s in signals:
                # signal
                self.count_signals = self.count_signals + 1
                receivers = s.receivers
                for receiver in receivers:
                    # print(count, signal.name, signal.length, receiver)
                    self.receiver_set.add(receiver)
                    self.count_signals_path = self.count_signals_path + 1

                    if len(m.senders) == 1:
                        sender = m.senders[0]
                        signal = Signal(s.name, sender, receiver,
                                        s.length, s.minimum, s.maximum, s.unit)
                        self.signal_set.add(signal)
                    else:
                        print('exceptional case : no sender')

            # ecu
            for e in self.ecu_set:
                if e.name == m.senders:
                    print(e.name, 'already exist')
                    continue

            assert len(m.senders) < 2, 'senders should be one'

            if len(m.senders) == 1:
                sender = m.senders[0]
                ecu = ECU(sender)
                self.ecu_set.add(ecu)
            else:
                print('exceptional case : no sender')

    def show_messages(self):
        count = 0
        for m in self.message_set:
            print(count, m.name, m.sender, m.frame_id,
                  m.length, m.is_fd, m.is_container)
            count = count + 1

    def show_signals(self):
        count = 0
        for s in self.signal_set:
            print(count, s.name, s.sender, s.receiver)
            count = count + 1

    def show_receivers(self):
        count = 0
        for r in sorted(self.receiver_set):
            print(count, r)
            count = count + 1
        self.count_receivers = count

    def show_ecus(self):
        count = 0
        for e in self.ecu_set:
            print(count, e.name)
            count = count + 1
        self.count_receivers = count

    def show_counts(self):
        print('')
        self.eval_signals()

        print('total:', self.count_messages,                   # num of can messages
              'messages,', self.count_signals,                 # num of can signals total
              'signals,', self.count_receivers,                # num of can signals receivers
              'abnormal signals,', self.count_signal_abnormal,  # num of can signals receivers
              # num of signals to each receivers
              'receivers,', self.count_signals_path,
              'paths'
              )

    def eval_signals(self):
        count = 0
        for s in self.signal_set:
            if s.sender is None:
                self.count_signal_abnormal + self.count_signal_abnormal + 1
            count = count + 1

    def dump_signals(self):
        count = 0

        with open("signals.csv", 'w') as file:
            for s in self.signal_set:
                print(count, s.name, s.sender, s.receiver)
                row = [s.name, s.sender, s.receiver,
                       s.len, s.min, s.max, s.unit]
                count = count + 1
                writer = csv.writer(file)
                writer.writerow(row)
