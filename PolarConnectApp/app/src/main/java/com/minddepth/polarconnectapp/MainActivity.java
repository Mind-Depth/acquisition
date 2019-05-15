package com.minddepth.polarconnectapp;

import android.Manifest;
import android.bluetooth.BluetoothAdapter;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.databinding.DataBindingUtil;
import android.support.annotation.RequiresPermission;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.CompoundButton;
import android.widget.ToggleButton;

import com.minddepth.polarconnectapp.Server.PcaHttpServerController;
import com.minddepth.polarconnectapp.databinding.ActivityMainBinding;

public class MainActivity extends AppCompatActivity {

    private BLEConnector    mConnector;
    private DisplayableInfo mInfos;
    private PcaHttpServerController mServerController = new PcaHttpServerController();


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mInfos = new DisplayableInfo();
        mConnector = new BLEConnector(this, mInfos);
        if (mConnector.isBluetoothDisabled()) {
            Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            startActivityForResult(enableBtIntent, 42);
        }
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION)!= PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.ACCESS_COARSE_LOCATION},43);
        } //TODO add gps activation check when launched

        mServerController.startServer();

        ActivityMainBinding binding = DataBindingUtil.setContentView(this, R.layout.activity_main);
        binding.setInfo(mInfos);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        mConnector.disconnect();
        mServerController.stopServer();
    }

    @RequiresPermission(Manifest.permission.BLUETOOTH_ADMIN)
    public void onCheckedChanged(View view) {
        boolean isChecked = ((ToggleButton) view).isChecked();

        if (isChecked) {
            Log.d("panophobia", "connect clicked");
            mConnector.scanBluetoothDevices(true);
        } else {
            Log.d("panophobia", "disconnect clicked");
            mConnector.disconnect();
        }

    }
}
