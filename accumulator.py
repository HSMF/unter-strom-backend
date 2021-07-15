import threading
import time
import modbus


class Accumulator(threading.Thread):
    DELAY = 1

    def __init__(self, thread_id, ip, callback, runtime: int = 60) -> None:
        '''
        repeatedly download data for a minute and sum it up
        '''
        self.thread_id = thread_id
        self.val = 0
        self.runtime = runtime
        self.upload_func = callback
        self.client = modbus.ModbusClient(ip)
        threading.Thread.__init__(self)

    def run(self) -> None:
        t0 = time.time()
        while (time.time() - t0) < self.runtime:
            # ignore transaction time
            # not smart
            try:
                power = self.client.g3p() * self.DELAY # poor man's integration
            except:
                power = 0 
            self.val += power
            time.sleep(self.DELAY) # dont DoS the UMD
        self.client.close()
        self.upload_func(self.val)
        print(f"[*] {self.thread_id} has completed")
