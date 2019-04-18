package com.minddepth.polarconnectapp.Server;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.minddepth.polarconnectapp.Models.ControlSessionPacket;
import com.minddepth.polarconnectapp.Models.GenericPacket;
import com.minddepth.polarconnectapp.Models.InitPacket;

public class PcaPacketParser {
    private Gson mGsonBuilder = new GsonBuilder().create();

    public Object parsePacket(String json) {
        GenericPacket gp = mGsonBuilder.fromJson(json, GenericPacket.class);
        switch (gp.message_type) {
            case "INIT":
                InitPacket ip = mGsonBuilder.fromJson(json, InitPacket.class);
                return ip;
            case "CONTROL_SESSION":
                ControlSessionPacket csp = mGsonBuilder.fromJson(json, ControlSessionPacket.class);
                return csp;
        }
        return null;
    }
}
