package com.minddepth.polarconnectapp.Models;

import com.google.gson.GsonBuilder;

public class BiofeedbackPacket {
    public String message_type;
    public int bf;
    public long timestamp;

    public BiofeedbackPacket(int data, long time) {
        message_type = "BIOFEEDBACK";
        bf = data;
        timestamp = time;
    }

    public String toJson() {
        return new GsonBuilder().create().toJson(this);
    }
}
