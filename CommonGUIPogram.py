#
#   Data preparation
#
import os
from fnmatch import fnmatch

def getAllDatatablesFromFolder(dirName):
    pattern = "*.csv"
    dataTables = []
    for path, subdirs, files in os.walk(dirName):
        for name in files:
            if fnmatch(name, pattern):
                filePath = os.path.join(path, name)
                dataTables.append(filePath)
    dataTables.sort()
    return dataTables

def trimDataTablesPaths(dataTablesPaths, dirLength):
    result = []
    for path in dataTablesPaths:
        name = path[dirLength+1 :-4]
        name = name.replace("Covid", "")
        name = name.replace("/", "_|_")
        result.append(name)

    return result


dirName = os.getcwd() + "/Data"
dataTablesPaths = getAllDatatablesFromFolder(dirName)
dataTables = trimDataTablesPaths(dataTablesPaths, len(dirName))

#
#   Run modules
#
import benfords_law as benford
import SIR as sir
import pearson_test as pearson
import Spearman_corr as sperman

def startAnalytics(title, path):
    try:
        print("Start " + title)

        benford.Benfords_law(title, path).train()
        print("Benford completed")

        sir.Learner(title, path, sir.loss, 140).train()
        print("SIR completed")

        pearson.Pearson(title)
        print("Pearson completed")

        sperman.Spearman(title, path).train()
        print("Spearman completed")

        print(title + " completed\n")

    except Exception as error:
        print("Title: " + title + "\tError: " + str(error) + "\n")

#
#   GUI Layout
#
import PySimpleGUI as sg
import os.path

defaultButtonColor = ('black', '#D9D9D9')
fileListColumn = [
    [
        sg.Input(size=(65, 13), key="-FOLDER_BROWSING-", default_text=dirName, enable_events=True, visible=True),
        sg.FolderBrowse("Browse data folder", initial_folder=dirName, key="-FOLDER_BROWSING-", button_color=defaultButtonColor),
    ],
    [
        sg.Listbox(values=dataTables, enable_events=True, size=(80, 20), key="-FILE LIST-", select_mode="multiple")
    ],
]

buttonsColumn = [
    [sg.Button("Start data analytics", button_color=defaultButtonColor)],
    [sg.Button("Start full data analytics", button_color=defaultButtonColor) ]
]

layout = [
    [
        sg.Column(fileListColumn),
        sg.VSeperator(),
        sg.Column(buttonsColumn),
    ]
]

appFont = (12)
sg.set_options(font=appFont)
sg.theme("DarkTeal2")
window = sg.Window("Covid_MIPT", layout)

#
#   Layout loop
#
while True:
    event, values = window.Read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    elif event == "-FOLDER_BROWSING-":
        newValue = values["-FOLDER_BROWSING-"]
        if newValue != dirName and newValue != "":
            dirName = values["-FOLDER_BROWSING-"]
            print("Switch dir to:\t" + dirName)
            dataTablesPaths = getAllDatatablesFromFolder(dirName)
            dataTables = trimDataTablesPaths(dataTablesPaths, len(dirName))
            window["-FILE LIST-"].update(dataTables)

    elif event == "Start data analytics": 
        for selectedItem in values["-FILE LIST-"]:
            index = dataTables.index(selectedItem)
            startAnalytics(selectedItem, dataTablesPaths[index])
        window['-FILE LIST-'].set_value([])

    elif event == "Start full data analytics":
        for selectedItem in dataTables:
            index = dataTables.index(selectedItem)
            startAnalytics(selectedItem, dataTablesPaths[index])

window.close()