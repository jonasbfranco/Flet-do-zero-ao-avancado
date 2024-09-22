import flet as ft

# classe para criar as tarefas
class Task(ft.Column):
    def __init__(self, task_name, task_status_change, task_delete):
        super().__init__()
        self.completed = False
        self.task_name = task_name
        self.task_status_change = task_status_change
        self.task_delete = task_delete

    def build(self):
        self.display_task = ft.Checkbox(
            value=False,
            label=self.task_name,
            label_style=ft.TextStyle(color="#3450A1", weight="bold", size=16),
            check_color="#EB06FF",
            fill_color="#3450A1",
            on_change=self.status_changed
        )

        self.edit_name = ft.TextField(expand=1, on_submit=self.save_clicked)

        
        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_task,
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.CREATE_OUTLINED,
                            tooltip="Editar tarefa",
                            on_click=self.edit_clicked,
                            icon_color=ft.colors.GREEN,
                        ),
                        ft.IconButton(
                            icon=ft.icons.DELETE_OUTLINE,
                            tooltip="Deletar tarefa",
                            on_click=self.delete_clicked,
                            icon_color=ft.colors.RED,
                        ),
                    ]
                ),
            ]
        )

        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name,
                ft.IconButton(
                    icon=ft.icons.DONE_OUTLINE_OUTLINED,
                    tooltip="Atualizar tarefa",
                    on_click=self.save_clicked,
                    icon_color=ft.colors.GREEN,
                ),
            ]
        )
        
    
        return ft.Column(controls=[self.display_view, self.edit_view])
        
        
    def edit_clicked(self,e):
        #print(f"edi:", self.display_task.label)
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.edit_name.focus()
        self.update()

        
    def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

        
    def delete_clicked(self, e):
        self.task_delete(self)


    def status_changed(self, e):
        self.completed = self.display_task.value
        self.task_status_change(self)



# classe para criar o aplicaitivo
class TodoApp(ft.Column):
    def build(self):
        self.new_task = ft.TextField(
            hint_text="Qual tarefa precisa ser feita?",
            text_size=16,
            # color="#3450A1",
            expand=True,
            border_color="#3450A1",
            filled=True,
            # fill_color="#97B4FF",
            cursor_color="#3450A1",
            on_submit=self.add_task,
        )

        self.tasks = ft.Column(scroll=ft.ScrollMode.ADAPTIVE, height=400)

        self.filter = ft.Tabs(
            scrollable=False,
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[
                ft.Tab(text="Todas"),
                ft.Tab(text="Ativas"),
                ft.Tab(text="Concluídas"),
            ],
        )

        self.items_left = ft.Text("0 tarefas adicionadas", opacity=0.5)

        self.button_clear = ft.OutlinedButton(
            text="Apagar todas as concluídas".upper(),
            on_click=self.clear_completed_tasks,
            disabled=True,
        )


        return ft.Column(
            width=600,
            controls=[
                # Insercao das tarefas
                ft.Row(
                    controls=[
                        self.new_task,
                        ft.FloatingActionButton(
                            icon=ft.icons.ADD, 
                            bgcolor="#EB06FF",
                            tooltip="Adicionar tarefa",
                            height=50,
                            width=50,
                            on_click=self.add_task
                            ),
                    ]
                ),
                # lista das tarefas
                ft.Column(
                    controls=[
                        self.filter,
                        self.tasks,
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                self.items_left,
                                self.button_clear,
                            ],
                        ),   
                    ],
                ),
            ],
        )



    def tabs_changed(self, e):
        self.update()

    def add_task(self, e):
        if self.new_task.value:
            task=Task(self.new_task.value, self.task_status_change, self.task_delete)
            self.tasks.controls.append(task)
            self.new_task.value = ""
            self.new_task.focus()
            self.update()
            


    def clear_completed_tasks(self, e):
        for task in self.tasks.controls[:]:
            if task.completed:
                self.task_delete(task)
                self.button_clear.disabled = True


    def task_status_change(self, task):
        self.button_clear.disabled = True
        self.update()

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()


    def before_update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        count = 0
        task_complete = 0
        
        for task in self.tasks.controls:
            task.visible = (
                status == "Todas"
                or(status == "Ativas" and task.completed == False)
                or (status == "Concluídas" and task.completed)
            )
                 
            if not task.completed:
                count += 1
        

            if task.completed:
                task_complete += 1
                if task_complete == len(self.tasks.controls):
                    self.button_clear.disabled = False
                    print("Todas as tarefas estão completas")
                    print(task_complete)
                    print(len(self.tasks.controls))
                elif task_complete != len(self.tasks.controls):
                    self.button_clear.disabled = False
                    print("Algumas tarefas estão completas")
                    print(task_complete)
                    print(len(self.tasks.controls))
                else:
                    self.button_clear.disabled = False
                    print("Nenhuma tarefa esta completa")
                    print(task_complete)
                    print(len(self.tasks.controls))

        self.items_left.value = f"{count} tarefa(s) não concluída(s)"
        super().before_update()




def main(page: ft.Page):
    page.title = "Minhas Tarefas"
    page.window.width = 520
    page.window.height = 710
    page.window.maximizable = False
    page.window.resizable = False
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = ft.padding.only(top=20, bottom=20, left=20, right=20)
    
    def theme_change(e):
        # print(page.theme_mode)
        page.theme_mode = (
            ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        )
        # print(page.theme_mode)

        theme_icon.icon = (
            ft.icons.WB_SUNNY_OUTLINED if page.theme_mode == ft.ThemeMode.LIGHT else ft.icons.DARK_MODE_OUTLINED
        )
        page.update()


    
    page.theme_mode = ft.ThemeMode.LIGHT

    theme_icon = ft.IconButton(
        icon=ft.icons.WB_SUNNY_OUTLINED,
        tooltip="Alternar tema",
        on_click=theme_change
    )


    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Column(
                    alignment=ft.MainAxisAlignment.START,
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(value="Minhas Tarefas", size=44, weight="bold", color="#97B4FF"),
                            ]
                        )
                    ]
                ),
                ft.Column(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[theme_icon]
                )
            ]
        ),
    )

    page.update()

    app = TodoApp()

    page.add(app)

ft.app(target=main)