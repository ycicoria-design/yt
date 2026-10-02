package com.twobad.esp;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.Service;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.PixelFormat;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.os.Build;
import android.os.IBinder;
import android.view.Gravity;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.HorizontalScrollView;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.SeekBar;
import android.widget.Space;
import android.widget.Switch;
import android.widget.TextView;

public class OverlayService extends Service {
    private WindowManager wm;
    private TextView bubble;
    private LinearLayout menu;
    private LinearLayout content;
    private TextView sectionTitle;
    private WindowManager.LayoutParams bubbleParams;
    private WindowManager.LayoutParams menuParams;
    private boolean handcamMode = false;
    private boolean streamerMode = false;

    private final int bg = Color.rgb(8, 10, 14);
    private final int card = Color.rgb(17, 21, 28);
    private final int card2 = Color.rgb(24, 29, 39);
    private final int accent = Color.rgb(68, 245, 187);
    private final int muted = Color.rgb(154, 164, 181);
    private final int border = Color.rgb(42, 50, 62);

    @Override
    public void onCreate() {
        super.onCreate();
        startAsForeground();
        wm = (WindowManager) getSystemService(WINDOW_SERVICE);
        createBubble();
        createMenu();
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        if (bubble != null) bubble.setVisibility(View.VISIBLE);
        return START_STICKY;
    }

    private void startAsForeground() {
        String channelId = "2bad_overlay";
        NotificationManager nm = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel ch = new NotificationChannel(
                    channelId, "2BAD Overlay", NotificationManager.IMPORTANCE_LOW
            );
            nm.createNotificationChannel(ch);
        }

        Notification.Builder b = Build.VERSION.SDK_INT >= Build.VERSION_CODES.O
                ? new Notification.Builder(this, channelId)
                : new Notification.Builder(this);

        Notification n = b
                .setContentTitle("2BAD ESP")
                .setContentText("Overlay is active")
                .setSmallIcon(android.R.drawable.ic_menu_view)
                .setOngoing(true)
                .build();

