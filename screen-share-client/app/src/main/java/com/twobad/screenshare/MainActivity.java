package com.twobad.screenshare;

import android.Manifest;
import android.app.Activity;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.media.projection.MediaProjectionManager;
import android.os.Build;
import android.os.Bundle;
import android.view.Gravity;
import android.view.ViewGroup;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.Space;
import android.widget.TextView;

public class MainActivity extends Activity {
    private static final int CAPTURE_REQUEST = 4101;
    private static final int NOTIFICATION_REQUEST = 4102;

    private MediaProjectionManager projectionManager;
    private EditText nameInput;
    private TextView status;

    private final int bg = Color.rgb(10, 13, 18);
    private final int card = Color.rgb(19, 25, 34);
    private final int accent = Color.rgb(68, 245, 187);
    private final int muted = Color.rgb(157, 167, 183);

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Window w = getWindow();
        w.setStatusBarColor(bg);
        w.setNavigationBarColor(bg);
        w.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);

        projectionManager = (MediaProjectionManager) getSystemService(MEDIA_PROJECTION_SERVICE);
        buildUi();

        if (Build.VERSION.SDK_INT >= 33 &&
                checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS) != getPackageManager().PERMISSION_GRANTED) {
            requestPermissions(new String[]{Manifest.permission.POST_NOTIFICATIONS}, NOTIFICATION_REQUEST);
        }
    }

    private void buildUi() {
        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(dp(24), dp(40), dp(24), dp(28));
        root.setBackgroundColor(bg);
        setContentView(root);

        TextView title = text("Screen Share", 30, Color.WHITE, true);
        root.addView(title, matchWrap());

        TextView sub = text("You control when your screen is shared.", 14, muted, false);
        sub.setPadding(0, dp(6), 0, 0);
        root.addView(sub, matchWrap());

        gap(root, 24);

        LinearLayout notice = new LinearLayout(this);
        notice.setOrientation(LinearLayout.VERTICAL);
        notice.setPadding(dp(16), dp(16), dp(16), dp(16));
        notice.setBackground(roundRect(card, 18));
        root.addView(notice, matchWrap());

        TextView privacy = text("Before sharing", 16, Color.WHITE, true);
        notice.addView(privacy, matchWrap());

        TextView details = text(
                "Android will show its official screen-capture permission prompt. Sharing starts only after you approve it. A persistent notification stays visible while sharing is active, and you can stop at any time.",
                13, muted, false
        );
        details.setPadding(0, dp(8), 0, 0);
        notice.addView(details, matchWrap());

        gap(root, 18);

        TextView nameLabel = text("Display name", 13, muted, true);
        root.addView(nameLabel, matchWrap());

        nameInput = new EditText(this);
        nameInput.setHint("Example: Alex's phone");
        nameInput.setHintTextColor(Color.rgb(100, 110, 126));
        nameInput.setTextColor(Color.WHITE);
        nameInput.setSingleLine(true);
        nameInput.setPadding(dp(14), 0, dp(14), 0);
        nameInput.setBackground(roundRect(card, 14));
        root.addView(nameInput, new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, dp(54)
        ));

        gap(root, 18);

        Button share = button("SHARE SCREEN", accent, Color.BLACK);
        root.addView(share, new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, dp(58)
        ));
        share.setOnClickListener(v -> requestScreenShare());

        gap(root, 10);

        Button stop = button("STOP SHARING", Color.rgb(142, 42, 52), Color.WHITE);
        root.addView(stop, new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, dp(54)
        ));
        stop.setOnClickListener(v -> {
            stopService(new Intent(this, ScreenShareService.class));
            status.setText("Sharing stopped");
            status.setTextColor(Color.WHITE);
        });

        gap(root, 18);

        status = text("Not sharing", 13, muted, true);
        status.setGravity(Gravity.CENTER);
        status.setPadding(dp(12), dp(12), dp(12), dp(12));
        status.setBackground(roundRect(card, 14));
        root.addView(status, matchWrap());

        gap(root, 12);

        TextView scope = text(
                "Screen only. This app does not share your camera or microphone and does not allow remote control.",
                11, muted, false
        );
        scope.setGravity(Gravity.CENTER);
        root.addView(scope, matchWrap());
    }

    private void requestScreenShare() {
        Intent capture = projectionManager.createScreenCaptureIntent();
        startActivityForResult(capture, CAPTURE_REQUEST);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode != CAPTURE_REQUEST) return;

        if (resultCode == RESULT_OK && data != null) {
            String displayName = nameInput.getText().toString().trim();
            if (displayName.isEmpty()) displayName = "Android user";

            Intent service = new Intent(this, ScreenShareService.class);
            service.setAction(ScreenShareService.ACTION_START);
            service.putExtra(ScreenShareService.EXTRA_RESULT_CODE, resultCode);
            service.putExtra(ScreenShareService.EXTRA_RESULT_DATA, data);
            service.putExtra(ScreenShareService.EXTRA_DISPLAY_NAME, displayName);

            if (Build.VERSION.SDK_INT >= 26) startForegroundService(service);
            else startService(service);

            status.setText("Sharing is active");
            status.setTextColor(accent);
        } else {
            status.setText("Screen sharing was not started");
            status.setTextColor(Color.WHITE);
        }
    }

    private Button button(String value, int bgColor, int textColor) {
        Button b = new Button(this);
        b.setText(value);
        b.setTextSize(13);
        b.setTypeface(Typeface.DEFAULT_BOLD);
        b.setTextColor(textColor);
        b.setAllCaps(false);
        b.setBackground(roundRect(bgColor, 16));
        return b;
    }

    private TextView text(String value, int sp, int color, boolean bold) {
        TextView t = new TextView(this);
        t.setText(value);
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
}
