package com.minddepth.polarconnectapp.Server;

import android.util.Log;

import com.koushikdutta.async.AsyncServer;
import com.koushikdutta.async.http.body.AsyncHttpRequestBody;
import com.koushikdutta.async.http.server.AsyncHttpServer;
import com.koushikdutta.async.http.server.AsyncHttpServerRequest;
import com.koushikdutta.async.http.server.AsyncHttpServerResponse;
import com.koushikdutta.async.http.server.HttpServerRequestCallback;
import com.minddepth.polarconnectapp.Interfaces.IPcaPacketHandler;
import com.minddepth.polarconnectapp.Models.ControlSessionPacket;
import com.minddepth.polarconnectapp.Models.InitPacket;

import org.json.JSONException;
import org.json.JSONObject;

public class PcaHttpServer {

    private static final String TAG = "PcaHttpServer";

    private AsyncHttpServer mServer = new AsyncHttpServer();
    private AsyncServer mAsyncServer = new AsyncServer();
    private PcaPacketParser mPacketHandler = new PcaPacketParser();
    private IPcaPacketHandler mHandler;
    private AsyncHttpServerResponse mPendingResponse = null;

    private HttpServerRequestCallback mCallback = new HttpServerRequestCallback() {
        @Override
        public void onRequest(AsyncHttpServerRequest request, AsyncHttpServerResponse response) {
            AsyncHttpRequestBody requestBody = request.getBody();
            try {
                String packet = new JSONObject(requestBody.get().toString()).getString("body");
                Log.d(TAG, "New post request received with the following content : " + packet);
                Object parsedPacket = mPacketHandler.parsePacket(packet);
                if (parsedPacket == null) {
                    Log.e(TAG, "Unable to parse the packet with the following content : " + packet);
                    response.code(400).send("Unable to parse the packet");
                } else {
                    mPendingResponse = response;
                    if (parsedPacket instanceof ControlSessionPacket) {
                        Log.d(TAG, "New Control Session packet received !");
                        mHandler.onControlSessionPacketReceived((ControlSessionPacket)parsedPacket);
                    } else if (parsedPacket instanceof InitPacket) {
                        Log.d(TAG, "New Init packet received !");
                        mHandler.onInitPacketReceived((InitPacket)parsedPacket);
                    }
                }
                response.code(200).send(packet);
            } catch (JSONException e) {
                Log.e(TAG, e.getMessage());
            }
        }
    };

    public PcaHttpServer(IPcaPacketHandler handler) {
        mHandler = handler;
    }

    public void start() {
        mServer.listen(mAsyncServer, 8080);
        mServer.post("/", mCallback);
    }

    public void stop() {
        mServer.stop();
        mAsyncServer.stop();
    }

    public void sendPendingResponse(int code, String message) {
        mPendingResponse.code(code).send(message);
        mPendingResponse = null;
    }
}
