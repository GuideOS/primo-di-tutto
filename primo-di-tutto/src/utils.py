def enable_high_dpi_awareness(self=None, scaling=None):
    """Enable high dpi awareness.

    **Windows OS**  
    Call the method BEFORE creating the `Tk` object. No parameters
    required.

    **Linux OS**  
    Must provided the `self` and `scaling` parameters. Call the method 
    AFTER creating the `Tk` object. A number between 1.6 and 2.0 is 
    usually suffient to scale for high-dpi screen.

    !!! warning
        If the `self` argument is provided, then `scaling` must also
        be provided. Otherwise, there is no effect.

    Parameters:
    
        self (tk.Tk):
            The self widget

        scaling (float):
            Sets and queries the current scaling factor used by Tk to 
            convert between physical units (for example, points, 
            inches, or millimeters) and pixels. The number argument is 
            a floating point number that specifies the number of pixels 
            per point on window's display. If the window argument is 
            omitted, it defaults to the main window. If the number 
            argument is omitted, the current value of the scaling 
            factor is returned.

            A “point” is a unit of measurement equal to 1/72 inch. A 
            scaling factor of 1.0 corresponds to 1 pixel per point, 
            which is equivalent to a standard 72 dpi monitor. A scaling 
            factor of 1.25 would mean 1.25 pixels per point, which is 
            the setting for a 90 dpi monitor; setting the scaling factor 
            to 1.25 on a 72 dpi monitor would cause everything in the 
            application to be displayed 1.25 times as large as normal. 
            The initial value for the scaling factor is set when the 
            application starts, based on properties of the installed 
            monitor, but it can be changed at any time. Measurements 
            made after the scaling factor is changed will use the new 
            scaling factor, but it is undefined whether existing 
            widgets will resize themselves dynamically to accommodate 
            the new scaling factor.
    """
    try:
        from ctypes import windll
        windll.user32.SetProcessDPIAware()
    except:
        pass

    try:
        if self and scaling:
            self.tk.call('tk', 'scaling', scaling)
    except:
        pass

def get_image_name(image):
    """Extract and return the tcl/tk image name from a PhotoImage 
    object.
    
    Parameters:

        image (ImageTk.PhotoImage):
            A photoimage object.

    Returns:

        str:
            The tcl/tk name of the photoimage object.
    """
    return image._PhotoImage__photo.name

def scale_size(widget, size):
    """Scale the size based on the scaling factor of tkinter. 
    This is used most frequently to adjust the assets for 
    image-based widget layouts and font sizes.

    Parameters:

        widget (Widget):
            The widget object.

        size (Union[int, List, Tuple]):
            A single integer or an iterable of integers

    Returns:

        Union[int, List]:
            An integer or list of integers representing the new size.
    """
    BASELINE = 1.33398982438864281
    scaling = widget.tk.call('tk', 'scaling')
    factor = scaling / BASELINE

    if isinstance(size, int):
        return int(size * factor)
    elif isinstance(size, tuple) or isinstance(size, list):
        return [int(x * factor) for x in size]
    
scaling = 4.0