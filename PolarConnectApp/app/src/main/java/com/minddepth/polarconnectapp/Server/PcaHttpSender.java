package com.minddepth.polarconnectapp.Server;

import android.util.Log;

import com.minddepth.polarconnectapp.Models.BiofeedbackPacket;

import java.io.DataOutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class PcaHttpSender {

    private final static String TAG =  "PcaHttpSender";
    private String mClientEndPoint;

    public void initEndpoint(String ip, int port, String route) {
        mClientEndPoint = "http://" + ip + ":" + port + route;
    }

    public void sendPacket(final BiofeedbackPacket bfp) {
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    Log.d(TAG,  "Sending bfp to " + mClientEndPoint + " ...");
                    URL url = new URL(mClientEndPoint);
                    HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                    conn.setRequestMethod("POST");
                    conn.setRequestProperty("Content-Type", "application/json;charset=UTF-8");
                    conn.setRequestProperty("Accept","application/json");
                    conn.setReadTimeout(1);
                    conn.setDoOutput(true);
                    conn.setDoInput(false);
                    //conn.setReadTimeout(2000);

                    DataOutputStream os = new DataOutputStream(conn.getOutputStream());
                    os.writeBytes(bfp.toJson());

                    os.flush();
                    os.close();

                    Log.i("STATUS", String.valueOf(conn.getResponseCode()));
                    Log.i("MSG" , conn.getResponseMessage());

                    conn.disconnect();
                } catch (Exception e) {
                    Log.e(TAG, e.getMessage());
                }
            }
        }).start();
    }
}
