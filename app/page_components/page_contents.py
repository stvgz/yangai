# some layout components
import dash_table

def crate_table():

    a=dash_table.DataTable(
        id='table',
        columns=[],
        page_current=0,
        page_size=20,
        page_action='native', #front end
        sort_mode='single',
        filter_action='native',
        sort_action='native',

    )

# some layout components
import dash_table

def crate_table():

    a=dash_table.DataTable(
        id='table',
        columns=[],
        page_current=0,
        page_size=20,
        page_action='native', #front end
        sort_mode='single',
        filter_action='native',
        sort_action='native',

    )

    return a