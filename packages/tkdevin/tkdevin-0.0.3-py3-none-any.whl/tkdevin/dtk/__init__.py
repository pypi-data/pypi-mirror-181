from tkinter import Widget, Tk


class DWidget(Widget):
    def wm_clear_mark(self):
        from tkdevin.mark import clear_mark_data
        clear_mark_data()

    clear_mark = wm_clear_mark

    def wm_mark_id(self, id=None, data=None):
        from tkdevin.mark import get_mark_data_key, is_mark_data_key
        if data is not None:
            from tkdevin.mark import mark_data_key
            mark_data_key(id, data)
        if self.wm_is_mark_id(id):
            return get_mark_data_key(id)

    mark_id = wm_mark_id

    def wm_is_mark_id(self, id) -> bool:
        from tkdevin.mark import is_mark_data_key
        return is_mark_data_key(id)

    is_mark_id = wm_is_mark_id

    def wm_tooltip(self, text=None):
        if not text is None:
            from tkdevin import set_tooltip
            set_tooltip(self, text)

    tooltip = wm_tooltip

class DTk(Tk, DWidget):

    def wm_destroy_with_mark_size(self, id) -> None:
        def record(_event):
            data = self.wm_mark_id(id)

            data["size"] = {
                "x": self.winfo_x(),
                "y": self.winfo_y(),
                "width": self.winfo_width(),
                "height": self.winfo_height()
            }
            data["attr"] = {
                "state": self.wm_state()
            }

            self.wm_mark_id(id, data)
        self.bind("<Destroy>", record, add="+")

    destroy_with_mark_size = wm_destroy_with_mark_size

    def wm_mark_size(self, id, default_size=False) -> None:
        self.wm_destroy_with_mark_size(id)
        geo = self.wm_mark_id(id)
        if "size" in geo:
            geo_size = [
                geo["size"]["width"],
                geo["size"]["height"],
                geo["size"]["x"],
                geo["size"]["y"]]
            if not default_size:
                self.wm_geometry(f"{geo_size[0]}x{geo_size[1]}+{geo_size[2]}+{geo_size[3]}")
            else:
                self.wm_geometry(f"{geo_size[0]}x{geo_size[1]}")
        if "attr" in geo:
            geo_attr = [
                geo["attr"]["state"],
            ]
            if not geo_attr[0] == "normal":
                self.wm_state(geo_attr[0])

    mark_size = wm_mark_size


if __name__ == '__main__':
    from tkinter import Canvas
    from tkdevin import draw_gradient, make_movable_object, SelectedCanvas

    root = DTk()
    if not root.wm_is_mark_id("devin"):
        root.wm_mark_id("devin", {})
    root.wm_mark_size("devin", default_size=True)

    select = SelectedCanvas()

    canvas = Canvas(select)
    canvas.configure(cursor="hand2")
    draw_gradient(canvas)

    select.pack()
    select.set_widget(canvas)

    root.mainloop()