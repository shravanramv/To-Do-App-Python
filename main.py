import flet as ft

class Task(ft.UserControl):
    def __init__(self, task_name, task_delete, update_task_list):
        super().__init__()
        self.task_name = task_name
        self.task_delete = task_delete
        self.update_task_list = update_task_list
        self.completed = False

        self.display_task = ft.Checkbox(
            value=self.completed, 
            label=self.task_name, 
            on_change=self.toggle_completed
        )
        self.edit_name = ft.TextField(expand=1)

        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_task,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.CREATE_OUTLINED,
                            tooltip="Edit To-Do",
                            on_click=self.edit_clicked,
                        ),
                        ft.IconButton(
                            ft.icons.DELETE_OUTLINE,
                            tooltip="Delete To-Do",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name,
                ft.IconButton(
                    icon=ft.icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.colors.GREEN,
                    tooltip="Update To-Do",
                    on_click=self.save_clicked,
                ),
            ],
        )

        self.controls = [self.display_view, self.edit_view]

    def toggle_completed(self, e):
        self.completed = self.display_task.value
        self.update_task_list()
        self.update()

    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    def delete_clicked(self, e):
        self.task_delete(self)


class TodoApp(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.new_task = ft.TextField(
            hint_text="What needs to be done?", 
            expand=True, 
            border_color="blue",
            border_radius=10,
            color="black",
            bgcolor="#e0f7fa",  # Light cyan background
            on_submit=self.add_clicked  # Handle the "Enter" key press
        )
        self.warning_text = ft.Text(
            value="", 
            color="red", 
            size=14, 
            weight=ft.FontWeight.BOLD
        )
        self.tasks = ft.Column(spacing=10)
        self.items_left = ft.Text("0 items left")

        self.filter = ft.Tabs(
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[ft.Tab(text="all"), ft.Tab(text="active"), ft.Tab(text="completed")],
        )

        self.controls = [
            ft.Row(
                [ft.Text(value="Todos", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM)],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=[
                    self.new_task,
                    ft.FloatingActionButton(
                        icon=ft.icons.ADD, 
                        on_click=self.add_clicked,
                        bgcolor="#00bcd4",
                    ),
                ],
                spacing=10,
            ),
            self.warning_text,
            self.filter,
            self.tasks,
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.items_left,
                    ft.OutlinedButton(
                        text="Clear completed", 
                        on_click=self.clear_clicked
                    ),
                ],
            ),
        ]

    def add_clicked(self, e):
        if not self.new_task.value.strip():
            self.warning_text.value = "Please enter a task before adding."
        else:
            task = Task(self.new_task.value, self.task_delete, self.update_task_list)
            self.tasks.controls.append(task)
            self.new_task.value = ""
            self.warning_text.value = ""  # Clear the warning message
            self.new_task.focus()  # Set focus back to the TextField
            self.update_task_list()
        self.update()

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update_task_list()
        self.update()

    def clear_clicked(self, e):
        for task in self.tasks.controls[:]:
            if task.completed:
                self.task_delete(task)
        self.update_task_list()

    def tabs_changed(self, e):
        self.update_task_list()

    def update_task_list(self):
        status = self.filter.tabs[self.filter.selected_index].text.lower()
        count = 0
        for task in self.tasks.controls:
            task.visible = (
                status == "all"
                or (status == "active" and not task.completed)
                or (status == "completed" and task.completed)
            )
            if not task.completed:
                count += 1
        self.items_left.value = f"{count} active item(s) left"
        self.update()

    def build(self):
        return ft.Column(controls=self.controls)


def main(page: ft.Page):
    page.title = "To-Do App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#f5f5f5"  # Light grey background for the page
    page.padding = 20
    page.update()

    # Create application instance
    todo = TodoApp()

    # Add application's root control to the page
    page.add(todo)

ft.app(target=main, view=ft.WEB_BROWSER)
