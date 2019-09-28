package com.minddepth.polarconnectapp;

import android.app.Service;
import android.bluetooth.BluetoothAdapter;
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
import android.widget.Toast;

import com.minddepth.polarconnectapp.Interfaces.IPcaPacketHandler;
import com.minddepth.polarconnectapp.Models.BiofeedbackPacket;

import java.util.UUID;

public class BLEConnector extends Service {
    private BluetoothDevice     mDevice;
    private BluetoothAdapter    mBluetoothAdapter;
    private BluetoothLeScanner  mBluetoothScanner;
    private BluetoothGatt       mBluetoothGatt;
    private Context             mContext;
    private Handler             mHandler;
    private IPcaPacketHandler   mPcaHandler;
    
    private static final long   SCAN_PERIOD = 10000;
    public final static UUID    UUID_HEART_RATE_MEASUREMENT = UUID.fromString("00002a37-0000-1000-8000-00805f9b34fb");

    private DisplayableInfo     mInfos;

    BLEConnector(Context context, DisplayableInfo infos, IPcaPacketHandler pcaPacketHandler) {
        mContext = context;
        mInfos = infos;
        mPcaHandler = pcaPacketHandler;

        final BluetoothManager bluetoothManager =
                (BluetoothManager) mContext.getSystemService(Context.BLUETOOTH_SERVICE);
        mBluetoothAdapter = bluetoothManager.getAdapter();
        mHandler = new Handler();
    }

    void getScanner() {
        mBluetoothScanner = mBluetoothAdapter.getBluetoothLeScanner();
    }

    boolean isBluetoothDisabled() {
        return (mBluetoothAdapter == null || !mBluetoothAdapter.isEnabled());
    }

    private ScanCallback leScanCallback = new ScanCallback() {

        @Override
        public void onScanFailed(int errorCode) {
            super.onScanFailed(errorCode);
            Toast.makeText(mContext, "Scanning for devices failed", Toast.LENGTH_SHORT).show();
        }

        @Override
        public void onScanResult(int callbackType, ScanResult result) {
            super.onScanResult(callbackType, result);
            if (result.getDevice().getAddress().equals(mInfos.getMacAddress())) {
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
                    if (mDevice == null)
                        mInfos.setState(DisplayableInfo.STATUS_DISCO);
                }
            }, SCAN_PERIOD);

            Log.i("MinDepth", "Scanning");
            mBluetoothScanner.startScan(leScanCallback);
            mInfos.setState(DisplayableInfo.STATUS_SCAN);
        } else {
            Log.i("MinDepth", "Stopping scan");
            mBluetoothScanner.stopScan(leScanCallback);
            if (mDevice == null)
                mInfos.setState(DisplayableInfo.STATUS_DISCO);
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

                    } else if (newState == BluetoothProfile.STATE_DISCONNECTED) {
                        Log.i("MinDepth", "Disconnected from GATT server.");
                        mInfos.setState(DisplayableInfo.STATUS_DISCO);
                        mInfos.setHeartBeat("???");
                    }
                }

                @Override
                public void onServicesDiscovered(BluetoothGatt gatt, int status) {
                    if (status == BluetoothGatt.GATT_SUCCESS) {
                        for (BluetoothGattService gattService : gatt.getServices()) {
                            for (BluetoothGattCharacteristic gattCharacteristic : gattService.getCharacteristics()) {
                                if (gattCharacteristic.getUuid().equals(UUID_HEART_RATE_MEASUREMENT)) {
                                    Log.i("MinDepth", "Found heart rate characteristic of Polar H10");
                                    if (gatt.setCharacteristicNotification(gattCharacteristic, true))
                                        mInfos.setState(DisplayableInfo.STATUS_POLAR);
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
            mInfos.setHeartBeat(String.valueOf(characteristic.getIntValue(format, 1)));
            mPcaHandler.onNewBiofeedbackReceived(new BiofeedbackPacket(characteristic.getIntValue(format, 1), System.currentTimeMillis()));
        }
    }

    void disconnect() {
        if (mBluetoothGatt != null) {
            Log.i("MinDepth", "Disconnecting");
            mBluetoothGatt.disconnect();
        }
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
}
