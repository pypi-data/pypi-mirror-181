import matplotlib.pyplot
import matplotlib.backends.backend_tkagg
import os
import re
import tkinter
import tkinter.ttk
import tkinter.scrolledtext

import appdirs
import factoriohelper.planner


class FactorioHelperGUI(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.recipes_source = ""
        self.planner = factoriohelper.planner.ProductionPlanner()

        style = tkinter.ttk.Style()
        style.theme_use("clam")
        style.configure(
            "TFrame", borderwidth=20, relief="groove"
        )

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self._init_notebook()

        self._init_planner()
        self._init_recipes()

        self.var_planner_speed.trace_add("write", lambda *args, **kwargs: self.calculate_production_plan())
        self.var_planner_speed_unit.trace_add("write", lambda *args, **kwargs: self.calculate_production_plan())
        self.var_planner_item.trace_add("write", lambda *args, **kwargs: self.calculate_production_plan())
        self.var_planner_layout.trace_add("write", lambda *args, **kwargs: self.calculate_production_plan())

    @staticmethod
    def _get_storage_file(file_):
        storage_directory = appdirs.user_data_dir("factoriohelper")
        os.makedirs(storage_directory, exist_ok=True)
        return os.path.join(storage_directory, file_)

    def _init_notebook(self):
        self.notebook = tkinter.ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky="news", padx=5, pady=(8, 5))

    def _init_planner(self):
        self.frame_planner = tkinter.ttk.Frame(self.notebook)
        self.frame_planner.columnconfigure(0, weight=1)
        self.frame_planner.grid(row=0, column=0, sticky="news")

        self.notebook.add(self.frame_planner, text="Planner")

        self.frame_planner_entry = tkinter.ttk.Frame(self.frame_planner)
        self.frame_planner_entry.grid(row=0, column=0, sticky="news")

        self.var_planner_speed = tkinter.DoubleVar()
        self.var_planner_speed_unit = tkinter.StringVar()
        self.var_planner_item = tkinter.StringVar()
        self.var_planner_layout = tkinter.StringVar()
        self.var_planner_speed.set(1)

        self.frame_planner_entry.columnconfigure(0, pad=10)
        label_speed = tkinter.ttk.Label(
            self.frame_planner_entry,
            justify="center",
            text="Speed",
        )
        label_speed.grid(row=0, column=0, sticky="news")

        self.frame_planner_entry.columnconfigure(1, pad=10)
        entry_speed = tkinter.ttk.Entry(
            self.frame_planner_entry,
            justify="center",
            textvariable=self.var_planner_speed,
            validate="key",
            validatecommand=(
                self.register(
                    lambda val: re.fullmatch("\s*\d*(?:\.\d*)?\s*", val) is not None
                ),
                "%P",
            ),
            width=5,
        )
        entry_speed.grid(row=0, column=1, sticky="news")

        self.frame_planner_entry.columnconfigure(2, pad=10, weight=0)
        option_menu_speed_unit = tkinter.ttk.OptionMenu(
            self.frame_planner_entry,
            self.var_planner_speed_unit,
            "item/sec",
            *["item/sec", "item/min", "item/hour"],
        )
        option_menu_speed_unit.config(width=9)
        option_menu_speed_unit.grid(row=0, column=2, sticky="news")

        self.frame_planner_entry.columnconfigure(3, pad=10)
        label_item = tkinter.ttk.Label(
            self.frame_planner_entry,
            justify="center",
            text="Item",
        )
        label_item.grid(row=0, column=3, sticky="news")

        self.frame_planner_entry.columnconfigure(4, weight=1)
        entry_item = tkinter.ttk.Entry(
            self.frame_planner_entry, textvariable=self.var_planner_item
        )
        entry_item.grid(row=0, column=4, sticky="news")

        self.frame_planner_entry.columnconfigure(5, pad=10)
        button_plan = tkinter.ttk.Button(self.frame_planner_entry, text="Plan!", command=self.calculate_production_plan)
        button_plan.grid(row=0, column=5, sticky="news")

        option_menu_layout = tkinter.ttk.OptionMenu(
            self.frame_planner_entry,
            self.var_planner_layout,
            "dot",
            *["dot", "neato"],
        )
        option_menu_layout.config(width=9)
        option_menu_layout.grid(row=0, column=6, sticky="news")


        self.frame_planner.rowconfigure(1, weight=1)
        frame_planner_viewer = tkinter.ttk.Frame(self.frame_planner)
        frame_planner_viewer.grid(row=1, column=0, sticky="news")

        frame_planner_viewer.rowconfigure(0, weight=1)
        frame_planner_viewer.columnconfigure(0, weight=1)
        figure_planner_viewer = matplotlib.pyplot.Figure()
        self.ax_planner_viewer = figure_planner_viewer.add_axes([0, 0, 1, 1])
        self.canvas_planner_viewer = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(figure_planner_viewer, master=frame_planner_viewer)
        self.canvas_planner_viewer.get_tk_widget().grid(row=0, column=0, sticky="news")

        self.ax_planner_viewer.set_frame_on(False)
        self.ax_planner_viewer.axis("off")

        frame_planner_viewer_toolbar = tkinter.ttk.Frame(frame_planner_viewer)
        frame_planner_viewer_toolbar.grid(row=1, column=0, sticky="news")

        toolbar = matplotlib.backends.backend_tkagg.NavigationToolbar2Tk(self.canvas_planner_viewer, frame_planner_viewer_toolbar)
        toolbar.update()
        toolbar.pan()

    def _init_recipes(self):
        self.frame_recipes = tkinter.ttk.Frame(self.notebook)
        self.frame_recipes.grid(row=0, column=0, sticky="news")
        self.notebook.add(self.frame_recipes, text="Recipes")

        self.frame_recipes.columnconfigure(0, weight=1)
        self.frame_recipes.rowconfigure(0, weight=1)
        self.scrolled_text_recipes = tkinter.scrolledtext.ScrolledText(self.frame_recipes)
        self.scrolled_text_recipes.grid(row=0, column=0, sticky="news")

        self._load_recipes_from_storage()


    def _load_recipes_from_storage(self):
        try:
            with open(FactorioHelperGUI._get_storage_file("recipes.txt"), "r") as file_:
                self.scrolled_text_recipes.insert("1.0", file_.read())
        except FileNotFoundError:
            pass
        self._parse_recipes()

    def _parse_recipes(self):
        try:
            recipes_source = self.scrolled_text_recipes.get("1.0", "end").strip()
            if self.recipes_source == recipes_source:
                return
            self.recipes_source = recipes_source
            recipes = factoriohelper.planner.RecipesParser.parse(recipes_source)
            self.planner = factoriohelper.planner.ProductionPlanner()
            self.planner.register_recipes(recipes)
            with open(FactorioHelperGUI._get_storage_file("recipes.txt"), "w") as file_:
                file_.write(recipes_source)
        except:
            pass

    def calculate_production_plan(self):
        self._parse_recipes()

        speed_factor = {
            "item/sec": 1,
            "item/min": 1/60,
            "item/hour": 1/60/60,
        }[self.var_planner_speed_unit.get()]
        item_per_s = self.var_planner_speed.get() * speed_factor
        item_name = self.var_planner_item.get()

        item = factoriohelper.planner.Item.parse(item_name)
        item.amount = item_per_s

        graph = self.planner.calculate_graph(item)
        if len(graph.edges) + len(graph.nodes) == 0:
            return

        layout_prog = self.var_planner_layout.get()

        self.ax_planner_viewer.cla()
        graph.plot_onto(self.ax_planner_viewer, layout_prog=layout_prog)
        self.canvas_planner_viewer.draw()


def main():
    FactorioHelperGUI().mainloop()


if __name__ == "__main__":
    main()
