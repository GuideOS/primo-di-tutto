// Import APIs provided by Cinnamon defined in /usr/share/cinnamon/js/
const Applet = imports.ui.applet;       // /usr/share/cinnamon/js/ui/applet.js
const Settings = imports.ui.settings;   // /usr/share/cinnamon/js/ui/settings.js
const PopupMenu = imports.ui.popupMenu; // /usr/share/cinnamon/js/ui/popupMenu.js

const Lang = imports.lang;

// The UUID (Universally Unique IDentifier) of your applet.
// Change this constant to something like the-name-of-your-applet@your-name-or-domain-name
// It must match the uuid on the metadata.json file and the name of the folder of your applet.
const APPLET_UUID = "guideos-menu@guideos";

// The directory of the applet. In this case is ~/.local/share/cinnamon/applets/guideos-menu@guideos
const APPLET_DIR = imports.ui.appletManager.appletMeta[APPLET_UUID].path;

const GLib = imports.gi.GLib;
const Gettext = imports.gettext;

Gettext.bindtextdomain(APPLET_UUID, GLib.get_home_dir() + "/.local/share/locale");

// Used to translate strings into different languages
function _(str){
    return Gettext.dgettext(APPLET_UUID, str);
}

// The constructor of our applet.
function GuideosMenuApplet(metadata, orientation, panel_height, instance_id) {
    this._init(metadata, orientation, panel_height, instance_id);
}

GuideosMenuApplet.prototype = {

    // Inherit from Applet.IconApplet's prototype, which is an applet that displays an icon.
    // There are more options like Applet, TextApplet, and TextIconApplet.
    __proto__: Applet.IconApplet.prototype,

    _init: function(metadata, orientation, panel_height, instance_id) {
        Applet.IconApplet.prototype._init.call(this, orientation, panel_height, instance_id);

        // Set the path to our custom icon.
        this.set_applet_icon_path(APPLET_DIR + "/icon.png");

        // Or use an icon available at /usr/share/icons/, for example,
        // this.set_applet_icon_name("folder");

        // By wrapping the string with the _( ) function,
        // we are telling Cinnamon to translate the string to the correct language,
        // if translations are available.
        this.set_applet_tooltip("Starte ein Programm");

    },

    on_applet_clicked: function() {
        // Execute the command com.github.libredeb.lightpad
        GLib.spawn_command_line_async('com.github.libredeb.lightpad');
    }

};

// To load an applet, Cinnamon calls the main function in the applet's code, and
// expects to get an Applet object, which it will add to the panel.
// Parameters:
//    * metadata      the information inside metadata.json plus some more.
//    * orientation   is whether the panel is at the top or the bottom.
//                    The applet can behave differently depending on its position,
//                    eg. to make the popup menus show up on the right side.
//    * panel_height  tells you, unsurprisingly, the height of the panel.
//                    This way we can scale the icons up and down depending on how large the panel is.
//    * instance_id   tells you which instance of the applet you are, since there can be multiple instances of the applet present.
//                    While this is just a number assigned to the applet and doesn't have much meaning by itself,
//                    it is required to access, say, the individual settings of an applet.
function main(metadata, orientation, panel_height, instance_id) {

    // Instantiate and return our applet object.
    return new GuideosMenuApplet(metadata, orientation, panel_height, instance_id);
}
