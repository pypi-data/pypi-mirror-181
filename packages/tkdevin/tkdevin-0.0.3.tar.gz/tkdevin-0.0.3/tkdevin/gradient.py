from tkinter import Widget


def use_gradient():
    from tkinter import _default_root
    _default_root.eval(
        """
 proc DrawGradient {win axis col1Str col2Str} {
    if {[winfo class $win] != "Canvas"} {
        return -code error "$win must be a canvas widget"
    }

    $win delete gradient

    set width  [winfo width $win]
    set height [winfo height $win]
    switch -- $axis {
        "x" { set max $width; set x 1 }
        "y" { set max $height; set x 0 }
        default {
            return -code error "Invalid axis $axis: must be x or y"
        }
    }

    if {[catch {winfo rgb $win $col1Str} color1]} {
        return -code error "Invalid color $col1Str"
    }

    if {[catch {winfo rgb $win $col2Str} color2]} {
        return -code error "Invalid color $col2Str"
    }

    lassign $color1 r1 g1 b1
    lassign $color2 r2 g2 b2
    set rRange [expr $r2.0 - $r1]
    set gRange [expr $g2.0 - $g1]
    set bRange [expr $b2.0 - $b1]

    set rRatio [expr $rRange / $max]
    set gRatio [expr $gRange / $max]
    set bRatio [expr $bRange / $max]

    for {set i 0} {$i < $max} {incr i} {
        set nR [expr int( $r1 + ($rRatio * $i) )]
        set nG [expr int( $g1 + ($gRatio * $i) )]
        set nB [expr int( $b1 + ($bRatio * $i) )]

        set col [format {%4.4x} $nR]
        append col [format {%4.4x} $nG]
        append col [format {%4.4x} $nB]
        if {$x} {
            $win create line $i 0 $i $height -tags gradient -fill #${col}
        } else {
            $win create line 0 $i $width $i -tags gradient -fill #${col}
        }
    }
    bind $win <Configure> [list DrawGradient $win $axis $col1Str $col2Str]
    return $win
 }
        """
    )

def draw_gradient(widget: Widget, axis="x", color1="blue", color2="red") -> Widget:
    use_gradient()
    from tkinter import _default_root
    return _default_root.eval(f"DrawGradient {widget} {axis} {color1} {color2}")