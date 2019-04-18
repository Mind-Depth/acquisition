package com.minddepth.polarconnectapp;

import android.os.AsyncTask;

import java.net.InetAddress;
import java.net.NetworkInterface;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.util.Enumeration;

public class NetworkUtils extends AsyncTask<Void, Integer, String> {

    @Override
    protected String doInBackground(Void... voids) {
        try {
            String ipAddress = "lul";
            for (Enumeration<NetworkInterface> en = NetworkInterface.getNetworkInterfaces(); en.hasMoreElements();) {
                NetworkInterface intf = en.nextElement();
                for (Enumeration<InetAddress> enumIpAddr = intf.getInetAddresses(); enumIpAddr.hasMoreElements();) {
                    InetAddress inetAddress = enumIpAddr.nextElement();
                    if (!inetAddress.isLoopbackAddress()) {
                        ipAddress = inetAddress.getHostAddress();
                    }
                }
            }
            return ipAddress;
        } catch (SocketException e) {
            e.printStackTrace();
            return "Error";
        }
    }


}
