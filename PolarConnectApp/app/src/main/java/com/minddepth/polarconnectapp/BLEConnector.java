package com.minddepth.polarconnectapp;

import android.app.Service;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothClass;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothGatt;
import android.bluetooth.BluetoothGattCallback;
import android.bluetooth.BluetoothGattCharacteristic;
import android.bluetooth.BluetoothGattDescriptor;
import android.bluetooth.BluetoothGattService;
import android.bluetooth.BluetoothManager;
import android.bluetooth.BluetoothProfile;
import android.bluetooth.le.BluetoothLeScanner;
import android.bluetooth.le.ScanCallback;
import android.bluetooth.le.ScanResult;
import android.content.Context;
import android.content.Intent;
import android.os.Handler;
import android.os.IBinder;
import android.util.Log;

import java.util.List;
import java.util.UUID;

public class BLEConnector extends Service {
    private BluetoothDevice     mDevice;
    private BluetoothAdapter    mBluetoothAdapter;
    private BluetoothLeScanner  mBluetoothScanner;
    private BluetoothGatt       mBluetoothGatt;
    private Context             mContext;
    private Handler             mHandler;
    
    private static final String POLAR_MAC_ADDRESS = "F1:1D:4A:90:FC:BD";
    private static final long   SCAN_PERIOD = 10000;
    public final static UUID    UUID_HEART_RATE_MEASUREMENT = UUID.fromString("00002a37-0000-1000-8000-00805f9b34fb");
    

    BLEConnector(Context context) {
        mContext = context;

        final BluetoothManager bluetoothManager =
                (BluetoothManager) mContext.getSystemService(Context.BLUETOOTH_SERVICE);
        mBluetoothAdapter = bluetoothManager.getAdapter();
        mBluetoothScanner = mBluetoothAdapter.getBluetoothLeScanner();
        mHandler = new Handler();
    }

    boolean isBluetoothDisabled() {
        return (mBluetoothAdapter == null || !mBluetoothAdapter.isEnabled());
    }

    private ScanCallback leScanCallback = new ScanCallback() {

        @Override
        public void onScanFailed(int errorCode) {
            super.onScanFailed(errorCode);
            Log.d("MinDepth", "Scanning for devices failed");
            //TODO trigger a visual response for the user
        }

        @Override
        public void onScanResult(int callbackType, ScanResult result) {
            super.onScanResult(callbackType, result);
            if (result.getDevice().getAddress().equals(POLAR_MAC_ADDRESS)) {
                Log.i("MinDepth", "Polar H10 device found");
                mDevice = result.getDevice();
                scanBluetoothDevices(false);
            }
        }
    };

    void scanBluetoothDevices(final boolean toggle) {
        // Stops scanning after a pre-defined scan period.
        if (toggle) {
            mHandler.postDelayed(new Runnable() {
                @Override
                public void run() {
                    Log.i("MinDepth", "Stopping scan (timeout)");
                    mBluetoothScanner.stopScan(leScanCallback);
                }
            }, SCAN_PERIOD);

            Log.i("MinDepth", "Scanning");
            mBluetoothScanner.startScan(leScanCallback);
        } else {
            Log.i("MinDepth", "Stopping scan");
            mBluetoothScanner.stopScan(leScanCallback);
        }
        if (mDevice != null)
            mBluetoothGatt = mDevice.connectGatt(this, false, gattCallback);
    }

    private final BluetoothGattCallback gattCallback =
            new BluetoothGattCallback() {
                @Override
                public void onConnectionStateChange(BluetoothGatt gatt, int status,
                                                    int newState) {
                    if (newState == BluetoothProfile.STATE_CONNECTED) {
                        Log.i("MinDepth", "Connected to GATT server.");
                        Log.i("MinDepth", "Attempting to start service discovery : " + mBluetoothGatt.discoverServices());

                    } else if (newState == BluetoothProfile.STATE_DISCONNECTED)
                        Log.i("MinDepth", "Disconnected from GATT server.");
                }

                @Override
                public void onServicesDiscovered(BluetoothGatt gatt, int status) {
                    if (status == BluetoothGatt.GATT_SUCCESS) {
                        for (BluetoothGattService gattService : gatt.getServices()) {
                            for (BluetoothGattCharacteristic gattCharacteristic : gattService.getCharacteristics()) {
                                if (gattCharacteristic.getUuid().equals(UUID_HEART_RATE_MEASUREMENT)) {
                                    Log.i("MinDepth", "Found heart rate characteristic of Polar H10");
                                    gatt.setCharacteristicNotification(gattCharacteristic, true);
                                    BluetoothGattDescriptor descriptor = gattCharacteristic.getDescriptors().get(0);
                                    descriptor.setValue(BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE);
                                    gatt.writeDescriptor(descriptor);
                                }
                            }
                        }
                    } else
                        Log.i("MinDepth", "onServicesDiscovered failed with status : " + status);
                }

                @Override
                public void onCharacteristicChanged(BluetoothGatt gatt, BluetoothGattCharacteristic characteristic) {
                    getHeartRateValue(characteristic);
                }
            };

    private void getHeartRateValue(final BluetoothGattCharacteristic characteristic) {
        if (UUID_HEART_RATE_MEASUREMENT.equals(characteristic.getUuid())) {
            int flag = characteristic.getProperties();
            int format = -1;
            if ((flag & 0x01) != 0)
                format = BluetoothGattCharacteristic.FORMAT_UINT16;
            else
                format = BluetoothGattCharacteristic.FORMAT_UINT8; //this is the format used by the Polar H10, but keeping the if/else in case we change the device
            final int heartRate = characteristic.getIntValue(format, 1);
        }
    }

    void disconnect() {
        if (mBluetoothGatt != null) {
            Log.i("MinDepth", "Disconnecting");
            mBluetoothGatt.disconnect();
            mBluetoothGatt.close();
        }
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
}