        startForeground(22, n);
    }

    private int overlayType() {
        return Build.VERSION.SDK_INT >= Build.VERSION_CODES.O
                ? WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
                : WindowManager.LayoutParams.TYPE_PHONE;
    }

    private void createBubble() {
        bubble = label("2B", 15, Color.BLACK, true);
        bubble.setGravity(Gravity.CENTER);
        bubble.setBackground(roundRect(accent, 25));
        bubble.setElevation(dp(10));

        bubbleParams = new WindowManager.LayoutParams(
                dp(54), dp(54),
                overlayType(),
                WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE
                        | WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS,
                PixelFormat.TRANSLUCENT
        );
        bubbleParams.gravity = Gravity.TOP | Gravity.START;
        bubbleParams.x = dp(18);
        bubbleParams.y = dp(150);

        wm.addView(bubble, bubbleParams);
        enableBubbleDrag();
    }

    private void enableBubbleDrag() {
        bubble.setOnTouchListener(new View.OnTouchListener() {
            float downX, downY;
            int startX, startY;
            long downAt;

            @Override
            public boolean onTouch(View v, MotionEvent e) {
                switch (e.getActionMasked()) {
                    case MotionEvent.ACTION_DOWN:
                        downX = e.getRawX();
                        downY = e.getRawY();
                        startX = bubbleParams.x;
                        startY = bubbleParams.y;
                        downAt = System.currentTimeMillis();
                        return true;

                    case MotionEvent.ACTION_MOVE:
                        bubbleParams.x = startX + (int) (e.getRawX() - downX);
                        bubbleParams.y = startY + (int) (e.getRawY() - downY);
                        wm.updateViewLayout(bubble, bubbleParams);
                        return true;

                    case MotionEvent.ACTION_UP:
                        float dx = Math.abs(e.getRawX() - downX);
                        float dy = Math.abs(e.getRawY() - downY);
                        if (dx < dp(8) && dy < dp(8) && System.currentTimeMillis() - downAt < 500) {
                            showMenu();
                        }
                        return true;
                }
                return false;
            }
        });
    }

    private void createMenu() {
        menu = new LinearLayout(this);
        menu.setOrientation(LinearLayout.VERTICAL);
        menu.setPadding(dp(12), dp(12), dp(12), dp(14));
        menu.setBackground(strokedRect(bg, 20, border));
        menu.setElevation(dp(16));
        menu.setVisibility(View.GONE);

        menuParams = new WindowManager.LayoutParams(
                dp(346), WindowManager.LayoutParams.WRAP_CONTENT,
                overlayType(),
                WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL
                        | WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS,
                PixelFormat.TRANSLUCENT
        );
        menuParams.gravity = Gravity.TOP | Gravity.START;
        menuParams.x = dp(14);
        menuParams.y = dp(105);

        buildHeader();
        gap(menu, 10);
        buildTabs();
        gap(menu, 10);

        sectionTitle = label("ESP", 12, accent, true);
        sectionTitle.setLetterSpacing(0.12f);
        sectionTitle.setPadding(dp(4), 0, 0, dp(7));
        menu.addView(sectionTitle, matchWrap());

        content = new LinearLayout(this);
        content.setOrientation(LinearLayout.VERTICAL);
        menu.addView(content, matchWrap());

        wm.addView(menu, menuParams);
        renderCategory("ESP");
    }

    private void buildHeader() {
        LinearLayout header = new LinearLayout(this);
        header.setOrientation(LinearLayout.HORIZONTAL);
        header.setGravity(Gravity.CENTER_VERTICAL);
        header.setPadding(dp(8), dp(7), dp(8), dp(7));
        header.setBackground(roundRect(card, 15));
        menu.addView(header, matchWrap());

        ImageView logo = new ImageView(this);
        logo.setImageResource(R.drawable.logo);
        logo.setScaleType(ImageView.ScaleType.CENTER_CROP);
        logo.setBackground(roundRect(card2, 11));
        logo.setClipToOutline(true);
        header.addView(logo, new LinearLayout.LayoutParams(dp(40), dp(40)));

        LinearLayout titles = new LinearLayout(this);
        titles.setOrientation(LinearLayout.VERTICAL);
        titles.setPadding(dp(10), 0, 0, 0);
        header.addView(titles, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));

        TextView name = label("2BAD ESP", 16, Color.WHITE, true);
        titles.addView(name, matchWrap());
        TextView sub = label("OVERLAY MENU", 9, muted, true);
        sub.setLetterSpacing(0.14f);
        titles.addView(sub, matchWrap());

        Button hide = smallButton("—");
        header.addView(hide, new LinearLayout.LayoutParams(dp(42), dp(38)));
        hide.setOnClickListener(v -> hideMenu());
    }

    private void buildTabs() {
        HorizontalScrollView hs = new HorizontalScrollView(this);
        hs.setHorizontalScrollBarEnabled(false);
        menu.addView(hs, matchWrap());

        LinearLayout row = new LinearLayout(this);
        row.setOrientation(LinearLayout.HORIZONTAL);
        hs.addView(row, new HorizontalScrollView.LayoutParams(
                ViewGroup.LayoutParams.WRAP_CONTENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
        ));

        addTab(row, "ESP");
        addTab(row, "WORLD");
        addTab(row, "DISPLAY");
        addTab(row, "UTILITY");
    }

    private void addTab(LinearLayout row, String name) {
        Button b = actionButton(name);
        LinearLayout.LayoutParams p = new LinearLayout.LayoutParams(dp(92), dp(42));
        p.setMargins(0, 0, dp(6), 0);
        row.addView(b, p);
        b.setOnClickListener(v -> renderCategory(name));
    }

    private void renderCategory(String category) {
        if (content == null) return;
        content.removeAllViews();
        sectionTitle.setText(category);

        if ("ESP".equals(category)) {
            addSwitchRow("Enable ESP", true);
            addSwitchRow("Box", true);
            addSwitchRow("Skeleton", false);
            addSwitchRow("Health Bar", true);
            addSwitchRow("Name", true);
            addSwitchRow("Distance", true);
        } else if ("WORLD".equals(category)) {
            addSwitchRow("Loot", true);
            addSwitchRow("Vehicles", true);
            addSwitchRow("Grenade Warning", true);
        } else if ("DISPLAY".equals(category)) {
            Switch streamer = addSwitchRow("Streamer Mode", streamerMode);
            streamer.setOnCheckedChangeListener((buttonView, checked) -> streamerMode = checked);

            TextView op = label("MENU OPACITY", 10, muted, true);
            op.setPadding(dp(4), dp(8), 0, dp(4));
            content.addView(op, matchWrap());

            SeekBar seek = new SeekBar(this);
            seek.setMax(100);
            seek.setProgress((int) (menu.getAlpha() * 100));
            content.addView(seek, matchWrap());
            seek.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
                @Override public void onProgressChanged(SeekBar s, int p, boolean fromUser) {
                    menu.setAlpha(Math.max(.45f, p / 100f));
                }
                @Override public void onStartTrackingTouch(SeekBar s) {}
                @Override public void onStopTrackingTouch(SeekBar s) {}
            });
        } else {
            Button hide = primaryButton("HIDE SCREEN");
            content.addView(hide, new LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT, dp(48)
            ));
            hide.setOnClickListener(v -> hideMenu());

            gap(content, 8);

            Button handcam = actionButton(handcamMode ? "EXIT HANDCAM MODE" : "HANDCAM MODE");
            content.addView(handcam, new LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT, dp(48)
            ));
            handcam.setOnClickListener(v -> {
                handcamMode = !handcamMode;
                if (handcamMode) {
                    menu.setAlpha(.76f);
                    menuParams.width = dp(285);
                } else {
                    menu.setAlpha(1f);
                    menuParams.width = dp(346);
                }
                wm.updateViewLayout(menu, menuParams);
                renderCategory("UTILITY");
            });

            gap(content, 8);

            Button stop = actionButton("DISABLE OVERLAY");
            content.addView(stop, new LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT, dp(48)
            ));
            stop.setOnClickListener(v -> stopSelf());
        }
    }

    private Switch addSwitchRow(String name, boolean checked) {
        LinearLayout row = new LinearLayout(this);
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.setGravity(Gravity.CENTER_VERTICAL);
        row.setPadding(dp(12), dp(8), dp(10), dp(8));
        row.setBackground(strokedRect(card, 14, border));

        LinearLayout.LayoutParams rp = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
        );
        rp.setMargins(0, 0, 0, dp(6));
        content.addView(row, rp);

        TextView nameView = label(name, 13, Color.WHITE, true);
        row.addView(nameView, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));

        Switch sw = new Switch(this);
        sw.setChecked(checked);
        row.addView(sw, new LinearLayout.LayoutParams(dp(56), dp(36)));
        row.setOnClickListener(v -> sw.setChecked(!sw.isChecked()));
        return sw;
    }

    private void showMenu() {
        bubble.setVisibility(View.GONE);
        menu.setVisibility(View.VISIBLE);
        menuParams.x = Math.max(dp(8), bubbleParams.x - dp(6));
        menuParams.y = Math.max(dp(55), bubbleParams.y - dp(35));
        wm.updateViewLayout(menu, menuParams);
    }

    private void hideMenu() {
        menu.setVisibility(View.GONE);
        bubble.setVisibility(View.VISIBLE);
    }

    private Button primaryButton(String text) {
        Button b = new Button(this);
        b.setText(text);
        b.setTextSize(12);
        b.setTypeface(Typeface.DEFAULT_BOLD);
        b.setTextColor(Color.BLACK);
        b.setAllCaps(false);
        b.setBackground(roundRect(accent, 14));
        return b;
    }

    private Button actionButton(String text) {
        Button b = new Button(this);
        b.setText(text);
        b.setTextSize(11);
        b.setTypeface(Typeface.DEFAULT_BOLD);
        b.setTextColor(Color.WHITE);
        b.setAllCaps(false);
        b.setBackground(strokedRect(card2, 13, border));
        b.setPadding(dp(6), 0, dp(6), 0);
        return b;
    }

    private Button smallButton(String text) {
        Button b = actionButton(text);
        b.setTextSize(18);
        return b;
    }

    private TextView label(String text, int sp, int color, boolean bold) {
        TextView t = new TextView(this);
        t.setText(text);
        t.setTextSize(sp);
        t.setTextColor(color);
        if (bold) t.setTypeface(Typeface.DEFAULT_BOLD);
        return t;
    }

    private GradientDrawable roundRect(int color, int radiusDp) {
        GradientDrawable g = new GradientDrawable();
        g.setColor(color);
        g.setCornerRadius(dp(radiusDp));
        return g;
    }

    private GradientDrawable strokedRect(int color, int radiusDp, int strokeColor) {
        GradientDrawable g = roundRect(color, radiusDp);
        g.setStroke(dp(1), strokeColor);
        return g;
    }

    private LinearLayout.LayoutParams matchWrap() {
        return new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
        );
    }

    private void gap(LinearLayout parent, int h) {
        Space s = new Space(this);
        parent.addView(s, new LinearLayout.LayoutParams(1, dp(h)));
    }

    private int dp(int v) {
        return Math.round(v * getResources().getDisplayMetrics().density);
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        try { if (bubble != null) wm.removeView(bubble); } catch (Exception ignored) {}
        try { if (menu != null) wm.removeView(menu); } catch (Exception ignored) {}
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
}
