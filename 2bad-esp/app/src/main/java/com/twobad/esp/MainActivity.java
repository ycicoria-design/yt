package com.twobad.esp;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.Settings;
import android.view.Gravity;
import android.view.ViewGroup;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.Space;
import android.widget.TextView;

public class MainActivity extends Activity {
    private LinearLayout root;
    private TextView status;
    private Button mainButton;

    private final int bg = Color.rgb(8, 10, 14);
    private final int card = Color.rgb(17, 21, 28);
    private final int accent = Color.rgb(68, 245, 187);
    private final int muted = Color.rgb(154, 164, 181);

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Window w = getWindow();
        w.setStatusBarColor(bg);
        w.setNavigationBarColor(bg);
        w.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);
        buildUi();
    }

    @Override
    protected void onResume() {
        super.onResume();
        updateState();
    }

    private void buildUi() {
        root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setGravity(Gravity.CENTER_HORIZONTAL);
        root.setPadding(dp(26), dp(42), dp(26), dp(32));
        root.setBackgroundColor(bg);
        setContentView(root);

        Space top = new Space(this);
        root.addView(top, new LinearLayout.LayoutParams(1, dp(30)));

        ImageView logo = new ImageView(this);
        logo.setImageResource(R.drawable.logo);
        logo.setScaleType(ImageView.ScaleType.CENTER_CROP);
        logo.setBackground(roundRect(card, 28));
        logo.setClipToOutline(true);
        logo.setElevation(dp(8));
        root.addView(logo, new LinearLayout.LayoutParams(dp(150), dp(150)));

        addGap(22);

        TextView title = text("2BAD ESP", 30, Color.WHITE, true);
        title.setGravity(Gravity.CENTER);
        root.addView(title, matchWrap());

        TextView sub = text("FLOATING OVERLAY", 12, muted, true);
        sub.setLetterSpacing(0.20f);
        sub.setGravity(Gravity.CENTER);
        sub.setPadding(0, dp(6), 0, 0);
        root.addView(sub, matchWrap());

        addGap(28);

        status = text("", 13, Color.WHITE, true);
        status.setGravity(Gravity.CENTER);
        status.setPadding(dp(14), dp(14), dp(14), dp(14));
        status.setBackground(roundRect(card, 16));
        root.addView(status, matchWrap());

        addGap(16);

        mainButton = new Button(this);
        mainButton.setTextSize(13);
        mainButton.setTypeface(Typeface.DEFAULT_BOLD);
        mainButton.setAllCaps(false);
        mainButton.setTextColor(Color.BLACK);
        mainButton.setBackground(roundRect(accent, 16));
        root.addView(mainButton, new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, dp(58)
        ));
        mainButton.setOnClickListener(v -> handleMainAction());

        addGap(12);

        TextView help = text("After enabling it once, the 2B bubble can stay over other apps. Tap the bubble to open the categorized menu.", 11, muted, false);
        help.setGravity(Gravity.CENTER);
        root.addView(help, matchWrap());
    }

    private void handleMainAction() {
        if (!Settings.canDrawOverlays(this)) {
            Intent intent = new Intent(
                    Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                    Uri.parse("package:" + getPackageName())
            );
            startActivity(intent);
            return;
        }

        Intent service = new Intent(this, OverlayService.class);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            startForegroundService(service);
        } else {
            startService(service);
        }
        moveTaskToBack(true);
    }

    private void updateState() {
        if (Settings.canDrawOverlays(this)) {
            status.setText("OVERLAY ACCESS READY");
            status.setTextColor(accent);
            mainButton.setText("START OVERLAY");
        } else {
            status.setText("OVERLAY ACCESS REQUIRED");
            status.setTextColor(Color.WHITE);
            mainButton.setText("ENABLE OVERLAY");
        }
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

    private void addGap(int amountDp) {
        Space s = new Space(this);
        root.addView(s, new LinearLayout.LayoutParams(1, dp(amountDp)));
    }

    private int dp(int v) {
        return Math.round(v * getResources().getDisplayMetrics().density);
    }
}
