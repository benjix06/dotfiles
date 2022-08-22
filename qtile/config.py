"""
    Qtile - 2022 version
    Created by Benjamin Nguyen

"""

import os
import subprocess
from typing import List  # noqa: F401

from libqtile import bar, hook, init, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.dgroups import simple_key_binder
from libqtile.lazy import lazy

# from libqtile.utils import guess_terminal

mod = "mod4"
altkey = "mod1"
control = "control"

terminal = "alacritty"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, control], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, control], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, control], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, control], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key(
        [altkey], "space",
        lazy.spawn("rofi -show drun -font 'Jetbrains Mono 17' -show-icon"),
        desc="Spawn a command using rofi",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle next layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, control], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, control], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "b", lazy.hide_show_bar("top")),

    # Toggle floating for window
    Key([altkey], "t", lazy.window.toggle_floating()),

    # Minimizar
    Key([altkey], "n", lazy.window.toggle_minimize()),

    # Maximize
    Key([mod], "f", lazy.window.toggle_fullscreen()),

    # Switch focus of monitors
    Key([mod], "period",
        lazy.to_screen(1),
        desc='Move focus to next monitor'
        ),
    Key([mod], "comma",
        lazy.to_screen(0),
        desc='Move focus to prev monitor'
        ),


    # PC commands
    Key([mod, altkey], "u", lazy.spawn(
        "shutdown -h now"), desc="Shut down PC"),
    Key([mod, altkey], "i", lazy.spawn("shutdown -r now"), desc="Reboot PC"),
    Key([mod, altkey], "o", lazy.spawn(
        "systemctl suspend"), desc="Suspend PC"),

    # --- Monadtall
    Key([mod, control], "h",
        lazy.layout.shrink(),
        lazy.layout.decrease_nmaster(),
        desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
        ),

    Key([mod, control], "l",
        lazy.layout.grow(),
        lazy.layout.increase_nmaster(),
        desc='Expand window (MonadTall), increase number in master pane (Tile)'
        ),
]

# ----------------------------
# Moving between screens


def window_to_previous_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i - 1)


def window_to_next_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i + 1)


keys.extend([
    # Key([mod, "shift"],  "period",  lazy.function(window_to_next_screen)),
    # Key([mod, "shift"],  "comma", lazy.function(window_to_previous_screen)),
    Key([mod, "control"], "period",  lazy.function(
        window_to_next_screen, switch_screen=True)),
    Key([mod, "control"], "comma", lazy.function(
        window_to_previous_screen, switch_screen=True)),
])


groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}"),

            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True), desc=f"Switch to & move focused window to group {i.name}",
            )
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc=f"move focused window to group {i.name}"),
        ]
    )


layout_theme = {
    "border_focus": "#f2d0ff",
    "border_normal": "#79ad86",
    "border_width": 4,
    "margin": 8
}

