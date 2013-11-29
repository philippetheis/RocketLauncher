# ----------------------------------------------------------------------------
# GSI's hack for dummys in coorperation with "Binary retards"
# ----------------------------------------------------------------------------

from __future__ import print_function

import time
import serial               # pyserial

# ---------------------------------------------------------------------------|
class Serial_Tester(object):

    # -----------------------------------------------------------------------|
    def __init__(self, port_name, BR=38400):
        """
        port_name   "com1", ...
        BR          9600, 19200, 38400, 57600
        """

        self._port = serial.Serial(port_name, BR, timeout = 0.1)

    # -----------------------------------------------------------------------|
    def _write(self, cmd):
        s = ""
        for b in cmd:
            s = s + chr(b)
        print("here it comes: ", s)    
        self._port.write(s)

    # -----------------------------------------------------------------------|
    def _read(self):
        s = ""
        ref = time.time()
        while 1:
            while self._port.inWaiting() == 0:
                if (time.time() - ref) > 1:
                    raise Exception()
            s = s + self._port.read(1)

            # check if length of answer is equal to length byte
            if len(s) == ord(s[0]) + 1:
                break

        # convert answer to bytes
        a = []
        for c in s:
            a.append(ord(c))
        return a

    # -----------------------------------------------------------------------|
    def _wait(self, timeout):
        """
        timeout in seconds
        """
        ref = time.time()
        while (time.time() - ref) < timeout:
            pass

    # -----------------------------------------------------------------------|
    def cmd_IDLE(self):
        """
        send_cmd
        """
        
        print("here I start writing")
        # send command
        cmd = [0x04,0x00,0x02,0x79,0x40]

        #send cmd over Serial
        self._write(cmd)

        # get answer
        asw = self._read()

        # print answer
        print("and here is your answer Richard ;-): ", asw)

    # -----------------------------------------------------------------------|
    def cmd_SEARCH_TXP_443A(self):
        """
        send_cmd
        """
        
        print("here I start writing")
        # send command
        cmd = [0x04,0x17,0x02,0xA1,0xD9]

        #send cmd over Serial
        self._write(cmd)

        # get answer
        asw = self._read()

        # print answer
        print("and here is your answer Richard ;-): ", asw)
        
        
# ---------------------------------------------------------------------------|
if __name__ == "__main__":
    
    st = Serial_Tester(port_name = "COM9", BR=115200)
    st.cmd_IDLE()
    st.cmd_SEARCH_TXP_443A()


 #==============================================================================
 # ---------------------------------------------------------------------------|
 # end of file
 #==============================================================================
