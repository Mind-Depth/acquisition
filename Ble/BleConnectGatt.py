#!/usr/local/bin/python3

import gatt

manager = gatt.DeviceManager(adapter_name='hci0')

class AnyDevice(gatt.Device):
    def connect_succeeded(self):
        super().connect_succeeded()
        print("[%s] Connected" % (self.mac_address))

    def connect_failed(self, error):
        super().connect_failed(error)
        print("[%s] Connection failed: %s" % (self.mac_address, str(error)))

    def disconnect_succeeded(self):
        super().disconnect_succeeded()
        print("[%s] Disconnected" % (self.mac_address))

    def services_resolved(self):
        super().services_resolved()

        print("[%s] Resolved services" % (self.mac_address))
        for service in self.services:
            print("[%s]  Service [%s]" % (self.mac_address, service.uuid))
            for characteristic in service.characteristics:
                if ("00002a37-0000-1000-8000-00805f9b34fb" in characteristic.uuid):
                    print (characteristic)
                    characteristic.enable_notifications()
                    characteristic.write_value([0,1,0,0])
                    #print("[%s]    Characteristic [%s]" % (self.mac_address, characteristic.uuid))

    def characteristic_value_updated(self, characteristic, value):
        print(value)

device = AnyDevice(mac_address='F1:1D:4A:90:FC:BD', manager=manager)
device.connect()

manager.run()