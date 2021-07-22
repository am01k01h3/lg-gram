rofi $* \
  -show drun \
  -modi drun,run,window \
  -show-icons \
  -no-disable-history \
  -fake-transparency \
  -display-drun "Apps " \
  -display-run "Cmds " \
  -display-window "Windows " \
  -scroll-method 0 \
  -sidebar-mode \
  -lines 15 \
  -columns 1 \
  -eh 1 \
  -line-margin 100 \
  -width 500 \
  -padding 100 \
  -terminal st
#  -theme themes/arc-red-dark-menu.rasi

#rofi -show drun -modi drun,run,window -show-icons -fake-transparency -display-drun 'Apps ' -display-run 'Cmds ' -display-window 'Windows ' -scroll-method 0 -sidebar-mode -lines 20 -columns 1 -terminal sakura -theme ~/.config/qtile/rofi/themes/arc-red-dark-menu.rasi

#rofi $* \
#  -show combi -combi-modi "drun,run,window" -modi combi \
#  -show-icons \
#  -no-disable-history \
#  -fake-transparency \
#  -scroll-method 1 \
#  -sidebar-mode \
#  -lines 20 \
#  -terminal st \
#  -theme themes/slate-menu.rasi

