package com.minddepth.polarconnectapp.Interfaces;

import com.minddepth.polarconnectapp.Models.BiofeedbackPacket;
import com.minddepth.polarconnectapp.Models.ControlSessionPacket;
import com.minddepth.polarconnectapp.Models.InitPacket;

public interface IPcaPacketHandler {
    void onInitPacketReceived(InitPacket packet);
    void onControlSessionPacketReceived(ControlSessionPacket packet);
    void onNewBiofeedbackReceived(BiofeedbackPacket packet);
}
