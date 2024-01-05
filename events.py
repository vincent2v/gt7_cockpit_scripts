import asyncio
from string import printable
import sys
import os


from gt_telem import TurismoClient
from gt_telem.events import GameEvents
from gt_telem.errors.playstation_errors import *

# ansi prefix
pref = "\033["

def printAt(str, row=1, column=1, bold=0, underline=0, reverse=0):
        sys.stdout.write('{}{};{}H'.format(pref, row, column))
        if reverse:
            sys.stdout.write('{}7m'.format(pref))
        if bold:
            sys.stdout.write('{}1m'.format(pref))
        if underline:
            sys.stdout.write('{}4m'.format(pref))
        if not bold and not underline and not reverse:
            sys.stdout.write('{}0m'.format(pref))
        sys.stdout.write(str)
        sys.stdout.flush()

def clearscreen():
    clear = lambda:os.system('clear') #clear screen
    clear()                           #clear screen
           
class MySimpleTelemetryRecorder():
    def __init__(self, tc: TurismoClient):
        self.tc = tc
        self.storage = []

    def start(self):
        self.tc.register_callback(MySimpleTelemetryRecorder.receive_telem, [self])

    def stop(self):
        self.tc.deregister_callback(MySimpleTelemetryRecorder.receive_telem)
        # save self.storage somewhere

    @staticmethod
    async def receive_telem(t, context):
        context.storage.append(t)
        #print(f"{t.engine_rpm}RPM - {t.boost_pressure}kPa")
        #print(f"Best: {t.best_lap_time}\tLast: {t.last_lap_time}")
       
      
       #printAt('GRAND TURISMO LIVE DATA' ,3,10, reverse=1, bold=1)
        printAt('{:<92}'.format("          GRAND TURISMO LIVE DATA"), 3,1, reverse=1, bold=1)

        RPM = f"{t.engine_rpm}"
        printAt("Drehzahl:",4,1)
        printAt(RPM  + ' U/min',4,15, bold=1)
        
        



printAt("SPEED", 1, 1)
printAt("RPM", 1,71)
clearscreen()       

if __name__ == "__main__":
    clearscreen()
    try:
        tc = TurismoClient()
        tc.run()
    except PlayStatonOnStandbyError as e:
        print("Turn the playstation on")
        print(e)
    except PlayStationNotFoundError:
        print("Maybe I'm on the wrong network")
        print(e)
    else:
      #  clear = lambda:os.system('clear') #clear screen
       # clear()                           #clear screen
        ge = GameEvents(tc)
        mstr = MySimpleTelemetryRecorder(tc)
        ge.on_in_race.append(mstr.start)
        ge.on_race_end.append(mstr.stop)
        ge.on_paused.append(mstr.stop)
        print("Listening for telemetry. CTRL+C to stop")
        asyncio.run(tc.run())
        