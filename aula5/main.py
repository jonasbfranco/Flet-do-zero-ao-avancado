import flet as ft

def main(page: ft.Page):
    page.title = "Minhas Tarefas"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 400
    page.window.height = 650
    page.padding = ft.padding.only(top=20, left=20, right=20, bottom=20)

    def add_task(e):
        print(new_task.value)
        task_list.controls.append(ft.Checkbox(label=new_task.value)) 
        new_task.value = ''
        page.update()
    
  
    new_task = ft.TextField(hint_text='Insira uma tarefa...', expand=True)
    new_button = ft.FloatingActionButton(icon=ft.icons.ADD, on_click=add_task)

    task_list = ft.Column()
  
    card = ft.Column(
        width=400,
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
