from customtkinter import CTk, CTkCanvas, set_default_color_theme
from tkdevin.dtk import DTk


class CDTk(CTk, DTk):
    pass


if __name__ == '__main__':
    from tkinter import Canvas
    from tkdevin import draw_gradient, make_movable_object, CSelectedCanvas

    root = CDTk()
    if not root.wm_is_mark_id("devin"):
        root.wm_mark_id("devin", {})
    root.wm_mark_size("devin")

    select = CSelectedCanvas()

    canvas = CTkCanvas(select)
    canvas.configure(cursor="hand2")
    draw_gradient(canvas)

    select.place(width=100, height=100)
    select.set_widget(canvas)

    root.mainloop()