from nicegui import ui ,app,events
import os 

resource_dir = "resources"
pics = os.path.join(resource_dir,'pics')
app.add_static_files("/resources",resource_dir)
@ui.page("/")
def main():
    with ui.row().classes("w-full"):
        with ui.column().classes("col-7"):
            ui.label("abc")
            #ui.image("resources/pics/start.jpeg")
            circle_list = []
            def mouse_handler(e: events.MouseEventArguments):
                print(e)
                if e.button==0 and e.type == 'mousedown':
                    #color = 'SkyBlue' if e.type == 'mousedown' else 'SteelBlue'
                    e.image_x,e.image_y
                    circle_list.append(f'<circle cx="{e.image_x}" cy="{e.image_y}" r="15" fill="none" stroke="{'SkyBlue'}" stroke-width="4" />')
                    ii.content = "".join(circle_list)
                   # ui.notify(f'{e.type} at ({e.image_x:.1f}, {e.image_y:.1f})')
                if e.button==2 and e.type == 'mousedown':
                    #color = 'SkyBlue' if e.type == 'mousedown' else 'SteelBlue'
                    if len(circle_list) > 0:
                        circle_list.pop()
                        ii.content = "".join(circle_list)
                    #ii.content += f'<circle cx="{e.image_x}" cy="{e.image_y}" r="15" fill="none" stroke="{'Red'}" stroke-width="4" />'
                   # ui.notify(f'{e.type} at ({e.image_x:.1f}, {e.image_y:.1f})')
                print(ii.content)
            src = "/resources/pics/start.jpeg"
            ii = ui.interactive_image(src, on_mouse=mouse_handler, events=['mousedown'], cross=True)
            
        with ui.column().classes("col-1"):
            ui.label("abc")
        with ui.column().classes("col-2"):
            ui.label("你好")
    with ui.row().classes("w-full"):
        pass

ui.run(native=True)


