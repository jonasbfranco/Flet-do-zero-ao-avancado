import flet as ft
from custom_checkbox import Checkbox

def main(page: ft.Page):
    page.title = "Minhas Tarefas"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 450
    page.window.height = 650
    page.padding = ft.padding.only(top=20, left=20, right=20, bottom=20)
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def add_task(e):
        #print(new_task.value)
        if new_task.value == "":
            new_task.focus()
            return
        task_list.controls.append(Checkbox(new_task.value)) 
        new_task.value = ''
        page.update()
        new_task.focus()
    
  
    new_task = ft.TextField(hint_text='Insira uma tarefa...', expand=True,
                            autofocus=True, on_submit=add_task)
    new_button = ft.FloatingActionButton(icon=ft.icons.ADD, on_click=add_task)

    task_list = ft.Column()
  
    card = ft.Column(
        width=450,
            controls=[
                ft.Row(
                    controls=[
                        new_task,
                        new_button
                    ]
                ),
                task_list,
            ]
        )


    page.add(card)
    

ft.app(target=main)
