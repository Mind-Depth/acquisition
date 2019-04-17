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

import com.minddepth.polarconnectapp.databinding.ActivityMainBinding;

public class MainActivity extends AppCompatActivity {

    BLEConnector    mConnector;
    DisplayableInfo infos;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        infos = new DisplayableInfo();
        mConnector = new BLEConnector(this, infos);
        if (mConnector.isBluetoothDisabled()) {
            Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            startActivityForResult(enableBtIntent, 42);
        }
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION)!= PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.ACCESS_COARSE_LOCATION},43);
        } //TODO add gps activation check when launched


        ActivityMainBinding binding = DataBindingUtil.setContentView(this, R.layout.activity_main);
        binding.setInfo(infos);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        mConnector.disconnect();
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
