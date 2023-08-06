def use_move():
    from tkinter import _default_root
    _default_root.eval(
        """
#! bin/env tclsh

package require Tk
# ------------------------------------------------------------------------------
bind . <Configure> {set components(geo) [split [split [wm geometry .] x] +]}

# ------------------------------------------------------------------------------
bind . <Motion> {
    if {$components(moveObject) != ""} {
        place $components(moveObject) \
            -x [expr {[winfo pointerx .] - [lindex $components(geo) 1] - 3  - $objectXoff}] \
            -y [expr {[winfo pointery .] - [lindex $components(geo) 2] - 29 - $objectYoff}]
    }
}

# ------------------------------------------------------------------------------
proc makeMovableObject {w} {
    bind $w <ButtonPress-1> {+
        set objectXoff %x
        set objectYoff %y
        set components(moveObject) %W 
        event generate %W <Motion>
    }
    bind $w <ButtonRelease-1> {+
        set components(moveObject) ""
    }
}

set components(moveObject) ""
event generate . <Configure>
        """
    )

def make_movable_object(widget):
    use_move()
    from tkinter import _default_root
    _default_root.eval(f"makeMovableObject {widget}")
