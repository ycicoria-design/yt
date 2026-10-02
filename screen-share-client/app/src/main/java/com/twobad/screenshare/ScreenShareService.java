package com.twobad.screenshare;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.ServiceInfo;
import android.media.projection.MediaProjection;
import android.os.Build;
import android.os.IBinder;

import org.json.JSONObject;
import org.webrtc.DataChannel;
import org.webrtc.DefaultVideoDecoderFactory;
import org.webrtc.DefaultVideoEncoderFactory;
import org.webrtc.EglBase;
import org.webrtc.IceCandidate;
import org.webrtc.MediaConstraints;
import org.webrtc.MediaStream;
import org.webrtc.MediaStreamTrack;
import org.webrtc.PeerConnection;
import org.webrtc.PeerConnectionFactory;
import org.webrtc.RtpReceiver;
import org.webrtc.ScreenCapturerAndroid;
import org.webrtc.SdpObserver;
import org.webrtc.SessionDescription;
import org.webrtc.SurfaceTextureHelper;
import org.webrtc.VideoCapturer;
import org.webrtc.VideoSource;
import org.webrtc.VideoTrack;

import java.util.Collections;
import java.util.UUID;
import java.util.concurrent.TimeUnit;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import okhttp3.WebSocket;
import okhttp3.WebSocketListener;

public class ScreenShareService extends Service {
    public static final String ACTION_START = "com.twobad.screenshare.START";
    public static final String ACTION_STOP = "com.twobad.screenshare.STOP";
    public static final String EXTRA_RESULT_CODE = "resultCode";
    public static final String EXTRA_RESULT_DATA = "resultData";
    public static final String EXTRA_DISPLAY_NAME = "displayName";

    private static final String SERVER_WS = "wss://twobad-screen-share-admin.onrender.com/ws";
    private static final String CHANNEL_ID = "screen_share_active";
    private static final int NOTIFICATION_ID = 5201;

    private OkHttpClient http;
    private WebSocket socket;
    private String deviceId;
    private String displayName;
    private String adminPeerId;

    private EglBase eglBase;
    private PeerConnectionFactory factory;
    private SurfaceTextureHelper textureHelper;
    private VideoCapturer capturer;
    private VideoSource videoSource;
    private VideoTrack videoTrack;
    private PeerConnection peer;

    private Intent capturePermissionData;

    @Override
    public void onCreate() {
        super.onCreate();
        SharedPreferences p = getSharedPreferences("screen_share", MODE_PRIVATE);
        deviceId = p.getString("device_id", null);
        if (deviceId == null) {
            deviceId = UUID.randomUUID().toString();
            p.edit().putString("device_id", deviceId).apply();
        }
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        if (intent != null && ACTION_STOP.equals(intent.getAction())) {
            stopSelf();
            return START_NOT_STICKY;
        }
        if (intent == null || !ACTION_START.equals(intent.getAction())) {
            return START_NOT_STICKY;
        }

        displayName = intent.getStringExtra(EXTRA_DISPLAY_NAME);
        if (displayName == null || displayName.trim().isEmpty()) displayName = "Android user";

        if (Build.VERSION.SDK_INT >= 33) {
            capturePermissionData = intent.getParcelableExtra(EXTRA_RESULT_DATA, Intent.class);
        } else {
            capturePermissionData = intent.getParcelableExtra(EXTRA_RESULT_DATA);
        }

        int resultCode = intent.getIntExtra(EXTRA_RESULT_CODE, 0);
        if (capturePermissionData == null || resultCode == 0) {
            stopSelf();
            return START_NOT_STICKY;
        }

        startVisibleForeground();
        initWebRtc();
        startScreenCapture();
        connectSignaling();
        return START_STICKY;
    }

