#!/usr/bin/env python3
import flet as ft
import markdown2
import os

class FileAlert(ft.UserControl):
    
    file_path = None
    markdown = None
    
    def __init__(self, page):
        super().__init__()
        
        self.page = page
        
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Please confirm"),
            content=ft.Text("Overwrite?"),
            actions=[
                ft.TextButton("No", on_click=self.close_dlg),
                ft.TextButton("Yes", on_click=self.yes_click),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("closed"),
        )
        
    # *** Add popup.   
    def open(self):
        self.page.dialog = self.dlg_modal
        self.dlg_modal.open = True
        self.page.update()
                
    def close_dlg(self, e):
        self.dlg_modal.open = False
        self.page.update()
    
    def yes_click(self, e):
            
        save_markup(self.page, self.file_path, self.markdown)
            
        self.dlg_modal.open = False
        self.page.update()
        
def save_markup(page, save_path, content):
    if 'md' in os.path.splitext(save_path)[-1].lower():
        data = content
    elif 'html' in os.path.splitext(save_path)[-1].lower():
        data = markdown2.markdown(content)
        
    try:
        with open(save_path, 'w') as export:
            export.write(data)
        page.snack_bar = ft.SnackBar(ft.Text(f"File saved."),
                                    bgcolor=ft.colors.PINK_100)
        page.snack_bar.open = True
    except Exception as err:
        page.snack_bar = ft.SnackBar(ft.Text(str(err)),
                                    bgcolor=ft.colors.PINK_100)
        page.snack_bar.open = True

def main(page: ft.Page):
    
    # *** Page setup. ***
    page.title = "Flet Markdown Example"
    page.padding=4
    
    # *** Add floating button for saving. ***
    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.icons.SAVE_ALT_ROUNDED,  
        bgcolor=ft.colors.PINK_900,
        tooltip="Save Markdown?",
        width=35,
        height=35,
        on_click=lambda _: export_dialog.save_file(allowed_extensions=["md","html"],file_name="Untitled.md"),
    )
    
    # *** Add file save dialog and actions. ***
    def export_file(e: ft.FilePickerResultEvent):
        save_path = e.path
        if len(MarkDownOutput.value) > 0:
            if '.' not in save_path:
                page.snack_bar = ft.SnackBar(ft.Text(f"Please provide a proper filename. You can save as .md or .html."),
                                            bgcolor=ft.colors.PINK_100)
                page.snack_bar.open = True
            else:
                if os.path.exists(save_path):
                    
                    OWAlert = FileAlert(page)
                    OWAlert.markdown = MarkDownOutput.value
                    OWAlert.file_path = save_path
                    OWAlert.open()
                    
                else:
                    
                    save_markup(page, save_path, MarkDownOutput.value)
                    
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Nothing to save."),
                                        bgcolor=ft.colors.PINK_100)
            page.snack_bar.open = True
            
        page.update()
        
    export_dialog = ft.FilePicker(on_result=export_file)
    page.overlay.append(export_dialog)
    
    # *** Add test and markdown controls and action. ***
    def update_markdown(e):
        MarkDownOutput.value = MarkDownInput.value
        MarkDownOutput.update()
        
    MarkDownInput = ft.TextField(label="MarkDown", 
                                 multiline=True, 
                                 autofocus=True, 
                                 border=ft.InputBorder.NONE, 
                                 filled=True, 
                                 on_change=update_markdown)
    
    MarkDownOutput = ft.Markdown(MarkDownInput.value,
            selectable=True,
            code_theme="tomorrow-night-eighties",
            code_style=ft.TextStyle(font_family="Roboto Mono"),
            extension_set=ft.MarkdownExtensionSet.GITHUB_FLAVORED,
            on_tap_link=lambda e: page.launch_url(e.data),)
    

    # *** Build the page. ***
    page.add(
        ft.Row(
            [ 
                ft.Container(
                    MarkDownInput,
                    alignment=ft.alignment.top_left,
                    expand=True,
                    padding=4
                ),
                ft.VerticalDivider(width=12, thickness=4),
                ft.Column(
                    controls=[ft.Container(
                        MarkDownOutput,
                        padding=4,
                    )],
                    scroll=ft.ScrollMode.AUTO,
                    alignment=ft.CrossAxisAlignment.START,
                    expand=True,
                )
            ],
            spacing=0,
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START
        ),
    )
 
# MAIN : Run with assets folder set.    
if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")