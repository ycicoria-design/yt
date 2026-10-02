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
import android.widget.HorizontalScrollView;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.SeekBar;
import android.widget.Space;
import android.widget.Switch;
import android.widget.TextView;

public class MainActivity extends Activity {
    private FrameLayout root;
    private ScrollView homeScroll;\n    private LinearLayout homePanel;
    private ScrollView menuScroll;
    private LinearLayout menuPanel;
    private LinearLayout categoryContent;
    private TextView categoryTitle;
    private TextView restoreBubble;
    private boolean handcamMode = false;
    private float downX, downY, startX, startY;

    private final int bg = Color.rgb(8, 10, 14);
    private final int card = Color.rgb(17, 21, 28);
    private final int card2 = Color.rgb(24, 29, 39);
    private final int accent = Color.rgb(68, 245, 187);
    private final int muted = Color.rgb(154, 164, 181);
    private final int border = Color.rgb(40, 47, 59);

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

        buildHome();
        buildMenu();
        buildRestoreBubble();
        showHome();
    }

    private void buildHome() {
        homeScroll = new ScrollView(this);
        homeScroll.setFillViewport(true);
        root.addView(homeScroll, new FrameLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.MATCH_PARENT
        ));

        homePanel = new LinearLayout(this);
        homePanel.setOrientation(LinearLayout.VERTICAL);
        homePanel.setGravity(Gravity.CENTER_HORIZONTAL);
        homePanel.setPadding(dp(22), dp(34), dp(22), dp(32));
        homeScroll.addView(homePanel, new ScrollView.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
        ));

        gap(homePanel, 18);

        ImageView heroLogo = new ImageView(this);
        heroLogo.setImageResource(R.drawable.logo);
        heroLogo.setScaleType(ImageView.ScaleType.CENTER_CROP);
        heroLogo.setBackground(roundRect(card2, 26));
        heroLogo.setClipToOutline(true);
        LinearLayout.LayoutParams logoParams = new LinearLayout.LayoutParams(dp(142), dp(142));
        heroLogo.setElevation(dp(8));
        homePanel.addView(heroLogo, logoParams);

        gap(homePanel, 24);

        TextView title = label("2BAD ESP", 32, Color.WHITE, true);
        title.setGravity(Gravity.CENTER);
        homePanel.addView(title, matchWrap());

        TextView subtitle = label("CONTROL CENTER", 12, muted, true);
        subtitle.setLetterSpacing(0.22f);
        subtitle.setGravity(Gravity.CENTER);
        subtitle.setPadding(0, dp(6), 0, 0);
        homePanel.addView(subtitle, matchWrap());

        gap(homePanel, 28);

        LinearLayout statusCard = new LinearLayout(this);
        statusCard.setOrientation(LinearLayout.HORIZONTAL);
        statusCard.setGravity(Gravity.CENTER_VERTICAL);
        statusCard.setPadding(dp(16), dp(14), dp(16), dp(14));
        statusCard.setBackground(strokedRect(card, 18, border));
        homePanel.addView(statusCard, matchWrap());

        TextView dot = label("●", 18, accent, true);
        statusCard.addView(dot, new LinearLayout.LayoutParams(dp(28), ViewGroup.LayoutParams.WRAP_CONTENT));

        LinearLayout statusText = new LinearLayout(this);
        statusText.setOrientation(LinearLayout.VERTICAL);
        LinearLayout.LayoutParams stp = new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f);
        statusCard.addView(statusText, stp);

        TextView ready = label("READY", 14, Color.WHITE, true);
        statusText.addView(ready, matchWrap());
        TextView readySub = label("Open the menu to configure options", 11, muted, false);
        readySub.setPadding(0, dp(2), 0, 0);
        statusText.addView(readySub, matchWrap());

        gap(homePanel, 18);

        Button openMenu = primaryButton("OPEN MENU");
        LinearLayout.LayoutParams openParams = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, dp(58)
        );
        homePanel.addView(openMenu, openParams);
        openMenu.setOnClickListener(v -> showMenu("ESP"));

        gap(homePanel, 12);

        TextView hint = label("Tap Open Menu to access the sorted categories.", 11, muted, false);
        hint.setGravity(Gravity.CENTER);
        homePanel.addView(hint, matchWrap());
    }

    private void buildMenu() {
        menuScroll = new ScrollView(this);
        menuScroll.setFillViewport(true);
        root.addView(menuScroll, new FrameLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.MATCH_PARENT
        ));

        menuPanel = new LinearLayout(this);
        menuPanel.setOrientation(LinearLayout.VERTICAL);
        menuPanel.setPadding(dp(16), dp(16), dp(16), dp(30));
        menuScroll.addView(menuPanel, new ScrollView.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
        ));

        LinearLayout top = new LinearLayout(this);
        top.setOrientation(LinearLayout.HORIZONTAL);
        top.setGravity(Gravity.CENTER_VERTICAL);
        top.setPadding(dp(12), dp(10), dp(12), dp(10));
        top.setBackground(roundRect(card, 18));
        menuPanel.addView(top, matchWrap());

        Button back = smallButton("‹");
        LinearLayout.LayoutParams bp = new LinearLayout.LayoutParams(dp(46), dp(42));
        top.addView(back, bp);
        back.setOnClickListener(v -> showHome());

        ImageView smallLogo = new ImageView(this);
        smallLogo.setImageResource(R.drawable.logo);
        smallLogo.setScaleType(ImageView.ScaleType.CENTER_CROP);
        smallLogo.setBackground(roundRect(card2, 12));
        smallLogo.setClipToOutline(true);
        LinearLayout.LayoutParams slp = new LinearLayout.LayoutParams(dp(42), dp(42));
        slp.setMargins(dp(10), 0, dp(10), 0);
        top.addView(smallLogo, slp);

        LinearLayout titles = new LinearLayout(this);
        titles.setOrientation(LinearLayout.VERTICAL);
        top.addView(titles, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));

        TextView appName = label("2BAD ESP", 18, Color.WHITE, true);
        titles.addView(appName, matchWrap());
        TextView appSub = label("MENU", 10, muted, true);
        appSub.setLetterSpacing(0.18f);
        titles.addView(appSub, matchWrap());

        TextView ready = label("READY", 10, Color.BLACK, true);
        ready.setGravity(Gravity.CENTER);
        ready.setBackground(roundRect(accent, 99));
        top.addView(ready, new LinearLayout.LayoutParams(dp(58), dp(28)));

        gap(menuPanel, 14);

        HorizontalScrollView categoriesScroll = new HorizontalScrollView(this);
        categoriesScroll.setHorizontalScrollBarEnabled(false);
        menuPanel.addView(categoriesScroll, matchWrap());

        LinearLayout categories = new LinearLayout(this);
        categories.setOrientation(LinearLayout.HORIZONTAL);
        categoriesScroll.addView(categories, new HorizontalScrollView.LayoutParams(
                ViewGroup.LayoutParams.WRAP_CONTENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
        ));

        addCategoryButton(categories, "ESP");
        addCategoryButton(categories, "WORLD");
        addCategoryButton(categories, "DISPLAY");
        addCategoryButton(categories, "UTILITY");

        gap(menuPanel, 14);

        categoryTitle = label("ESP", 13, accent, true);
        categoryTitle.setLetterSpacing(0.14f);
        categoryTitle.setPadding(dp(4), 0, 0, dp(8));
        menuPanel.addView(categoryTitle, matchWrap());

        categoryContent = new LinearLayout(this);
        categoryContent.setOrientation(LinearLayout.VERTICAL);
        menuPanel.addView(categoryContent, matchWrap());

        gap(menuPanel, 16);
        TextView footer = label("2BAD ESP  •  v1.1", 11, muted, false);
        footer.setGravity(Gravity.CENTER);
        menuPanel.addView(footer, matchWrap());
    }

    private void buildRestoreBubble() {
        restoreBubble = label("2B", 15, Color.BLACK, true);
        restoreBubble.setGravity(Gravity.CENTER);
        restoreBubble.setBackground(roundRect(accent, 24));
        restoreBubble.setVisibility(View.GONE);
        restoreBubble.setElevation(dp(10));
        FrameLayout.LayoutParams rp = new FrameLayout.LayoutParams(dp(54), dp(54), Gravity.TOP | Gravity.END);
        rp.setMargins(0, dp(26), dp(18), 0);
        root.addView(restoreBubble, rp);
        enableDrag(restoreBubble);
    }

    private void addCategoryButton(LinearLayout parent, String name) {
        Button b = actionButton(name);
        LinearLayout.LayoutParams p = new LinearLayout.LayoutParams(dp(112), dp(46));
        p.setMargins(0, 0, dp(8), 0);
        parent.addView(b, p);
        b.setOnClickListener(v -> renderCategory(name));
    }

    private void renderCategory(String category) {
        categoryContent.removeAllViews();
        categoryTitle.setText(category);

        if ("ESP".equals(category)) {
            addSwitchRow(categoryContent, "Enable ESP", "Master visual toggle", true);
            addSwitchRow(categoryContent, "Box", "Player box display", true);
            addSwitchRow(categoryContent, "Skeleton", "Skeleton lines", false);
            addSwitchRow(categoryContent, "Health Bar", "Health indicator", true);
            addSwitchRow(categoryContent, "Name", "Player name label", true);
            addSwitchRow(categoryContent, "Distance", "Distance readout", true);
        } else if ("WORLD".equals(category)) {
            addSwitchRow(categoryContent, "Loot", "Item markers", true);
            addSwitchRow(categoryContent, "Vehicles", "Vehicle markers", true);
            addSwitchRow(categoryContent, "Grenade Warning", "Nearby warning", true);
        } else if ("DISPLAY".equals(category)) {
            addSwitchRow(categoryContent, "Streamer Mode", "Cleaner on-screen layout", false);
            addSwitchRow(categoryContent, "Floating Button", "Show quick restore button", true);

            TextView opacityLabel = label("MENU OPACITY", 12, accent, true);
            opacityLabel.setPadding(dp(4), dp(12), 0, dp(6));
            categoryContent.addView(opacityLabel, matchWrap());

            SeekBar opacity = new SeekBar(this);
            opacity.setMax(100);
            opacity.setProgress(100);
            categoryContent.addView(opacity, matchWrap());
            opacity.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
                @Override public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                    float alpha = Math.max(0.45f, progress / 100f);
                    menuPanel.setAlpha(alpha);
                }
                @Override public void onStartTrackingTouch(SeekBar seekBar) {}
                @Override public void onStopTrackingTouch(SeekBar seekBar) {}
            });
        } else if ("UTILITY".equals(category)) {
            Button hide = primaryButton("HIDE SCREEN");
            LinearLayout.LayoutParams p1 = new LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT, dp(54)
            );
            categoryContent.addView(hide, p1);
            hide.setOnClickListener(v -> hideMenu());

            gap(categoryContent, 10);

            Button handcam = actionButton(handcamMode ? "EXIT HANDCAM MODE" : "HANDCAM MODE");
            LinearLayout.LayoutParams p2 = new LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT, dp(54)
            );
            categoryContent.addView(handcam, p2);
            handcam.setOnClickListener(v -> {
                handcamMode = !handcamMode;
                renderCategory("UTILITY");
            });

            gap(categoryContent, 10);

            LinearLayout info = new LinearLayout(this);
            info.setOrientation(LinearLayout.VERTICAL);
            info.setPadding(dp(14), dp(14), dp(14), dp(14));
            info.setBackground(strokedRect(card, 16, border));
            categoryContent.addView(info, matchWrap());

            TextView mode = label(handcamMode ? "HANDCAM MODE ACTIVE" : "STANDARD MODE", 13,
                    handcamMode ? accent : Color.WHITE, true);
            info.addView(mode, matchWrap());
            TextView detail = label(
                    handcamMode ? "Menu is set to the cleaner handcam layout." :
                            "Use Handcam Mode for a cleaner recording layout.",
                    11, muted, false
            );
            detail.setPadding(0, dp(4), 0, 0);
            info.addView(detail, matchWrap());
        }
    }

    private void showHome() {
        homeScroll.setVisibility(View.VISIBLE);
        menuScroll.setVisibility(View.GONE);
        restoreBubble.setVisibility(View.GONE);
    }

    private void showMenu(String category) {
        homeScroll.setVisibility(View.GONE);
        menuScroll.setVisibility(View.VISIBLE);
        menuPanel.setAlpha(1f);
        renderCategory(category);
    }

    private void hideMenu() {
        menuScroll.setVisibility(View.GONE);
        restoreBubble.setVisibility(View.VISIBLE);
    }

    private void restoreMenu() {
        restoreBubble.setVisibility(View.GONE);
        menuScroll.setVisibility(View.VISIBLE);
    }

    private Switch addSwitchRow(LinearLayout parent, String name, String desc, boolean checked) {
        LinearLayout row = new LinearLayout(this);
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.setGravity(Gravity.CENTER_VERTICAL);
        row.setPadding(dp(14), dp(12), dp(12), dp(12));
        row.setBackground(strokedRect(card, 16, border));
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

    private Button primaryButton(String text) {
        Button b = new Button(this);
        b.setText(text);
        b.setTextSize(13);
        b.setTextColor(Color.BLACK);
        b.setTypeface(Typeface.DEFAULT_BOLD);
        b.setAllCaps(false);
        b.setBackground(roundRect(accent, 16));
        b.setPadding(dp(8), 0, dp(8), 0);
        return b;
    }

    private Button actionButton(String text) {
        Button b = new Button(this);
        b.setText(text);
        b.setTextSize(12);
        b.setTextColor(Color.WHITE);
        b.setTypeface(Typeface.DEFAULT_BOLD);
        b.setAllCaps(false);
        b.setBackground(strokedRect(card2, 14, border));
        b.setPadding(dp(8), 0, dp(8), 0);
        return b;
    }

    private Button smallButton(String text) {
        Button b = actionButton(text);
        b.setTextSize(22);
        b.setPadding(0, 0, 0, dp(2));
        return b;
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
                    if (Math.abs(event.getRawX() - downX) < dp(8) &&
                            Math.abs(event.getRawY() - downY) < dp(8)) {
                        restoreMenu();
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

    private void gap(LinearLayout parent, int amountDp) {
        Space s = new Space(this);
        parent.addView(s, new LinearLayout.LayoutParams(1, dp(amountDp)));
    }

    private int dp(int v) {
        return Math.round(v * getResources().getDisplayMetrics().density);
    }
}