    private void startVisibleForeground() {
        NotificationManager nm = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
        if (Build.VERSION.SDK_INT >= 26) {
            NotificationChannel channel = new NotificationChannel(
                    CHANNEL_ID,
                    "Active screen sharing",
                    NotificationManager.IMPORTANCE_HIGH
            );
            channel.setDescription("Shown while your screen is being shared");
            nm.createNotificationChannel(channel);
        }

        Intent stopIntent = new Intent(this, ScreenShareService.class);
        stopIntent.setAction(ACTION_STOP);
        PendingIntent stopPending = PendingIntent.getService(
                this, 99, stopIntent,
                PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE
        );

        Intent openIntent = new Intent(this, MainActivity.class);
        PendingIntent openPending = PendingIntent.getActivity(
                this, 98, openIntent,
                PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE
        );

        Notification.Builder builder = Build.VERSION.SDK_INT >= 26
                ? new Notification.Builder(this, CHANNEL_ID)
                : new Notification.Builder(this);

        Notification notification = builder
                .setContentTitle("Screen sharing is active")
                .setContentText("Your screen is being shared. Tap Stop Sharing to end it.")
                .setSmallIcon(android.R.drawable.ic_menu_view)
                .setOngoing(true)
                .setContentIntent(openPending)
                .addAction(new Notification.Action.Builder(
                        null, "Stop Sharing", stopPending
                ).build())
                .build();

        if (Build.VERSION.SDK_INT >= 29) {
            startForeground(
                    NOTIFICATION_ID,
                    notification,
                    ServiceInfo.FOREGROUND_SERVICE_TYPE_MEDIA_PROJECTION
            );
        } else {
            startForeground(NOTIFICATION_ID, notification);
        }
    }

    private void initWebRtc() {
        PeerConnectionFactory.initialize(
                PeerConnectionFactory.InitializationOptions.builder(this)
                        .createInitializationOptions()
        );

        eglBase = EglBase.create();
        DefaultVideoEncoderFactory encoderFactory = new DefaultVideoEncoderFactory(
                eglBase.getEglBaseContext(), true, true
        );
        DefaultVideoDecoderFactory decoderFactory = new DefaultVideoDecoderFactory(
                eglBase.getEglBaseContext()
        );

        factory = PeerConnectionFactory.builder()
                .setVideoEncoderFactory(encoderFactory)
                .setVideoDecoderFactory(decoderFactory)
                .createPeerConnectionFactory();

        textureHelper = SurfaceTextureHelper.create(
                "ScreenCaptureThread",
                eglBase.getEglBaseContext()
        );

        videoSource = factory.createVideoSource(true);
        capturer = new ScreenCapturerAndroid(
                capturePermissionData,
                new MediaProjection.Callback() {
                    @Override
                    public void onStop() {
                        stopSelf();
                    }
                }
        );

        capturer.initialize(textureHelper, this, videoSource.getCapturerObserver());
        videoTrack = factory.createVideoTrack("screen-video", videoSource);
    }

    private void startScreenCapture() {
        try {
            capturer.startCapture(720, 1280, 20);
        } catch (Exception e) {
            stopSelf();
        }
    }

    private void connectSignaling() {
        http = new OkHttpClient.Builder()
                .pingInterval(20, TimeUnit.SECONDS)
                .retryOnConnectionFailure(true)
                .build();

        Request req = new Request.Builder().url(SERVER_WS).build();
        socket = http.newWebSocket(req, new WebSocketListener() {
            @Override
            public void onOpen(WebSocket webSocket, Response response) {
                try {
                    JSONObject hello = new JSONObject();
                    hello.put("type", "hello");
                    hello.put("role", "client");
                    hello.put("deviceId", deviceId);
                    hello.put("name", displayName);
                    webSocket.send(hello.toString());
                } catch (Exception ignored) {}
            }

            @Override
            public void onMessage(WebSocket webSocket, String text) {
                handleMessage(text);
            }
        });
    }

    private void handleMessage(String text) {
        try {
            JSONObject m = new JSONObject(text);
            if (!"signal".equals(m.optString("type"))) return;

            String from = m.optString("from");
            JSONObject data = m.optJSONObject("data");
            if (data == null) return;

            String kind = data.optString("kind");
            if ("offer".equals(kind)) {
                adminPeerId = from;
                createPeerConnection();

                SessionDescription offer = new SessionDescription(
                        SessionDescription.Type.OFFER,
                        data.getString("sdp")
                );

                peer.setRemoteDescription(new SimpleSdpObserver() {
                    @Override
                    public void onSetSuccess() {
                        MediaConstraints constraints = new MediaConstraints();
                        peer.createAnswer(new SimpleSdpObserver() {
                            @Override
                            public void onCreateSuccess(SessionDescription answer) {
                                peer.setLocalDescription(new SimpleSdpObserver() {
                                    @Override
                                    public void onSetSuccess() {
                                        sendSdp("answer", answer);
                                    }
                                }, answer);
                            }
                        }, constraints);
                    }
                }, offer);
            } else if ("candidate".equals(kind) && peer != null) {
                JSONObject c = data.optJSONObject("candidate");
                if (c != null) {
                    IceCandidate candidate = new IceCandidate(
                            c.optString("sdpMid"),
                            c.optInt("sdpMLineIndex"),
                            c.optString("candidate")
                    );
                    peer.addIceCandidate(candidate);
                }
            }
        } catch (Exception ignored) {}
    }

