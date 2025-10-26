
#!/bin/bash
# Automatische DPI-Erkennung unter X11
XFT_DPI=$(xrdb -query | awk '/Xft.dpi/ {print $2}')
if [ -n "$XFT_DPI" ]; then
	# Standard-DPI von Tkinter ist 72
	SCALE=$(echo "$XFT_DPI/72" | bc -l)
	# GDK_SCALE bleibt meist 1, GDK_DPI_SCALE wird gesetzt
	export GDK_SCALE=1
	export GDK_DPI_SCALE=$SCALE
else
	# Fallback: Standardwerte
	export GDK_SCALE=1
	export GDK_DPI_SCALE=1
fi

LOG_LEVEL=INFO python3 $(pwd)/src/main.py


