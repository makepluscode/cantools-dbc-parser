import os
import cantools

class CANDBC:
    db = None
    message_set, signal_set, receiver_set = set([]), set([]), set([])
    count_messages, count_signals, count_receivers, count_signals_path = 0, 0, 0, 0

    def __init__(self, file_path):
        self.db =  cantools.database.load_file(file_path)

        if self.db is None:
            print('dbc file path is wrong')
            exit() 

        for message in self.db.messages:
            signals = message.signals
            self.message_set.add(message)
            self.count_messages = self.count_messages + 1
            for signal in signals:
                self.signal_set.add(signal)
                self.count_signals = self.count_signals + 1
                receivers = signal.receivers
                if signal.name == 'SAS_Angle':
                    print('SAS_Angle')
                for receiver in receivers:
                    # print(count, signal.name, signal.length, receiver)
                    self.receiver_set.add(receiver)
                    self.count_signals_path = self.count_signals_path + 1

    def show_messages(self):
        count = 0
        for m in self.message_set:
            print(count, m)
            count = count + 1

    def show_signals(self):
        count = 0
        for s in self.signal_set:
            print(count, s)
            count = count + 1

    def show_receivers(self):
        count = 0
        for r in sorted(self.receiver_set):
            print(count, r)
            count = count + 1
        self.count_receivers = count

    def show_counts(self):
        print('')
        print('total:', self.count_messages,      # num of can messages
              'messages,', self.count_signals,       # num of can signals total
              'signals,', self.count_receivers,     # num of can signals receivers
              'receivers,', self.count_signals_path,   # num of signals to each receivers
              'paths'
              )