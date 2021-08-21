import PySimpleGUI as sg
import os


DEFAULT_TITLE = 'Entropy'
DEFAULT_FONT = 'Consolas'
DEFAULT_FONT_SIZE = 12
DEFAULT_THEME = 'Light'
ICON_PATH = '..\icon.ico'
BCKG_COLOR = '#1c1c1c'
SUPPORTED_FORMATS = (('Text Files', '*.txt'),('INI Files', '*.ini'),('Config Files', '*.cfg'),('All Files','*.*'))

index_list = str([[x for x in range(0, 100)]])

index_list = index_list.replace(',', '\n')
index_list = index_list.replace(' ', '')
index_list = index_list.replace('[', '')
index_list = index_list.replace(']', '')

theme = DEFAULT_THEME
font = DEFAULT_FONT
font_size = DEFAULT_FONT_SIZE

menu_def = [['&File', ['&New', '&Open', '&Save', 'Properties']],
            ['&Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
            ['&Config', ['&Font', '&Theme']]]

#ICON_PATH = sg.PopupGetFile('Choose Icon', file_types=(('PNG images','*.png'),), no_window=True)

sg.SetOptions(
    icon = ICON_PATH,
    background_color= BCKG_COLOR,
    text_color= 'white',
    text_element_background_color=BCKG_COLOR
)

layout = [
[sg.Menu(menu_def)],
[sg.T('Untitled',
      visible=True,
      size=(100,1),
      justification='center',
      pad=(5,0),
      font=(DEFAULT_FONT, 16),
      background_color=BCKG_COLOR,
      key='lbl')],
[sg.Multiline(
    size=(100, 20),
    pad=(5,0),
    justification='left',
    default_text='',
    expand_x=True,
    expand_y=True,
    border_width=0,
    font=(DEFAULT_FONT, 12),
    key='mtl',
    text_color='#eeeeee',
    background_color = BCKG_COLOR,
    autoscroll=False,
    no_scrollbar=True)]]

window = sg.Window(
    title=DEFAULT_TITLE,
    layout=layout,
    icon=ICON_PATH,
    location=(0, 0),
    margins=(0, 0),
    size=(800, 600),
    resizable=True,
    background_color= BCKG_COLOR,
    enable_close_attempted_event=True,
    )


class TextFile:
    def __init__(self, name, path, text):
        self.name = name
        self.path = path
        self.text = text


mtl = window['mtl']
lbl = window['lbl']
file_path = ''
current_file = TextFile('Untitled', '', '')
window.read(timeout=100)
mtl.Widget.config(insertbackground='white')


def update_editor(nf):
    mtl.Update(nf.text)
    window.set_title(nf.path)
    lbl.Update(nf.name)
    mtl.Widget.mark_set("insert", 0.0)


update_editor(current_file)


def open_file():
    f_path = sg.PopupGetFile('Open File', no_window=True, file_types=SUPPORTED_FORMATS)
    # check if empty
    if f_path == '':
        return None

    cur_file = open(f_path, 'r+')
    text = cur_file.read()
    filename = os.path.basename(cur_file.name)
    cur_file.close()
    # create TextFile instance
    tf = TextFile(filename, f_path, text)

    # update the editor
    update_editor(tf)

    return tf


def save_file(tf):
    if tf.path == '':
        tf.path = sg.PopupGetFile('Save File', no_window=True, save_as=True, file_types=SUPPORTED_FORMATS, icon=ICON_PATH)
        if tf.path == '':
            return
    cur_file = open(tf.path, 'w')
    cur_file.write(mtl.Get())
    tf.name = os.path.basename(cur_file.name)
    cur_file.close()
    update_editor(tf)
    return tf


def new_file():
    tf = TextFile('Untitled', '', '')
    update_editor(tf)
    return tf

def set_theme():
    new_theme = theme
    st_layout = [
        [sg.T('Theme')],[sg.Radio('Light', 0, background_color=BCKG_COLOR, enable_events=True, key='L')],[sg.Radio('Dark', 0 , background_color=BCKG_COLOR, default=True,enable_events=True, key='D')], [sg.OK()]
    ]
    st = sg.Window(
        title='Theme',
        layout=st_layout,
        modal=True,
        keep_on_top=True
    )
    while True:
        event, values = st.read()
        if event == 'OK':
            break
        if event == sg.WIN_CLOSED or event == 'CANCEL':
            break
        if event == 'L':
            print('you chose light')
        if event == 'D':
            print('you chose dark')

    st.close()

def set_font():
    new_font = font
    new_font_size = font_size
    sf_layout = [
        [sg.T('Font'),
        sg.InputCombo(['Consolas', 'OCR A Extended'], change_submits=True, default_value=font, key ='font_combo', readonly=True, enable_events=True)],
        [sg.T('Size'),
        sg.InputCombo([x for x in range(6, 74, 2)], bind_return_key=True, change_submits=True, default_value=font_size, key = 'size_combo', enable_events=True)],
        [sg.Button('OK', key='OK_BUTTON'),
        sg.Button('Cancel', key='CANCEL')]
    ]
    sf = sg.Window(layout=sf_layout, title='Change Font', keep_on_top=True, modal=True)
    while True:
        _event, _values = sf.read()
        if _event == 'OK_BUTTON':
            break
        if _event == sg.WIN_CLOSED or _event == 'CANCEL':
            mtl.update(font=(font, font_size))
            lbl.update(font=(font, 16))
            break
        new_font = str(_values['font_combo'])
        new_font_size = int(_values['size_combo'])
        mtl.update(font=(new_font, new_font_size))
        lbl.update(font=(new_font, 16))
        print(_event, _values)
    sf.close()
    return new_font, new_font_size


while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT:
        tmp = mtl.Get()
        tmp = tmp.replace('\n', '', 1)
        print('Current text is: >', tmp, '<', len(tmp), ' file text is: ', len(current_file.text))
        print(tmp == current_file.text)
        if tmp == current_file.text:
            break

        if sg.PopupYesNo('Save File?', line_width=50, icon=ICON_PATH) == 'Yes':
            save_file(current_file)
            break
        else:
            break

    if event == 'Open':
        current_file = open_file()
    if event == 'Save':
        current_file = save_file(current_file)
    if event == 'New':
        current_file = new_file()
    if event == 'Font':
        font, font_size = set_font()
    if event == 'Theme':
        set_theme()
    print('You entered ', values[0])

window.close()
