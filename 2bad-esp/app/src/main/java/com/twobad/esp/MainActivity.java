package com.twobad.esp;

import android.app.Activity;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.os.Bundle;
import android.view.Gravity;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.FrameLayout;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.SeekBar;
import android.widget.Space;
import android.widget.Switch;
import android.widget.TextView;

public class MainActivity extends Activity {
    private FrameLayout root;
    private LinearLayout mainPanel;
    private LinearLayout featureBlock;
    private ImageView logo;
    private TextView subtitle;
    private TextView status;
    private TextView restoreBubble;
    private Button handcamButton;
    private boolean handcamMode = false;
    private float downX, downY, startX, startY;

    private final int bg = Color.rgb(8, 10, 14);
    private final int card = Color.rgb(17, 21, 28);
    private final int card2 = Color.rgb(24, 29, 39);
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

    private void buildUi() {
        root = new FrameLayout(this);
        root.setBackgroundColor(bg);
        setContentView(root);

        ScrollView scroll = new ScrollView(this);
        scroll.setFillViewport(true);
        FrameLayout.LayoutParams sp = new FrameLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.MATCH_PARENT
        );
        root.addView(scroll, sp);

        mainPanel = new LinearLayout(this);
        mainPanel.setOrientation(LinearLayout.VERTICAL);
        mainPanel.setPadding(dp(18), dp(18), dp(18), dp(28));
        scroll.addView(mainPanel, new ScrollView.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
        ));

        buildHeader();
        gap(mainPanel, 14);
        buildTopActions();
        gap(mainPanel, 14);

        featureBlock = new LinearLayout(this);
        featureBlock.setOrientation(LinearLayout.VERTICAL);
        mainPanel.addView(featureBlock, matchWrap());

        addSection(featureBlock, "PLAYER ESP");
        addSwitchRow(featureBlock, "Enable ESP", "Master visual toggle", true);
        addSwitchRow(featureBlock, "Box", "Player box display", true);
        addSwitchRow(featureBlock, "Skeleton", "Skeleton lines", false);
        addSwitchRow(featureBlock, "Health Bar", "Health indicator", true);
        addSwitchRow(featureBlock, "Name", "Player name label", true);
        addSwitchRow(featureBlock, "Distance", "Distance readout", true);

        gap(featureBlock, 12);
        addSection(featureBlock, "WORLD");
        addSwitchRow(featureBlock, "Loot", "Item markers", true);
        addSwitchRow(featureBlock, "Vehicles", "Vehicle markers", true);
        addSwitchRow(featureBlock, "Grenade Warning", "Nearby warning", true);

        gap(featureBlock, 12);
        addSection(featureBlock, "MISC");
        addSwitchRow(featureBlock, "Streamer Mode", "Cleaner on-screen layout", false);
        addSwitchRow(featureBlock, "Floating Button", "Show quick restore button", true);

        TextView opacityLabel = label("MENU OPACITY", 12, accent, true);
        opacityLabel.setPadding(0, dp(18), 0, dp(6));
        featureBlock.addView(opacityLabel);
        SeekBar opacity = new SeekBar(this);
        opacity.setMax(100);
        opacity.setProgress(92);
        featureBlock.addView(opacity, matchWrap());
        opacity.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                float alpha = Math.max(0.35f, progress / 100f);
                mainPanel.setAlpha(alpha);
            }
            @Override public void onStartTrackingTouch(SeekBar seekBar) {}
            @Override public void onStopTrackingTouch(SeekBar seekBar) {}
        });

        gap(mainPanel, 18);
        TextView footer = label("2BAD ESP  •  v1.0", 11, muted, false);
        footer.setGravity(Gravity.CENTER);
        mainPanel.addView(footer, matchWrap());

        restoreBubble = label("2B", 15, Color.WHITE, true);
        restoreBubble.setGravity(Gravity.CENTER);
        restoreBubble.setBackground(roundRect(accent, 24));
        restoreBubble.setVisibility(View.GONE);
        restoreBubble.setElevation(dp(10));
        FrameLayout.LayoutParams rp = new FrameLayout.LayoutParams(dp(54), dp(54), Gravity.TOP | Gravity.END);
        rp.setMargins(0, dp(26), dp(18), 0);
        root.addView(restoreBubble, rp);
        enableDrag(restoreBubble);
    }

    private void buildHeader() {
        LinearLayout header = new LinearLayout(this);
        header.setOrientation(LinearLayout.HORIZONTAL);
        header.setGravity(Gravity.CENTER_VERTICAL);
        header.setPadding(dp(14), dp(14), dp(14), dp(14));
        header.setBackground(roundRect(card, 20));
        mainPanel.addView(header, matchWrap());

        logo = new ImageView(this);
        logo.setImageResource(R.drawable.logo);
        logo.setScaleType(ImageView.ScaleType.CENTER_CROP);
        GradientDrawable logoBg = roundRect(card2, 18);
        logo.setBackground(logoBg);
        logo.setClipToOutline(true);
        LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(dp(74), dp(74));
        header.addView(logo, lp);

        LinearLayout titles = new LinearLayout(this);
        titles.setOrientation(LinearLayout.VERTICAL);
        titles.setPadding(dp(14), 0, 0, 0);
        LinearLayout.LayoutParams tp = new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f);
        header.addView(titles, tp);

        TextView title = label("2BAD ESP", 24, Color.WHITE, true);
        titles.addView(title, matchWrap());
        subtitle = label("CONTROL PANEL", 11, muted, true);
        subtitle.setLetterSpacing(0.18f);
        subtitle.setPadding(0, dp(4), 0, 0);
        titles.addView(subtitle, matchWrap());

        status = label("READY", 11, Color.BLACK, true);
        status.setGravity(Gravity.CENTER);
        status.setBackground(roundRect(accent, 99));
        LinearLayout.LayoutParams st = new LinearLayout.LayoutParams(dp(64), dp(30));
        header.addView(status, st);
    }

    private void buildTopActions() {
        LinearLayout actions = new LinearLayout(this);
        actions.setOrientation(LinearLayout.HORIZONTAL);
        mainPanel.addView(actions, matchWrap());

        Button hide = actionButton("HIDE SCREEN");
        LinearLayout.LayoutParams a = new LinearLayout.LayoutParams(0, dp(52), 1f);
        a.setMargins(0, 0, dp(6), 0);
        actions.addView(hide, a);
        hide.setOnClickListener(v -> hidePanel());

        handcamButton = actionButton("HANDCAM MODE");
        LinearLayout.LayoutParams b = new LinearLayout.LayoutParams(0, dp(52), 1f);
        b.setMargins(dp(6), 0, 0, 0);
        actions.addView(handcamButton, b);
        handcamButton.setOnClickListener(v -> toggleHandcam());
    }

    private void addSection(LinearLayout parent, String text) {
        TextView section = label(text, 12, accent, true);
        section.setLetterSpacing(0.12f);
        section.setPadding(dp(4), dp(6), 0, dp(8));
        parent.addView(section, matchWrap());
    }

    private Switch addSwitchRow(LinearLayout parent, String name, String desc, boolean checked) {
        LinearLayout row = new LinearLayout(this);
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.setGravity(Gravity.CENTER_VERTICAL);
        row.setPadding(dp(14), dp(12), dp(12), dp(12));
        row.setBackground(roundRect(card, 16));
        LinearLayout.LayoutParams rowParams = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
        );
        rowParams.setMargins(0, 0, 0, dp(8));
        parent.addView(row, rowParams);

        LinearLayout copy = new LinearLayout(this);
        copy.setOrientation(LinearLayout.VERTICAL);
        LinearLayout.LayoutParams cp = new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f);
        row.addView(copy, cp);

        TextView t = label(name, 15, Color.WHITE, true);
        copy.addView(t, matchWrap());
        TextView d = label(desc, 11, muted, false);
        d.setPadding(0, dp(3), 0, 0);
        copy.addView(d, matchWrap());

        Switch sw = new Switch(this);
        sw.setChecked(checked);
        sw.setShowText(false);
        row.addView(sw, new LinearLayout.LayoutParams(dp(58), dp(40)));
        row.setOnClickListener(v -> sw.setChecked(!sw.isChecked()));
        return sw;
    }

    private Button actionButton(String text) {
        Button b = new Button(this);
        b.setText(text);
        b.setTextSize(12);
        b.setTextColor(Color.WHITE);
        b.setTypeface(Typeface.DEFAULT_BOLD);
        b.setAllCaps(false);
        b.setBackground(roundRect(card2, 16));
        b.setPadding(dp(8), 0, dp(8), 0);
        return b;
    }

    private void hidePanel() {
        mainPanel.setVisibility(View.GONE);
        restoreBubble.setVisibility(View.VISIBLE);
    }

    private void restorePanel() {
        restoreBubble.setVisibility(View.GONE);
        mainPanel.setVisibility(View.VISIBLE);
    }

    private void toggleHandcam() {
        handcamMode = !handcamMode;
        if (handcamMode) {
            logo.setVisibility(View.GONE);
            subtitle.setText("HANDCAM");
            status.setText("HC");
            handcamButton.setText("EXIT HANDCAM");
            featureBlock.setAlpha(0.76f);
        } else {
            logo.setVisibility(View.VISIBLE);
            subtitle.setText("CONTROL PANEL");
            status.setText("READY");
            handcamButton.setText("HANDCAM MODE");
            featureBlock.setAlpha(1f);
        }
    }

    private void enableDrag(View v) {
        v.setOnTouchListener((view, event) -> {
            switch (event.getActionMasked()) {
                case MotionEvent.ACTION_DOWN:
                    downX = event.getRawX();
                    downY = event.getRawY();
                    startX = view.getX();
                    startY = view.getY();
                    return true;
                case MotionEvent.ACTION_MOVE:
                    float nx = startX + (event.getRawX() - downX);
                    float ny = startY + (event.getRawY() - downY);
                    nx = Math.max(0, Math.min(root.getWidth() - view.getWidth(), nx));
                    ny = Math.max(0, Math.min(root.getHeight() - view.getHeight(), ny));
                    view.setX(nx);
                    view.setY(ny);
                    return true;
                case MotionEvent.ACTION_UP:
                    if (Math.abs(event.getRawX() - downX) < dp(8) && Math.abs(event.getRawY() - downY) < dp(8)) {
                        restorePanel();
                    }
                    return true;
            }
            return false;
        });
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

    private LinearLayout.LayoutParams matchWrap() {
        return new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
        );
    }

    private void gap(LinearLayout parent, int amountDp) {
        Space s = new Space(this);
        parent.addView(s, new LinearLayout.LayoutParams(1, dp(amountDp)));
    }

    private int dp(int v) {
        return Math.round(v * getResources().getDisplayMetrics().density);
    }
}
