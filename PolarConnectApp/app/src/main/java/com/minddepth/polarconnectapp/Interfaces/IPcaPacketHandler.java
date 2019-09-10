package com.minddepth.polarconnectapp.Interfaces;

import com.minddepth.polarconnectapp.Models.BiofeedbackPacket;
import com.minddepth.polarconnectapp.Models.ControlSessionPacket;
import com.minddepth.polarconnectapp.Models.InitPacket;

import org.json.JSONException;

public interface IPcaPacketHandler {
    void onInitPacketReceived(InitPacket packet) throws JSONException;
    void onControlSessionPacketReceived(ControlSessionPacket packet) throws JSONException;
    void onNewBiofeedbackReceived(BiofeedbackPacket packet);
}
