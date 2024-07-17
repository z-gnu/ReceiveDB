from nicegui import ui
from datetime import datetime as dt
from os import get_terminal_size
from random import choice

from colorama import Fore, Back, Style, init

from db import save_to_db, search_db, Config

init()
config = Config()
dark = ui.dark_mode()
if config.dark_mode:
    dark.enable()

# Function to gather input data and save it to the database
def gather_data():
    data = {
        "supplier": supplier_input.value,
        "part_number": part_number_input.value,
        "date": date_input.value,
        "inspector": inspector_input.value
    }
    save_to_db(data)  # Save data to the database
    print(f"Data saved: {data}")  # Print the saved data to the console for confirmation
    clear_inputs()  # Clear the input fields after submission

# Function to clear input fields
def clear_inputs():
    supplier_input.value = ""
    part_number_input.value = ""
    date_input.value = ""
    inspector_input.value = ""

# Function to search data and update the result display
def search_data():
    query = search_input.value
    results = search_db(query)
    results_display.clear()
    if results:
        with results_display:
            table = ui.table().classes('w-full')
            table.add_column('Supplier')
            table.add_column('Part Number')
            table.add_column('Date')
            table.add_column('Inspector')
            for result in results:
                table.add_row(result)
    else:
        ui.label("No results found.").classes('w-full').parent(results_display)

with ui.tabs().classes('w-full') as tabs:
    one = ui.tab('Data Entry')
    two = ui.tab('Search & Destroy')

with ui.tab_panels(tabs, value=one).classes('w-full'):  # Set 'one' as the default tab
    with ui.tab_panel(one):
        with ui.card().classes('p-12 w-full max-w-4xl mx-auto'):  # Adjusted card width and centered it
            supplier_input = ui.input(placeholder='Supplier').props('filled').style('font-size: 20px; height: 40px; padding: 10px; width: 100%; margin-bottom: 20px')
            part_number_input = ui.input(placeholder='Part number').props('filled').style('font-size: 20px; height: 40px; padding: 10px; width: 100%; margin-bottom: 20px')
            date_input = ui.input(placeholder='Date').props('filled').style('font-size: 20px; height: 40px; padding: 10px; width: 100%; margin-bottom: 20px')
            inspector_input = ui.input(placeholder='Inspector').props('filled').style('font-size: 20px; height: 40px; padding: 10px; width: 100%; margin-bottom: 80px')
            ui.button('Submit', on_click=gather_data).style('font-size: 20px; padding: 10px 20px')
    with ui.tab_panel(two):
        with ui.card().classes('p-12 w-full max-w-4xl mx-auto'):
            search_input = ui.input(placeholder='Search').props('filled').style('font-size: 20px; height: 40px; padding: 10px; width: 100%; margin-bottom: 20px')
            ui.button('Search', on_click=search_data).style('font-size: 20px; padding: 10px 20px')
            results_display = ui.column().classes('w-full mt-4')


c = ''.join(['*' for i in range(get_terminal_size()[0])])
colors = list(vars(Fore).values())

bad_colors = ['\x1b[97m', '\x1b[37m', '\x1b[90m']
for bad_color in bad_colors:
    colors.remove(bad_color)

colored_chars = [choice(colors) + Style.BRIGHT + char for char in c]
print(''.join(colored_chars) + Style.RESET_ALL)


ui.run()
