import os
from tkinter import filedialog
import tkinter as tk
import balance_module
import image_patching
import whitespace_filter
import initialisation
import image_normalisation
import augmentation
import image_patching_controller
import settings


def SaveData():
    global Active_Module
    DefaultFile = [('HistoClean File', '*.hc')]
    SavePath = filedialog.asksaveasfilename(initialdir=os.getcwd(), filetypes=DefaultFile, defaultextension=DefaultFile)
    print(f"Saving data to {SavePath}")
    Data = []

    if Active_Module == "Patch":
        Data.append("Patch")
        # Data.append(SettingValues)


def run():
    tk.mainloop()


def patch_image(imageFolder, saveLocation, outputTileSize, magnification, outputExtension):
    image_patching.ImagePatching.PreChecks(imageFolder, saveLocation, outputTileSize, magnification, outputExtension)


def white_filter(imgFolder, minTissueCoverage, method, blur, keepSubThresholdImagesSeparate = 1, createBinaryMasks = 1):
    #  Needs the checkboxes at bottom added as parameters
    # This is done in gui using KeepCheckVar, which updates on checkbox update (needs checked)
    whitespace_filter.WhitespaceFilter.WS_Thread_Threading(imgFolder, minTissueCoverage, method, blur, keepSubThresholdImagesSeparate, createBinaryMasks)

def balance(imgFolders, balance, folderVal):
    balance_module.Balance.Adjust_ProgressBar(imgFolders, balance, folderVal)

def image_normalisation(targetImage, targetFolder, method, newSaveFolder=None):
    image_normalisation.ImageNormalisation.Norm_Thread_Threading(targetImage, targetFolder, method, newSaveFolder)

def augment_images(imgFolder, augments, applySize, applyMethod):
    augmentation.Augmentation.augment(imgFolder, augments, applySize, applyMethod)


if __name__ == '__main__':
    print('main')
    pixelmethod = {"name": 'Positive Pixel Classification', "cutoff": 0.7}

    augments = [{"type": 'Brightness and Contrast', "subtype": "Brightness", "parameters": [100, 1]}]
    # augment_images('/home/smurfy/Desktop/University/jpg2', augments, 0, '/home/smurfy/Desktop/University/test')

    run()
    # print(tet)
    # print(list(filter(None, tet)))
    # ^ useful for error handling ?



    # balance(['/home/smurfy/Desktop/University/jpg', '/home/smurfy/Desktop/University/jpg2'], 0, 1)
    # white_filter('/home/smurfy/Desktop/University/jpg', 30, pixelmethod, 1)

    # patch_image('/home/smurfy/Desktop/University/svs', '/home/smurfy/Desktop/University/test/test2', 20, 10, 0)
    # Could also make it so instead of saving the images they are returned in a function ? or is there too many
    # (storing on hardisk vs memory)