    private void createPeerConnection() {
        if (peer != null) {
            peer.close();
            peer = null;
        }

        PeerConnection.IceServer stun = PeerConnection.IceServer
                .builder("stun:stun.l.google.com:19302")
                .createIceServer();

        PeerConnection.RTCConfiguration config =
                new PeerConnection.RTCConfiguration(Collections.singletonList(stun));

        peer = factory.createPeerConnection(config, new PeerConnection.Observer() {
            @Override public void onSignalingChange(PeerConnection.SignalingState state) {}
            @Override public void onIceConnectionChange(PeerConnection.IceConnectionState state) {}
            @Override public void onIceConnectionReceivingChange(boolean receiving) {}
            @Override public void onIceGatheringChange(PeerConnection.IceGatheringState state) {}
            @Override public void onIceCandidate(IceCandidate candidate) { sendCandidate(candidate); }
            @Override public void onIceCandidatesRemoved(IceCandidate[] candidates) {}
            @Override public void onAddStream(MediaStream stream) {}
            @Override public void onRemoveStream(MediaStream stream) {}
            @Override public void onDataChannel(DataChannel dataChannel) {}
            @Override public void onRenegotiationNeeded() {}
            @Override public void onAddTrack(RtpReceiver receiver, MediaStream[] streams) {}
        });

        if (peer != null) {
            peer.addTrack(videoTrack, Collections.singletonList("screen-stream"));
        }
    }

    private void sendSdp(String kind, SessionDescription sdp) {
        if (socket == null || adminPeerId == null) return;
        try {
            JSONObject data = new JSONObject();
            data.put("kind", kind);
            data.put("type", sdp.type.canonicalForm());
            data.put("sdp", sdp.description);
            sendSignal(data);
        } catch (Exception ignored) {}
    }

    private void sendCandidate(IceCandidate c) {
        if (socket == null || adminPeerId == null) return;
        try {
            JSONObject candidate = new JSONObject();
            candidate.put("sdpMid", c.sdpMid);
            candidate.put("sdpMLineIndex", c.sdpMLineIndex);
            candidate.put("candidate", c.sdp);

            JSONObject data = new JSONObject();
            data.put("kind", "candidate");
            data.put("candidate", candidate);
            sendSignal(data);
        } catch (Exception ignored) {}
    }

    private void sendSignal(JSONObject data) throws Exception {
        JSONObject msg = new JSONObject();
        msg.put("type", "signal");
        msg.put("to", adminPeerId);
        msg.put("data", data);
        socket.send(msg.toString());
    }

    @Override
    public void onDestroy() {
        super.onDestroy();

        try { if (socket != null) socket.close(1000, "stopped"); } catch (Exception ignored) {}
        try { if (http != null) http.dispatcher().executorService().shutdown(); } catch (Exception ignored) {}
        try { if (peer != null) peer.close(); } catch (Exception ignored) {}
        try { if (capturer != null) capturer.stopCapture(); } catch (Exception ignored) {}
        try { if (capturer != null) capturer.dispose(); } catch (Exception ignored) {}
        try { if (videoSource != null) videoSource.dispose(); } catch (Exception ignored) {}
        try { if (textureHelper != null) textureHelper.dispose(); } catch (Exception ignored) {}
        try { if (factory != null) factory.dispose(); } catch (Exception ignored) {}
        try { if (eglBase != null) eglBase.release(); } catch (Exception ignored) {}
        stopForeground(true);
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    private static class SimpleSdpObserver implements SdpObserver {
        @Override public void onCreateSuccess(SessionDescription sdp) {}
        @Override public void onSetSuccess() {}
        @Override public void onCreateFailure(String error) {}
        @Override public void onSetFailure(String error) {}
    }
}
