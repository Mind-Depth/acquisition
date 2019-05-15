package com.minddepth.polarconnectapp.Server;

import android.util.Log;

import com.minddepth.polarconnectapp.Interfaces.IPcaPacketHandler;
import com.minddepth.polarconnectapp.Models.BiofeedbackPacket;
import com.minddepth.polarconnectapp.Models.ControlSessionPacket;
import com.minddepth.polarconnectapp.Models.InitPacket;

public class PcaHttpServerController implements IPcaPacketHandler {
    private enum PcaHttpServerControllerState {
        IDLE,
        INIT,
        STARTED
    }

    private final static String TAG = "PcaHttpServerController";

    private PcaHttpServer mServer;
    private PcaHttpSender mSender;
    private PcaHttpServerControllerState mState;
    private String mClientIp;
    private int mClientPort;
    private String mClientRoute;


    public PcaHttpServerController() {
        mServer = new PcaHttpServer(this);
        mSender = new PcaHttpSender();
        mState = PcaHttpServerControllerState.IDLE;
    }

    public void startServer() {
        mServer.start();
    }

    public void stopServer() {
        mServer.stop();
    }

    public void sendBiofeedbackToClient(BiofeedbackPacket packet) {
        if (mState ==  PcaHttpServerControllerState.STARTED) {
            mSender.sendPacket(packet);
        } else {
            Log.e(TAG, "Unable to send biofeedback data to client : Server is not started");
        }
    }

    private void initClientInfo(String ip, int port, String route) {
        mClientIp = ip;
        mClientPort = port;
        mClientRoute = route;
    }

    // IPcaPacketHandler methods

    @Override
    public void onInitPacketReceived(InitPacket packet) {
        if (mState == PcaHttpServerControllerState.IDLE)  {
            initClientInfo(packet.client_ip, packet.client_port, packet.client_rte);
            mSender.initEndpoint(mClientIp, mClientPort, mClientRoute);
            mState = PcaHttpServerControllerState.INIT;
            mServer.sendPendingResponse(200, "Pca successfully init ");
            Log.d(TAG, "Initialization with the following values : "  + mClientIp + ":" + mClientPort + mClientRoute);
        } else {
            mServer.sendPendingResponse(400, "Pca already init or launched");
            Log.e(TAG, "Pca already init or launched");
        }
    }

    @Override
    public void onControlSessionPacketReceived(ControlSessionPacket packet) {
        if (mState == PcaHttpServerControllerState.INIT && packet.status) {
            mState = PcaHttpServerControllerState.STARTED;
            mServer.sendPendingResponse(200, "Pca successfully started");
            Log.d(TAG, "Launching Pca broadcasting...");


            sendBiofeedbackToClient(new BiofeedbackPacket(55, 123456789));
        } else if (mState == PcaHttpServerControllerState.STARTED && !packet.status) {
            mState = PcaHttpServerControllerState.INIT;
            mServer.sendPendingResponse(200, "Pca successfully stopped");
            Log.d(TAG, "Stopping Pca broadcasting...");
        } else {
            mServer.sendPendingResponse(400, "Pca not init or started");
            Log.e(TAG, "Pca not init or started");
        }
    }
}