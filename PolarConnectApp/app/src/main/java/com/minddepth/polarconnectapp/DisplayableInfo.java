package com.minddepth.polarconnectapp;

import android.databinding.BaseObservable;
import android.databinding.Bindable;

import java.util.concurrent.ExecutionException;

public class DisplayableInfo extends BaseObservable {
    private String heartBeat = "???";
    private String macAddress = "F1:1D:4A:90:FC:BD";
    private String status = "Status : Disconnected";
    private String state = STATUS_DISCO;
    private String ipAddress = "Unknown";

    static final String STATUS_DISCO = "Disconnected";
    static final String STATUS_SCAN = "Scanning for BLE device";
    static final String STATUS_POLAR = "Connected to BLE device";
    static final String STATUS_TRANS = "Transmitting";

    DisplayableInfo() {
        NetworkUtils utils = new NetworkUtils();
        try {
            ipAddress = utils.execute().get();
        } catch (ExecutionException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    @Bindable
    public String getHeartBeat() {
        return heartBeat;
    }

    public void setHeartBeat(String hb) {
        heartBeat = hb;
        notifyPropertyChanged(BR.heartBeat);
    }

    @Bindable
    public String getMacAddress() {
        return macAddress;
    }

    public void setMacAddress(String mac) {
        macAddress = mac;
        notifyPropertyChanged(BR.macAddress);
    }

    @Bindable
    public String getStatus() {
        return status;
    }

    public void setStatus(String stat) {
        status = stat;
        notifyPropertyChanged(BR.status);
    }

    void setState(String newState) {
        state = newState;
        setStatus("Status : " + state);
    }

    @Bindable
    public String getIpAddress() {
        return ipAddress;
    }

    public void setIpAddress(String addr) {
        ipAddress = addr;
        notifyPropertyChanged(BR.ipAddress);
    }
}