layouts = [
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    layout.Columns(**layout_theme),
    layout.Max(),

    # Try more layouts by unleashing below layouts.
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

colors = [["#282c34", "#282c34"],
          ["#1c1f24", "#1c1f24"],
          ["#dfdfdf", "#dfdfdf"],
          ["#ff6c6b", "#ff6c6b"],
          ["#98be65", "#98be65"],
          ["#da8548", "#da8548"],
          ["#51afef", "#51afef"],
          ["#c678dd", "#c678dd"],
          ["#46d9ff", "#46d9ff"],
          ["#a9a1e1", "#a9a1e1"]]


widget_defaults = dict(
    font="Jetbrains Mono",
    fontsize=15,
    padding=3,
    background=colors[0]
)
extension_defaults = widget_defaults.copy()


def init_widget_lst():
    return [
        widget.Image(
            filename="~/.config/qtile/icons/python.png",
            scale="False",
            mouse_callbacks={
                'Button1': lambda: qtile.cmd_spawn(terminal)}
        ),

        widget.GroupBox(
            font="Ubuntu Bold",
            fontsize=15,
            margin_y=3,
            margin_x=0,
            padding_y=5,
            padding_x=3,
            borderwidth=3,
            active=colors[4],
            inactive=colors[7],
            rounded=False,
            highlight_color=colors[1],
            highlight_method="line",
            this_current_screen_border=colors[8],
            this_screen_border=colors[4],
            other_current_screen_border=colors[8],
            other_screen_border=colors[4],
            foreground=colors[2],
        ),
        widget.TextBox(
            text='|',
            font="Ubuntu Mono",
            foreground='#474747',
            padding=2,
            fontsize=15
        ),
        widget.Prompt(
            foreground=colors[5],
            font="JetBrains Mono Bold",
            fontsize=17,
        ),
        widget.CurrentLayoutIcon(
            custom_icon_paths=[os.path.expanduser(
                "~/.config/qtile/icons")],
            foreground=colors[2],
            padding=0,
            scale=0.7
        ),
        widget.CurrentLayout(
            foreground=colors[2],
            padding=5,
            font="Ubuntu Bold",
            fontsize=16,
        ),
        widget.TextBox(
            text='|',
            font="Ubuntu Mono",
            foreground='#474747',
            padding=2,
            fontsize=15
        ),
        widget.WindowName(
            foreground=colors[4],
            font="JetBrains Mono Bold",
            fontsize=17,
            padding=0
        ),
        widget.Systray(
            padding=5
        ),
        widget.TextBox(
            text='|',
            font="Ubuntu Mono",
            foreground='#474747',
            padding=2,
            fontsize=15
        ),
        widget.CheckUpdates(
            update_interval=1800,
            distro="Ubuntu_checkupdates",
            execute="alacritty --hold -e sudo apt update",
            display_format="Update: {updates}",
            foreground=colors[8],
            colour_have_updates=colors[1],
            colour_no_updates=colors[8],
            mouse_callbacks={
                'Button1': lambda: qtile.cmd_spawn('alacritty sudo apt upgrade')},
        ),
        widget.TextBox(
            text='|',
            font="Ubuntu Mono",
            foreground='#474747',
            padding=2,
            fontsize=15
        ),
        widget.Net(
            foreground=colors[4],
            fontsize=16,
        ),
        widget.TextBox(
            text='|',
            font="Ubuntu Mono",
            foreground='#474747',
            padding=2,
            fontsize=15
        ),
        widget.Volume(
            fmt="Volume: {}",
            mute_command="amixer -D pulse set Master toggle",
            foreground=colors[5],
            fontsize=16
        ),
        widget.TextBox(
            text='|',
            font="Ubuntu Mono",
            foreground='#474747',
            padding=2,
            fontsize=15
        ),
        widget.Clock(
            format="%A, %B %d - %H:%M ",
            foreground="#8BE61A",
            font="JetBrains Mono Bold",
            fontsize=16

        ),
        widget.QuickExit(
            foreground=colors[3],
        ),
    ]


def init_widget_lst_screen1():  # Screen 1
    return init_widget_lst()


def init_widget_lst_screen2():  # Screen 2
    widget_list_screen2 = init_widget_lst()
    del widget_list_screen2[8:15]
    return widget_list_screen2
    # return init_widget_lst()[:8] + init_widget_lst()[14:]


screens = [
    Screen(
        wallpaper='/home/benjamin/Pictures/leaf.jpg',
        wallpaper_mode="fill",
        top=bar.Bar(init_widget_lst_screen1(),
                    size=26,
                    ),
    ),
    Screen(
        wallpaper='/home/benjamin/Pictures/leaf.jpg',
        wallpaper_mode="fill",
        top=bar.Bar(init_widget_lst_screen2(),
                    size=24,
                    ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

# Float layouts
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(title="Stacer"),  # Stacer - app to clean up
        Match(title="zoom"),  # Zoom
        Match(title="Lutris"),  # Lutris - Gaming
        Match(title="Peek"),  # Peek - App to record the screen
        Match(title="Monster Hunter Rise"),  # Game
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([home])


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
