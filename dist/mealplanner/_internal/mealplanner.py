# imports
import fileinput
import math
import random
import copy
from tabulate import tabulate
from contextlib import redirect_stdout
import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivymd.app import MDApp
from kivy.uix.progressbar import ProgressBar
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.text import LabelBase
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
import shutil
from kivy.properties import StringProperty
from kivy.uix.scrollview import ScrollView
from pathlib import Path
from pygments.formatters import ImageFormatter
import pygments.lexers
from kivy.clock import Clock
from kivy.loader import Loader
from bs4 import BeautifulSoup
import requests
from recipe_scrapers import scrape_me
from recipe_scrapers import scrape_html
import textwrap
import os
import json
import time

from functools import partial
from kivy.uix.popup import Popup
import sys
from kivy.resources import resource_add_path, resource_find
# values
# represents start day of meal plan as in monday,tuesday etc.
stday = 0
# represents how many days to generate mealplans for days * 3 meals per day etc.
days = 0
# represents whether fish should be considered for every meal
fish_aval_everyday = 0
# represents whether mexican food should be considered everyday
mex_fd_everyday = 0
# represents whether to choose a fish dish for dinner meal on friday
fishfr = 0
fishfrml = 0
# represents whether to choose a mexican food dish for dinner on tuesday
tacot = 0
tacotml = 0
# represents how many entrees to generate per meal
ent = 0
# represents how many sides to generate per meal
sidecount = 0
# command function just represents selected function values
command = 0
# set item indicates whether some meals should be the same everyday of the week
setitem = 0
setdaysiter = 0
setdaysday = ""
setdayslunch = 0
setdaysdinner = 0
setdaysidecount = 0
setdayssides = 0
setdaysentreecount = 0
setdaysentree = 0
setentreecounter = 1
# this value represents where the week starts with its day as an integer
stweek = 0
# this value handles how many times day of week cycles
daystp = 0
# this number handles total days to generate
totaldays = 1
# this value handles the exact days to generate from the day of week table
dyweektbl = 0
# this number will be used to multiply the sides and entrees and then to count
# down the generator
gendays = 0
# genent represents the actual number of entrees to generate
genent = 0
# gensides represents the actual sides to generate
genside = 0
daysetup=""
daysetup2=0

daysetupconv=0
daysetupconv2=0
#
startweekmon = "y"
startweektue = "y"
startweekwed = "y"
startweekthu = "y"
startweekfri = "y"
startweeksat = "y"
startweeksun = "y"
dictlength = 0
#added for maintanence of the ui classes and transfer of variables
sideret=0
entret=0
addnwentree=""
scraped_item=""
scraped_entree=[]
scraped_side=[]
scraped_dessert=[]
scraped_bread=[]
scraped_salad=[]
scraped_breakfast=[]
scraped_mexicanfd=[]
scraped_fish=[]
scraped_request=0
# starting with food entree dishes sorted by type
# e.g chicken/beef/pork/fish
# dictionaries stored here
# entree nested dictionary
# 1 is chicken dishes   2 is beef dishes 3 is pork dishes 4 is soups
# 5 is pasta dishes 8 is other category 7 is fish dishes 6 is mexican food
# 10 is breakfast
entree = {
    1: {1: "grilled chicken", 2: "chicken and dumplings", 3: "outback chicken",
        4: "chicken parmesian", 5: "chicken fetticini alfredo",
        6: "mississippi chicken", 7: "cajun chicken alfredo", 8: "chicken gnocchi",
        9: "chicken tortellini alfredo", 10: "hawaiian chicken",
        11: "chicken francaise", 12: "chicken wraps", 13: "roasted whole chicken",
        14: "vegetable soup", 15: "gumbo", 16: "chili",
        17: "beef stew", 18: "manwich", 19: "mississippi beef", 20: "roast beef", 21: "meat loaf"
        , 22: "philly cheese steak", 23: "stuffed peppers", 24: "salisbury steak",
        25: "chicken fried steak", 26: "smoked brisket",
        27: "grilled porkchops", 28: "bbq porkchops", 29: "brats and sauerkraut",
        30: "pork tenderloin", 31: "pineapple ham", 32: "pulled pork", 33: "bbq ribs",
        34: "soy honey porkchops",35: "beef stroganaff",
        36: "spaghetti and meatballs", 37: "lasagna", 38: "ravioli"},


    7: {1: "shrimp scampy", 2: "salmon patties", 3: "fried catfish", 4: "orange roughy",
        5: "salmon", 6: "snow crab"},

    6: {1: "quesadillas", 2: "burritos", 3: "tacos", 4: "enchiladas"},





    10: {1: "cheese grits", 2: "oatmeal", 3: "french toast casserole",
         4: "eggs benedict", 5: "breakfast pizza", 6: "pancakes",
         7: "breakfast casserole", 8: "omelets", 9: "breakfast burritos",
         10: "french toast", 11: "montecristo sandwiches", 12: "stuffed crescents"},

    8: {}}
# all sides nested dictionary
# 1 is veggie sides 2 is chicken sides 3 is beef sides
# 4 is pasta sides 5 is soup sides 6 is rice sides

side = {
    1: {1: "buttery corn", 2: "corn on the cob", 3: "mexican street corn",
        4: "spinach", 5: "fried cabbage", 6: "green bean casserole",
        7: "grilled corn on the cob", 8: "sweet peas", 9: "asparagus", 10: "green beans",
        11: "collard greens", 12: "corn casserole", 13: "brussel sprouts",
        14: "potatoes au gratin", 15: "tater tot casserole",
        16: "roasted broccoli and cauliflower", 17: "baked potatoes",
        18: "twice baked potatoes", 19: "cowboy beans",
        20: "roasted zucchini and squash", 21: "mashed potatoes",
        22: "broccoli casserole", 23: "sweet potato casserole",
        24: "diced red potatoes with cheese and bacon bits",
        25: "copper penny carrots", 26: "bacon wrapped asparagus",
        27: "stuffed jalapenos", 28: "broccoli parmesian", 29: "potato cakes",
        30: "fondant potatoes", 31: "corn pudding", 32: "squash casserole",
        33: "butternut squash soufle", 34: "parmesian corn",
        35: "honey roasted carrots", 36: "vegetable casserole",
        37: "parmesian stuffed mushrooms",38:"chicken casserole", 39: "chicken pot pie",
        40:"shepherds pie",41:"red beans and rice", 42: "white rice", 43: "dirty rice",
        44:"tomato sauce pasta", 45: "alfredo sauce pasta",46: "cheese sauce pasta",
        47: "broccoli soup" },



    "bread": {1: "cornbread", 2: "grilled cheese", 3: "cheddar biscuits", 4: "dinner rolls",
              5: "garlic bread", 6: "mexican cornbread", 7: "hawaiian rolls",
              8: "zuchhini bread"},




    5: {}, }
# salads dictionary
salad = {1: "potato salad", }
# desserts dictionary
dessert = {1: "cinnamon rolls", 2: "chocolate cake", 3: "rice crispy treats",
           4: "oatmeal cookies", 5: "chocolate chip cookies", 6: "pecan pie",
           7: "butterfinger cake", 8: "double chocolate muffins", 9: "brownies",
           10: "layer brownies", 11: "blueberry muffins", 12: "chocolate cream pie",
           13: "banana cream pie", 14: "reeses chip cookies", 15: "cheesecake",
           16: "orange cake", 17: "red velvet cake", 18: "banana nut muffins",
           19: "chocolate pudding", 20: "banana pudding", 21: "butterscotch cookies",
           22: "oreo pudding", 23: "butterscotch pudding", 24: "jello"}
daysweek = {"mon": 1, "tue": 2, "wed": 3
    , "thu": 4, "fri": 5, "sat": 6, "sun": 7}
dysweekc = {1: "Monday ", 2: "Tuesday ", 3: "Wednesday ", 4: "Thursday ", 5: "Friday ", 6: "Saturday ", 7: "Sunday "}

# daysconvtolist={"mon":}
# set item dictionaries these dicts will save set menu items to days and meals
# dinnere represents dinner entree, lunche represents lunch entree
setdays = {
    "mon": {"Monday > breakfast": 0, "lunch": 0, "dinner": 0},
    "tue": {"Tuesday > breakfast": 0, "lunch": 0, "dinner": 0},
    "wed": {"Wednesday > breakfast": 0, "lunch": 0, "dinner": 0},
    "thu": {"Thursday > breakfast": 0, "lunch": 0, "dinner": 0},
    "fri": {"Friday > breakfast": 0, "lunch": 0, "dinner": 0},
    "sat": {"Saturday > breakfast": 0, "lunch": 0, "dinner": 0},
    "sun": {"Sunday > breakfast": 0, "lunch": 0, "dinner": 0}, }

# this will track which week the functions will work on at the time

week_one = {}
week_two = {}
week_three = {}
week_four = {}
week_five = {}
week_six = {}

working_week = 0
weeks = {1: week_one, 2: week_two, 3: week_three, 4: week_four, 5: week_five, 6: week_six}
# these dictionaries will be actual week plans generated


setdaymealdinner4 = []
setdaymealdinner3 = []
setdaymealdinner2 = []
setdaymealdinner = []
setdaymeallunch4 = []
setdaymeallunch3 = []
setdaymeallunch2 = []
setdaymeallunch = []
# this section is for working lists+dictionaries used to build data tables
# this list fills with the days of the week in the order from start day
daysweekgen = []
every_gen_entree=[]
every_gen_side=[]
every_gen_dessert=[]
every_gen_salad=[]
every_gen_breakfast=[]
every_gen_brd=[]
# these list represent lists to be generated and added to the primary dict.
monbreak1 = []
monlunch1 = []
mondinner1 = []
tuebreak1 = []
tuelunch1 = []
tuedinner1 = []
wedbreak1 = []
wedlunch1 = []
weddinner1 = []
thubreak1 = []
thulunch1 = []
thudinner1 = []
fribreak1 = []
frilunch1 = []
fridinner1 = []
satbreak1 = []
satlunch1 = []
satdinner1 = []
sunbreak1 = []
sunlunch1 = []
sundinner1 = []
monbreak2 = []
monlunch2 = []
mondinner2 = []
tuebreak2 = []
tuelunch2 = []
tuedinner2 = []
wedbreak2 = []
wedlunch2 = []
weddinner2 = []
thubreak2 = []
thulunch2 = []
thudinner2 = []
fribreak2 = []
frilunch2 = []
fridinner2 = []
satbreak2 = []
satlunch2 = []
satdinner2 = []
sunbreak2 = []
sunlunch2 = []
sundinner2 = []
monbreak3 = []
monlunch3 = []
mondinner3 = []
tuebreak3 = []
tuelunch3 = []
tuedinner3 = []
wedbreak3 = []
wedlunch3 = []
weddinner3 = []
thubreak3 = []
thulunch3 = []
thudinner3 = []
fribreak3 = []
frilunch3 = []
fridinner3 = []
satbreak3 = []
satlunch3 = []
satdinner3 = []
sunbreak3 = []
sunlunch3 = []
sundinner3 = []
monbreak4 = []
monlunch4 = []
mondinner4 = []
tuebreak4 = []
tuelunch4 = []
tuedinner4 = []
wedbreak4 = []
wedlunch4 = []
weddinner4 = []
thubreak4 = []
thulunch4 = []
thudinner4 = []
fribreak4 = []
frilunch4 = []
fridinner4 = []
satbreak4 = []
satlunch4 = []
satdinner4 = []
sunbreak4 = []
sunlunch4 = []
sundinner4 = []
monbreak5 = []
monlunch5 = []
mondinner5 = []
tuebreak5 = []
tuelunch5 = []
tuedinner5 = []
wedbreak5 = []
wedlunch5 = []
weddinner5 = []
thubreak5 = []
thulunch5 = []
thudinner5 = []
fribreak5 = []
frilunch5 = []
fridinner5 = []
satbreak5 = []
satlunch5 = []
satdinner5 = []
sunbreak5 = []
sunlunch5 = []
sundinner5 = []
monbreak6 = []
monlunch6 = []
mondinner6 = []
tuebreak6 = []
tuelunch6 = []
tuedinner6 = []
wedbreak6 = []
wedlunch6 = []
weddinner6 = []
thubreak6 = []
thulunch6 = []
thudinner6 = []
fribreak6 = []
frilunch6 = []
fridinner6 = []
satbreak6 = []
satlunch6 = []
satdinner6 = []
sunbreak6 = []
sunlunch6 = []
sundinner6 = []
#file and save handling here
entreeload=[]
sideload=[]
dessertload=[]
breadload=[]
saladload=[]
breakfastload=[]
mexicanfdload=[]
fishload=[]

trigger="n"

dayvaluecheck = []
dayvaluecheck1 = []
ent_rec_comp=[]
side_rec_comp=[]
salad_rec_comp=[]
brk_rec_comp=[]
brd_rec_comp=[]
des_rec_comp=[]
mex_rec_comp=[]
fsh_rec_comp=[]
urls_pre_filter1=""


#gui section
def gendaysmath(gendays,days):
    gendays=+days

    return gendays
def startwkmath(stday,daysweekgen,dysweekc,stweek,daystp,totaldays,days):
    stweek = daysweek.get(stday)
    daysweekgen = dysweekc.get(stweek)
    daystp = 7 - (stweek)
    totaldays = -1
    totaldays = +(days - daystp - 1)
    while stweek < 7:  # start work here
        daysweekgen += (dysweekc.get(stweek + 1))
        stweek += 1
    stweek -= 7
    while totaldays > 0:
        stweek += 1
        totaldays -= 1
        daysweekgen += dysweekc.get(stweek)

        if stweek == 7:
            stweek -= 7
    print(daysweekgen)
    return stday,daysweekgen,stweek
def entsidesmath(ent, sidecount,entret,sideret,Entsidegen):


    ent=+entret
    sidecount=+sideret
    print(ent)
    print(sidecount)
    return ent,sidecount,entret,sideret
def fishfrsetup(fishfrml,setdays):
    if fishfrml == "lunch":
        setdays.update({"fri": {"lunch": "fish friday"}})
        print(setdays)
    elif fishfrml == "dinner":
        setdays.update({"fri": {"dinner": "fish friday"}})
        print(setdays)

    elif fishfrml == "allday" or "all day":
        setdays.update({"fri": {"breakfast": 0, "lunch": "fish friday", "dinner": "fish friday"}})
        print(setdays)
        return setdays
def tacotsetup(tacotml,setdays):
    if tacotml == "lunch":
        setdays.update({"tue": {"lunch": "taco tuesday"}})
        print(setdays)
    elif tacotml == "dinner":
        setdays.update({"tue": {"dinner": "taco tuesday"}})
        print(setdays)

    elif tacotml == "allday" or "all day":
        setdays.update({"tue": {"lunch": "taco tuesday", "dinner": "taco tuesday"}})
        print(setdays)
        return setdays

def setday1lunch(setdaymeallunch,sete1,sets11,sets12,sets13):
    setdaymeallunch.append(sete1)
    setdaymeallunch.append(sets11)
    setdaymeallunch.append(sets12)
    setdaymeallunch.append(sets13)
    print(setdaymeallunch)
    return  setdaymeallunch
def setday1dinner(setdaymeallunch,seted1,setsd11,setsd12,setsd13,setdaymealdinner,setdays,daysetup,setdaysday):
    setdaymealdinner.append(seted1)
    setdaymealdinner.append(setsd11)
    setdaymealdinner.append(setsd12)
    setdaymealdinner.append(setsd13)
    print(setdaymealdinner)
    setdaysday = daysetup
    setdays.update({setdaysday: {"lunch": setdaymeallunch, "dinner": setdaymealdinner}})
    print(daysetup)
    print(setdaysday)
    print(setdays)
    return setdays
def setday2lunch(setdaymeallunch2,sete2,sets21,sets22,sets23):
    setdaymeallunch2.append(sete2)
    setdaymeallunch2.append(sets21)
    setdaymeallunch2.append(sets22)
    setdaymeallunch2.append(sets23)
    print(setdaymeallunch2)
    return  setdaymeallunch2
def setday2dinner(setdaymeallunch2,seted2,setsd21,setsd22,setsd23,setdaymealdinner2,setdays,setdaysday,daysetup2):
    setdaymealdinner2.append(seted2)
    setdaymealdinner2.append(setsd21)
    setdaymealdinner2.append(setsd22)
    setdaymealdinner2.append(setsd23)
    print(setdaymealdinner2)
    setdaysday = daysetup2
    setdays.update({setdaysday: {"lunch": setdaymeallunch2, "dinner": setdaymealdinner2}})
    print(setdays)
    return setdays

def add_new_entree(entree,entreeload,addnwentree):

    with open("addedentree.py", "r") as mae:
        entpreload = str(mae.readlines())
        # these 3 functions clean up the text
        entpreload = entpreload.strip("""['""")
        entinload = list(entpreload.split(","))
        entinload.pop(-1)
        entinload.append(addnwentree)
        # strictly text cleanup ^
        entreeload = entinload
        mae.close()

        mae = open("addedentree.py", "w")
        ent_tuple=tuple(dict.values(entree[1]))
        add_ent_tuple=tuple(entreeload)
        #this unpacks and then merges the tuples
        merged_ent_tuples_prefilter=*ent_tuple,*add_ent_tuple
        entree_duplicate_filter=set(merged_ent_tuples_prefilter)
        merged_ent_tuples=tuple(entree_duplicate_filter)
        #this enumerates the tuple variable items
        entreeloadcount=[]
        for count, ele in enumerate(merged_ent_tuples,1):
            entreeloadcount.append(count)
        #converts and zips the tuple and list into a dictionary
        entdic=dict(zip(entreeloadcount,merged_ent_tuples))
        #patches the old dictionary with the updated one
        entree.update({1:entdic})
        entoffload=list(add_ent_tuple)
        entoffload=set(entoffload)
        entoffload=list(entoffload)
        writeiter=len(entoffload)
        while writeiter!=0:
            mae.writelines(str(entoffload[-1]))
            mae.write(",")
            entoffload.pop(-1)
            writeiter-=1
    mae.close()
    return entree

def add_new_side(side, sideload,addnwside):
    with open("addedsides.py","r")as mas:
        sidespreload = str(mas.readlines())
        # these 3 functions clean up the text
        sidespreload = sidespreload.strip("""['""")
        sidesinload = list(sidespreload.split(","))
        sidesinload.pop(-1)
        # strictly text cleanup ^
        sidesinload.append(addnwside)
        sideload = sidesinload
        mas.close

        mas = open("addedsides.py", 'w')
        side_tuple = tuple(dict.values(side[1]))
        add_side_tuple = tuple(sideload)
        # this unpacks and then merges the tuples
        merged_side_tuples_prefilter = *side_tuple, *add_side_tuple
        side_duplicate_filter = set(merged_side_tuples_prefilter)
        merged_side_tuples = tuple(side_duplicate_filter)
        # this enumerates the tuple variable items
        sideloadcount = []
        for count, ele in enumerate(merged_side_tuples, 1):
            sideloadcount.append(count)
        # converts and zips the tuple and list into a dictionary
        sidedic = dict(zip(sideloadcount, merged_side_tuples))
        # patches the old dictionary with the updated one
        side.update({1: sidedic})
        sideoffload = list(add_side_tuple)
        sideoffload = set(sideoffload)
        sideoffload = list(sideoffload)
        writeiter = len(sideoffload)
        while writeiter != 0:
            mas.writelines(str(sideoffload[-1]))
            mas.write(",")
            sideoffload.pop(-1)
            writeiter -= 1

    mas.close()
    return side
def add_new_brd(side, breadload,addnwbrd):
    with open("addedbread.py", 'r') as mab:
        brdpreload = str(mab.readlines())
        # these 3 functions clean up the text
        brdpreload = brdpreload.strip("""['""")
        brdinload = list(brdpreload.split(","))
        brdinload.pop(-1)
        # strictly text cleanup ^
        brdinload.append(addnwbrd)
        breadload = brdinload
        mab.close

        mab = open("addedbread.py", 'w')
        brd_tuple = tuple(dict.values(side["bread"]))
        add_brd_tuple = tuple(breadload)
        # this unpacks and then merges the tuples
        merged_brd_tuples_prefilter = *brd_tuple, *add_brd_tuple
        brd_duplicate_filter = set(merged_brd_tuples_prefilter)
        merged_brd_tuples = tuple(brd_duplicate_filter)
        # this enumerates the tuple variable items
        brdloadcount = []
        for count, ele in enumerate(merged_brd_tuples, 1):
            brdloadcount.append(count)
        # converts and zips the tuple and list into a dictionary
        brddic = dict(zip(brdloadcount, merged_brd_tuples))
        # patches the old dictionary with the updated one
        side.update({"bread": brddic})
        brdoffload = list(add_brd_tuple)
        brdoffload = set(brdoffload)
        brdoffload = list(brdoffload)
        writeiter = len(brdoffload)
        while writeiter != 0:
            mab.writelines(str(brdoffload[-1]))
            mab.write(",")
            brdoffload.pop(-1)
            writeiter -= 1
    mab.close()
    return side
def add_new_sld(side, saladload,addnwsld):
    with open("addedsalad.py", 'r') as masal:
        salpreload = str(masal.readlines())
        # these 3 functions clean up the text
        salpreload = salpreload.strip("""['""")
        salinload = list(salpreload.split(","))
        salinload.pop(-1)
        # strictly text cleanup ^
        salinload.append(addnwsld)
        saladload = salinload
        masal.close

        masal = open("addedsalad.py", 'w')
        sal_tuple = tuple(dict.values(salad))
        add_sal_tuple = tuple(saladload)
        # this unpacks and then merges the tuples
        merged_sal_tuples_prefilter = *sal_tuple, *add_sal_tuple
        sal_duplicate_filter = set(merged_sal_tuples_prefilter)
        merged_sal_tuples = tuple(sal_duplicate_filter)
        # this enumerates the tuple variable items
        salloadcount = []
        for count, ele in enumerate(merged_sal_tuples, 1):
            salloadcount.append(count)
        # converts and zips the tuple and list into a dictionary
        saldic = dict(zip(salloadcount, merged_sal_tuples))
        # patches the old dictionary with the updated one
        salad.update(saldic)
        saloffload = list(add_sal_tuple)
        saloffload = set(saloffload)
        saloffload = list(saloffload)
        writeiter = len(saloffload)
        while writeiter != 0:
            masal.writelines(str(saloffload[-1]))
            masal.write(",")
            saloffload.pop(-1)
            writeiter -= 1
    masal.close()
    return salad
def add_new_des(dessertload,addnwdes,dessert):
    with open("addeddesserts.py",'r')as mad:
        despreload = str(mad.readlines())
        # these 3 functions clean up the text
        despreload = despreload.strip("""['""")
        desinload = list(despreload.split(","))
        desinload.pop(-1)
        # strictly text cleanup ^
        desinload.append(addnwdes)
        dessertload = desinload
        mad.close()

        mad = open("addeddesserts.py", 'w')
        des_tuple = tuple(dict.values(dessert))
        add_des_tuple = tuple(dessertload)
        # this unpacks and then merges the tuples
        merged_des_tuples_prefilter = *des_tuple, *add_des_tuple
        des_duplicate_filter = set(merged_des_tuples_prefilter)
        merged_des_tuples = tuple(des_duplicate_filter)
        # this enumerates the tuple variable items
        desloadcount = []
        for count, ele in enumerate(merged_des_tuples, 1):
            desloadcount.append(count)
        # converts and zips the tuple and list into a dictionary
        desdic = dict(zip(desloadcount, merged_des_tuples))
        # patches the old dictionary with the updated one
        dessert.update(desdic)
        desoffload = list(add_des_tuple)
        desoffload = set(desoffload)
        desoffload = list(desoffload)
        writeiter = len(desoffload)
        while writeiter != 0:
            mad.writelines(str(desoffload[-1]))
            mad.write(",")
            desoffload.pop(-1)
            writeiter -= 1
    mad.close()
    return dessert
def add_new_brk(breakfastload,addnwbrk,entree):
    with open("addedbreakfast.py",'r')as mabreak:
        brkpreload = str(mabreak.readlines())
        # these 3 functions clean up the text
        brkpreload = brkpreload.strip("""['""")
        brkinload = list(brkpreload.split(","))
        brkinload.pop(-1)
        # strictly text cleanup ^
        brkinload.append(addnwbrk)
        breakfastload = brkinload
        mabreak.close()

        mabreak = open("addedbreakfast.py", "w")
        brk_tuple=tuple(dict.values(entree[10]))
        add_brk_tuple=tuple(breakfastload)
        #this unpacks and then merges the tuples
        merged_brk_tuples_prefilter=*brk_tuple,*add_brk_tuple
        brk_duplicate_filter=set(merged_brk_tuples_prefilter)
        merged_brk_tuples=tuple(brk_duplicate_filter)
        #this enumerates the tuple variable items
        brkloadcount=[]
        for count, ele in enumerate(merged_brk_tuples,1):
            brkloadcount.append(count)
        #converts and zips the tuple and list into a dictionary
        brkdic=dict(zip(brkloadcount,merged_brk_tuples))
        #patches the old dictionary with the updated one
        entree.update({10:brkdic})
        brkoffload=list(add_brk_tuple)
        brkoffload = set(brkoffload)
        brkoffload = list(brkoffload)
        writeiter=len(brkoffload)
        while writeiter!=0:
            mabreak.writelines(str(brkoffload[-1]))
            mabreak.write(",")
            brkoffload.pop(-1)
            writeiter-=1
    mabreak.close()
    return entree
def add_new_mex(mexicanfdload,addnwmex,entree):
    with open("addedmexicanfd.py",'r')as mamex:
        mexpreload = str(mamex.readlines())
        # these 3 functions clean up the text
        mexpreload = mexpreload.strip("""['""")
        mexinload = list(mexpreload.split(","))
        mexinload.pop(-1)
        # strictly text cleanup ^
        mexinload.append(addnwmex)
        mexicanfdload = mexinload
        mamex.close()

        mamex = open("addedmexicanfd.py", "w")
        mex_tuple=tuple(dict.values(entree[6]))
        add_mex_tuple=tuple(mexicanfdload)
        #this unpacks and then merges the tuples
        merged_mex_tuples_prefilter=*mex_tuple,*add_mex_tuple
        mex_duplicate_filter=set(merged_mex_tuples_prefilter)
        merged_mex_tuples=tuple(mex_duplicate_filter)
        #this enumerates the tuple variable items
        mexloadcount=[]
        for count, ele in enumerate(merged_mex_tuples,1):
            mexloadcount.append(count)
        #converts and zips the tuple and list into a dictionary
        mexdic=dict(zip(mexloadcount,merged_mex_tuples))
        #patches the old dictionary with the updated one
        entree.update({6:mexdic})
        mexoffload=list(add_mex_tuple)
        mexoffload = set(mexoffload)
        mexoffload = list(mexoffload)
        writeiter=len(mexoffload)
        while writeiter!=0:
            mamex.writelines(str(mexoffload[-1]))
            mamex.write(",")
            mexoffload.pop(-1)
            writeiter-=1
    mamex.close()
    return entree
def add_new_fsh(fishload, addnwfsh, entree):
    with open("addedfish.py",'r')as mafish:
        fshpreload = str(mafish.readlines())
        # these 3 functions clean up the text
        fshpreload = fshpreload.strip("""['""")
        fshinload = list(fshpreload.split(","))
        fshinload.pop(-1)
        # strictly text cleanup ^
        fshinload.append(addnwfsh)
        fishload = fshinload
        mafish.close()

        mafish = open("addedfish.py", "w")
        fsh_tuple = tuple(dict.values(entree[7]))
        add_fsh_tuple = tuple(fishload)
        # this unpacks and then merges the tuples
        merged_fsh_tuples_prefilter = *fsh_tuple, *add_fsh_tuple
        fsh_duplicate_filter = set(merged_fsh_tuples_prefilter)
        merged_fsh_tuples = tuple(fsh_duplicate_filter)
        # this enumerates the tuple variable items
        fshloadcount = []
        for count, ele in enumerate(merged_fsh_tuples, 1):
            fshloadcount.append(count)
        # converts and zips the tuple and list into a dictionary
        fshdic = dict(zip(fshloadcount, merged_fsh_tuples))
        # patches the old dictionary with the updated one
        entree.update({7: fshdic})
        fshoffload = list(add_fsh_tuple)
        writeiter = len(fshoffload)
        fshoffload = set(fshoffload)
        fshoffload = list(fshoffload)
        while writeiter != 0:
            mafish.writelines(str(fshoffload[-1]))
            mafish.write(",")
            fshoffload.pop(-1)
            writeiter -= 1
    mafish.close()
    return entree

def build_dictionary():
    global scraper_m_filter
    global ent_rec_comp
    global side_rec_comp
    global des_rec_comp
    global salad_rec_comp
    global brk_rec_comp
    global mex_rec_comp
    global fsh_rec_comp
    global brd_rec_comp
    scraper_m_filter = []
    ent_rec_comp=[]
    side_rec_comp=[]
    des_rec_comp=[]
    salad_rec_comp=[]
    brk_rec_comp=[]
    mex_rec_comp=[]
    fsh_rec_comp=[]
    brd_rec_comp=[]
    with open("addedentree.py", "r") as mae:
        if scraped_entree != 0:
            scraped_entree_iter = len(scraped_entree)
            while scraped_entree_iter != 0:
                print(scraped_entree)
                entreeload.append(scraped_entree[-1])
                scraped_entree.pop(-1)
                scraped_entree_iter -= 1
        entpreload = str(mae.readlines())
        # these 3 functions clean up the text
        entpreload=entpreload.replace('\\' , "")
        #entpreload=entpreload.replace(" ","")
        entpreload = entpreload.strip("""['""")
        entinload = list(entpreload.split(","))
        entinload.pop(-1)
        # strictly text cleanup ^
        entreeload.extend(entinload)
        mae.close()
        mae = open("addedentree.py", "w")
        ent_tuple = tuple(dict.values(entree[1]))
        add_ent_tuple = tuple(entreeload)
        # this unpacks and then merges the tuples
        merged_ent_tuples_prefilter = *ent_tuple, *add_ent_tuple
        entree_duplicate_filter = set(merged_ent_tuples_prefilter)
        merged_ent_tuples = tuple(entree_duplicate_filter)
        # this line builds the master filter for the scraper to compare
        scraper_m_filter.extend(list(merged_ent_tuples))
        # this builds a list to help recipe builder
        ent_rec_comp.extend(list(merged_ent_tuples))
        # this enumerates the tuple variable items
        entreeloadcount = []
        for count, ele in enumerate(merged_ent_tuples, 1):
            entreeloadcount.append(count)
        # converts and zips the tuple and list into a dictionary
        entdic = dict(zip(entreeloadcount, merged_ent_tuples))
        # patches the old dictionary with the updated one
        entree.update({1: entdic})
        entoffload = list(add_ent_tuple)
        entoffload = set(entoffload)
        entoffload = list(entoffload)
        writeiter = len(entoffload)
        while writeiter != 0:
            entoffload[-1] = (entoffload[-1].strip('"'))
            mae.writelines(str(entoffload[-1]))
            mae.write(",")
            entoffload.pop(-1)
            writeiter -= 1
    mae.close()
    with open("addedsides.py", "r") as mas:
        if scraped_side != 0:
            scraped_side_iter = len(scraped_side)
            while scraped_side_iter != 0:
                print(scraped_side)
                sideload.append(scraped_side[-1])
                scraped_side.pop(-1)
                scraped_side_iter -= 1
        sidespreload = str(mas.readlines())
        sidespreload = sidespreload.replace('\\', "")
        # these 3 functions clean up the text
        sidespreload = sidespreload.strip("""['""")
        sidesinload = list(sidespreload.split(","))
        sidesinload.pop(-1)
        # strictly text cleanup ^
        sideload.extend(sidesinload)
        mas.close
        mas = open("addedsides.py", 'w')
        side_tuple = tuple(dict.values(side[1]))
        add_side_tuple = tuple(sideload)
        # this unpacks and then merges the tuples
        merged_side_tuples_prefilter = *side_tuple, *add_side_tuple
        side_duplicate_filter = set(merged_side_tuples_prefilter)
        merged_side_tuples = tuple(side_duplicate_filter)
        # this line builds the master filter for the scraper to compare
        scraper_m_filter.extend(list(merged_side_tuples))
        # this builds a list to help recipe builder
        side_rec_comp.extend(list(merged_side_tuples))
        # this enumerates the tuple variable items
        sideloadcount = []
        for count, ele in enumerate(merged_side_tuples, 1):
            sideloadcount.append(count)
        # converts and zips the tuple and list into a dictionary
        sidedic = dict(zip(sideloadcount, merged_side_tuples))
        # patches the old dictionary with the updated one
        side.update({1: sidedic})
        sideoffload = list(add_side_tuple)
        sideoffload = set(sideoffload)
        sideoffload = list(sideoffload)
        # this builds a list to help recipe builder
        writeiter = len(sideoffload)
        while writeiter != 0:
            sideoffload[-1]=str(sideoffload[-1])
            sideoffload[-1]=(sideoffload[-1].strip('"'))
            mas.writelines(str(sideoffload[-1]))
            mas.write(",")
            sideoffload.pop(-1)
            writeiter -= 1
        with open("addedbread.py", 'r') as mab:
            if scraped_bread != 0:
                scraped_brd_iter = len(scraped_bread)
                while scraped_brd_iter != 0:
                    print(scraped_bread)
                    breadload.append(scraped_bread[-1])
                    scraped_bread.pop(-1)
                    scraped_brd_iter -= 1
            brdpreload = str(mab.readlines())
            brdpreload = brdpreload.replace('\\', "")
            # these 3 functions clean up the text
            brdpreload = brdpreload.strip("""['""")
            brdinload = list(brdpreload.split(","))
            brdinload.pop(-1)
            # strictly text cleanup ^
            breadload.extend(brdinload)
            mab.close
            mab = open("addedbread.py", 'w')
            brd_tuple = tuple(dict.values(side["bread"]))
            add_brd_tuple = tuple(breadload)
            # this unpacks and then merges the tuples
            merged_brd_tuples_prefilter = *brd_tuple, *add_brd_tuple
            brd_duplicate_filter = set(merged_brd_tuples_prefilter)
            merged_brd_tuples = tuple(brd_duplicate_filter)
            # this line builds the master filter for the scraper to compare
            scraper_m_filter.extend(list(merged_brd_tuples))
            # this builds a list to help recipe builder
            brd_rec_comp.extend(list(merged_brd_tuples))
            # this enumerates the tuple variable items
            brdloadcount = []
            for count, ele in enumerate(merged_brd_tuples, 1):
                brdloadcount.append(count)
            # converts and zips the tuple and list into a dictionary
            brddic = dict(zip(brdloadcount, merged_brd_tuples))
            # patches the old dictionary with the updated one
            side.update({"bread": brddic})
            brdoffload = list(add_brd_tuple)
            brdoffload= set(brdoffload)
            brdoffload= list(brdoffload)
            brd_rec_comp.extend(brdoffload)
            writeiter = len(brdoffload)
            while writeiter != 0:
                brdoffload[-1] = (brdoffload[-1].strip('"'))
                mab.writelines(str(brdoffload[-1]))
                mab.write(",")
                brdoffload.pop(-1)
                writeiter -= 1
        mab.close()
    mas.close()
    with open("addedsalad.py", 'r') as masal:
        if scraped_salad != 0:
            scraped_sld_iter = len(scraped_salad)
            while scraped_sld_iter != 0:
                print(scraped_salad)
                saladload.append(scraped_salad[-1])
                scraped_salad.pop(-1)
                scraped_sld_iter -= 1
        salpreload = str(masal.readlines())
        salpreload = salpreload.replace('\\', "")
        # these 3 functions clean up the text
        salpreload = salpreload.strip("""['""")
        salinload = list(salpreload.split(","))
        salinload.pop(-1)
        # strictly text cleanup ^
        saladload.extend(salinload)
        masal.close
        masal = open("addedsalad.py", 'w')
        sal_tuple = tuple(dict.values(salad))
        add_sal_tuple = tuple(saladload)
        # this unpacks and then merges the tuples
        merged_sal_tuples_prefilter = *sal_tuple, *add_sal_tuple
        sal_duplicate_filter = set(merged_sal_tuples_prefilter)
        merged_sal_tuples = tuple(sal_duplicate_filter)
        # this line builds the master filter for the scraper to compare
        scraper_m_filter.extend(list(merged_sal_tuples))
        # this builds a list to help recipe builder
        salad_rec_comp.extend(list(merged_sal_tuples))
        # this enumerates the tuple variable items
        salloadcount = []
        for count, ele in enumerate(merged_sal_tuples, 1):
            salloadcount.append(count)
        # converts and zips the tuple and list into a dictionary
        saldic = dict(zip(salloadcount, merged_sal_tuples))
        # patches the old dictionary with the updated one
        salad.update(saldic)
        saloffload = list(add_sal_tuple)
        saloffload = set(saloffload)
        saloffload = list(saloffload)
        # this builds a list to help recipe builder
        salad_rec_comp.extend(saloffload)
        writeiter = len(saloffload)
        while writeiter != 0:
            saloffload[-1] = (saloffload[-1].strip('"'))
            masal.writelines(str(saloffload[-1]))
            masal.write(",")
            saloffload.pop(-1)
            writeiter -= 1
    masal.close()
    with open("addeddesserts.py", 'r') as mad:
        if scraped_dessert != 0:
            scraped_des_iter = len(scraped_dessert)
            while scraped_des_iter != 0:
                print(scraped_dessert)
                dessertload.append(scraped_dessert[-1])
                scraped_dessert.pop(-1)
                scraped_des_iter -= 1
        despreload = str(mad.readlines())
        despreload = despreload.replace('\\', "")
        # these 3 functions clean up the text
        despreload = despreload.strip("""['""")
        desinload = list(despreload.split(","))
        desinload.pop(-1)
        # strictly text cleanup ^
        dessertload.extend(desinload)
        mad.close()
        mad = open("addeddesserts.py", 'w')
        des_tuple = tuple(dict.values(dessert))
        add_des_tuple = tuple(dessertload)
        # this unpacks and then merges the tuples
        merged_des_tuples_prefilter = *des_tuple, *add_des_tuple
        des_duplicate_filter = set(merged_des_tuples_prefilter)
        merged_des_tuples = tuple(des_duplicate_filter)
        # this line builds the master filter for the scraper to compare
        scraper_m_filter.extend(list(merged_des_tuples))
        # this builds a list to help recipe builder
        des_rec_comp.extend(list(merged_des_tuples))
        # this enumerates the tuple variable items
        desloadcount = []
        for count, ele in enumerate(merged_des_tuples, 1):
            desloadcount.append(count)
        # converts and zips the tuple and list into a dictionary
        desdic = dict(zip(desloadcount, merged_des_tuples))
        # patches the old dictionary with the updated one
        dessert.update(desdic)
        desoffload = list(add_des_tuple)
        desoffload = set(desoffload)
        desoffload = list(desoffload)
        # this builds a list to help recipe builder
        des_rec_comp.extend(desoffload)
        writeiter = len(desoffload)
        while writeiter != 0:
            desoffload[-1] = (desoffload[-1].strip('"'))
            mad.writelines(str(desoffload[-1]))
            mad.write(",")
            desoffload.pop(-1)
            writeiter -= 1
    mad.close()
    with open("addedbreakfast.py", 'r') as mabreak:
        if scraped_breakfast != 0:
            scraped_brk_iter = len(scraped_breakfast)
            while scraped_brk_iter != 0:
                print(scraped_breakfast)
                breakfastload.append(scraped_breakfast[-1])
                scraped_breakfast.pop(-1)
                scraped_brk_iter -= 1
        brkpreload = str(mabreak.readlines())
        brkpreload = brkpreload.replace('\\', "")
        # these 3 functions clean up the text
        brkpreload = brkpreload.strip("""['""")
        brkinload = list(brkpreload.split(","))
        brkinload.pop(-1)
        # strictly text cleanup ^
        breakfastload.extend(brkinload)
        mabreak.close()
        mabreak = open("addedbreakfast.py", "w")
        brk_tuple = tuple(dict.values(entree[10]))
        add_brk_tuple = tuple(breakfastload)
        # this unpacks and then merges the tuples
        merged_brk_tuples_prefilter = *brk_tuple, *add_brk_tuple
        brk_duplicate_filter = set(merged_brk_tuples_prefilter)
        merged_brk_tuples = tuple(brk_duplicate_filter)
        # this line builds the master filter for the scraper to compare
        scraper_m_filter.extend(list(merged_brk_tuples))
        # this builds a list to help recipe builder
        brk_rec_comp.extend(merged_brk_tuples)
        # this enumerates the tuple variable items
        brkloadcount = []
        for count, ele in enumerate(merged_brk_tuples, 1):
            brkloadcount.append(count)
        # converts and zips the tuple and list into a dictionary
        brkdic = dict(zip(brkloadcount, merged_brk_tuples))
        # patches the old dictionary with the updated one
        entree.update({10: brkdic})
        brkoffload = list(add_brk_tuple)
        brkoffload = set(brkoffload)
        brkoffload = list(brkoffload)
        writeiter = len(brkoffload)
        while writeiter != 0:
            brkoffload[-1] = (brkoffload[-1].strip('"'))
            mabreak.writelines(str(brkoffload[-1]))
            mabreak.write(",")
            brkoffload.pop(-1)
            writeiter -= 1
    mabreak.close()
    with open("addedmexicanfd.py", 'r') as mamex:
        if scraped_mexicanfd != 0:
            scraped_mx_iter = len(scraped_mexicanfd)
            while scraped_mx_iter != 0:
                print(scraped_mexicanfd)
                mexicanfdload.append(scraped_mexicanfd[-1])
                scraped_mexicanfd.pop(-1)
                scraped_mx_iter -= 1
        mexpreload = str(mamex.readlines())
        mexpreload = mexpreload.replace('\\', "")
        # these 3 functions clean up the text
        mexpreload = mexpreload.strip("""['""")
        mexinload = list(mexpreload.split(","))
        mexinload.pop(-1)
        # strictly text cleanup ^
        mexicanfdload.extend(mexinload)
        mamex.close()
        mamex = open("addedmexicanfd.py", "w")
        mex_tuple = tuple(dict.values(entree[6]))
        add_mex_tuple = tuple(mexicanfdload)
        # this unpacks and then merges the tuples
        merged_mex_tuples_prefilter = *mex_tuple, *add_mex_tuple
        mex_duplicate_filter = set(merged_mex_tuples_prefilter)
        merged_mex_tuples = tuple(mex_duplicate_filter)
        # this line builds the master filter for the scraper to compare
        scraper_m_filter.extend(list(merged_mex_tuples))
        # this builds a list to help recipe builder
        mex_rec_comp.extend(list(merged_mex_tuples))
        # this enumerates the tuple variable items
        mexloadcount = []
        for count, ele in enumerate(merged_mex_tuples, 1):
            mexloadcount.append(count)
        # converts and zips the tuple and list into a dictionary
        mexdic = dict(zip(mexloadcount, merged_mex_tuples))
        # patches the old dictionary with the updated one
        entree.update({6: mexdic})
        mexoffload = list(add_mex_tuple)
        mexoffload = set(mexoffload)
        mexoffload = list(mexoffload)
        # this builds a list to help recipe builder
        mex_rec_comp.extend(mexoffload)
        writeiter = len(mexoffload)
        while writeiter != 0:
            mexoffload[-1] = (mexoffload[-1].strip('"'))
            mamex.writelines(str(mexoffload[-1]))
            mamex.write(",")
            mexoffload.pop(-1)
            writeiter -= 1
    mamex.close()
    with open("addedfish.py", 'r') as mafish:
        if scraped_fish != 0:
            scraped_fsh_iter = len(scraped_fish)
            while scraped_fsh_iter != 0:
                print(scraped_fish)
                fishload.append(scraped_fish[-1])
                scraped_fish.pop(-1)
                scraped_fsh_iter -= 1
        fshpreload = str(mafish.readlines())
        fshpreload = fshpreload.replace('\\', "")
        # these 3 functions clean up the text
        fshpreload = fshpreload.strip("""['""")
        fshinload = list(fshpreload.split(","))
        fshinload.pop(-1)
        # strictly text cleanup ^
        fishload.extend(fshinload)
        mafish.close()
        mafish = open("addedfish.py", "w")
        fsh_tuple = tuple(dict.values(entree[7]))
        add_fsh_tuple = tuple(fishload)
        # this unpacks and then merges the tuples
        merged_fsh_tuples_prefilter = *fsh_tuple, *add_fsh_tuple
        fsh_duplicate_filter = set(merged_fsh_tuples_prefilter)
        merged_fsh_tuples = tuple(fsh_duplicate_filter)
        # this line builds the master filter for the scraper to compare
        scraper_m_filter.extend(list(merged_fsh_tuples))
        # this builds a list to help recipe builder
        fsh_rec_comp.extend(list(merged_fsh_tuples))
        # this enumerates the tuple variable items
        fshloadcount = []
        for count, ele in enumerate(merged_fsh_tuples, 1):
            fshloadcount.append(count)
        # converts and zips the tuple and list into a dictionary
        fshdic = dict(zip(fshloadcount, merged_fsh_tuples))
        print(scraper_m_filter)

        # patches the old dictionary with the updated one
        entree.update({7: fshdic})
        fshoffload = list(add_fsh_tuple)
        fshoffload = set(fshoffload)
        fshoffload = list(fshoffload)
        # this builds a list to help recipe builder
        fsh_rec_comp.extend(fshoffload)
        writeiter = len(fshoffload)
        while writeiter != 0:
            fshoffload[-1] = (fshoffload[-1].strip('"'))
            mafish.writelines(str(fshoffload[-1]))
            mafish.write(",")
            fshoffload.pop(-1)
            writeiter -= 1
    mafish.close()
    print(ent_rec_comp)
    return  (scraper_m_filter,ent_rec_comp,side_rec_comp,brd_rec_comp,brk_rec_comp,
             salad_rec_comp,mex_rec_comp,fsh_rec_comp,des_rec_comp)








def mondaybreak(sidecount, monbreak1, monbreak2, monbreak3, monbreak4, monbreak5, monbreak6):
    while sidecount > 0:
        dictlength = (len(entree[10]))
        monbreak1.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        monbreak2.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        monbreak3.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        monbreak4.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        monbreak5.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        monbreak6.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        print(monbreak1)
        sidecount -= 1
        if sidecount == 0:
            # recipe list handling
            every_gen_breakfast.extend(monbreak1)
            every_gen_breakfast.extend(monbreak2)
            every_gen_breakfast.extend(monbreak3)
            every_gen_breakfast.extend(monbreak4)
            every_gen_breakfast.extend(monbreak5)
            every_gen_breakfast.extend(monbreak6)
            return monbreak1, monbreak2, monbreak3, monbreak4, monbreak5, monbreak6


def mondaylunch(sidecount, ent, monlunch1, monlunch2, monlunch3, monlunch4, monlunch5, monlunch6):
    while ent > 0:
        dict_select = 1
        dictlength = (len(entree[dict_select]))
        monlunch1.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset1 = set(monlunch1)
        if len(monlunch1) != len(myset1):
            mondaylunch(sidecount, ent, monlunch1, monlunch2, monlunch3, monlunch4, monlunch5, monlunch6)
        monlunch2.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset2 = set(monlunch2)
        if len(monlunch2) != len(myset2):
            mondaylunch(sidecount, ent, monlunch1, monlunch2, monlunch3, monlunch4, monlunch5, monlunch6)
        monlunch3.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset3 = set(monlunch3)
        if len(monlunch3) != len(myset3):
            mondaylunch(sidecount, ent, monlunch1, monlunch2, monlunch3, monlunch4, monlunch5, monlunch6)
        monlunch4.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset4 = set(monlunch4)
        if len(monlunch4) != len(myset4):
            mondaylunch(sidecount, ent, monlunch1, monlunch2, monlunch3, monlunch4, monlunch5, monlunch6)
        monlunch5.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset5 = set(monlunch5)
        if len(monlunch5) != len(myset5):
            mondaylunch(sidecount, ent, monlunch1, monlunch2, monlunch3, monlunch4, monlunch5, monlunch6)
        monlunch6.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset6 = set(monlunch6)
        if len(monlunch6) != len(myset6):
            mondaylunch(sidecount, ent, monlunch1, monlunch2, monlunch3, monlunch4, monlunch5, monlunch6)

        ent -= 1
        if ent == 0:




            while sidecount > 0:
                dict_select = 1
                dictlength = (len(side[dict_select]))
                monlunch1.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset1 = set(monlunch1)
                if len(monlunch1) != len(myset1):
                    mondaylunch(sidecount, ent, monlunch1, monlunch2, monlunch3, monlunch4, monlunch5, monlunch6)
                monlunch2.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset2 = set(monlunch2)
                if len(monlunch2) != len(myset2):
                    mondaylunch(sidecount, ent, monlunch1, monlunch2, monlunch3, monlunch4, monlunch5, monlunch6)
                monlunch3.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset3 = set(monlunch3)
                if len(monlunch3) != len(myset3):
                    mondaylunch(sidecount, ent, monlunch1, monlunch2, monlunch3, monlunch4, monlunch5, monlunch6)
                monlunch4.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset4 = set(monlunch4)
                if len(monlunch4) != len(myset4):
                    mondaylunch(sidecount, ent, monlunch1, monlunch2, monlunch3, monlunch4, monlunch5, monlunch6)
                monlunch5.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset5 = set(monlunch5)
                if len(monlunch5) != len(myset5):
                    mondaylunch(sidecount, ent, monlunch1, monlunch2, monlunch3, monlunch4, monlunch5, monlunch6)
                monlunch6.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset6 = set(monlunch6)
                if len(monlunch6) != len(myset6):
                    mondaylunch(sidecount, ent, monlunch1, monlunch2, monlunch3, monlunch4, monlunch5, monlunch6)

                sidecount -= 1

                if sidecount == 0:

                    dictlength = (len(side["bread"]))
                    monlunch1.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    monlunch2.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    monlunch3.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    monlunch4.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    monlunch5.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    monlunch6.append(side.get("bread", {}).get(random.randint(1, dictlength)))

                    dictlength = (len(salad))
                    monlunch1.append("--Salad--")
                    monlunch2.append("--Salad--")
                    monlunch3.append("--Salad--")
                    monlunch4.append("--Salad--")
                    monlunch5.append("--Salad--")
                    monlunch6.append("--Salad--")
                    monlunch1.append(salad.get(random.randint(1, dictlength)))
                    monlunch2.append(salad.get(random.randint(1, dictlength)))
                    monlunch3.append(salad.get(random.randint(1, dictlength)))
                    monlunch4.append(salad.get(random.randint(1, dictlength)))
                    monlunch5.append(salad.get(random.randint(1, dictlength)))
                    monlunch6.append(salad.get(random.randint(1, dictlength)))

                    dictlength = (len(dessert))
                    monlunch1.append("--Dessert--")
                    monlunch2.append("--Dessert--")
                    monlunch3.append("--Dessert--")
                    monlunch4.append("--Dessert--")
                    monlunch5.append("--Dessert--")
                    monlunch6.append("--Dessert--")
                    monlunch1.append(dessert.get(random.randint(1, dictlength)))
                    monlunch2.append(dessert.get(random.randint(1, dictlength)))
                    monlunch3.append(dessert.get(random.randint(1, dictlength)))
                    monlunch4.append(dessert.get(random.randint(1, dictlength)))
                    monlunch5.append(dessert.get(random.randint(1, dictlength)))
                    monlunch6.append(dessert.get(random.randint(1, dictlength)))
                    # recipe list handling
                    every_gen_entree.extend(monlunch1)
                    every_gen_entree.extend(monlunch2)
                    every_gen_entree.extend(monlunch3)
                    every_gen_entree.extend(monlunch4)
                    every_gen_entree.extend(monlunch5)
                    every_gen_entree.extend(monlunch6)
                    # recipe list handling
                    every_gen_side.extend(monlunch1)
                    every_gen_side.extend(monlunch2)
                    every_gen_side.extend(monlunch3)
                    every_gen_side.extend(monlunch4)
                    every_gen_side.extend(monlunch5)
                    every_gen_side.extend(monlunch6)
                    # recipe list handling
                    every_gen_brd.extend(monlunch1)
                    every_gen_brd.extend(monlunch2)
                    every_gen_brd.extend(monlunch3)
                    every_gen_brd.extend(monlunch4)
                    every_gen_brd.extend(monlunch5)
                    every_gen_brd.extend(monlunch6)
                    # recipe list handling
                    every_gen_salad.extend(monlunch1)
                    every_gen_salad.extend(monlunch2)
                    every_gen_salad.extend(monlunch3)
                    every_gen_salad.extend(monlunch4)
                    every_gen_salad.extend(monlunch5)
                    every_gen_salad.extend(monlunch6)
                    # recipe list handling
                    every_gen_dessert.extend(monlunch1)
                    every_gen_dessert.extend(monlunch2)
                    every_gen_dessert.extend(monlunch3)
                    every_gen_dessert.extend(monlunch4)
                    every_gen_dessert.extend(monlunch5)
                    every_gen_dessert.extend(monlunch6)
                    return monlunch1, monlunch2, monlunch3, monlunch4, monlunch5, monlunch6


def mondaydinner(sidecount, ent, mondinner1, mondinner2, mondinner3, mondinner4, mondinner5, mondinner6):
    while ent > 0:
        dict_select = 1
        dictlength = (len(entree[dict_select]))
        mondinner1.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset1 = set(mondinner1)
        if len(mondinner1) != len(myset1):
            mondaydinner(sidecount, ent, mondinner1, mondinner2, mondinner3, mondinner4, mondinner5, mondinner6)
        mondinner2.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset2 = set(mondinner2)
        if len(mondinner2) != len(myset2):
            mondaydinner(sidecount, ent, mondinner1, mondinner2, mondinner3, mondinner4, mondinner5, mondinner6)
        mondinner3.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset3 = set(mondinner3)
        if len(mondinner3) != len(myset3):
            mondaydinner(sidecount, ent, mondinner1, mondinner2, mondinner3, mondinner4, mondinner5, mondinner6)
        mondinner4.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset4 = set(mondinner4)
        if len(mondinner4) != len(myset4):
            mondaydinner(sidecount, ent, mondinner1, mondinner2, mondinner3, mondinner4, mondinner5, mondinner6)
        mondinner5.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset5 = set(mondinner5)
        if len(mondinner5) != len(myset5):
            mondaydinner(sidecount, ent, mondinner1, mondinner2, mondinner3, mondinner4, mondinner5, mondinner6)
        mondinner6.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset6 = set(mondinner6)
        if len(mondinner6) != len(myset6):
            mondaydinner(sidecount, ent, mondinner1, mondinner2, mondinner3, mondinner4, mondinner5, mondinner6)

        ent -= 1
        if ent == 0:

            while sidecount > 0:
                dict_select = 1
                dictlength = (len(side[dict_select]))
                mondinner1.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset1 = set(mondinner1)
                if len(mondinner1) != len(myset1):
                    mondaydinner(sidecount, ent, mondinner1, mondinner2, mondinner3, mondinner4, mondinner5, mondinner6)
                mondinner2.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset2 = set(mondinner2)
                if len(mondinner2) != len(myset2):
                    mondaydinner(sidecount, ent, mondinner1, mondinner2, mondinner3, mondinner4, mondinner5, mondinner6)
                mondinner3.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset3 = set(mondinner3)
                if len(mondinner3) != len(myset3):
                    mondaydinner(sidecount, ent, mondinner1, mondinner2, mondinner3, mondinner4, mondinner5, mondinner6)
                mondinner4.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset4 = set(mondinner4)
                if len(mondinner4) != len(myset4):
                    mondaydinner(sidecount, ent, mondinner1, mondinner2, mondinner3, mondinner4, mondinner5, mondinner6)
                mondinner5.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset5 = set(mondinner5)
                if len(mondinner5) != len(myset5):
                    mondaydinner(sidecount, ent, mondinner1, mondinner2, mondinner3, mondinner4, mondinner5, mondinner6)
                mondinner6.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset6 = set(mondinner6)
                if len(mondinner6) != len(myset6):
                    mondaydinner(sidecount, ent, mondinner1, mondinner2, mondinner3, mondinner4, mondinner5, mondinner6)
                sidecount -= 1

                if sidecount == 0:
                    dictlength = (len(side["bread"]))
                    mondinner1.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    mondinner2.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    mondinner3.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    mondinner4.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    mondinner5.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    mondinner6.append(side.get("bread", {}).get(random.randint(1, dictlength)))

                    dictlength = (len(salad))
                    mondinner1.append("--Salad--")
                    mondinner2.append("--Salad--")
                    mondinner3.append("--Salad--")
                    mondinner4.append("--Salad--")
                    mondinner5.append("--Salad--")
                    mondinner6.append("--Salad--")
                    mondinner1.append(salad.get(random.randint(1, dictlength)))
                    mondinner2.append(salad.get(random.randint(1, dictlength)))
                    mondinner3.append(salad.get(random.randint(1, dictlength)))
                    mondinner4.append(salad.get(random.randint(1, dictlength)))
                    mondinner5.append(salad.get(random.randint(1, dictlength)))
                    mondinner6.append(salad.get(random.randint(1, dictlength)))
                    dictlength = (len(dessert))
                    mondinner1.append("--Dessert--")
                    mondinner2.append("--Dessert--")
                    mondinner3.append("--Dessert--")
                    mondinner4.append("--Dessert--")
                    mondinner5.append("--Dessert--")
                    mondinner6.append("--Dessert--")
                    mondinner1.append(dessert.get(random.randint(1, dictlength)))
                    mondinner2.append(dessert.get(random.randint(1, dictlength)))
                    mondinner3.append(dessert.get(random.randint(1, dictlength)))
                    mondinner4.append(dessert.get(random.randint(1, dictlength)))
                    mondinner5.append(dessert.get(random.randint(1, dictlength)))
                    mondinner6.append(dessert.get(random.randint(1, dictlength)))
                    # recipe list handling
                    every_gen_entree.extend(mondinner1)
                    every_gen_entree.extend(mondinner2)
                    every_gen_entree.extend(mondinner3)
                    every_gen_entree.extend(mondinner4)
                    every_gen_entree.extend(mondinner5)
                    every_gen_entree.extend(mondinner6)
                    # recipe list handling
                    every_gen_side.extend(mondinner1)
                    every_gen_side.extend(mondinner2)
                    every_gen_side.extend(mondinner3)
                    every_gen_side.extend(mondinner4)
                    every_gen_side.extend(mondinner5)
                    every_gen_side.extend(mondinner6)
                    # recipe list handling
                    every_gen_brd.extend(mondinner1)
                    every_gen_brd.extend(mondinner2)
                    every_gen_brd.extend(mondinner3)
                    every_gen_brd.extend(mondinner4)
                    every_gen_brd.extend(mondinner5)
                    every_gen_brd.extend(mondinner6)
                    # recipe list handling
                    every_gen_salad.extend(mondinner1)
                    every_gen_salad.extend(mondinner2)
                    every_gen_salad.extend(mondinner3)
                    every_gen_salad.extend(mondinner4)
                    every_gen_salad.extend(mondinner5)
                    every_gen_salad.extend(mondinner6)
                    # recipe list handling
                    every_gen_dessert.extend(mondinner1)
                    every_gen_dessert.extend(mondinner2)
                    every_gen_dessert.extend(mondinner3)
                    every_gen_dessert.extend(mondinner4)
                    every_gen_dessert.extend(mondinner5)
                    every_gen_dessert.extend(mondinner6)

                    return mondinner1, mondinner2, mondinner3, mondinner4, mondinner5, mondinner6


def tuesdaybreak(sidecount, tuebreak1, tuebreak2, tuebreak3, tuebreak4, tuebreak5, tuebreak6):
    while sidecount > 0:

        dictlength = (len(entree[10]))
        tuebreak1.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        tuebreak2.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        tuebreak3.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        tuebreak4.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        tuebreak5.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        tuebreak6.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        sidecount -= 1
        if sidecount == 0:
            # recipe list handling
            every_gen_breakfast.extend(tuebreak1)
            every_gen_breakfast.extend(tuebreak2)
            every_gen_breakfast.extend(tuebreak3)
            every_gen_breakfast.extend(tuebreak4)
            every_gen_breakfast.extend(tuebreak5)
            every_gen_breakfast.extend(tuebreak6)
            return tuebreak1, tuebreak2, tuebreak3, tuebreak4, tuebreak5, tuebreak6


def tuesdaylunch(sidecount, ent, tuelunch1, tuelunch2, tuelunch3, tuelunch4, tuelunch5, tuelunch6):
    while ent > 0:
        dict_select = 1
        dictlength = (len(entree[dict_select]))
        tuelunch1.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset1 = set(tuelunch1)
        if len(tuelunch1) != len(myset1):
            tuesdaylunch(sidecount, ent, tuelunch1, tuelunch2, tuelunch3, tuelunch4, tuelunch5, tuelunch6)
        tuelunch2.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset2 = set(tuelunch2)
        if len(tuelunch2) != len(myset2):
            tuesdaylunch(sidecount, ent, tuelunch1, tuelunch2, tuelunch3, tuelunch4, tuelunch5, tuelunch6)
        tuelunch3.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset3 = set(tuelunch3)
        if len(tuelunch3) != len(myset3):
            tuesdaylunch(sidecount, ent, tuelunch1, tuelunch2, tuelunch3, tuelunch4, tuelunch5, tuelunch6)
        tuelunch4.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset4 = set(tuelunch4)
        if len(tuelunch4) != len(myset4):
            tuesdaylunch(sidecount, ent, tuelunch1, tuelunch2, tuelunch3, tuelunch4, tuelunch5, tuelunch6)
        tuelunch5.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset5 = set(tuelunch5)
        if len(tuelunch5) != len(myset5):
            tuesdaylunch(sidecount, ent, tuelunch1, tuelunch2, tuelunch3, tuelunch4, tuelunch5, tuelunch6)
        tuelunch6.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset6 = set(tuelunch6)
        if len(tuelunch6) != len(myset6):
            tuesdaylunch(sidecount, ent, tuelunch1, tuelunch2, tuelunch3, tuelunch4, tuelunch5, tuelunch6)

        ent -= 1
        if ent == 0:

            while sidecount > 0:
                dict_select = 1
                dictlength = (len(side[dict_select]))
                tuelunch1.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset1 = set(tuelunch1)
                if len(tuelunch1) != len(myset1):
                    tuesdaylunch(sidecount, ent, tuelunch1, tuelunch2, tuelunch3, tuelunch4, tuelunch5, tuelunch6)
                tuelunch2.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset2 = set(tuelunch2)
                if len(tuelunch2) != len(myset2):
                    tuesdaylunch(sidecount, ent, tuelunch1, tuelunch2, tuelunch3, tuelunch4, tuelunch5, tuelunch6)
                tuelunch3.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset3 = set(tuelunch3)
                if len(tuelunch3) != len(myset3):
                    tuesdaylunch(sidecount, ent, tuelunch1, tuelunch2, tuelunch3, tuelunch4, tuelunch5, tuelunch6)
                tuelunch4.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset4 = set(tuelunch4)
                if len(tuelunch4) != len(myset4):
                    tuesdaylunch(sidecount, ent, tuelunch1, tuelunch2, tuelunch3, tuelunch4, tuelunch5, tuelunch6)
                tuelunch5.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset5 = set(tuelunch5)
                if len(tuelunch5) != len(myset5):
                    tuesdaylunch(sidecount, ent, tuelunch1, tuelunch2, tuelunch3, tuelunch4, tuelunch5, tuelunch6)
                tuelunch6.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset6 = set(tuelunch6)
                if len(tuelunch6) != len(myset6):
                    tuesdaylunch(sidecount, ent, tuelunch1, tuelunch2, tuelunch3, tuelunch4, tuelunch5, tuelunch6)
                sidecount -= 1

                if sidecount == 0:
                    dictlength = (len(side["bread"]))
                    tuelunch1.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    tuelunch2.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    tuelunch3.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    tuelunch4.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    tuelunch5.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    tuelunch6.append(side.get("bread", {}).get(random.randint(1, dictlength)))

                    dictlength = (len(salad))
                    tuelunch1.append("--Salad--")
                    tuelunch2.append("--Salad--")
                    tuelunch3.append("--Salad--")
                    tuelunch4.append("--Salad--")
                    tuelunch5.append("--Salad--")
                    tuelunch6.append("--Salad--")
                    tuelunch1.append(salad.get(random.randint(1, dictlength)))
                    tuelunch2.append(salad.get(random.randint(1, dictlength)))
                    tuelunch3.append(salad.get(random.randint(1, dictlength)))
                    tuelunch4.append(salad.get(random.randint(1, dictlength)))
                    tuelunch5.append(salad.get(random.randint(1, dictlength)))
                    tuelunch6.append(salad.get(random.randint(1, dictlength)))
                    dictlength = (len(dessert))
                    tuelunch1.append("--Dessert--")
                    tuelunch2.append("--Dessert--")
                    tuelunch3.append("--Dessert--")
                    tuelunch4.append("--Dessert--")
                    tuelunch5.append("--Dessert--")
                    tuelunch6.append("--Dessert--")
                    tuelunch1.append(dessert.get(random.randint(1, dictlength)))
                    tuelunch2.append(dessert.get(random.randint(1, dictlength)))
                    tuelunch3.append(dessert.get(random.randint(1, dictlength)))
                    tuelunch4.append(dessert.get(random.randint(1, dictlength)))
                    tuelunch5.append(dessert.get(random.randint(1, dictlength)))
                    tuelunch6.append(dessert.get(random.randint(1, dictlength)))
                    # recipe list handling
                    every_gen_entree.extend(tuelunch1)
                    every_gen_entree.extend(tuelunch2)
                    every_gen_entree.extend(tuelunch3)
                    every_gen_entree.extend(tuelunch4)
                    every_gen_entree.extend(tuelunch5)
                    every_gen_entree.extend(tuelunch6)
                    # recipe list handling
                    every_gen_side.extend(tuelunch1)
                    every_gen_side.extend(tuelunch2)
                    every_gen_side.extend(tuelunch3)
                    every_gen_side.extend(tuelunch4)
                    every_gen_side.extend(tuelunch5)
                    every_gen_side.extend(tuelunch6)
                    # recipe list handling
                    every_gen_brd.extend(tuelunch1)
                    every_gen_brd.extend(tuelunch2)
                    every_gen_brd.extend(tuelunch3)
                    every_gen_brd.extend(tuelunch4)
                    every_gen_brd.extend(tuelunch5)
                    every_gen_brd.extend(tuelunch6)
                    # recipe list handling
                    every_gen_salad.extend(tuelunch1)
                    every_gen_salad.extend(tuelunch2)
                    every_gen_salad.extend(tuelunch3)
                    every_gen_salad.extend(tuelunch4)
                    every_gen_salad.extend(tuelunch5)
                    every_gen_salad.extend(tuelunch6)
                    # recipe list handling
                    every_gen_dessert.extend(tuelunch1)
                    every_gen_dessert.extend(tuelunch2)
                    every_gen_dessert.extend(tuelunch3)
                    every_gen_dessert.extend(tuelunch4)
                    every_gen_dessert.extend(tuelunch5)
                    every_gen_dessert.extend(tuelunch6)
                    return tuelunch1, tuelunch2, tuelunch3, tuelunch4, tuelunch5, tuelunch6


def tuesdaydinner(sidecount, ent, tuedinner1, tuedinner2, tuedinner3, tuedinner4, tuedinner5, tuedinner6):
    while ent > 0:
        dict_select = 1
        dictlength = (len(entree[dict_select]))
        tuedinner1.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset1 = set(tuedinner1)
        if len(tuedinner1) != len(myset1):
            tuesdaydinner(sidecount, ent, tuedinner1, tuedinner2, tuedinner3, tuedinner4, tuedinner5, tuedinner6)
        tuedinner2.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset2 = set(tuedinner2)
        if len(tuedinner2) != len(myset2):
            tuesdaydinner(sidecount, ent, tuedinner1, tuedinner2, tuedinner3, tuedinner4, tuedinner5, tuedinner6)
        tuedinner3.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset3 = set(tuedinner3)
        if len(tuedinner3) != len(myset3):
            tuesdaydinner(sidecount, ent, tuedinner1, tuedinner2, tuedinner3, tuedinner4, tuedinner5, tuedinner6)
        tuedinner4.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset4 = set(tuedinner4)
        if len(tuedinner4) != len(myset4):
            tuesdaydinner(sidecount, ent, tuedinner1, tuedinner2, tuedinner3, tuedinner4, tuedinner5, tuedinner6)
        tuedinner5.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset5 = set(tuedinner5)
        if len(tuedinner5) != len(myset5):
            tuesdaydinner(sidecount, ent, tuedinner1, tuedinner2, tuedinner3, tuedinner4, tuedinner5, tuedinner6)
        tuedinner6.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset6 = set(tuedinner6)
        if len(tuedinner6) != len(myset6):
            tuesdaydinner(sidecount, ent, tuedinner1, tuedinner2, tuedinner3, tuedinner4, tuedinner5, tuedinner6)
        ent -= 1
        if ent == 0:

            while sidecount > 0:
                dict_select = 1
                dictlength = (len(side[dict_select]))
                tuedinner1.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset1 = set(tuedinner1)
                if len(tuedinner1) != len(myset1):
                    tuesdaydinner(sidecount, ent, tuedinner1, tuedinner2, tuedinner3, tuedinner4, tuedinner5,
                                  tuedinner6)
                tuedinner2.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset2 = set(tuedinner2)
                if len(tuedinner2) != len(myset2):
                    tuesdaydinner(sidecount, ent, tuedinner1, tuedinner2, tuedinner3, tuedinner4, tuedinner5,
                                  tuedinner6)
                tuedinner3.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset3 = set(tuedinner3)
                if len(tuedinner3) != len(myset3):
                    tuesdaydinner(sidecount, ent, tuedinner1, tuedinner2, tuedinner3, tuedinner4, tuedinner5,
                                  tuedinner6)
                tuedinner4.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset4 = set(tuedinner4)
                if len(tuedinner4) != len(myset4):
                    tuesdaydinner(sidecount, ent, tuedinner1, tuedinner2, tuedinner3, tuedinner4, tuedinner5,
                                  tuedinner6)
                tuedinner5.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset5 = set(tuedinner5)
                if len(tuedinner5) != len(myset5):
                    tuesdaydinner(sidecount, ent, tuedinner1, tuedinner2, tuedinner3, tuedinner4, tuedinner5,
                                  tuedinner6)
                tuedinner6.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset6 = set(tuedinner6)
                if len(tuedinner6) != len(myset6):
                    tuesdaydinner(sidecount, ent, tuedinner1, tuedinner2, tuedinner3, tuedinner4, tuedinner5,
                                  tuedinner6)
                sidecount -= 1
                if sidecount == 0:
                    dictlength = (len(side["bread"]))
                    tuedinner1.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    tuedinner2.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    tuedinner3.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    tuedinner4.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    tuedinner5.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    tuedinner6.append(side.get("bread", {}).get(random.randint(1, dictlength)))

                    dictlength = (len(salad))
                    tuedinner1.append("--Salad--")
                    tuedinner2.append("--Salad--")
                    tuedinner3.append("--Salad--")
                    tuedinner4.append("--Salad--")
                    tuedinner5.append("--Salad--")
                    tuedinner6.append("--Salad--")
                    tuedinner1.append(salad.get(random.randint(1, dictlength)))
                    tuedinner2.append(salad.get(random.randint(1, dictlength)))
                    tuedinner3.append(salad.get(random.randint(1, dictlength)))
                    tuedinner4.append(salad.get(random.randint(1, dictlength)))
                    tuedinner5.append(salad.get(random.randint(1, dictlength)))
                    tuedinner6.append(salad.get(random.randint(1, dictlength)))
                    dictlength = (len(dessert))
                    tuedinner1.append("--Dessert--")
                    tuedinner2.append("--Dessert--")
                    tuedinner3.append("--Dessert--")
                    tuedinner4.append("--Dessert--")
                    tuedinner5.append("--Dessert--")
                    tuedinner6.append("--Dessert--")
                    tuedinner1.append(dessert.get(random.randint(1, dictlength)))
                    tuedinner2.append(dessert.get(random.randint(1, dictlength)))
                    tuedinner3.append(dessert.get(random.randint(1, dictlength)))
                    tuedinner4.append(dessert.get(random.randint(1, dictlength)))
                    tuedinner5.append(dessert.get(random.randint(1, dictlength)))
                    tuedinner6.append(dessert.get(random.randint(1, dictlength)))
                    # recipe list handling
                    every_gen_entree.extend(tuedinner1)
                    every_gen_entree.extend(tuedinner2)
                    every_gen_entree.extend(tuedinner3)
                    every_gen_entree.extend(tuedinner4)
                    every_gen_entree.extend(tuedinner5)
                    every_gen_entree.extend(tuedinner6)
                    # recipe list handling
                    every_gen_side.extend(tuedinner1)
                    every_gen_side.extend(tuedinner2)
                    every_gen_side.extend(tuedinner3)
                    every_gen_side.extend(tuedinner4)
                    every_gen_side.extend(tuedinner5)
                    every_gen_side.extend(tuedinner6)
                    # recipe list handling
                    every_gen_brd.extend(tuedinner1)
                    every_gen_brd.extend(tuedinner2)
                    every_gen_brd.extend(tuedinner3)
                    every_gen_brd.extend(tuedinner4)
                    every_gen_brd.extend(tuedinner5)
                    every_gen_brd.extend(tuedinner6)
                    # recipe list handling
                    every_gen_salad.extend(tuedinner1)
                    every_gen_salad.extend(tuedinner2)
                    every_gen_salad.extend(tuedinner3)
                    every_gen_salad.extend(tuedinner4)
                    every_gen_salad.extend(tuedinner5)
                    every_gen_salad.extend(tuedinner6)
                    # recipe list handling
                    every_gen_dessert.extend(tuedinner1)
                    every_gen_dessert.extend(tuedinner2)
                    every_gen_dessert.extend(tuedinner3)
                    every_gen_dessert.extend(tuedinner4)
                    every_gen_dessert.extend(tuedinner5)
                    every_gen_dessert.extend(tuedinner6)
                    return tuedinner1, tuedinner2, tuedinner3, tuedinner4, tuedinner5, tuedinner6


def wednesdaybreak(sidecount, wedbreak1, wedbreak2, wedbreak3, wedbreak4, wedbreak5, wedbreak6):
    while sidecount > 0:
        dictlength = (len(entree[10]))
        wedbreak1.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        wedbreak2.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        wedbreak3.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        wedbreak4.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        wedbreak5.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        wedbreak6.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        sidecount -= 1
        if sidecount == 0:
            # recipe list handling
            every_gen_breakfast.extend(wedbreak1)
            every_gen_breakfast.extend(wedbreak2)
            every_gen_breakfast.extend(wedbreak3)
            every_gen_breakfast.extend(wedbreak4)
            every_gen_breakfast.extend(wedbreak5)
            every_gen_breakfast.extend(wedbreak6)
            return wedbreak1, wedbreak2, wedbreak3, wedbreak4, wedbreak5, wedbreak6


def wednesdaylunch(sidecount, ent, wedlunch1, wedlunch2, wedlunch3, wedlunch4, wedlunch5, wedlunch6):
    while ent > 0:
        dict_select = 1
        dictlength = (len(entree[dict_select]))
        wedlunch1.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset1 = set(wedlunch1)
        if len(wedlunch1) != len(myset1):
            wednesdaylunch(sidecount, ent, wedlunch1, wedlunch2, wedlunch3, wedlunch4, wedlunch5, wedlunch6)
        wedlunch2.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset2 = set(wedlunch2)
        if len(wedlunch2) != len(myset2):
            wednesdaylunch(sidecount, ent, wedlunch1, wedlunch2, wedlunch3, wedlunch4, wedlunch5, wedlunch6)
        wedlunch3.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset3 = set(wedlunch3)
        if len(wedlunch3) != len(myset3):
            wednesdaylunch(sidecount, ent, wedlunch1, wedlunch2, wedlunch3, wedlunch4, wedlunch5, wedlunch6)
        wedlunch4.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset4 = set(wedlunch4)
        if len(wedlunch4) != len(myset4):
            wednesdaylunch(sidecount, ent, wedlunch1, wedlunch2, wedlunch3, wedlunch4, wedlunch5, wedlunch6)
        wedlunch5.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset5 = set(wedlunch5)
        if len(wedlunch5) != len(myset5):
            wednesdaylunch(sidecount, ent, wedlunch1, wedlunch2, wedlunch3, wedlunch4, wedlunch5, wedlunch6)
        wedlunch6.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset6 = set(wedlunch6)
        if len(wedlunch6) != len(myset6):
            wednesdaylunch(sidecount, ent, wedlunch1, wedlunch2, wedlunch3, wedlunch4, wedlunch5, wedlunch6)
        ent -= 1
        if ent == 0:

            while sidecount > 0:
                dict_select = 1
                dictlength = (len(side[dict_select]))
                wedlunch1.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset1 = set(wedlunch1)
                if len(wedlunch1) != len(myset1):
                    wednesdaylunch(sidecount, ent, wedlunch1, wedlunch2, wedlunch3, wedlunch4, wedlunch5, wedlunch6)
                wedlunch2.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset2 = set(wedlunch2)
                if len(wedlunch2) != len(myset2):
                    wednesdaylunch(sidecount, ent, wedlunch1, wedlunch2, wedlunch3, wedlunch4, wedlunch5, wedlunch6)
                wedlunch3.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset3 = set(wedlunch3)
                if len(wedlunch3) != len(myset3):
                    wednesdaylunch(sidecount, ent, wedlunch1, wedlunch2, wedlunch3, wedlunch4, wedlunch5, wedlunch6)
                wedlunch4.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset4 = set(wedlunch4)
                if len(wedlunch4) != len(myset4):
                    wednesdaylunch(sidecount, ent, wedlunch1, wedlunch2, wedlunch3, wedlunch4, wedlunch5, wedlunch6)
                wedlunch5.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset5 = set(wedlunch5)
                if len(wedlunch5) != len(myset5):
                    wednesdaylunch(sidecount, ent, wedlunch1, wedlunch2, wedlunch3, wedlunch4, wedlunch5, wedlunch6)
                wedlunch6.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset6 = set(wedlunch6)
                if len(wedlunch6) != len(myset6):
                    wednesdaylunch(sidecount, ent, wedlunch1, wedlunch2, wedlunch3, wedlunch4, wedlunch5, wedlunch6)
                sidecount -= 1

                if sidecount == 0:
                    dictlength = (len(side["bread"]))
                    wedlunch1.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    wedlunch2.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    wedlunch3.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    wedlunch4.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    wedlunch5.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    wedlunch6.append(side.get("bread", {}).get(random.randint(1, dictlength)))

                    dictlength = (len(salad))
                    wedlunch1.append("--Salad--")
                    wedlunch2.append("--Salad--")
                    wedlunch3.append("--Salad--")
                    wedlunch4.append("--Salad--")
                    wedlunch5.append("--Salad--")
                    wedlunch6.append("--Salad--")
                    wedlunch1.append(salad.get(random.randint(1, dictlength)))
                    wedlunch2.append(salad.get(random.randint(1, dictlength)))
                    wedlunch3.append(salad.get(random.randint(1, dictlength)))
                    wedlunch4.append(salad.get(random.randint(1, dictlength)))
                    wedlunch5.append(salad.get(random.randint(1, dictlength)))
                    wedlunch6.append(salad.get(random.randint(1, dictlength)))
                    dictlength = (len(dessert))
                    wedlunch1.append("--Dessert--")
                    wedlunch2.append("--Dessert--")
                    wedlunch3.append("--Dessert--")
                    wedlunch4.append("--Dessert--")
                    wedlunch5.append("--Dessert--")
                    wedlunch6.append("--Dessert--")
                    wedlunch1.append(dessert.get(random.randint(1, dictlength)))
                    wedlunch2.append(dessert.get(random.randint(1, dictlength)))
                    wedlunch3.append(dessert.get(random.randint(1, dictlength)))
                    wedlunch4.append(dessert.get(random.randint(1, dictlength)))
                    wedlunch5.append(dessert.get(random.randint(1, dictlength)))
                    wedlunch6.append(dessert.get(random.randint(1, dictlength)))
                    # recipe list handling
                    every_gen_entree.extend(wedlunch1)
                    every_gen_entree.extend(wedlunch2)
                    every_gen_entree.extend(wedlunch3)
                    every_gen_entree.extend(wedlunch4)
                    every_gen_entree.extend(wedlunch5)
                    every_gen_entree.extend(wedlunch6)
                    # recipe list handling
                    every_gen_side.extend(wedlunch1)
                    every_gen_side.extend(wedlunch2)
                    every_gen_side.extend(wedlunch3)
                    every_gen_side.extend(wedlunch4)
                    every_gen_side.extend(wedlunch5)
                    every_gen_side.extend(wedlunch6)
                    # recipe list handling
                    every_gen_brd.extend(wedlunch1)
                    every_gen_brd.extend(wedlunch2)
                    every_gen_brd.extend(wedlunch3)
                    every_gen_brd.extend(wedlunch4)
                    every_gen_brd.extend(wedlunch5)
                    every_gen_brd.extend(wedlunch6)
                    # recipe list handling
                    every_gen_salad.extend(wedlunch1)
                    every_gen_salad.extend(wedlunch2)
                    every_gen_salad.extend(wedlunch3)
                    every_gen_salad.extend(wedlunch4)
                    every_gen_salad.extend(wedlunch5)
                    every_gen_salad.extend(wedlunch6)
                    # recipe list handling
                    every_gen_dessert.extend(wedlunch1)
                    every_gen_dessert.extend(wedlunch2)
                    every_gen_dessert.extend(wedlunch3)
                    every_gen_dessert.extend(wedlunch4)
                    every_gen_dessert.extend(wedlunch5)
                    every_gen_dessert.extend(wedlunch6)
                    return wedlunch1, wedlunch2, wedlunch3, wedlunch4, wedlunch5, wedlunch6


def wednesdaydinner(sidecount, ent, weddinner1, weddinner2, weddinner3, weddinner4, weddinner5, weddinner6):
    while ent > 0:
        dict_select = 1
        dictlength = (len(entree[dict_select]))
        weddinner1.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset1 = set(weddinner1)
        if len(weddinner1) != len(myset1):
            wednesdaydinner(sidecount, ent, weddinner1, weddinner2, weddinner3, weddinner4, weddinner5, weddinner6)
        weddinner2.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset2 = set(weddinner2)
        if len(weddinner2) != len(myset2):
            wednesdaydinner(sidecount, ent, weddinner1, weddinner2, weddinner3, weddinner4, weddinner5, weddinner6)
        weddinner3.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset3 = set(weddinner3)
        if len(weddinner3) != len(myset3):
            wednesdaydinner(sidecount, ent, weddinner1, weddinner2, weddinner3, weddinner4, weddinner5, weddinner6)
        weddinner4.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset4 = set(weddinner4)
        if len(weddinner4) != len(myset4):
            wednesdaydinner(sidecount, ent, weddinner1, weddinner2, weddinner3, weddinner4, weddinner5, weddinner6)
        weddinner5.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset5 = set(weddinner5)
        if len(weddinner5) != len(myset5):
            wednesdaydinner(sidecount, ent, weddinner1, weddinner2, weddinner3, weddinner4, weddinner5, weddinner6)
        weddinner6.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset6 = set(weddinner6)
        if len(weddinner6) != len(myset6):
            wednesdaydinner(sidecount, ent, weddinner1, weddinner2, weddinner3, weddinner4, weddinner5, weddinner6)
        ent -= 1
        if ent == 0:

            while sidecount > 0:
                dict_select = 1
                dictlength = (len(side[dict_select]))
                weddinner1.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset1 = set(weddinner1)
                if len(weddinner1) != len(myset1):
                    wednesdaydinner(sidecount, ent, weddinner1, weddinner2, weddinner3, weddinner4, weddinner5,
                                    weddinner6)
                weddinner2.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset2 = set(weddinner2)
                if len(weddinner2) != len(myset2):
                    wednesdaydinner(sidecount, ent, weddinner1, weddinner2, weddinner3, weddinner4, weddinner5,
                                    weddinner6)
                weddinner3.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset3 = set(weddinner3)
                if len(weddinner3) != len(myset3):
                    wednesdaydinner(sidecount, ent, weddinner1, weddinner2, weddinner3, weddinner4, weddinner5,
                                    weddinner6)
                weddinner4.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset4 = set(weddinner4)
                if len(weddinner4) != len(myset4):
                    wednesdaydinner(sidecount, ent, weddinner1, weddinner2, weddinner3, weddinner4, weddinner5,
                                    weddinner6)
                weddinner5.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset5 = set(weddinner5)
                if len(weddinner5) != len(myset5):
                    wednesdaydinner(sidecount, ent, weddinner1, weddinner2, weddinner3, weddinner4, weddinner5,
                                    weddinner6)
                weddinner6.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset6 = set(weddinner6)
                if len(weddinner6) != len(myset6):
                    wednesdaydinner(sidecount, ent, weddinner1, weddinner2, weddinner3, weddinner4, weddinner5,
                                    weddinner6)
                sidecount -= 1

                if sidecount == 0:
                    dictlength = (len(side["bread"]))
                    weddinner1.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    weddinner2.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    weddinner3.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    weddinner4.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    weddinner5.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    weddinner6.append(side.get("bread", {}).get(random.randint(1, dictlength)))

                    dictlength = (len(salad))
                    weddinner1.append("--Salad--")
                    weddinner2.append("--Salad--")
                    weddinner3.append("--Salad--")
                    weddinner4.append("--Salad--")
                    weddinner5.append("--Salad--")
                    weddinner6.append("--Salad--")
                    weddinner1.append(salad.get(random.randint(1, dictlength)))
                    weddinner2.append(salad.get(random.randint(1, dictlength)))
                    weddinner3.append(salad.get(random.randint(1, dictlength)))
                    weddinner4.append(salad.get(random.randint(1, dictlength)))
                    weddinner5.append(salad.get(random.randint(1, dictlength)))
                    weddinner6.append(salad.get(random.randint(1, dictlength)))
                    dictlength = (len(dessert))
                    weddinner1.append("--Dessert--")
                    weddinner2.append("--Dessert--")
                    weddinner3.append("--Dessert--")
                    weddinner4.append("--Dessert--")
                    weddinner5.append("--Dessert--")
                    weddinner6.append("--Dessert--")
                    weddinner1.append(dessert.get(random.randint(1, dictlength)))
                    weddinner2.append(dessert.get(random.randint(1, dictlength)))
                    weddinner3.append(dessert.get(random.randint(1, dictlength)))
                    weddinner4.append(dessert.get(random.randint(1, dictlength)))
                    weddinner5.append(dessert.get(random.randint(1, dictlength)))
                    weddinner6.append(dessert.get(random.randint(1, dictlength)))
                    # recipe list handling
                    every_gen_entree.extend(weddinner1)
                    every_gen_entree.extend(weddinner2)
                    every_gen_entree.extend(weddinner3)
                    every_gen_entree.extend(weddinner4)
                    every_gen_entree.extend(weddinner5)
                    every_gen_entree.extend(weddinner6)
                    # recipe list handling
                    every_gen_side.extend(weddinner1)
                    every_gen_side.extend(weddinner2)
                    every_gen_side.extend(weddinner3)
                    every_gen_side.extend(weddinner4)
                    every_gen_side.extend(weddinner5)
                    every_gen_side.extend(weddinner6)
                    # recipe list handling
                    every_gen_brd.extend(weddinner1)
                    every_gen_brd.extend(weddinner2)
                    every_gen_brd.extend(weddinner3)
                    every_gen_brd.extend(weddinner4)
                    every_gen_brd.extend(weddinner5)
                    every_gen_brd.extend(weddinner6)
                    # recipe list handling
                    every_gen_salad.extend(weddinner1)
                    every_gen_salad.extend(weddinner2)
                    every_gen_salad.extend(weddinner3)
                    every_gen_salad.extend(weddinner4)
                    every_gen_salad.extend(weddinner5)
                    every_gen_salad.extend(weddinner6)
                    # recipe list handling
                    every_gen_dessert.extend(weddinner1)
                    every_gen_dessert.extend(weddinner2)
                    every_gen_dessert.extend(weddinner3)
                    every_gen_dessert.extend(weddinner4)
                    every_gen_dessert.extend(weddinner5)
                    every_gen_dessert.extend(weddinner6)
                    return weddinner1, weddinner2, weddinner3, weddinner4, weddinner5, weddinner6


def thursdaybreak(sidecount, thubreak1, thubreak2, thubreak3, thubreak4, thubreak5, thubreak6):
    while sidecount > 0:
        dictlength = (len(entree[10]))
        thubreak1.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        thubreak2.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        thubreak3.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        thubreak4.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        thubreak5.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        thubreak6.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        sidecount -= 1
        if sidecount == 0:
            # recipe list handling
            every_gen_breakfast.extend(thubreak1)
            every_gen_breakfast.extend(thubreak2)
            every_gen_breakfast.extend(thubreak3)
            every_gen_breakfast.extend(thubreak4)
            every_gen_breakfast.extend(thubreak5)
            every_gen_breakfast.extend(thubreak6)
            return thubreak1, thubreak2, thubreak3, thubreak4, thubreak5, thubreak6


def thursdaylunch(sidecount, ent, thulunch1, thulunch2, thulunch3, thulunch4, thulunch5, thulunch6):
    while ent > 0:
        dict_select = 1
        dictlength = (len(entree[dict_select]))
        thulunch1.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset1 = set(thulunch1)
        if len(thulunch1) != len(myset1):
            thursdaylunch(sidecount, ent, thulunch1, thulunch2, thulunch3, thulunch4, thulunch5, thulunch6)
        thulunch2.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset2 = set(thulunch2)
        if len(thulunch2) != len(myset2):
            thursdaylunch(sidecount, ent, thulunch1, thulunch2, thulunch3, thulunch4, thulunch5, thulunch6)
        thulunch3.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset3 = set(thulunch3)
        if len(thulunch3) != len(myset3):
            thursdaylunch(sidecount, ent, thulunch1, thulunch2, thulunch3, thulunch4, thulunch5, thulunch6)
        thulunch4.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset4 = set(thulunch4)
        if len(thulunch4) != len(myset4):
            thursdaylunch(sidecount, ent, thulunch1, thulunch2, thulunch3, thulunch4, thulunch5, thulunch6)
        thulunch5.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset5 = set(thulunch5)
        if len(thulunch5) != len(myset5):
            thursdaylunch(sidecount, ent, thulunch1, thulunch2, thulunch3, thulunch4, thulunch5, thulunch6)
        thulunch6.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset6 = set(thulunch6)
        if len(thulunch6) != len(myset6):
            thursdaylunch(sidecount, ent, thulunch1, thulunch2, thulunch3, thulunch4, thulunch5, thulunch6)
        ent -= 1
        if ent == 0:

            while sidecount > 0:
                dict_select = 1
                dictlength = (len(side[dict_select]))
                thulunch1.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset1 = set(thulunch1)
                if len(thulunch1) != len(myset1):
                    thursdaylunch(sidecount, ent, thulunch1, thulunch2, thulunch3, thulunch4, thulunch5, thulunch6)
                thulunch2.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset2 = set(thulunch2)
                if len(thulunch2) != len(myset2):
                    thursdaylunch(sidecount, ent, thulunch1, thulunch2, thulunch3, thulunch4, thulunch5, thulunch6)
                thulunch3.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset3 = set(thulunch3)
                if len(thulunch3) != len(myset3):
                    thursdaylunch(sidecount, ent, thulunch1, thulunch2, thulunch3, thulunch4, thulunch5, thulunch6)
                thulunch4.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset4 = set(thulunch4)
                if len(thulunch4) != len(myset4):
                    thursdaylunch(sidecount, ent, thulunch1, thulunch2, thulunch3, thulunch4, thulunch5, thulunch6)
                thulunch5.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset5 = set(thulunch5)
                if len(thulunch5) != len(myset5):
                    thursdaylunch(sidecount, ent, thulunch1, thulunch2, thulunch3, thulunch4, thulunch5, thulunch6)
                thulunch6.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset6 = set(thulunch6)
                if len(thulunch6) != len(myset6):
                    thursdaylunch(sidecount, ent, thulunch1, thulunch2, thulunch3, thulunch4, thulunch5, thulunch6)
                sidecount -= 1

                if sidecount == 0:
                    dictlength = (len(side["bread"]))
                    thulunch1.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    thulunch2.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    thulunch3.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    thulunch4.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    thulunch5.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    thulunch6.append(side.get("bread", {}).get(random.randint(1, dictlength)))

                    dictlength = (len(salad))
                    thulunch1.append("--Salad--")
                    thulunch2.append("--Salad--")
                    thulunch3.append("--Salad--")
                    thulunch4.append("--Salad--")
                    thulunch5.append("--Salad--")
                    thulunch6.append("--Salad--")
                    thulunch1.append(salad.get(random.randint(1, dictlength)))
                    thulunch2.append(salad.get(random.randint(1, dictlength)))
                    thulunch3.append(salad.get(random.randint(1, dictlength)))
                    thulunch4.append(salad.get(random.randint(1, dictlength)))
                    thulunch5.append(salad.get(random.randint(1, dictlength)))
                    thulunch6.append(salad.get(random.randint(1, dictlength)))
                    dictlength = (len(dessert))
                    thulunch1.append("--Dessert--")
                    thulunch2.append("--Dessert--")
                    thulunch3.append("--Dessert--")
                    thulunch4.append("--Dessert--")
                    thulunch5.append("--Dessert--")
                    thulunch6.append("--Dessert--")
                    thulunch1.append(dessert.get(random.randint(1, dictlength)))
                    thulunch2.append(dessert.get(random.randint(1, dictlength)))
                    thulunch3.append(dessert.get(random.randint(1, dictlength)))
                    thulunch4.append(dessert.get(random.randint(1, dictlength)))
                    thulunch5.append(dessert.get(random.randint(1, dictlength)))
                    thulunch6.append(dessert.get(random.randint(1, dictlength)))
                    # recipe list handling
                    every_gen_entree.extend(thulunch1)
                    every_gen_entree.extend(thulunch2)
                    every_gen_entree.extend(thulunch3)
                    every_gen_entree.extend(thulunch4)
                    every_gen_entree.extend(thulunch5)
                    every_gen_entree.extend(thulunch6)
                    # recipe list handling
                    every_gen_side.extend(thulunch1)
                    every_gen_side.extend(thulunch2)
                    every_gen_side.extend(thulunch3)
                    every_gen_side.extend(thulunch4)
                    every_gen_side.extend(thulunch5)
                    every_gen_side.extend(thulunch6)
                    # recipe list handling
                    every_gen_brd.extend(thulunch1)
                    every_gen_brd.extend(thulunch2)
                    every_gen_brd.extend(thulunch3)
                    every_gen_brd.extend(thulunch4)
                    every_gen_brd.extend(thulunch5)
                    every_gen_brd.extend(thulunch6)
                    # recipe list handling
                    every_gen_salad.extend(thulunch1)
                    every_gen_salad.extend(thulunch2)
                    every_gen_salad.extend(thulunch3)
                    every_gen_salad.extend(thulunch4)
                    every_gen_salad.extend(thulunch5)
                    every_gen_salad.extend(thulunch6)
                    # recipe list handling
                    every_gen_dessert.extend(thulunch1)
                    every_gen_dessert.extend(thulunch2)
                    every_gen_dessert.extend(thulunch3)
                    every_gen_dessert.extend(thulunch4)
                    every_gen_dessert.extend(thulunch5)
                    every_gen_dessert.extend(thulunch6)
                    return thulunch1, thulunch2, thulunch3, thulunch4, thulunch5, thulunch6


def thursdaydinner(sidecount, ent, thudinner1, thudinner2, thudinner3, thudinner4, thudinner5, thudinner6):
    while ent > 0:
        dict_select = 1
        dictlength = (len(entree[dict_select]))
        thudinner1.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset1 = set(thudinner1)
        if len(thudinner1) != len(myset1):
            thursdaydinner(sidecount, ent, thudinner1, thudinner2, thudinner3, thudinner4, thudinner5, thudinner6)
        thudinner2.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset2 = set(thudinner2)
        if len(thudinner2) != len(myset2):
            thursdaydinner(sidecount, ent, thudinner1, thudinner2, thudinner3, thudinner4, thudinner5, thudinner6)
        thudinner3.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset3 = set(thudinner3)
        if len(thudinner3) != len(myset3):
            thursdaydinner(sidecount, ent, thudinner1, thudinner2, thudinner3, thudinner4, thudinner5, thudinner6)
        thudinner4.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset4 = set(thudinner4)
        if len(thudinner4) != len(myset4):
            thursdaydinner(sidecount, ent, thudinner1, thudinner2, thudinner3, thudinner4, thudinner5, thudinner6)
        thudinner5.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset5 = set(thudinner5)
        if len(thudinner5) != len(myset5):
            thursdaydinner(sidecount, ent, thudinner1, thudinner2, thudinner3, thudinner4, thudinner5, thudinner6)
        thudinner6.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset6 = set(thudinner6)
        if len(thudinner6) != len(myset6):
            thursdaydinner(sidecount, ent, thudinner1, thudinner2, thudinner3, thudinner4, thudinner5, thudinner6)
        ent -= 1
        if ent == 0:

            while sidecount > 0:
                dict_select = 1
                dictlength = (len(side[dict_select]))
                thudinner1.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset1 = set(thudinner1)
                if len(thudinner1) != len(myset1):
                    thursdaydinner(sidecount, ent, thudinner1, thudinner2, thudinner3, thudinner4, thudinner5,
                                   thudinner6)
                thudinner2.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset2 = set(thudinner2)
                if len(thudinner2) != len(myset2):
                    thursdaydinner(sidecount, ent, thudinner1, thudinner2, thudinner3, thudinner4, thudinner5,
                                   thudinner6)
                thudinner3.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset3 = set(thudinner3)
                if len(thudinner3) != len(myset3):
                    thursdaydinner(sidecount, ent, thudinner1, thudinner2, thudinner3, thudinner4, thudinner5,
                                   thudinner6)
                thudinner4.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset4 = set(thudinner4)
                if len(thudinner4) != len(myset4):
                    thursdaydinner(sidecount, ent, thudinner1, thudinner2, thudinner3, thudinner4, thudinner5,
                                   thudinner6)
                thudinner5.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset5 = set(thudinner5)
                if len(thudinner5) != len(myset5):
                    thursdaydinner(sidecount, ent, thudinner1, thudinner2, thudinner3, thudinner4, thudinner5,
                                   thudinner6)
                thudinner6.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset6 = set(thudinner6)
                if len(thudinner6) != len(myset6):
                    thursdaydinner(sidecount, ent, thudinner1, thudinner2, thudinner3, thudinner4, thudinner5,
                                   thudinner6)
                sidecount -= 1

                if sidecount == 0:
                    dictlength = (len(side["bread"]))
                    thudinner1.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    thudinner2.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    thudinner3.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    thudinner4.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    thudinner5.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    thudinner6.append(side.get("bread", {}).get(random.randint(1, dictlength)))

                    dictlength = (len(salad))
                    thudinner1.append("--Salad--")
                    thudinner2.append("--Salad--")
                    thudinner3.append("--Salad--")
                    thudinner4.append("--Salad--")
                    thudinner5.append("--Salad--")
                    thudinner6.append("--Salad--")
                    thudinner1.append(salad.get(random.randint(1, dictlength)))
                    thudinner2.append(salad.get(random.randint(1, dictlength)))
                    thudinner3.append(salad.get(random.randint(1, dictlength)))
                    thudinner4.append(salad.get(random.randint(1, dictlength)))
                    thudinner5.append(salad.get(random.randint(1, dictlength)))
                    thudinner6.append(salad.get(random.randint(1, dictlength)))
                    dictlength = (len(dessert))
                    thudinner1.append("--Dessert--")
                    thudinner2.append("--Dessert--")
                    thudinner3.append("--Dessert--")
                    thudinner4.append("--Dessert--")
                    thudinner5.append("--Dessert--")
                    thudinner6.append("--Dessert--")
                    thudinner1.append(dessert.get(random.randint(1, dictlength)))
                    thudinner2.append(dessert.get(random.randint(1, dictlength)))
                    thudinner3.append(dessert.get(random.randint(1, dictlength)))
                    thudinner4.append(dessert.get(random.randint(1, dictlength)))
                    thudinner5.append(dessert.get(random.randint(1, dictlength)))
                    thudinner6.append(dessert.get(random.randint(1, dictlength)))
                    # recipe list handling
                    every_gen_entree.extend(thudinner1)
                    every_gen_entree.extend(thudinner2)
                    every_gen_entree.extend(thudinner3)
                    every_gen_entree.extend(thudinner4)
                    every_gen_entree.extend(thudinner5)
                    every_gen_entree.extend(thudinner6)
                    # recipe list handling
                    every_gen_side.extend(thudinner1)
                    every_gen_side.extend(thudinner2)
                    every_gen_side.extend(thudinner3)
                    every_gen_side.extend(thudinner4)
                    every_gen_side.extend(thudinner5)
                    every_gen_side.extend(thudinner6)
                    # recipe list handling
                    every_gen_brd.extend(thudinner1)
                    every_gen_brd.extend(thudinner2)
                    every_gen_brd.extend(thudinner3)
                    every_gen_brd.extend(thudinner4)
                    every_gen_brd.extend(thudinner5)
                    every_gen_brd.extend(thudinner6)
                    # recipe list handling
                    every_gen_salad.extend(thudinner1)
                    every_gen_salad.extend(thudinner2)
                    every_gen_salad.extend(thudinner3)
                    every_gen_salad.extend(thudinner4)
                    every_gen_salad.extend(thudinner5)
                    every_gen_salad.extend(thudinner6)
                    # recipe list handling
                    every_gen_dessert.extend(thudinner1)
                    every_gen_dessert.extend(thudinner2)
                    every_gen_dessert.extend(thudinner3)
                    every_gen_dessert.extend(thudinner4)
                    every_gen_dessert.extend(thudinner5)
                    every_gen_dessert.extend(thudinner6)
                    return thudinner1, thudinner2, thudinner3, thudinner4, thudinner5, thudinner6


def fridaybreak(sidecount, fribreak1, fribreak2, fribreak3, fribreak4, fribreak5, fribreak6):
    while sidecount > 0:
        dictlength = (len(entree[10]))
        fribreak1.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        fribreak2.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        fribreak3.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        fribreak4.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        fribreak5.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        fribreak6.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        sidecount -= 1
        if sidecount == 0:
            # recipe list handling
            every_gen_breakfast.extend(fribreak1)
            every_gen_breakfast.extend(fribreak2)
            every_gen_breakfast.extend(fribreak3)
            every_gen_breakfast.extend(fribreak4)
            every_gen_breakfast.extend(fribreak5)
            every_gen_breakfast.extend(fribreak6)
            return fribreak1, fribreak2, fribreak3, fribreak4, fribreak5, fribreak6


def fridaylunch(sidecount, ent, frilunch1, frilunch2, frilunch3, frilunch4, frilunch5, frilunch6):
    while ent > 0:
        dict_select = 1
        dictlength = (len(entree[dict_select]))
        frilunch1.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset1 = set(frilunch1)
        if len(frilunch1) != len(myset1):
            fridaylunch(sidecount, ent, frilunch1, frilunch2, frilunch3, frilunch4, frilunch5, frilunch6)
        frilunch2.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset2 = set(frilunch2)
        if len(frilunch2) != len(myset2):
            fridaylunch(sidecount, ent, frilunch1, frilunch2, frilunch3, frilunch4, frilunch5, frilunch6)
        frilunch3.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset3 = set(frilunch3)
        if len(frilunch3) != len(myset3):
            fridaylunch(sidecount, ent, frilunch1, frilunch2, frilunch3, frilunch4, frilunch5, frilunch6)
        frilunch4.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset4 = set(frilunch4)
        if len(frilunch4) != len(myset4):
            fridaylunch(sidecount, ent, frilunch1, frilunch2, frilunch3, frilunch4, frilunch5, frilunch6)
        frilunch5.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset5 = set(frilunch5)
        if len(frilunch5) != len(myset5):
            fridaylunch(sidecount, ent, frilunch1, frilunch2, frilunch3, frilunch4, frilunch5, frilunch6)
        frilunch6.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset6 = set(frilunch6)
        if len(frilunch6) != len(myset6):
            fridaylunch(sidecount, ent, frilunch1, frilunch2, frilunch3, frilunch4, frilunch5, frilunch6)
        ent -= 1
        if ent == 0:

            while sidecount > 0:
                dict_select = 1
                dictlength = (len(side[dict_select]))
                frilunch1.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset1 = set(frilunch1)
                if len(frilunch1) != len(myset1):
                    fridaylunch(sidecount, ent, frilunch1, frilunch2, frilunch3, frilunch4, frilunch5, frilunch6)
                frilunch2.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset2 = set(frilunch2)
                if len(frilunch2) != len(myset2):
                    fridaylunch(sidecount, ent, frilunch1, frilunch2, frilunch3, frilunch4, frilunch5, frilunch6)
                frilunch3.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset3 = set(frilunch3)
                if len(frilunch3) != len(myset3):
                    fridaylunch(sidecount, ent, frilunch1, frilunch2, frilunch3, frilunch4, frilunch5, frilunch6)
                frilunch4.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset4 = set(frilunch4)
                if len(frilunch4) != len(myset4):
                    fridaylunch(sidecount, ent, frilunch1, frilunch2, frilunch3, frilunch4, frilunch5, frilunch6)
                frilunch5.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset5 = set(frilunch5)
                if len(frilunch5) != len(myset5):
                    fridaylunch(sidecount, ent, frilunch1, frilunch2, frilunch3, frilunch4, frilunch5, frilunch6)
                frilunch6.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset6 = set(frilunch6)
                if len(frilunch6) != len(myset6):
                    fridaylunch(sidecount, ent, frilunch1, frilunch2, frilunch3, frilunch4, frilunch5, frilunch6)
                sidecount -= 1

                if sidecount == 0:
                    dictlength = (len(side["bread"]))
                    frilunch1.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    frilunch2.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    frilunch3.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    frilunch4.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    frilunch5.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    frilunch6.append(side.get("bread", {}).get(random.randint(1, dictlength)))

                    dictlength = (len(salad))
                    frilunch1.append("--Salad--")
                    frilunch2.append("--Salad--")
                    frilunch3.append("--Salad--")
                    frilunch4.append("--Salad--")
                    frilunch5.append("--Salad--")
                    frilunch6.append("--Salad--")
                    frilunch1.append(salad.get(random.randint(1, dictlength)))
                    frilunch2.append(salad.get(random.randint(1, dictlength)))
                    frilunch3.append(salad.get(random.randint(1, dictlength)))
                    frilunch4.append(salad.get(random.randint(1, dictlength)))
                    frilunch5.append(salad.get(random.randint(1, dictlength)))
                    frilunch6.append(salad.get(random.randint(1, dictlength)))
                    dictlength = (len(dessert))
                    frilunch1.append("--Dessert--")
                    frilunch2.append("--Dessert--")
                    frilunch3.append("--Dessert--")
                    frilunch4.append("--Dessert--")
                    frilunch5.append("--Dessert--")
                    frilunch6.append("--Dessert--")
                    frilunch1.append(dessert.get(random.randint(1, dictlength)))
                    frilunch2.append(dessert.get(random.randint(1, dictlength)))
                    frilunch3.append(dessert.get(random.randint(1, dictlength)))
                    frilunch4.append(dessert.get(random.randint(1, dictlength)))
                    frilunch5.append(dessert.get(random.randint(1, dictlength)))
                    frilunch6.append(dessert.get(random.randint(1, dictlength)))
                    # recipe list handling
                    every_gen_entree.extend(frilunch1)
                    every_gen_entree.extend(frilunch2)
                    every_gen_entree.extend(frilunch3)
                    every_gen_entree.extend(frilunch4)
                    every_gen_entree.extend(frilunch5)
                    every_gen_entree.extend(frilunch6)
                    # recipe list handling
                    every_gen_side.extend(frilunch1)
                    every_gen_side.extend(frilunch2)
                    every_gen_side.extend(frilunch3)
                    every_gen_side.extend(frilunch4)
                    every_gen_side.extend(frilunch5)
                    every_gen_side.extend(frilunch6)
                    # recipe list handling
                    every_gen_brd.extend(frilunch1)
                    every_gen_brd.extend(frilunch2)
                    every_gen_brd.extend(frilunch3)
                    every_gen_brd.extend(frilunch4)
                    every_gen_brd.extend(frilunch5)
                    every_gen_brd.extend(frilunch6)
                    # recipe list handling
                    every_gen_salad.extend(frilunch1)
                    every_gen_salad.extend(frilunch2)
                    every_gen_salad.extend(frilunch3)
                    every_gen_salad.extend(frilunch4)
                    every_gen_salad.extend(frilunch5)
                    every_gen_salad.extend(frilunch6)
                    # recipe list handling
                    every_gen_dessert.extend(frilunch1)
                    every_gen_dessert.extend(frilunch2)
                    every_gen_dessert.extend(frilunch3)
                    every_gen_dessert.extend(frilunch4)
                    every_gen_dessert.extend(frilunch5)
                    every_gen_dessert.extend(frilunch6)
                    return frilunch1, frilunch2, frilunch3, frilunch4, frilunch5, frilunch6


def fridaydinner(sidecount, ent, fridinner1, fridinner2, fridinner3, fridinner4, fridinner5, fridinner6):
    while ent > 0:
        dict_select = 1
        dictlength = (len(entree[dict_select]))
        fridinner1.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset1 = set(fridinner1)
        if len(fridinner1) != len(myset1):
            fridaydinner(sidecount, ent, fridinner1, fridinner2, fridinner3, fridinner4, fridinner5, fridinner6)
        fridinner2.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset2 = set(fridinner2)
        if len(fridinner2) != len(myset2):
            fridaydinner(sidecount, ent, fridinner1, fridinner2, fridinner3, fridinner4, fridinner5, fridinner6)
        fridinner3.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset3 = set(fridinner3)
        if len(fridinner3) != len(myset3):
            fridaydinner(sidecount, ent, fridinner1, fridinner2, fridinner3, fridinner4, fridinner5, fridinner6)
        fridinner4.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset4 = set(fridinner4)
        if len(fridinner4) != len(myset4):
            fridaydinner(sidecount, ent, fridinner1, fridinner2, fridinner3, fridinner4, fridinner5, fridinner6)
        fridinner5.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset5 = set(fridinner5)
        if len(fridinner5) != len(myset5):
            fridaydinner(sidecount, ent, fridinner1, fridinner2, fridinner3, fridinner4, fridinner5, fridinner6)
        fridinner6.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset6 = set(fridinner6)
        if len(fridinner6) != len(myset6):
            fridaydinner(sidecount, ent, fridinner1, fridinner2, fridinner3, fridinner4, fridinner5, fridinner6)
        ent -= 1
        if ent == 0:

            while sidecount > 0:
                dict_select = 1
                dictlength = (len(side[dict_select]))
                fridinner1.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset1 = set(fridinner1)
                if len(fridinner1) != len(myset1):
                    fridaydinner(sidecount, ent, fridinner1, fridinner2, fridinner3, fridinner4, fridinner5, fridinner6)
                fridinner2.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset2 = set(fridinner2)
                if len(fridinner2) != len(myset2):
                    fridaydinner(sidecount, ent, fridinner1, fridinner2, fridinner3, fridinner4, fridinner5, fridinner6)
                fridinner3.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset3 = set(fridinner3)
                if len(fridinner3) != len(myset3):
                    fridaydinner(sidecount, ent, fridinner1, fridinner2, fridinner3, fridinner4, fridinner5, fridinner6)
                fridinner4.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset4 = set(fridinner4)
                if len(fridinner4) != len(myset4):
                    fridaydinner(sidecount, ent, fridinner1, fridinner2, fridinner3, fridinner4, fridinner5, fridinner6)
                fridinner5.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset5 = set(fridinner5)
                if len(fridinner5) != len(myset5):
                    fridaydinner(sidecount, ent, fridinner1, fridinner2, fridinner3, fridinner4, fridinner5, fridinner6)
                fridinner6.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset6 = set(fridinner6)
                if len(fridinner6) != len(myset6):
                    fridaydinner(sidecount, ent, fridinner1, fridinner2, fridinner3, fridinner4, fridinner5, fridinner6)
                sidecount -= 1

                if sidecount == 0:
                    dictlength = (len(side["bread"]))
                    fridinner1.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    fridinner2.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    fridinner3.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    fridinner4.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    fridinner5.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    fridinner6.append(side.get("bread", {}).get(random.randint(1, dictlength)))

                    dictlength = (len(salad))
                    fridinner1.append("--Salad--")
                    fridinner2.append("--Salad--")
                    fridinner3.append("--Salad--")
                    fridinner4.append("--Salad--")
                    fridinner5.append("--Salad--")
                    fridinner6.append("--Salad--")
                    fridinner1.append(salad.get(random.randint(1, dictlength)))
                    fridinner2.append(salad.get(random.randint(1, dictlength)))
                    fridinner3.append(salad.get(random.randint(1, dictlength)))
                    fridinner4.append(salad.get(random.randint(1, dictlength)))
                    fridinner5.append(salad.get(random.randint(1, dictlength)))
                    fridinner6.append(salad.get(random.randint(1, dictlength)))
                    dictlength = (len(dessert))
                    fridinner1.append("--Dessert--")
                    fridinner2.append("--Dessert--")
                    fridinner3.append("--Dessert--")
                    fridinner4.append("--Dessert--")
                    fridinner5.append("--Dessert--")
                    fridinner6.append("--Dessert--")
                    fridinner1.append(dessert.get(random.randint(1, dictlength)))
                    fridinner2.append(dessert.get(random.randint(1, dictlength)))
                    fridinner3.append(dessert.get(random.randint(1, dictlength)))
                    fridinner4.append(dessert.get(random.randint(1, dictlength)))
                    fridinner5.append(dessert.get(random.randint(1, dictlength)))
                    fridinner6.append(dessert.get(random.randint(1, dictlength)))
                    #recipe list handling
                    every_gen_entree.extend(fridinner1)
                    every_gen_entree.extend(fridinner2)
                    every_gen_entree.extend(fridinner3)
                    every_gen_entree.extend(fridinner4)
                    every_gen_entree.extend(fridinner5)
                    every_gen_entree.extend(fridinner6)
                    # recipe list handling
                    every_gen_side.extend(fridinner1)
                    every_gen_side.extend(fridinner2)
                    every_gen_side.extend(fridinner3)
                    every_gen_side.extend(fridinner4)
                    every_gen_side.extend(fridinner5)
                    every_gen_side.extend(fridinner6)
                    # recipe list handling
                    every_gen_brd.extend(fridinner1)
                    every_gen_brd.extend(fridinner2)
                    every_gen_brd.extend(fridinner3)
                    every_gen_brd.extend(fridinner4)
                    every_gen_brd.extend(fridinner5)
                    every_gen_brd.extend(fridinner6)
                    # recipe list handling
                    every_gen_salad.extend(fridinner1)
                    every_gen_salad.extend(fridinner2)
                    every_gen_salad.extend(fridinner3)
                    every_gen_salad.extend(fridinner4)
                    every_gen_salad.extend(fridinner5)
                    every_gen_salad.extend(fridinner6)
                    # recipe list handling
                    every_gen_dessert.extend(fridinner1)
                    every_gen_dessert.extend(fridinner2)
                    every_gen_dessert.extend(fridinner3)
                    every_gen_dessert.extend(fridinner4)
                    every_gen_dessert.extend(fridinner5)
                    every_gen_dessert.extend(fridinner6)
                    return fridinner1, fridinner2, fridinner3, fridinner4, fridinner5, fridinner6


def saturdaybreak(sidecount, satbreak1, satbreak2, satbreak3, satbreak4, satbreak5, satbreak6):
    while sidecount > 0:
        dictlength = (len(entree[10]))
        satbreak1.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        satbreak2.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        satbreak3.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        satbreak4.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        satbreak5.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        satbreak6.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        sidecount -= 1
        if sidecount == 0:
            # recipe list handling
            every_gen_breakfast.extend(satbreak1)
            every_gen_breakfast.extend(satbreak2)
            every_gen_breakfast.extend(satbreak3)
            every_gen_breakfast.extend(satbreak4)
            every_gen_breakfast.extend(satbreak5)
            every_gen_breakfast.extend(satbreak6)
            return satbreak1, satbreak2, satbreak3, satbreak4, satbreak5, satbreak6


def saturdaylunch(sidecount, ent, satlunch1, satlunch2, satlunch3, satlunch4, satlunch5, satlunch6):
    while ent > 0:
        dict_select = 1
        dictlength = (len(entree[dict_select]))
        satlunch1.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset1 = set(satlunch1)
        if len(satlunch1) != len(myset1):
            saturdaylunch(sidecount, ent, satlunch1, satlunch2, satlunch3, satlunch4, satlunch5, satlunch6)
        satlunch2.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset2 = set(satlunch2)
        if len(satlunch2) != len(myset2):
            saturdaylunch(sidecount, ent, satlunch1, satlunch2, satlunch3, satlunch4, satlunch5, satlunch6)
        satlunch3.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset3 = set(satlunch3)
        if len(satlunch3) != len(myset3):
            saturdaylunch(sidecount, ent, satlunch1, satlunch2, satlunch3, satlunch4, satlunch5, satlunch6)
        satlunch4.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset4 = set(satlunch4)
        if len(satlunch4) != len(myset4):
            saturdaylunch(sidecount, ent, satlunch1, satlunch2, satlunch3, satlunch4, satlunch5, satlunch6)
        satlunch5.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset5 = set(satlunch5)
        if len(satlunch5) != len(myset5):
            saturdaylunch(sidecount, ent, satlunch1, satlunch2, satlunch3, satlunch4, satlunch5, satlunch6)
        satlunch6.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset6 = set(satlunch6)
        if len(satlunch6) != len(myset6):
            saturdaylunch(sidecount, ent, satlunch1, satlunch2, satlunch3, satlunch4, satlunch5, satlunch6)
        ent -= 1
        if ent == 0:

            while sidecount > 0:
                dict_select = 1
                dictlength = (len(side[dict_select]))
                satlunch1.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset1 = set(satlunch1)
                if len(satlunch1) != len(myset1):
                    saturdaylunch(sidecount, ent, satlunch1, satlunch2, satlunch3, satlunch4, satlunch5, satlunch6)
                satlunch2.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset2 = set(satlunch2)
                if len(satlunch2) != len(myset2):
                    saturdaylunch(sidecount, ent, satlunch1, satlunch2, satlunch3, satlunch4, satlunch5, satlunch6)
                satlunch3.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset3 = set(satlunch3)
                if len(satlunch3) != len(myset3):
                    saturdaylunch(sidecount, ent, satlunch1, satlunch2, satlunch3, satlunch4, satlunch5, satlunch6)
                satlunch4.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset4 = set(satlunch4)
                if len(satlunch4) != len(myset4):
                    saturdaylunch(sidecount, ent, satlunch1, satlunch2, satlunch3, satlunch4, satlunch5, satlunch6)
                satlunch5.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset5 = set(satlunch5)
                if len(satlunch5) != len(myset5):
                    saturdaylunch(sidecount, ent, satlunch1, satlunch2, satlunch3, satlunch4, satlunch5, satlunch6)
                satlunch6.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset6 = set(satlunch6)
                if len(satlunch6) != len(myset6):
                    saturdaylunch(sidecount, ent, satlunch1, satlunch2, satlunch3, satlunch4, satlunch5, satlunch6)
                sidecount -= 1

                if sidecount == 0:
                    dictlength = (len(side["bread"]))
                    satlunch1.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    satlunch2.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    satlunch3.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    satlunch4.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    satlunch5.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    satlunch6.append(side.get("bread", {}).get(random.randint(1, dictlength)))

                    dictlength = (len(salad))
                    satlunch1.append("--Salad--")
                    satlunch2.append("--Salad--")
                    satlunch3.append("--Salad--")
                    satlunch4.append("--Salad--")
                    satlunch5.append("--Salad--")
                    satlunch6.append("--Salad--")
                    satlunch1.append(salad.get(random.randint(1, dictlength)))
                    satlunch2.append(salad.get(random.randint(1, dictlength)))
                    satlunch3.append(salad.get(random.randint(1, dictlength)))
                    satlunch4.append(salad.get(random.randint(1, dictlength)))
                    satlunch5.append(salad.get(random.randint(1, dictlength)))
                    satlunch6.append(salad.get(random.randint(1, dictlength)))
                    dictlength = (len(dessert))
                    satlunch1.append("--Dessert--")
                    satlunch2.append("--Dessert--")
                    satlunch3.append("--Dessert--")
                    satlunch4.append("--Dessert--")
                    satlunch5.append("--Dessert--")
                    satlunch6.append("--Dessert--")
                    satlunch1.append(dessert.get(random.randint(1, dictlength)))
                    satlunch2.append(dessert.get(random.randint(1, dictlength)))
                    satlunch3.append(dessert.get(random.randint(1, dictlength)))
                    satlunch4.append(dessert.get(random.randint(1, dictlength)))
                    satlunch5.append(dessert.get(random.randint(1, dictlength)))
                    satlunch6.append(dessert.get(random.randint(1, dictlength)))
                    # recipe list handling
                    every_gen_entree.extend(satlunch1)
                    every_gen_entree.extend(satlunch2)
                    every_gen_entree.extend(satlunch3)
                    every_gen_entree.extend(satlunch4)
                    every_gen_entree.extend(satlunch5)
                    every_gen_entree.extend(satlunch6)
                    # recipe list handling
                    every_gen_side.extend(satlunch1)
                    every_gen_side.extend(satlunch2)
                    every_gen_side.extend(satlunch3)
                    every_gen_side.extend(satlunch4)
                    every_gen_side.extend(satlunch5)
                    every_gen_side.extend(satlunch6)
                    # recipe list handling
                    every_gen_brd.extend(satlunch1)
                    every_gen_brd.extend(satlunch2)
                    every_gen_brd.extend(satlunch3)
                    every_gen_brd.extend(satlunch4)
                    every_gen_brd.extend(satlunch5)
                    every_gen_brd.extend(satlunch6)
                    # recipe list handling
                    every_gen_salad.extend(satlunch1)
                    every_gen_salad.extend(satlunch2)
                    every_gen_salad.extend(satlunch3)
                    every_gen_salad.extend(satlunch4)
                    every_gen_salad.extend(satlunch5)
                    every_gen_salad.extend(satlunch6)
                    # recipe list handling
                    every_gen_dessert.extend(satlunch1)
                    every_gen_dessert.extend(satlunch2)
                    every_gen_dessert.extend(satlunch3)
                    every_gen_dessert.extend(satlunch4)
                    every_gen_dessert.extend(satlunch5)
                    every_gen_dessert.extend(satlunch6)
                    return satlunch1, satlunch2, satlunch3, satlunch4, satlunch5, satlunch6


def saturdaydinner(sidecount, ent, satdinner1, satdinner2, satdinner3, satdinner4, satdinner5, satdinner6):
    while ent > 0:
        dict_select = 1
        dictlength = (len(entree[dict_select]))
        satdinner1.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset1 = set(satdinner1)
        if len(satdinner1) != len(myset1):
            saturdaydinner(sidecount, ent, satdinner1, satdinner2, satdinner3, satdinner4, satdinner5, satdinner6)
        satdinner2.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset2 = set(satdinner2)
        if len(satdinner2) != len(myset2):
            saturdaydinner(sidecount, ent, satdinner1, satdinner2, satdinner3, satdinner4, satdinner5, satdinner6)
        satdinner3.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset3 = set(satdinner3)
        if len(satdinner3) != len(myset3):
            saturdaydinner(sidecount, ent, satdinner1, satdinner2, satdinner3, satdinner4, satdinner5, satdinner6)
        satdinner4.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset4 = set(satdinner4)
        if len(satdinner4) != len(myset4):
            saturdaydinner(sidecount, ent, satdinner1, satdinner2, satdinner3, satdinner4, satdinner5, satdinner6)
        satdinner5.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset5 = set(satdinner5)
        if len(satdinner5) != len(myset5):
            saturdaydinner(sidecount, ent, satdinner1, satdinner2, satdinner3, satdinner4, satdinner5, satdinner6)
        satdinner6.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset6 = set(satdinner6)
        if len(satdinner6) != len(myset6):
            saturdaydinner(sidecount, ent, satdinner1, satdinner2, satdinner3, satdinner4, satdinner5, satdinner6)
        ent -= 1
        if ent == 0:

            while sidecount > 0:
                dict_select = 1
                dictlength = (len(side[dict_select]))
                satdinner1.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset1 = set(satdinner1)
                if len(satdinner1) != len(myset1):
                    saturdaydinner(sidecount, ent, satdinner1, satdinner2, satdinner3, satdinner4, satdinner5,
                                   satdinner6)
                satdinner2.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset2 = set(satdinner2)
                if len(satdinner2) != len(myset2):
                    saturdaydinner(sidecount, ent, satdinner1, satdinner2, satdinner3, satdinner4, satdinner5,
                                   satdinner6)
                satdinner3.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset3 = set(satdinner3)
                if len(satdinner3) != len(myset3):
                    saturdaydinner(sidecount, ent, satdinner1, satdinner2, satdinner3, satdinner4, satdinner5,
                                   satdinner6)
                satdinner4.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset4 = set(satdinner4)
                if len(satdinner4) != len(myset4):
                    saturdaydinner(sidecount, ent, satdinner1, satdinner2, satdinner3, satdinner4, satdinner5,
                                   satdinner6)
                satdinner5.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset5 = set(satdinner5)
                if len(satdinner5) != len(myset5):
                    saturdaydinner(sidecount, ent, satdinner1, satdinner2, satdinner3, satdinner4, satdinner5,
                                   satdinner6)
                satdinner6.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset6 = set(satdinner6)
                if len(satdinner6) != len(myset6):
                    saturdaydinner(sidecount, ent, satdinner1, satdinner2, satdinner3, satdinner4, satdinner5,
                                   satdinner6)
                sidecount -= 1

                if sidecount == 0:
                    dictlength = (len(side["bread"]))
                    satdinner1.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    satdinner2.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    satdinner3.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    satdinner4.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    satdinner5.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    satdinner6.append(side.get("bread", {}).get(random.randint(1, dictlength)))

                    dictlength = (len(salad))
                    satdinner1.append("--Salad--")
                    satdinner2.append("--Salad--")
                    satdinner3.append("--Salad--")
                    satdinner4.append("--Salad--")
                    satdinner5.append("--Salad--")
                    satdinner6.append("--Salad--")
                    satdinner1.append(salad.get(random.randint(1, dictlength)))
                    satdinner2.append(salad.get(random.randint(1, dictlength)))
                    satdinner3.append(salad.get(random.randint(1, dictlength)))
                    satdinner4.append(salad.get(random.randint(1, dictlength)))
                    satdinner5.append(salad.get(random.randint(1, dictlength)))
                    satdinner6.append(salad.get(random.randint(1, dictlength)))
                    dictlength = (len(dessert))
                    satdinner1.append("--Dessert--")
                    satdinner2.append("--Dessert--")
                    satdinner3.append("--Dessert--")
                    satdinner4.append("--Dessert--")
                    satdinner5.append("--Dessert--")
                    satdinner6.append("--Dessert--")
                    satdinner1.append(dessert.get(random.randint(1, dictlength)))
                    satdinner2.append(dessert.get(random.randint(1, dictlength)))
                    satdinner3.append(dessert.get(random.randint(1, dictlength)))
                    satdinner4.append(dessert.get(random.randint(1, dictlength)))
                    satdinner5.append(dessert.get(random.randint(1, dictlength)))
                    satdinner6.append(dessert.get(random.randint(1, dictlength)))
                    # recipe list handling
                    every_gen_entree.extend(satdinner1)
                    every_gen_entree.extend(satdinner2)
                    every_gen_entree.extend(satdinner3)
                    every_gen_entree.extend(satdinner4)
                    every_gen_entree.extend(satdinner5)
                    every_gen_entree.extend(satdinner6)
                    # recipe list handling
                    every_gen_side.extend(satdinner1)
                    every_gen_side.extend(satdinner2)
                    every_gen_side.extend(satdinner3)
                    every_gen_side.extend(satdinner4)
                    every_gen_side.extend(satdinner5)
                    every_gen_side.extend(satdinner6)
                    # recipe list handling
                    every_gen_brd.extend(satdinner1)
                    every_gen_brd.extend(satdinner2)
                    every_gen_brd.extend(satdinner3)
                    every_gen_brd.extend(satdinner4)
                    every_gen_brd.extend(satdinner5)
                    every_gen_brd.extend(satdinner6)
                    # recipe list handling
                    every_gen_salad.extend(satdinner1)
                    every_gen_salad.extend(satdinner2)
                    every_gen_salad.extend(satdinner3)
                    every_gen_salad.extend(satdinner4)
                    every_gen_salad.extend(satdinner5)
                    every_gen_salad.extend(satdinner6)
                    # recipe list handling
                    every_gen_dessert.extend(satdinner1)
                    every_gen_dessert.extend(satdinner2)
                    every_gen_dessert.extend(satdinner3)
                    every_gen_dessert.extend(satdinner4)
                    every_gen_dessert.extend(satdinner5)
                    every_gen_dessert.extend(satdinner6)
                    return satdinner1, satdinner2, satdinner3, satdinner4, satdinner5, satdinner6


def sundaybreak(sidecount, sunbreak1, sunbreak2, sunbreak3, sunbreak4, sunbreak5, sunbreak6):
    while sidecount > 0:
        dictlength = (len(entree[10]))
        sunbreak1.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        sunbreak2.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        sunbreak3.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        sunbreak4.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        sunbreak5.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        sunbreak6.append(entree.get(10, {}).get(random.randint(1, dictlength)))
        sidecount -= 1
        if sidecount == 0:
            # recipe list handling
            every_gen_breakfast.extend(sunbreak1)
            every_gen_breakfast.extend(sunbreak2)
            every_gen_breakfast.extend(sunbreak3)
            every_gen_breakfast.extend(sunbreak4)
            every_gen_breakfast.extend(sunbreak5)
            every_gen_breakfast.extend(sunbreak6)
            return sunbreak1, sunbreak2, sunbreak3, sunbreak4, sunbreak5, sunbreak6


def sundaylunch(sidecount, ent, sunlunch1, sunlunch2, sunlunch3, sunlunch4, sunlunch5, sunlunch6):
    while ent > 0:
        dict_select = 1
        dictlength = (len(entree[dict_select]))
        sunlunch1.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset1 = set(sunlunch1)
        if len(sunlunch1) != len(myset1):
            sundaylunch(sidecount, ent, sunlunch1, sunlunch2, sunlunch3, sunlunch4, sunlunch5, sunlunch6)
        sunlunch2.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset2 = set(sunlunch2)
        if len(sunlunch2) != len(myset2):
            sundaylunch(sidecount, ent, sunlunch1, sunlunch2, sunlunch3, sunlunch4, sunlunch5, sunlunch6)
        sunlunch3.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset3 = set(sunlunch3)
        if len(sunlunch3) != len(myset3):
            sundaylunch(sidecount, ent, sunlunch1, sunlunch2, sunlunch3, sunlunch4, sunlunch5, sunlunch6)
        sunlunch4.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset4 = set(sunlunch4)
        if len(sunlunch4) != len(myset4):
            sundaylunch(sidecount, ent, sunlunch1, sunlunch2, sunlunch3, sunlunch4, sunlunch5, sunlunch6)
        sunlunch5.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset5 = set(sunlunch5)
        if len(sunlunch5) != len(myset5):
            sundaylunch(sidecount, ent, sunlunch1, sunlunch2, sunlunch3, sunlunch4, sunlunch5, sunlunch6)
        sunlunch6.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset6 = set(sunlunch6)
        if len(sunlunch6) != len(myset6):
            sundaylunch(sidecount, ent, sunlunch1, sunlunch2, sunlunch3, sunlunch4, sunlunch5, sunlunch6)
        ent -= 1
        if ent == 0:

            while sidecount > 0:
                dict_select = 1
                dictlength = (len(side[dict_select]))
                sunlunch1.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset1 = set(sunlunch1)
                if len(sunlunch1) != len(myset1):
                    sundaylunch(sidecount, ent, sunlunch1, sunlunch2, sunlunch3, sunlunch4, sunlunch5, sunlunch6)
                sunlunch2.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset2 = set(sunlunch2)
                if len(sunlunch2) != len(myset2):
                    sundaylunch(sidecount, ent, sunlunch1, sunlunch2, sunlunch3, sunlunch4, sunlunch5, sunlunch6)
                sunlunch3.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset3 = set(sunlunch3)
                if len(sunlunch3) != len(myset3):
                    sundaylunch(sidecount, ent, sunlunch1, sunlunch2, sunlunch3, sunlunch4, sunlunch5, sunlunch6)
                sunlunch4.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset4 = set(sunlunch4)
                if len(sunlunch4) != len(myset4):
                    sundaylunch(sidecount, ent, sunlunch1, sunlunch2, sunlunch3, sunlunch4, sunlunch5, sunlunch6)
                sunlunch5.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset5 = set(sunlunch5)
                if len(sunlunch5) != len(myset5):
                    sundaylunch(sidecount, ent, sunlunch1, sunlunch2, sunlunch3, sunlunch4, sunlunch5, sunlunch6)
                sunlunch6.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset6 = set(sunlunch6)
                if len(sunlunch6) != len(myset6):
                    sundaylunch(sidecount, ent, sunlunch1, sunlunch2, sunlunch3, sunlunch4, sunlunch5, sunlunch6)
                sidecount -= 1

                if sidecount == 0:
                    dictlength = (len(side["bread"]))
                    sunlunch1.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    sunlunch2.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    sunlunch3.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    sunlunch4.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    sunlunch5.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    sunlunch6.append(side.get("bread", {}).get(random.randint(1, dictlength)))

                    dictlength = (len(salad))
                    sunlunch1.append("--Salad--")
                    sunlunch2.append("--Salad--")
                    sunlunch3.append("--Salad--")
                    sunlunch4.append("--Salad--")
                    sunlunch5.append("--Salad--")
                    sunlunch6.append("--Salad--")
                    sunlunch1.append(salad.get(random.randint(1, dictlength)))
                    sunlunch2.append(salad.get(random.randint(1, dictlength)))
                    sunlunch3.append(salad.get(random.randint(1, dictlength)))
                    sunlunch4.append(salad.get(random.randint(1, dictlength)))
                    sunlunch5.append(salad.get(random.randint(1, dictlength)))
                    sunlunch6.append(salad.get(random.randint(1, dictlength)))
                    dictlength = (len(dessert))
                    sunlunch1.append("--Dessert--")
                    sunlunch2.append("--Dessert--")
                    sunlunch3.append("--Dessert--")
                    sunlunch4.append("--Dessert--")
                    sunlunch5.append("--Dessert--")
                    sunlunch6.append("--Dessert--")
                    sunlunch1.append(dessert.get(random.randint(1, dictlength)))
                    sunlunch2.append(dessert.get(random.randint(1, dictlength)))
                    sunlunch3.append(dessert.get(random.randint(1, dictlength)))
                    sunlunch4.append(dessert.get(random.randint(1, dictlength)))
                    sunlunch5.append(dessert.get(random.randint(1, dictlength)))
                    sunlunch6.append(dessert.get(random.randint(1, dictlength)))
                    # recipe list handling
                    every_gen_entree.extend(sunlunch1)
                    every_gen_entree.extend(sunlunch2)
                    every_gen_entree.extend(sunlunch3)
                    every_gen_entree.extend(sunlunch4)
                    every_gen_entree.extend(sunlunch5)
                    every_gen_entree.extend(sunlunch6)
                    # recipe list handling
                    every_gen_side.extend(sunlunch1)
                    every_gen_side.extend(sunlunch2)
                    every_gen_side.extend(sunlunch3)
                    every_gen_side.extend(sunlunch4)
                    every_gen_side.extend(sunlunch5)
                    every_gen_side.extend(sunlunch6)
                    # recipe list handling
                    every_gen_brd.extend(sunlunch1)
                    every_gen_brd.extend(sunlunch2)
                    every_gen_brd.extend(sunlunch3)
                    every_gen_brd.extend(sunlunch4)
                    every_gen_brd.extend(sunlunch5)
                    every_gen_brd.extend(sunlunch6)
                    # recipe list handling
                    every_gen_salad.extend(sunlunch1)
                    every_gen_salad.extend(sunlunch2)
                    every_gen_salad.extend(sunlunch3)
                    every_gen_salad.extend(sunlunch4)
                    every_gen_salad.extend(sunlunch5)
                    every_gen_salad.extend(sunlunch6)
                    # recipe list handling
                    every_gen_dessert.extend(sunlunch1)
                    every_gen_dessert.extend(sunlunch2)
                    every_gen_dessert.extend(sunlunch3)
                    every_gen_dessert.extend(sunlunch4)
                    every_gen_dessert.extend(sunlunch5)
                    every_gen_dessert.extend(sunlunch6)
                    return sunlunch1, sunlunch2, sunlunch3, sunlunch4, sunlunch5, sunlunch6


def sundaydinner(sidecount, ent, sundinner1, sundinner2, sundinner3, sundinner4, sundinner5, sundinner6):
    while ent > 0:
        dict_select = 1
        dictlength = (len(entree[dict_select]))
        sundinner1.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset1 = set(sundinner1)
        if len(sundinner1) != len(myset1):
            sundaydinner(sidecount, ent, sundinner1, sundinner2, sundinner3, sundinner4, sundinner5, sundinner6)
        sundinner2.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset2 = set(sundinner2)
        if len(sundinner2) != len(myset2):
            sundaydinner(sidecount, ent, sundinner1, sundinner2, sundinner3, sundinner4, sundinner5, sundinner6)
        sundinner3.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset3 = set(sundinner3)
        if len(sundinner3) != len(myset3):
            sundaydinner(sidecount, ent, sundinner1, sundinner2, sundinner3, sundinner4, sundinner5, sundinner6)
        sundinner4.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset4 = set(sundinner4)
        if len(sundinner4) != len(myset4):
            sundaydinner(sidecount, ent, sundinner1, sundinner2, sundinner3, sundinner4, sundinner5, sundinner6)
        sundinner5.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset5 = set(sundinner5)
        if len(sundinner5) != len(myset5):
            sundaydinner(sidecount, ent, sundinner1, sundinner2, sundinner3, sundinner4, sundinner5, sundinner6)
        sundinner6.append(entree.get(dict_select, {}).get(random.randint(1, dictlength)))
        myset6 = set(sundinner6)
        if len(sundinner6) != len(myset6):
            sundaydinner(sidecount, ent, sundinner1, sundinner2, sundinner3, sundinner4, sundinner5, sundinner6)
        ent -= 1
        if ent == 0:

            while sidecount > 0:
                dict_select = 1
                dictlength = (len(side[dict_select]))
                sundinner1.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset1 = set(sundinner1)
                if len(sundinner1) != len(myset1):
                    sundaydinner(sidecount, ent, sundinner1, sundinner2, sundinner3, sundinner4, sundinner5, sundinner6)
                sundinner2.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset2 = set(sundinner2)
                if len(sundinner2) != len(myset2):
                    sundaydinner(sidecount, ent, sundinner1, sundinner2, sundinner3, sundinner4, sundinner5, sundinner6)
                sundinner3.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset3 = set(sundinner3)
                if len(sundinner3) != len(myset3):
                    sundaydinner(sidecount, ent, sundinner1, sundinner2, sundinner3, sundinner4, sundinner5, sundinner6)
                sundinner4.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset4 = set(sundinner4)
                if len(sundinner4) != len(myset4):
                    sundaydinner(sidecount, ent, sundinner1, sundinner2, sundinner3, sundinner4, sundinner5, sundinner6)
                sundinner5.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset5 = set(sundinner5)
                if len(sundinner5) != len(myset5):
                    sundaydinner(sidecount, ent, sundinner1, sundinner2, sundinner3, sundinner4, sundinner5, sundinner6)
                sundinner6.append(side.get(dict_select, {}).get(random.randint(1, dictlength)))
                myset6 = set(sundinner6)
                if len(sundinner6) != len(myset6):
                    sundaydinner(sidecount, ent, sundinner1, sundinner2, sundinner3, sundinner4, sundinner5, sundinner6)
                sidecount -= 1

                if sidecount == 0:
                    dictlength = (len(side["bread"]))
                    sundinner1.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    sundinner2.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    sundinner3.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    sundinner4.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    sundinner5.append(side.get("bread", {}).get(random.randint(1, dictlength)))
                    sundinner6.append(side.get("bread", {}).get(random.randint(1, dictlength)))

                    dictlength = (len(salad))
                    sundinner1.append("--Salad--")
                    sundinner2.append("--Salad--")
                    sundinner3.append("--Salad--")
                    sundinner4.append("--Salad--")
                    sundinner5.append("--Salad--")
                    sundinner6.append("--Salad--")
                    sundinner1.append(salad.get(random.randint(1, dictlength)))
                    sundinner2.append(salad.get(random.randint(1, dictlength)))
                    sundinner3.append(salad.get(random.randint(1, dictlength)))
                    sundinner4.append(salad.get(random.randint(1, dictlength)))
                    sundinner5.append(salad.get(random.randint(1, dictlength)))
                    sundinner6.append(salad.get(random.randint(1, dictlength)))
                    dictlength = (len(dessert))
                    sundinner1.append("--Dessert--")
                    sundinner2.append("--Dessert--")
                    sundinner3.append("--Dessert--")
                    sundinner4.append("--Dessert--")
                    sundinner5.append("--Dessert--")
                    sundinner6.append("--Dessert--")
                    sundinner1.append(dessert.get(random.randint(1, dictlength)))
                    sundinner2.append(dessert.get(random.randint(1, dictlength)))
                    sundinner3.append(dessert.get(random.randint(1, dictlength)))
                    sundinner4.append(dessert.get(random.randint(1, dictlength)))
                    sundinner5.append(dessert.get(random.randint(1, dictlength)))
                    sundinner6.append(dessert.get(random.randint(1, dictlength)))
                    # recipe list handling
                    every_gen_entree.extend(sundinner1)
                    every_gen_entree.extend(sundinner2)
                    every_gen_entree.extend(sundinner3)
                    every_gen_entree.extend(sundinner4)
                    every_gen_entree.extend(sundinner5)
                    every_gen_entree.extend(sundinner6)
                    # recipe list handling
                    every_gen_side.extend(sundinner1)
                    every_gen_side.extend(sundinner2)
                    every_gen_side.extend(sundinner3)
                    every_gen_side.extend(sundinner4)
                    every_gen_side.extend(sundinner5)
                    every_gen_side.extend(sundinner6)
                    # recipe list handling
                    every_gen_brd.extend(sundinner1)
                    every_gen_brd.extend(sundinner2)
                    every_gen_brd.extend(sundinner3)
                    every_gen_brd.extend(sundinner4)
                    every_gen_brd.extend(sundinner5)
                    every_gen_brd.extend(sundinner6)
                    # recipe list handling
                    every_gen_salad.extend(sundinner1)
                    every_gen_salad.extend(sundinner2)
                    every_gen_salad.extend(sundinner3)
                    every_gen_salad.extend(sundinner4)
                    every_gen_salad.extend(sundinner5)
                    every_gen_salad.extend(sundinner6)
                    # recipe list handling
                    every_gen_dessert.extend(sundinner1)
                    every_gen_dessert.extend(sundinner2)
                    every_gen_dessert.extend(sundinner3)
                    every_gen_dessert.extend(sundinner4)
                    every_gen_dessert.extend(sundinner5)
                    every_gen_dessert.extend(sundinner6)
                    return sundinner1, sundinner2, sundinner3, sundinner4, sundinner5, sundinner6


def generator_randomizer(setdays,daysweekgen,gendays,stday,days,
    week_one,week_two,week_three,week_four,week_five,week_six,working_week,
        startweekmon,monlunch1,monlunch2,monlunch3,monlunch4,monlunch5
    ,monlunch6,mondaybreak,monbreak1, monbreak2, monbreak3, monbreak4,
    monbreak5, monbreak6,mondinner1, mondinner2, mondinner3, mondinner4, mondinner5,mondinner6,
    startweektue,startweekwed,startweekthu,startweekfri,startweeksat,startweeksun,
    tuebreak1, tuebreak2, tuebreak3, tuebreak4, tuebreak5, tuebreak6,tuelunch1, tuelunch2,
    tuelunch3, tuelunch4, tuelunch5, tuelunch6,tuedinner1, tuedinner2, tuedinner3,
    tuedinner4, tuedinner5,tuedinner6,wedbreak1, wedbreak2, wedbreak3, wedbreak4, wedbreak5, wedbreak6,
    wedlunch1, wedlunch2, wedlunch3, wedlunch4, wedlunch5, wedlunch6,weddinner1, weddinner2, weddinner3,
    weddinner4, weddinner5,weddinner6,thubreak1, thubreak2, thubreak3, thubreak4, thubreak5, thubreak6,
    thulunch1, thulunch2, thulunch3, thulunch4, thulunch5, thulunch6,thudinner1, thudinner2, thudinner3,
    thudinner4, thudinner5,thudinner6,fribreak1, fribreak2, fribreak3, fribreak4, fribreak5, fribreak6,
    frilunch1, frilunch2, frilunch3, frilunch4, frilunch5, frilunch6,fridinner1, fridinner2, fridinner3,
    fridinner4, fridinner5,fridinner6,satbreak1, satbreak2, satbreak3, satbreak4, satbreak5, satbreak6,
    satlunch1, satlunch2, satlunch3, satlunch4, satlunch5, satlunch6,satdinner1, satdinner2, satdinner3,
    satdinner4, satdinner5,satdinner6,sunbreak1, sunbreak2, sunbreak3, sunbreak4, sunbreak5, sunbreak6,
    sunlunch1, sunlunch2, sunlunch3, sunlunch4, sunlunch5, sunlunch6,sundinner1, sundinner2, sundinner3,
    sundinner4, sundinner5,sundinner6,mondaylunch,sidecount,ent,entret,sideret):


            daysweekcountdown = days
            mpf = open("Meal Plan Gen.txt", "w")
            week_one = copy.deepcopy(setdays)
            week_two = copy.deepcopy(setdays)
            week_three = copy.deepcopy(setdays)
            week_four = copy.deepcopy(setdays)
            week_five = copy.deepcopy(setdays)
            week_six = copy.deepcopy(setdays)
            working_week = week_six
            iter_week = "running"
            #somehow sides and entree values got mixed up \_('_')_/
            sidecount+=entret
            ent+=sideret
            global every_gen_entree
            global every_gen_breakfast
            every_gen_entree=[]
            every_gen_breakfast=[]
            # generator for monday
            while daysweekcountdown > 0:



                monbreakfast = 0
                mon_l = working_week.get("mon", {}).get("lunch")
                mon_d = working_week.get("mon", {}).get("dinner")
                if startweekmon == "y":

                    setdaysday = "mon"
                    if monbreakfast == 0:
                        print("generating monday")
                        mondaybreak(sidecount, monbreak1, monbreak2, monbreak3, monbreak4, monbreak5, monbreak6)

                    if mon_l != 0:
                        setmeal1 = working_week.get("mon", {}).get("lunch")
                        monlunch1.append(setmeal1)
                        monlunch2.append(setmeal1)
                        monlunch3.append(setmeal1)
                        monlunch4.append(setmeal1)
                        monlunch5.append(setmeal1)
                        monlunch6.append(setmeal1)
                        #recipe list handling
                        every_gen_entree.extend(monlunch1)
                        every_gen_entree.extend(monlunch2)
                        every_gen_entree.extend(monlunch3)
                        every_gen_entree.extend(monlunch4)
                        every_gen_entree.extend(monlunch5)
                        every_gen_entree.extend(monlunch6)
                    if mon_l == 0:
                        mondaylunch(sidecount, ent, monlunch1, monlunch2, monlunch3, monlunch4, monlunch5, monlunch6)

                    if mon_d != 0:
                        setmeal2 = working_week.get("mon", {}).get("dinner")
                        mondinner1.append(setmeal2)
                        mondinner2.append(setmeal2)
                        mondinner3.append(setmeal2)
                        mondinner4.append(setmeal2)
                        mondinner5.append(setmeal2)
                        mondinner6.append(setmeal2)
                        #recipe list handling
                        every_gen_entree.extend(mondinner1)
                        every_gen_entree.extend(mondinner2)
                        every_gen_entree.extend(mondinner3)
                        every_gen_entree.extend(mondinner4)
                        every_gen_entree.extend(mondinner5)
                        every_gen_entree.extend(mondinner6)
                    if mon_d == 0:
                        mondaydinner(sidecount, ent, mondinner1, mondinner2, mondinner3, mondinner4, mondinner5,
                                     mondinner6)

                    week_one.update({setdaysday: {"Monday > breakfast": monbreak1, "lunch": monlunch1, "dinner": mondinner1}})
                    week_two.update({setdaysday: {"Monday > breakfast": monbreak2, "lunch": monlunch2, "dinner": mondinner2}})
                    week_three.update({setdaysday: {"Monday > breakfast": monbreak3, "lunch": monlunch3,"dinner": mondinner3}})
                    week_four.update({setdaysday: {"Monday > breakfast": monbreak4, "lunch": monlunch4, "dinner": mondinner4}})
                    week_five.update({setdaysday: {"Monday > breakfast": monbreak5, "lunch": monlunch5, "dinner": mondinner5}})
                    week_six.update({setdaysday: {"Monday > breakfast": monbreak6, "lunch": monlunch6, "dinner": mondinner6}})

                # begin generator for tuesday
                tuebreakfast = 0
                tue_l = working_week.get("tue", {}).get("lunch")
                tue_d = working_week.get("tue", {}).get("dinner")
                if startweektue == "y":
                    setdaysday = "tue"
                    if tuebreakfast == 0:
                        print("generating tuesday")
                        tuesdaybreak(sidecount, tuebreak1, tuebreak2, tuebreak3, tuebreak4, tuebreak5, tuebreak6)
                    if tue_l != 0 and not "taco tuesday":
                        setmeal1 = working_week.get("tue", {}).get("lunch")
                        tuelunch1.append(setmeal1)
                        tuelunch2.append(setmeal1)
                        tuelunch3.append(setmeal1)
                        tuelunch4.append(setmeal1)
                        tuelunch5.append(setmeal1)
                        tuelunch6.append(setmeal1)
                        #recipe list handling
                        every_gen_entree.extend(tuelunch1)
                        every_gen_entree.extend(tuelunch2)
                        every_gen_entree.extend(tuelunch3)
                        every_gen_entree.extend(tuelunch4)
                        every_gen_entree.extend(tuelunch5)
                        every_gen_entree.extend(tuelunch6)
                    if tue_l == "taco tuesday":
                        dictlength = (len(entree[6]))
                        tuelunch1.append(entree.get(6, {}).get(random.randint(1, dictlength)))
                        tuelunch2.append(entree.get(6, {}).get(random.randint(1, dictlength)))
                        tuelunch3.append(entree.get(6, {}).get(random.randint(1, dictlength)))
                        tuelunch4.append(entree.get(6, {}).get(random.randint(1, dictlength)))
                        tuelunch5.append(entree.get(6, {}).get(random.randint(1, dictlength)))
                        tuelunch6.append(entree.get(6, {}).get(random.randint(1, dictlength)))
                        # recipe list handling
                        every_gen_entree.extend(tuelunch1)
                        every_gen_entree.extend(tuelunch2)
                        every_gen_entree.extend(tuelunch3)
                        every_gen_entree.extend(tuelunch4)
                        every_gen_entree.extend(tuelunch5)
                        every_gen_entree.extend(tuelunch6)
                    if tue_l == 0:
                        tuesdaylunch(sidecount, ent, tuelunch1, tuelunch2, tuelunch3, tuelunch4, tuelunch5, tuelunch6)

                    if tue_d != 0 and not "taco tuesday":
                        setmeal2 = working_week.get("tue", {}).get("dinner")
                        tuedinner1.append(setmeal2)
                        tuedinner2.append(setmeal2)
                        tuedinner3.append(setmeal2)
                        tuedinner4.append(setmeal2)
                        tuedinner5.append(setmeal2)
                        tuedinner6.append(setmeal2)
                        # recipe list handling
                        every_gen_entree.extend(tuedinner1)
                        every_gen_entree.extend(tuedinner2)
                        every_gen_entree.extend(tuedinner3)
                        every_gen_entree.extend(tuedinner4)
                        every_gen_entree.extend(tuedinner5)
                        every_gen_entree.extend(tuedinner6)
                    if tue_d == "taco tuesday":
                        dictlength = (len(entree[6]))
                        tuedinner1.append(entree.get(6, {}).get(random.randint(1, dictlength)))
                        tuedinner2.append(entree.get(6, {}).get(random.randint(1, dictlength)))
                        tuedinner3.append(entree.get(6, {}).get(random.randint(1, dictlength)))
                        tuedinner4.append(entree.get(6, {}).get(random.randint(1, dictlength)))
                        tuedinner5.append(entree.get(6, {}).get(random.randint(1, dictlength)))
                        tuedinner6.append(entree.get(6, {}).get(random.randint(1, dictlength)))
                        # recipe list handling
                        every_gen_entree.extend(tuedinner1)
                        every_gen_entree.extend(tuedinner2)
                        every_gen_entree.extend(tuedinner3)
                        every_gen_entree.extend(tuedinner4)
                        every_gen_entree.extend(tuedinner5)
                        every_gen_entree.extend(tuedinner6)
                    if tue_d == 0:
                        tuesdaydinner(sidecount, ent, tuedinner1, tuedinner2, tuedinner3, tuedinner4, tuedinner5,tuedinner6)

                    week_one.update({setdaysday: {"Tuesday > breakfast": tuebreak1, "lunch": tuelunch1, "dinner": tuedinner1}})
                    week_two.update({setdaysday: {"Tuesday > breakfast": tuebreak2, "lunch": tuelunch2, "dinner": tuedinner2}})
                    week_three.update({setdaysday: {"Tuesday > breakfast": tuebreak3, "lunch": tuelunch3, "dinner": tuedinner3}})
                    week_four.update({setdaysday: {"Tuesday > breakfast": tuebreak4, "lunch": tuelunch4, "dinner": tuedinner4}})
                    week_five.update({setdaysday: {"Tuesday > breakfast": tuebreak5, "lunch": tuelunch5, "dinner": tuedinner5}})
                    week_six.update({setdaysday: {"Tuesday > breakfast": tuebreak6, "lunch": tuelunch6, "dinner": tuedinner6}})

                    # begin generator for wednesday
                wedbreakfast = 0
                wed_l = working_week.get("wed", {}).get("lunch")
                wed_d = working_week.get("wed", {}).get("dinner")
                if startweekwed == "y":
                    setdaysday = "wed"
                    if wedbreakfast == 0:
                        print("generating wednesday")
                        wednesdaybreak(sidecount, wedbreak1, wedbreak2, wedbreak3, wedbreak4, wedbreak5, wedbreak6)

                    if wed_l != 0:
                        setmeal1 = working_week.get("wed", {}).get("lunch")
                        wedlunch1.append(setmeal1)
                        wedlunch2.append(setmeal1)
                        wedlunch3.append(setmeal1)
                        wedlunch4.append(setmeal1)
                        wedlunch5.append(setmeal1)
                        wedlunch6.append(setmeal1)
                        # recipe list handling
                        every_gen_entree.extend(wedlunch1)
                        every_gen_entree.extend(wedlunch2)
                        every_gen_entree.extend(wedlunch3)
                        every_gen_entree.extend(wedlunch4)
                        every_gen_entree.extend(wedlunch5)
                        every_gen_entree.extend(wedlunch6)
                    if wed_l == 0:
                        wednesdaylunch(sidecount, ent, wedlunch1, wedlunch2, wedlunch3, wedlunch4, wedlunch5, wedlunch6)

                    if wed_d != 0:
                        setmeal2 = working_week.get("wed", {}).get("dinner")
                        weddinner1.append(setmeal2)
                        weddinner2.append(setmeal2)
                        weddinner3.append(setmeal2)
                        weddinner4.append(setmeal2)
                        weddinner5.append(setmeal2)
                        weddinner6.append(setmeal2)
                        # recipe list handling
                        every_gen_entree.extend(weddinner1)
                        every_gen_entree.extend(weddinner2)
                        every_gen_entree.extend(weddinner3)
                        every_gen_entree.extend(weddinner4)
                        every_gen_entree.extend(weddinner5)
                        every_gen_entree.extend(weddinner6)
                    if wed_d == 0:
                        wednesdaydinner(sidecount, ent, weddinner1, weddinner2, weddinner3, weddinner4, weddinner5,
                                        weddinner6)

                    week_one.update({setdaysday: {"Wednesday > breakfast": wedbreak1, "lunch": wedlunch1, "dinner": weddinner1}})
                    week_two.update({setdaysday: {"Wednesday > breakfast": wedbreak2, "lunch": wedlunch2, "dinner": weddinner2}})
                    week_three.update({setdaysday: {"Wednesday > breakfast": wedbreak3, "lunch": wedlunch3, "dinner": weddinner3}})
                    week_four.update({setdaysday: {"Wednesday > breakfast": wedbreak4, "lunch": wedlunch4, "dinner": weddinner4}})
                    week_five.update({setdaysday: {"Wednesday > breakfast": wedbreak5, "lunch": wedlunch5, "dinner": weddinner5}})
                    week_six.update({setdaysday: {"Wednesday > breakfast": wedbreak6, "lunch": wedlunch6, "dinner": weddinner6}})


                # begin generator for thursday
                thubreakfast = 0
                thu_l = working_week.get("thu", {}).get("lunch")
                thu_d = working_week.get("thu", {}).get("dinner")
                if startweekthu == "y":
                    setdaysday = "thu"
                    if thubreakfast == 0:
                        print("generating thursday")
                        thursdaybreak(sidecount, thubreak1, thubreak2, thubreak3, thubreak4, thubreak5, thubreak6)

                    if thu_l != 0:
                        setmeal1 = working_week.get("thu", {}).get("lunch")
                        thulunch1.append(setmeal1)
                        thulunch2.append(setmeal1)
                        thulunch3.append(setmeal1)
                        thulunch4.append(setmeal1)
                        thulunch5.append(setmeal1)
                        thulunch6.append(setmeal1)
                        # recipe list handling
                        every_gen_entree.extend(thulunch1)
                        every_gen_entree.extend(thulunch2)
                        every_gen_entree.extend(thulunch3)
                        every_gen_entree.extend(thulunch4)
                        every_gen_entree.extend(thulunch5)
                        every_gen_entree.extend(thulunch6)
                    if thu_l == 0:
                        thursdaylunch(sidecount, ent, thulunch1, thulunch2, thulunch3, thulunch4, thulunch5, thulunch6)

                    if thu_d != 0:
                        setmeal2 = working_week.get("thu", {}).get("dinner")
                        thudinner1.append(setmeal2)
                        thudinner2.append(setmeal2)
                        thudinner3.append(setmeal2)
                        thudinner4.append(setmeal2)
                        thudinner5.append(setmeal2)
                        thudinner6.append(setmeal2)
                        # recipe list handling
                        every_gen_entree.extend(thudinner1)
                        every_gen_entree.extend(thudinner2)
                        every_gen_entree.extend(thudinner3)
                        every_gen_entree.extend(thudinner4)
                        every_gen_entree.extend(thudinner5)
                        every_gen_entree.extend(thudinner6)
                    if thu_d == 0:
                        thursdaydinner(sidecount, ent, thudinner1, thudinner2, thudinner3, thudinner4, thudinner5,
                                       thudinner6)

                    week_one.update({setdaysday: {"Thursday > breakfast": thubreak1, "lunch": thulunch1, "dinner": thudinner1}})
                    week_two.update({setdaysday: {"Thursday > breakfast": thubreak2, "lunch": thulunch2, "dinner": thudinner2}})
                    week_three.update({setdaysday: {"Thursday > breakfast": thubreak3, "lunch": thulunch3, "dinner": thudinner3}})
                    week_four.update({setdaysday: {"Thursday > breakfast": thubreak4, "lunch": thulunch4, "dinner": thudinner4}})
                    week_five.update({setdaysday: {"Thursday > breakfast": thubreak5, "lunch": thulunch5, "dinner": thudinner5}})
                    week_six.update({setdaysday: {"Thursday > breakfast": thubreak6, "lunch": thulunch6, "dinner": thudinner6}})


                # begin generator for friday
                fribreakfast = 0
                fri_l = working_week.get("fri", {}).get("lunch")
                fri_d = working_week.get("fri", {}).get("dinner")
                if startweekfri == "y":
                    setdaysday = "fri"
                    if fribreakfast == 0:
                        print("generating friday")
                        fridaybreak(sidecount, fribreak1, fribreak2, fribreak3, fribreak4, fribreak5, fribreak6)

                    if fri_l != 0 and not "fish friday":
                        setmeal1 = working_week.get("fri", {}).get("lunch")
                        frilunch1.append(setmeal1)
                        frilunch2.append(setmeal1)
                        frilunch3.append(setmeal1)
                        frilunch4.append(setmeal1)
                        frilunch5.append(setmeal1)
                        frilunch6.append(setmeal1)
                        # recipe list handling
                        every_gen_entree.extend(frilunch1)
                        every_gen_entree.extend(frilunch2)
                        every_gen_entree.extend(frilunch3)
                        every_gen_entree.extend(frilunch4)
                        every_gen_entree.extend(frilunch5)
                        every_gen_entree.extend(frilunch6)
                    if fri_l == "fish friday":
                        dictlength = (len(entree[7]))
                        frilunch1.append(entree.get(7, {}).get(random.randint(1, dictlength)))
                        frilunch2.append(entree.get(7, {}).get(random.randint(1, dictlength)))
                        frilunch3.append(entree.get(7, {}).get(random.randint(1, dictlength)))
                        frilunch4.append(entree.get(7, {}).get(random.randint(1, dictlength)))
                        frilunch5.append(entree.get(7, {}).get(random.randint(1, dictlength)))
                        frilunch6.append(entree.get(7, {}).get(random.randint(1, dictlength)))
                        # recipe list handling
                        every_gen_entree.extend(frilunch1)
                        every_gen_entree.extend(frilunch2)
                        every_gen_entree.extend(frilunch3)
                        every_gen_entree.extend(frilunch4)
                        every_gen_entree.extend(frilunch5)
                        every_gen_entree.extend(frilunch6)
                    if fri_l == 0:
                        fridaylunch(sidecount, ent, frilunch1, frilunch2, frilunch3, frilunch4, frilunch5, frilunch6)

                    if fri_d != 0 and not "fish friday":
                        setmeal2 = working_week.get("fri", {}).get("dinner")
                        fridinner1.append(setmeal2)
                        fridinner2.append(setmeal2)
                        fridinner3.append(setmeal2)
                        fridinner4.append(setmeal2)
                        fridinner5.append(setmeal2)
                        fridinner6.append(setmeal2)
                        # recipe list handling
                        every_gen_entree.extend(fridinner1)
                        every_gen_entree.extend(fridinner2)
                        every_gen_entree.extend(fridinner3)
                        every_gen_entree.extend(fridinner4)
                        every_gen_entree.extend(fridinner5)
                        every_gen_entree.extend(fridinner6)
                    if fri_d == "fish friday":
                        dictlength = (len(entree[7]))
                        fridinner1.append(entree.get(7, {}).get(random.randint(1, dictlength)))
                        fridinner2.append(entree.get(7, {}).get(random.randint(1, dictlength)))
                        fridinner3.append(entree.get(7, {}).get(random.randint(1, dictlength)))
                        fridinner4.append(entree.get(7, {}).get(random.randint(1, dictlength)))
                        fridinner5.append(entree.get(7, {}).get(random.randint(1, dictlength)))
                        fridinner6.append(entree.get(7, {}).get(random.randint(1, dictlength)))
                        # recipe list handling
                        every_gen_entree.extend(fridinner1)
                        every_gen_entree.extend(fridinner2)
                        every_gen_entree.extend(fridinner3)
                        every_gen_entree.extend(fridinner4)
                        every_gen_entree.extend(fridinner5)
                        every_gen_entree.extend(fridinner6)
                    if fri_d == 0:
                        fridaydinner(sidecount, ent, fridinner1, fridinner2, fridinner3, fridinner4, fridinner5,
                                     fridinner6)

                    week_one.update({setdaysday: {"Friday > breakfast": fribreak1, "lunch": frilunch1, "dinner": fridinner1}})
                    week_two.update({setdaysday: {"Friday > breakfast": fribreak2, "lunch": frilunch2, "dinner": fridinner2}})
                    week_three.update({setdaysday: {"Friday > breakfast": fribreak3, "lunch": frilunch3, "dinner": fridinner3}})
                    week_four.update({setdaysday: {"Friday > breakfast": fribreak4, "lunch": frilunch4, "dinner": fridinner4}})
                    week_five.update({setdaysday: {"Friday > breakfast": fribreak5, "lunch": frilunch5, "dinner": fridinner5}})
                    week_six.update({setdaysday: {"Friday > breakfast": fribreak6, "lunch": frilunch6, "dinner": fridinner6}})


                # begin generator for saturday
                satbreakfast = 0
                sat_l = working_week.get("sat", {}).get("lunch")
                sat_d = working_week.get("sat", {}).get("dinner")
                if startweeksat == "y":
                    setdaysday = "sat"
                    if satbreakfast == 0:
                        print("generating saturday")
                        saturdaybreak(sidecount, satbreak1, satbreak2, satbreak3, satbreak4, satbreak5, satbreak6)

                    if sat_l != 0:
                        setmeal1 = working_week.get("sat", {}).get("lunch")
                        satlunch1.append(setmeal1)
                        satlunch2.append(setmeal1)
                        satlunch3.append(setmeal1)
                        satlunch4.append(setmeal1)
                        satlunch5.append(setmeal1)
                        satlunch6.append(setmeal1)
                        # recipe list handling
                        every_gen_entree.extend(satlunch1)
                        every_gen_entree.extend(satlunch2)
                        every_gen_entree.extend(satlunch3)
                        every_gen_entree.extend(satlunch4)
                        every_gen_entree.extend(satlunch5)
                        every_gen_entree.extend(satlunch6)
                    if sat_l == 0:
                        saturdaylunch(sidecount, ent, satlunch1, satlunch2, satlunch3, satlunch4, satlunch5, satlunch6)

                    if sat_d != 0:
                        setmeal2 = working_week.get("sat", {}).get("dinner")
                        satdinner1.append(setmeal2)
                        satdinner2.append(setmeal2)
                        satdinner3.append(setmeal2)
                        satdinner4.append(setmeal2)
                        satdinner5.append(setmeal2)
                        satdinner6.append(setmeal2)
                        # recipe list handling
                        every_gen_entree.extend(satdinner1)
                        every_gen_entree.extend(satdinner2)
                        every_gen_entree.extend(satdinner3)
                        every_gen_entree.extend(satdinner4)
                        every_gen_entree.extend(satdinner5)
                        every_gen_entree.extend(satdinner6)
                    if sat_d == 0:
                        saturdaydinner(sidecount, ent, satdinner1, satdinner2, satdinner3, satdinner4, satdinner5,
                                       satdinner6)

                    week_one.update({setdaysday: {"Saturday > breakfast": satbreak1, "lunch": satlunch1, "dinner": satdinner1}})
                    week_two.update({setdaysday: {"Saturday > breakfast": satbreak2, "lunch": satlunch2, "dinner": satdinner2}})
                    week_three.update({setdaysday: {"Saturday > breakfast": satbreak3, "lunch": satlunch3, "dinner": satdinner3}})
                    week_four.update({setdaysday: {"Saturday > breakfast": satbreak4, "lunch": satlunch4, "dinner": satdinner4}})
                    week_five.update({setdaysday: {"Saturday > breakfast": satbreak5, "lunch": satlunch5, "dinner": satdinner5}})
                    week_six.update({setdaysday: {"Saturday > breakfast": satbreak6, "lunch": satlunch6, "dinner": satdinner6}})


                # begin generator for sunday
                sunbreakfast = 0
                sun_l = working_week.get("sun", {}).get("lunch")
                sun_d = working_week.get("sun", {}).get("dinner")
                if startweeksun == "y":
                    setdaysday = "sun"
                    if sunbreakfast == 0:
                        print("generating sunday")
                        sundaybreak(sidecount, sunbreak1, sunbreak2, sunbreak3, sunbreak4, sunbreak5, sunbreak6)

                    if sun_l != 0:
                        setmeal1 = working_week.get("sun", {}).get("lunch")
                        sunlunch1.append(setmeal1)
                        sunlunch2.append(setmeal1)
                        sunlunch3.append(setmeal1)
                        sunlunch4.append(setmeal1)
                        sunlunch5.append(setmeal1)
                        sunlunch6.append(setmeal1)
                        # recipe list handling
                        every_gen_entree.extend(sunlunch1)
                        every_gen_entree.extend(sunlunch2)
                        every_gen_entree.extend(sunlunch3)
                        every_gen_entree.extend(sunlunch4)
                        every_gen_entree.extend(sunlunch5)
                        every_gen_entree.extend(sunlunch6)
                    if sun_l == 0:
                        sundaylunch(sidecount, ent, sunlunch1, sunlunch2, sunlunch3, sunlunch4, sunlunch5, sunlunch6)

                    if sun_d != 0:
                        setmeal2 = working_week.get("sun", {}).get("dinner")
                        sundinner1.append(setmeal2)
                        sundinner2.append(setmeal2)
                        sundinner3.append(setmeal2)
                        sundinner4.append(setmeal2)
                        sundinner5.append(setmeal2)
                        sundinner6.append(setmeal2)
                        # recipe list handling
                        every_gen_entree.extend(sundinner1)
                        every_gen_entree.extend(sundinner2)
                        every_gen_entree.extend(sundinner3)
                        every_gen_entree.extend(sundinner4)
                        every_gen_entree.extend(sundinner5)
                        every_gen_entree.extend(sundinner6)
                    if sun_d == 0:
                        sundaydinner(sidecount, ent, sundinner1, sundinner2, sundinner3, sundinner4, sundinner5,
                                     sundinner6)

                    week_one.update({setdaysday: {"Sunday > breakfast": sunbreak1, "lunch": sunlunch1, "dinner": sundinner1}})
                    week_two.update({setdaysday: {"Sunday > breakfast": sunbreak2, "lunch": sunlunch2, "dinner": sundinner2}})
                    week_three.update({setdaysday: {"Sunday > breakfast": sunbreak3, "lunch": sunlunch3, "dinner": sundinner3}})
                    week_four.update({setdaysday: {"Sunday > breakfast": sunbreak4, "lunch": sunlunch4, "dinner": sundinner4}})
                    week_five.update({setdaysday: {"Sunday > breakfast": sunbreak5, "lunch": sunlunch5, "dinner": sundinner5}})
                    week_six.update({setdaysday: {"Sunday > breakfast": sunbreak6, "lunch": sunlunch6, "dinner": sundinner6}})




                    #begin output formatting and display
                    break

            while daysweekcountdown > 0:
                if stday=="mon":
                    print(tabulate(week_one["mon"],headers="keys",tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    print(tabulate(week_one["tue"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    print(tabulate(week_one["wed"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    print(tabulate(week_one["thu"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    print(tabulate(week_one["fri"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    print(tabulate(week_one["sat"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    print(tabulate(week_one["sun"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                else:
                    pass

                if stday == "tue":
                    print(tabulate(week_one["tue"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    print(tabulate(week_one["wed"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    print(tabulate(week_one["thu"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    print(tabulate(week_one["fri"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    print(tabulate(week_one["sat"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    print(tabulate(week_one["sun"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                else:
                    pass

                if stday == "wed":
                    print(tabulate(week_one["wed"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    print(tabulate(week_one["thu"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    print(tabulate(week_one["fri"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    print(tabulate(week_one["sat"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    print(tabulate(week_one["sun"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                else:
                    pass

                if stday == "thu":
                    print(tabulate(week_one["thu"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    print(tabulate(week_one["fri"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    print(tabulate(week_one["sat"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    print(tabulate(week_one["sun"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                else:
                    pass

                if stday == "fri":
                    print(tabulate(week_one["fri"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    print(tabulate(week_one["sat"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    print(tabulate(week_one["sun"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                else:
                    pass

                if stday == "sat":
                    print(tabulate(week_one["sat"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    print(tabulate(week_one["sun"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                else:
                    pass

                if stday == "sun":
                    print(tabulate(week_one["sun"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                else:
                    pass
                #start week two
                while daysweekcountdown > 0:

                    if daysweekcountdown <= 0: break
                    print(tabulate(week_two["mon"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(tabulate(week_two["tue"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(tabulate(week_two["wed"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(tabulate(week_two["thu"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(tabulate(week_two["fri"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(tabulate(week_two["sat"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(tabulate(week_two["sun"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(daysweekcountdown)
                    print(tabulate(week_three["mon"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(tabulate(week_three["tue"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(tabulate(week_three["wed"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(tabulate(week_three["thu"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(tabulate(week_three["fri"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(tabulate(week_three["sat"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(tabulate(week_three["sun"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(tabulate(week_four["mon"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(tabulate(week_four["tue"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(tabulate(week_four["wed"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(tabulate(week_four["thu"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(tabulate(week_four["fri"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(tabulate(week_four["sat"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(tabulate(week_four["sun"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(tabulate(week_five["mon"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(tabulate(week_five["tue"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(tabulate(week_five["wed"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(tabulate(week_five["thu"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(tabulate(week_five["fri"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(tabulate(week_five["sat"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(tabulate(week_five["sun"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(tabulate(week_six["mon"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(tabulate(week_six["tue"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(tabulate(week_six["wed"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(tabulate(week_six["thu"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(tabulate(week_six["fri"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(tabulate(week_six["sat"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(tabulate(week_six["sun"], headers="keys", tablefmt="outline"),file=mpf)
                    daysweekcountdown -=1
                    if daysweekcountdown <= 0: break
                    print(daysweekcountdown)
                    print(type(daysweekcountdown))

                print(every_gen_entree,'full list')

                if daysweekcountdown==0:
                    monbreak1.clear()
                    monlunch1.clear()
                    mondinner1.clear()
                    tuebreak1.clear()
                    tuelunch1.clear()
                    tuedinner1.clear()
                    wedbreak1.clear()
                    wedlunch1.clear()
                    weddinner1.clear()
                    thubreak1.clear()
                    thulunch1.clear()
                    thudinner1.clear()
                    fribreak1.clear()
                    frilunch1.clear()
                    fridinner1.clear()
                    satbreak1.clear()
                    satlunch1.clear()
                    satdinner1.clear()
                    sunbreak1.clear()
                    sunlunch1.clear()
                    sundinner1.clear()
                    monbreak2.clear()
                    monlunch2.clear()
                    mondinner2.clear()
                    tuebreak2.clear()
                    tuelunch2.clear()
                    tuedinner2.clear()
                    wedbreak2.clear()
                    wedlunch2.clear()
                    weddinner2.clear()
                    thubreak2.clear()
                    thulunch2.clear()
                    thudinner2.clear()
                    fribreak2.clear()
                    frilunch2.clear()
                    fridinner2.clear()
                    satbreak2.clear()
                    satlunch2.clear()
                    satdinner2.clear()
                    sunbreak2.clear()
                    sunlunch2.clear()
                    sundinner2.clear()
                    monbreak3.clear()
                    monlunch3.clear()
                    mondinner3.clear()
                    tuebreak3.clear()
                    tuelunch3.clear()
                    tuedinner3.clear()
                    wedbreak3.clear()
                    wedlunch3.clear()
                    weddinner3.clear()
                    thubreak3.clear()
                    thulunch3.clear()
                    thudinner3.clear()
                    fribreak3.clear()
                    frilunch3.clear()
                    fridinner3.clear()
                    satbreak3.clear()
                    satlunch3.clear()
                    satdinner3.clear()
                    sunbreak3.clear()
                    sunlunch3.clear()
                    sundinner3.clear()
                    monbreak4.clear()
                    monlunch4.clear()
                    mondinner4.clear()
                    tuebreak4.clear()
                    tuelunch4.clear()
                    tuedinner4.clear()
                    wedbreak4.clear()
                    wedlunch4.clear()
                    weddinner4.clear()
                    thubreak4.clear()
                    thulunch4.clear()
                    thudinner4.clear()
                    fribreak4.clear()
                    frilunch4.clear()
                    fridinner4.clear()
                    satbreak4.clear()
                    satlunch4.clear()
                    satdinner4.clear()
                    sunbreak4.clear()
                    sunlunch4.clear()
                    sundinner4.clear()
                    monbreak5.clear()
                    monlunch5.clear()
                    mondinner5.clear()
                    tuebreak5.clear()
                    tuelunch5.clear()
                    tuedinner5.clear()
                    wedbreak5.clear()
                    wedlunch5.clear()
                    weddinner5.clear()
                    thubreak5.clear()
                    thulunch5.clear()
                    thudinner5.clear()
                    fribreak5.clear()
                    frilunch5.clear()
                    fridinner5.clear()
                    satbreak5.clear()
                    satlunch5.clear()
                    satdinner5.clear()
                    sunbreak5.clear()
                    sunlunch5.clear()
                    sundinner5.clear()
                    monbreak6.clear()
                    monlunch6.clear()
                    mondinner6.clear()
                    tuebreak6.clear()
                    tuelunch6.clear()
                    tuedinner6.clear()
                    wedbreak6.clear()
                    wedlunch6.clear()
                    weddinner6.clear()
                    thubreak6.clear()
                    thulunch6.clear()
                    thudinner6.clear()
                    fribreak6.clear()
                    frilunch6.clear()
                    fridinner6.clear()
                    satbreak6.clear()
                    satlunch6.clear()
                    satdinner6.clear()
                    sunbreak6.clear()
                    sunlunch6.clear()
                    sundinner6.clear()
                    mpf.close
                    #RecipeBookBuilder.recipe_book_builder(every_gen_entree, every_gen_breakfast, ent_rec_comp, side_rec_comp, brd_rec_comp,brk_rec_comp, salad_rec_comp, mex_rec_comp, fsh_rec_comp, des_rec_comp)
                    return (every_gen_entree, every_gen_breakfast, ent_rec_comp, side_rec_comp, brd_rec_comp,
                            brk_rec_comp, salad_rec_comp, mex_rec_comp, fsh_rec_comp, des_rec_comp)














class LoginWindow(Screen):
    def trigger_libraries(self):
        build_dictionary()


class PageOne(Screen):
    daysinput = ObjectProperty(None)

    def daycaller(self,daysinput):
        try:
            global days
            days=int(self.daysinput.text)
            if days not in range(7,31):
                popupWindow = EntreeLimitPop()
                popupWindow.open()
            if days in range(7,31):
                self.parent.current = "Day Week"
        except:
            popupWindow = EntreeLimitPop()
            popupWindow.open()
        return days

class DayWeek(Screen):
    startweekinput=ObjectProperty(None)
    global stday
    def monday(self):
        stday="mon"
        startwkmath(stday,daysweekgen,dysweekc,stweek,daystp,totaldays,days)
    def tuesday(self):
        stday="tue"
        startwkmath(stday, daysweekgen, dysweekc, stweek, daystp, totaldays, days)
    def wednesday(self):
        stday="wed"
        startwkmath(stday, daysweekgen, dysweekc, stweek, daystp, totaldays, days)
    def thursday(self):
        stday="thu"
        startwkmath(stday, daysweekgen, dysweekc, stweek, daystp, totaldays, days)
    def friday(self):
        stday="fri"
        startwkmath(stday, daysweekgen, dysweekc, stweek, daystp, totaldays, days)
    def saturday(self):
        stday="sat"
        startwkmath(stday, daysweekgen, dysweekc, stweek, daystp, totaldays, days)
    def sunday(self):
        stday="sun"
        startwkmath(stday, daysweekgen, dysweekc, stweek, daystp, totaldays, days)
        return stday

class EntSideGen(Screen):
    entreequest = ObjectProperty(None)
    sidequest = ObjectProperty(None)
    def entsidestrigger(self):
        try:
            global entret
            global sideret
            entret = int(self.entreequest.text)
            sideret = int(self.sidequest.text)
            if entret != 1 or sideret not in range(1,4):
                popupWindow = SidesEntreesPop()
                popupWindow.open()
            if entret == 1 and sideret in range(1,4):
                entsidesmath(ent, sidecount,entret,sideret,EntSideGen)
                self.parent.current = "FishFrQuest"
        except:
            popupWindow = SidesEntreesPop()
            popupWindow.open()
        return  entret,sideret
class FishFrQuest(Screen):
    pass
class FishFrYes(Screen):
    global fishfrml
    def fishlunch(self):
        fishfrml="lunch"
        fishfrsetup(fishfrml, setdays)
        return fishfrml
    def fishdinner(self):
        fishfrml="dinner"
        fishfrsetup(fishfrml, setdays)
        return fishfrml
    def fishallday(self):
        fishfrml="allday"
        fishfrsetup(fishfrml, setdays)
        return fishfrml
class TacoTueQuest(Screen):
    pass
class TacoTueYes(Screen):
    global tacotml
    def tacolunch(self):
        tacotml="lunch"
        tacotsetup(tacotml, setdays)
        return fishfrml
    def tacodinner(self):
        tacotml="dinner"
        tacotsetup(tacotml, setdays)
        return fishfrml
    def tacoallday(self):
        tacotml="allday"
        tacotsetup(tacotml, setdays)
        return tacotml
class SetDaysQuest(Screen):
    pass
class SetDaysDay1(Screen):
    global daysetup
    global daysetupconv
    doodydoo= ObjectProperty(None)
    def monday(self):
        global daysetup
        daysetup="mon"
    def tuesday(self):
        global daysetup
        daysetup = "tue"
    def wednesday(self):
        global daysetup
        daysetup = "wed"
    def thursday(self):
        global daysetup
        daysetup = "thu"
    def friday(self):
        global daysetup
        daysetup = "fri"
    def saturday(self):
        global daysetup
        daysetup = "sat"
    def sunday(self):
        global daysetup
        daysetup = "sun"
        return daysetup

class SetDaysMealL1(Screen):
    setentree1 = ObjectProperty(None)
    setside11 = ObjectProperty(None)
    setside12 = ObjectProperty(None)
    setside13 = ObjectProperty(None)
    global sete1
    global sets11
    global sets12
    global sets13
    def setdaysmlL1func(self):
        sete1=(self.setentree1.text)
        sets11 =(self.setside11.text)
        sets12 =(self.setside12.text)
        sets13 =(self.setside13.text)
        print(sete1)
        print(sets11)
        print(sets12)
        print(sets13)
        setday1lunch(setdaymeallunch, sete1, sets11, sets12, sets13)
        return
class SetDaysMealD1(Screen):
    setentreed1 = ObjectProperty(None)
    setsided11 = ObjectProperty(None)
    setsided12 = ObjectProperty(None)
    setsided13 = ObjectProperty(None)
    global seted1
    global setsd11
    global setsd12
    global setsd13
    def setdaysmlD1func(self):
        seted1=(self.setentreed1.text)
        setsd11 =(self.setsided11.text)
        setsd12 =(self.setsided12.text)
        setsd13 =(self.setsided13.text)
        print(seted1)
        print(setsd11)
        print(setsd12)
        print(setsd13)
        setday1dinner(setdaymeallunch,seted1,setsd11,setsd12,setsd13,setdaymealdinner,setdays,daysetup,setdaysday)
        return
class SetDaysQuest2(Screen):
    pass
class SetDaysDay2(Screen):
    global daysetup2
    global daysetupconv2
    def monday(self):
        global daysetup2
        daysetup2 ="mon"
    def tuesday(self):
        global daysetup2
        daysetup2 = "tue"
    def wednesday(self):
        global daysetup2
        daysetup2 = "wed"
    def thursday(self):
        global daysetup2
        daysetup2 = "thu"
    def friday(self):
        global daysetup2
        daysetup2 = "fri"
    def saturday(self):
        global daysetup2
        daysetup2 = "sat"
    def sunday(self):
        global daysetup2
        daysetup2 = "sun"
        return daysetup2, daysetupconv2
class SetDaysMealL2(Screen):
    setentree2 = ObjectProperty(None)
    setside21 = ObjectProperty(None)
    setside22 = ObjectProperty(None)
    setside23 = ObjectProperty(None)
    global sete2
    global sets21
    global sets22
    global sets23
    def setdaysmlL2func(self):
        sete2 = (self.setentree2.text)
        sets21 = (self.setside21.text)
        sets22 = (self.setside22.text)
        sets23 = (self.setside23.text)
        print(sete2)
        print(sets21)
        print(sets22)
        print(sets23)
        setday2lunch(setdaymeallunch2, sete2, sets21, sets22, sets23)
        return
class SetDaysMealD2(Screen):
    setentreed2 = ObjectProperty(None)
    setsided21 = ObjectProperty(None)
    setsided22 = ObjectProperty(None)
    setsided23 = ObjectProperty(None)
    global seted2
    global setsd21
    global setsd22
    global setsd23

    def setdaysmlD2func(self):
        seted2 = (self.setentreed2.text)
        setsd21 = (self.setsided21.text)
        setsd22 = (self.setsided22.text)
        setsd23 = (self.setsided23.text)
        print(seted2)
        print(setsd21)
        print(setsd22)
        print(setsd23)
        setday2dinner(setdaymeallunch2, seted2, setsd21, setsd22, setsd23, setdaymealdinner2, setdays, setdaysday,daysetup2)
        return
class GeneratorScreen(Screen):
    def trigger_gen(self,**kwargs):
        generator_randomizer(setdays,daysweekgen,gendays,stday,days,
    week_one,week_two,week_three,week_four,week_five,week_six,working_week,
        startweekmon,monlunch1,monlunch2,monlunch3,monlunch4,monlunch5
    ,monlunch6,mondaybreak,monbreak1, monbreak2, monbreak3, monbreak4,
    monbreak5, monbreak6,mondinner1, mondinner2, mondinner3, mondinner4, mondinner5,mondinner6,
    startweektue,startweekwed,startweekthu,startweekfri,startweeksat,startweeksun,
    tuebreak1, tuebreak2, tuebreak3, tuebreak4, tuebreak5, tuebreak6,tuelunch1, tuelunch2,
    tuelunch3, tuelunch4, tuelunch5, tuelunch6,tuedinner1, tuedinner2, tuedinner3,
    tuedinner4, tuedinner5,tuedinner6,wedbreak1, wedbreak2, wedbreak3, wedbreak4, wedbreak5, wedbreak6,
    wedlunch1, wedlunch2, wedlunch3, wedlunch4, wedlunch5, wedlunch6,weddinner1, weddinner2, weddinner3,
    weddinner4, weddinner5,weddinner6,thubreak1, thubreak2, thubreak3, thubreak4, thubreak5, thubreak6,
    thulunch1, thulunch2, thulunch3, thulunch4, thulunch5, thulunch6,thudinner1, thudinner2, thudinner3,
    thudinner4, thudinner5,thudinner6,fribreak1, fribreak2, fribreak3, fribreak4, fribreak5, fribreak6,
    frilunch1, frilunch2, frilunch3, frilunch4, frilunch5, frilunch6,fridinner1, fridinner2, fridinner3,
    fridinner4, fridinner5,fridinner6,satbreak1, satbreak2, satbreak3, satbreak4, satbreak5, satbreak6,
    satlunch1, satlunch2, satlunch3, satlunch4, satlunch5, satlunch6,satdinner1, satdinner2, satdinner3,
    satdinner4, satdinner5,satdinner6,sunbreak1, sunbreak2, sunbreak3, sunbreak4, sunbreak5, sunbreak6,
    sunlunch1, sunlunch2, sunlunch3, sunlunch4, sunlunch5, sunlunch6,sundinner1, sundinner2, sundinner3,
    sundinner4, sundinner5,sundinner6,mondaylunch,sidecount,ent,sideret,entret)
        return

class AddNewItem(Screen):
    pass
class AddNewEntree(Screen):
    addentree=ObjectProperty(None)
    def addentree_trigger(self):
        global addnwentree
        addnwentree=(self.addentree.text)
        add_new_entree(entree, entreeload,addnwentree)
        return
class AddNewSide(Screen):
    addside=ObjectProperty(None)
    def addside_trigger(self):
        global addnwside
        addnwside=(self.addside.text)
        add_new_side(side, sideload,addnwside)
        return
class AddNewBrd(Screen):
    addbrd=ObjectProperty(None)
    def addbrd_trigger(self):
        global addnwbrd
        addnwbrd=(self.addbrd.text)
        add_new_brd(side, breadload,addnwbrd)
        return
class AddNewSld(Screen):
    addsld=ObjectProperty(None)
    def addsld_trigger(self):
        global addnwsld
        addnwsld=(self.addsld.text)
        add_new_sld(side, saladload,addnwsld)
        return
class AddNewBrk(Screen):
    addbrk=ObjectProperty(None)
    def addbrk_trigger(self):
        global addnwbrk
        addnwbrk=(self.addbrk.text)
        add_new_brk(breakfastload,addnwbrk,entree)
        return
class AddNewDes(Screen):
    adddes=ObjectProperty(None)
    def adddes_trigger(self):
        global addnwdes
        addnwdes=(self.adddes.text)
        add_new_des(dessertload,addnwdes,dessert)
        return
class AddNewMex(Screen):
    addmex=ObjectProperty(None)
    def addmex_trigger(self):
        global addnwmex
        addnwmex=(self.addmex.text)
        add_new_mex(mexicanfdload,addnwmex,entree)
        return
class AddNewFsh(Screen):
    addfsh=ObjectProperty(None)
    def addfsh_trigger(self):
        global addnwfsh
        addnwfsh=(self.addfsh.text)
        add_new_fsh(fishload,addnwfsh,entree)
        return
class SaveSlotSelect(Screen):
    def save_functions1(self):
        path = ".venv/"
        source = "Meal Plan Gen.txt"
        destination = "MP1.txt"
        dest = shutil.copyfile(source, destination)
        #this code handles converting the txt file to image for better format fit
        lexer = pygments.lexers.TextLexer()
        png = pygments.highlight(Path('MP1.txt').read_text(), lexer, ImageFormatter(line_numbers=False))
        Path('MP1.png').write_bytes(png)
        #this section will assign the generated recipe book to the meal plan
        path = ".venv/recipebooks"
        source = "recipebooks/workingrb.txt"
        destination = "recipebooks/mp1recbook.txt"
        dest = shutil.copyfile(source, destination)
        path = ".venv/recipebooks"
        source = "recipebooks/recbookrefwork.txt"
        destination = "recipebooks/mp1recbookref.txt"
        dest = shutil.copyfile(source, destination)
        return
    def save_functions2(self):
        path = ".venv/"
        source = "Meal Plan Gen.txt"
        destination = "MP2.txt"
        dest = shutil.copyfile(source, destination)
        # this code handles converting the txt file to image for better format fit
        lexer = pygments.lexers.TextLexer()
        png = pygments.highlight(Path('MP2.txt').read_text(), lexer, ImageFormatter(line_numbers=False))
        Path('MP2.png').write_bytes(png)
        # this section will assign the generated recipe book to the meal plan
        path = ".venv/recipebooks"
        source = "recipebooks/workingrb.txt"
        destination = "recipebooks/mp2recbook.txt"
        dest = shutil.copyfile(source, destination)
        path = ".venv/recipebooks"
        source = "recipebooks/recbookrefwork.txt"
        destination = "recipebooks/mp2recbookref.txt"
        dest = shutil.copyfile(source, destination)
        return
    def save_functions3(self):
        path = ".venv/"
        source = "Meal Plan Gen.txt"
        destination = "MP3.txt"
        dest = shutil.copyfile(source, destination)
        # this code handles converting the txt file to image for better format fit
        lexer = pygments.lexers.TextLexer()
        png = pygments.highlight(Path('MP3.txt').read_text(), lexer, ImageFormatter(line_numbers=False))
        Path('MP3.png').write_bytes(png)
        # this section will assign the generated recipe book to the meal plan
        path = ".venv/recipebooks"
        source = "recipebooks/workingrb.txt"
        destination = "recipebooks/mp3recbook.txt"
        dest = shutil.copyfile(source, destination)
        path = ".venv/recipebooks"
        source = "recipebooks/recbookrefwork.txt"
        destination = "recipebooks/mp3recbookref.txt"
        dest = shutil.copyfile(source, destination)
        return
    def save_functions4(self):
        path = ".venv/"
        source = "Meal Plan Gen.txt"
        destination = "MP4.txt"
        dest = shutil.copyfile(source, destination)
        # this code handles converting the txt file to image for better format fit
        lexer = pygments.lexers.TextLexer()
        png = pygments.highlight(Path('MP4.txt').read_text(), lexer, ImageFormatter(line_numbers=False))
        Path('MP4.png').write_bytes(png)
        # this section will assign the generated recipe book to the meal plan
        path = ".venv/recipebooks"
        source = "recipebooks/workingrb.txt"
        destination = "recipebooks/mp4recbook.txt"
        dest = shutil.copyfile(source, destination)
        path = ".venv/recipebooks"
        source = "recipebooks/recbookrefwork.txt"
        destination = "recipebooks/mp4recbookref.txt"
        dest = shutil.copyfile(source, destination)
        return
    def save_functions5(self):
        path = ".venv/"
        source = "Meal Plan Gen.txt"
        destination = "MP5.txt"
        dest = shutil.copyfile(source, destination)
        # this code handles converting the txt file to image for better format fit
        lexer = pygments.lexers.TextLexer()
        png = pygments.highlight(Path('MP5.txt').read_text(), lexer, ImageFormatter(line_numbers=False))
        Path('MP5.png').write_bytes(png)
        # this section will assign the generated recipe book to the meal plan
        path = ".venv/recipebooks"
        source = "recipebooks/workingrb.txt"
        destination = "recipebooks/mp5recbook.txt"
        dest = shutil.copyfile(source, destination)
        path = ".venv/recipebooks"
        source = "recipebooks/recbookrefwork.txt"
        destination = "recipebooks/mp5recbookref.txt"
        dest = shutil.copyfile(source, destination)
        return

class MealCheck(Screen):
    pass

class ViewMP1(Screen):
    img_source = StringProperty("MP1.png")
    def rld_img(self,**kwargs):
        self.img_source="fnv3.jpg"
        self.img_source = "MP1.png"
        return self.img_source
class ViewMP2(Screen):
    img_source2 = StringProperty("MP2.png")
    def rld_img(self, **kwargs):
        self.img_source2 = "fnv3.jpg"
        self.img_source2 = "MP2.png"
        return self.img_source2
class ViewMP3(Screen):
    img_source3 = StringProperty("MP3.png")
    def rld_img(self, **kwargs):
        self.img_source3 = "fnv3.jpg"
        self.img_source3 = "MP3.png"
        return self.img_source3
class ViewMP4(Screen):
    img_source4 = StringProperty("MP4.png")
    def rld_img(self, **kwargs):
        self.img_source4 = "fnv3.jpg"
        self.img_source4 = "MP4.png"
        return self.img_source4
class ViewMP5(Screen):
    img_source5 = StringProperty("MP5.png")
    def rld_img(self, **kwargs):
        self.img_source5 = "fnv3.jpg"
        self.img_source5 = "MP5.png"
        return self.img_source5
class HelpScreen(Screen):
    def displaytxt1(self):
        with open("Help.txt","r")as help:
            helpr=str(help.read())
            self.ids.textview.text=helpr
class WebScraperConfig(Screen):
    scraped_item=""
    scraped_item_select=""
    scraped_item_ent=ObjectProperty()
    scraped_item_side = ObjectProperty()
    scraped_item_dess = ObjectProperty()
    scraped_item_brk = ObjectProperty()
    scraped_item_brd = ObjectProperty()
    scraped_item_fsh = ObjectProperty()
    scraped_item_mxf = ObjectProperty()
    scraped_item_sld = ObjectProperty()
    def set_scraper_ent(self,scraped_item_sel):
        global scraped_item
        scraped_item=""
        if self.scraped_item_ent.text=="Entree":
            scraped_item = "entree"
            print("scraping for", scraped_item)
            return scraped_item
    def set_scraper_side(self, scraped_item_sel):
        global scraped_item
        scraped_item = ""
        if self.scraped_item_side.text=="Side":
            scraped_item = "side"
            print("scraping for", self.scraped_item)
            return scraped_item
    def set_scraper_dess(self, scraped_item_sel):
        global scraped_item
        scraped_item = ""
        if self.scraped_item_dess.text=="Dessert":
            scraped_item = "dessert"
            print("scraping for", self.scraped_item)
            return scraped_item
    def set_scraper_salad(self, scraped_item_sel):
        global scraped_item
        scraped_item = ""
        if self.scraped_item_sld.text=="Salad":
            scraped_item = "salad"
            print("scraping for", self.scraped_item)
            return scraped_item
    def set_scraper_brk(self, scraped_item_sel):
        global scraped_item
        scraped_item = ""
        if self.scraped_item_brk.text=="Breakfast":
            scraped_item = "breakfast"
            print("scraping for", self.scraped_item)
            return scraped_item
    def set_scraper_brd(self, scraped_item_sel):
        global scraped_item
        scraped_item = ""
        if self.scraped_item_brd.text=="Bread":
            scraped_item = "bread"
            print("scraping for", self.scraped_item)
            return scraped_item
    def set_scraper_mexfd(self, scraped_item_sel):
        global scraped_item
        scraped_item = ""
        if self.scraped_item_mxf.text=="Mexican Food":
            scraped_item = "mexicanfd"
            print("scraping for", self.scraped_item)
            return scraped_item
    def set_scraper_fish(self, scraped_item_sel):
        global scraped_item
        scraped_item = ""
        if self.scraped_item_fsh.text=="Fish":
            scraped_item = "fish"
            print("scraping for", self.scraped_item)
            return scraped_item



class WebScraperQty(Screen):

    scrape_amt=ObjectProperty()
    def scraper_amount(self):
        try:
            global scraped_request
            scraped_request=int(self.scrape_amt.text)
            if scraped_request > 100:
                popupWindow = WebScrapeLimitPop()
                popupWindow.open()
            if scraped_request in range (1,101):
                print(scraped_request)
                self.parent.current = "WebScraper"
        except:
            popupWindow = WebScrapeLimitPop()
            popupWindow.open()
        return scraped_request

class WebScraper(Screen,MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.start_clock()
        self.tick_loader=Clock.schedule_interval(self.prog_bar,.5)
        Clock.unschedule(self.tick_loader)
        self.p_bar_z=Clock.schedule_once(self.prog_bar_cleanup, 2)
        self.n_scr=Clock.schedule_once(self.nxt_scr,1)
        Clock.unschedule(self.n_scr)
    def webscrape_search(self,*args,**kwargs):
        print("starting scraper")
        print(scraped_item)
        print()
        global filter_15
        filter_15 = []
        filtered_entree=[]
        filtered_sides=[]
        filtered_desserts=[]
        filtered_break=[]
        filtered_salad=[]
        filtered_bread=[]
        filtered_mexfd=[]
        filtered_fish=[]

        urls_entree=["https://www.allrecipes.com/recipes/200/meat-and-poultry/beef/",
        "https://www.allrecipes.com/recipes/201/meat-and-poultry/chicken/",
        "https://www.allrecipes.com/recipes/205/meat-and-poultry/pork/"]
        urls_sides=["https://www.allrecipes.com/recipes/81/side-dish/"]
        urls_desserts=["https://www.allrecipes.com/recipes/79/desserts/"]
        urls_break=["https://www.allrecipes.com/recipes/78/breakfast-and-brunch/"]
        urls_salad=["https://www.allrecipes.com/recipes/96/salad/"]
        urls_bread=["https://www.allrecipes.com/recipes/156/bread/"]
        urls_mexfd=["https://www.allrecipes.com/recipes/728/world-cuisine/latin-american/mexican/"]
        urls_fish=["https://www.allrecipes.com/recipes/411/seafood/fish/"]
        url_list_step = 0
        url_pull = []
        index_loc_3 = 0
        url_search = len(urls_entree)
        if scraped_item=="entree":
            url_pull=urls_entree
        if scraped_item=="side":
            url_pull=urls_sides
        if scraped_item == "dessert":
            url_pull=urls_desserts
        if scraped_item == "bread":
            url_pull=urls_bread
        if scraped_item == "breakfast":
            url_pull=urls_break
        if scraped_item == "salad":
            url_pull=urls_salad
        if scraped_item == "fish":
            url_pull=urls_fish
        if scraped_item == "mexicanfd":
            url_pull=urls_mexfd
        for i in url_pull[:]:
            req_url = requests.get(i).text
            url_parsed = BeautifulSoup(req_url, "html.parser")
            # finds first instance of provided argument
            tags = json.loads(url_parsed.find("script", type="""application/ld+json""").text)
            filter_1 = tags[0]
            filter_2 = (filter_1.get("itemListElement"))
            filter_run_1_iter = (len(filter_2))
            filter_3 = ""
            filter_proc_run=1
            while filter_proc_run!=0:
                while filter_run_1_iter != 0:
                    filter_3 += str(filter_2[-1]).strip("{").strip("}")
                    filter_2.pop(-1)
                    filter_run_1_iter -= 1
                    filter_4 = filter_3.split(",")
                    filter_run_2_iter = len(filter_4)
                    filter_6 = []
                    index_loc2 = 0
                while filter_run_2_iter != 0:
                    filter_5 = filter_4[-1]
                    if len(filter_5) <= 29:
                        filter_4.pop(-1)
                        filter_run_2_iter -= 1
                        index_loc2 = +1
                    if len(filter_5) >= 30:
                        filter_6.append(filter_5)
                        filter_4.pop(-1)
                        filter_run_2_iter -= 1
                        index_loc2 = +1
                        filter_run_3_iter = len(filter_6)
                        while filter_run_3_iter != 0:
                            filter_7 = filter_6[-1]
                            filter_6.pop(-1)
                            filter_8 = filter_7.replace("""url""", ":")
                            filter_9 = filter_8.replace("""ListItem""", ":")
                            filter_10 = filter_9.replace("""@type""", ":")
                            filter_11 = filter_10.split(":")
                            filter_12 = (filter_11[2], filter_11[3])
                            filter_13 = ":".join(filter_12)
                            filter_14 = filter_13.replace("'", "")
                            filter_15.append(filter_14)
                            filter_run_3_iter -= 1
                            filter_proc_run=0
                            url_search-=1
            self.secondary_url_filter(filter_15)
        return
    def secondary_url_filter(self,filter_15):
        global cleaned_url_list
        global urls_pre_filter1
        self.urls_pre_filter1=[]
        cleaned_url_list = []
        un_used_urls=[]
        with open("datafiles/usedurls1.txt","r")as prev_urls:
            urls_preload=prev_urls.readlines()
            if len(urls_preload) !=0:
                self.urls_pre_filter1=urls_preload[0]
                self.urls_pre_filter1=self.urls_pre_filter1.split(",")
                for url_comp in filter_15:
                    if url_comp not in self.urls_pre_filter1:
                        un_used_urls.append(url_comp)
                for sec_filtering in un_used_urls:
                    if sec_filtering.find("https://www.allrecipes.com") == True:
                        cleaned_url_list.append(sec_filtering)
                        print("ran url prefilter")
            elif len(urls_preload)==0:
                for sec_filtering in filter_15:
                    if sec_filtering.find("https://www.allrecipes.com")==True:
                        cleaned_url_list.append(sec_filtering)
        prev_urls.close()

        self.webscrape_process(scraped_request,scraper_m_filter,urls_pre_filter1)
        return self.urls_pre_filter1

    def prog_reset(self):
        self.progress_bar.value=0

    def prog_bar(self,*args,**kwargs):
        self.progress_bar.max=scraped_request
        self.progress_bar.value +=  1
        if self.progress_bar.value==self.progress_bar.max:
            Clock.unschedule(self.tick_loader)
            Clock.schedule_once(self.p_bar_z,2)
            Clock.schedule_once(self.n_scr,0)

        return self.ids.progress_bar.value
    def prog_bar_cleanup(self,*args,**kwargs):
        Clock.unschedule(self.p_bar_z)
        self.ids.progress_bar.value-=self.progress_bar.max

        if self.progress_bar.value==0:
            self.progress_bar.value = 0
            print(self.progress_bar.value)
            print((self.progress_bar.max))
            print(scraped_request,"SR")
            print("ran reset")

        return self.ids.progress_bar.value
    def nxt_scr(self,*args):
        amountscrp=len(self.scraped_list)
        #WebScrapeReportPop.ids.scraperpt.text=f"You added {amountscrp} new meal items"
        #popupWindow = WebScrapeReportPop()
        #popupWindow.open()
        self.parent.current = "StartScreen"
        self.progress_bar.value = 1
        self.progress_bar.max=300
    def webscrape_process(self,scraped_request,scraper_m_filter,urls_pre_filter1,*args,**kwargs):

        global scraped_entree
        global scraped_item
        global scraped_entree
        global scraped_side
        global scraped_dessert
        global scraped_bread
        global scraped_salad
        global scraped_breakfast
        global scraped_mexicanfd
        global scraped_fish
        scraped_entree=[]
        scraped_side = []
        scraped_dessert = []
        scraped_bread = []
        scraped_salad = []
        scraped_breakfast = []
        scraped_mexicanfd = []
        scraped_fish = []
        self.scraped_list=[]
        self.scrape_prog=0
        self.used_urls=[]
        print(scraper_m_filter)
        self.scrape_int=scraped_request
        try:
                #this is the url conversion to meal list, recipe book and shopping list function
                #it also loads items into their respective meal lists and after
            try:    #adjustment will add them directly to the files
                for url in cleaned_url_list[:]:
                    print(cleaned_url_list)

                    try:


                        #countsdown scraped items
                        if self.scrape_int<=0:
                            Clock.schedule_once(self.tick_loader,.5)

                            break
                            return self.used_urls

                        scrap=open("recipes/scraper.txt",'w')
                        shp_list=open("shopping_list/scr_shoppinglist.txt","w")
                        scraper = (scrape_me(url, wild_mode=True))
                        scraper.links(**kwargs)
                        #this filters out duplicate meal items

                        for scrape_check in scraper_m_filter:
                            print(len(self.scraped_list),"scraped list")
                            if len(self.scraped_list)==scraped_request:
                                Clock.schedule_once(self.tick_loader, .5)
                                print("list worked")
                                return self.used_urls
                            #if self.scrape_int <= 0:
                                #Clock.schedule_once(self.tick_loader, .5)

                                #break
                                #return self.used_urls

                            if scraper.title()==scrape_check and self.scrape_int!=0:
                                self.used_urls.append(str(url))
                                self.urls_pre_filter1.append(str(url))
                                raise Exception ("duplicate item",scraper.title())
                            continue

                        if scraped_item=="entree":
                            scrape_title=scraper.title()
                            scrape_title_cleaned=scrape_title.replace(',',"")
                            print(scrape_title)
                            scraped_entree.append(str(scrape_title_cleaned))
                            self.scraped_list=scraped_entree
                        if scraped_item=="side":
                            scrape_title=scraper.title()
                            scrape_fix=scrape_title.replace('"',"")
                            scrape_title_cleaned = scrape_fix.replace(',', "")
                            print(scrape_title)
                            scraped_side.append(str(scrape_title_cleaned))
                            self.scraped_list = scraped_side
                        if scraped_item=="dessert":
                            scrape_title=scraper.title()
                            scrape_fix = scrape_title.replace('"', "")
                            scrape_title_cleaned = scrape_fix.replace(',', "")
                            print(scrape_title)
                            scraped_dessert.append(str(scrape_title_cleaned))
                            self.scraped_list = scraped_dessert
                        if scraped_item == "salad":
                            scrape_title = scraper.title()
                            scrape_fix = scrape_title.replace('"', "")
                            scrape_title_cleaned = scrape_fix.replace(',', "")
                            print(scrape_title)
                            scraped_salad.append(str(scrape_title_cleaned))
                            self.scraped_list = scraped_salad
                        if scraped_item == "breakfast":
                            scrape_title = scraper.title()
                            scrape_fix = scrape_title.replace('"', "")
                            scrape_title_cleaned = scrape_fix.replace(',', "")
                            print(scrape_title)
                            scraped_breakfast.append(str(scrape_title_cleaned))
                            self.scraped_list = scraped_breakfast
                        if scraped_item == "bread":
                            scrape_title = scraper.title()
                            scrape_fix = scrape_title.replace('"', "")
                            scrape_title_cleaned = scrape_fix.replace(',', "")
                            print(scrape_title)
                            scraped_bread.append(str(scrape_title_cleaned))
                            self.scraped_list = scraped_bread
                        if scraped_item == "mexicanfd":
                            scrape_title = scraper.title()
                            scrape_fix = scrape_title.replace('"', "")
                            scrape_title_cleaned = scrape_fix.replace(',', "")
                            print(scrape_title)
                            scraped_mexicanfd.append(str(scrape_title_cleaned))
                            self.scraped_list = scraped_mexicanfd
                        if scraped_item == "fish":
                            scrape_title = scraper.title()
                            scrape_fix = scrape_title.replace('"', "")
                            scrape_title_cleaned = scrape_fix.replace(',', "")
                            print(scrape_title)
                            scraped_fish.append(str(scrape_title_cleaned))
                            self.scraped_list = scraped_fish
                        self.used_urls.append(str(url))

                        scrape_title2=scrape_title_cleaned

                        ing_list=scraper.ingredients()
                        print(scrape_title2, file=scrap)
                        print("\n", file=scrap)
                        print(scraper.ingredients())
                        encode_iter_ing= len(ing_list)
                        ing_list_encoded = [""]
                        print("Ingredients",file=scrap)
                        while encode_iter_ing != 0:
                            encode_me=ing_list[-1]
                            encode_me=encode_me.encode("utf-8").decode("cp1252")
                            ing_list_encoded.append(encode_me)
                            ing_list.pop(-1)
                            encode_iter_ing-=1
                        writeiter = len(ing_list_encoded)

                        while writeiter != 0:
                            scrap.write(str(ing_list_encoded[-1]))
                            scrap.write("\n")
                            shp_list.write(str(ing_list_encoded[-1]))
                            shp_list.write(",")
                            ing_list_encoded.pop(-1)
                            writeiter -= 1
                        print("Cooking Instructions",file=scrap)
                        instr_list=scraper.instructions()
                        instr_list_encoded=[""]
                        textwrap_iter=len(instr_list)
                        text_wrapped_instr=[]
                        wrap_proc=textwrap.TextWrapper(width=60)
                        wrap_me = (wrap_proc.wrap(instr_list))
                        encode_iter_instr = len(wrap_me)
                        index_loc = int(0)
                        while encode_iter_instr != 0:
                            encode_me = wrap_me[index_loc]
                            encode_me = encode_me.encode("utf-8").decode("cp1252")
                            instr_list_encoded.append(encode_me)
                            index_loc += 1
                            encode_iter_instr -= 1
                        writeiter = len(instr_list_encoded)
                        index_loc=0
                        while writeiter != 0:
                            scrap.write(str(instr_list_encoded[index_loc]))
                            scrap.write("\n")
                            index_loc+=1
                            writeiter -= 1
                        print("Source","\n",file=scrap)
                        print(scraper.canonical_url(),"\n",file=scrap)
                        print("Reference Video","\n",file=scrap)
                        print(f"https://www.youtube.com/results?search_query={scrape_title2}",file=scrap)
                        scrap.close()
                        shp_list.close()
                        scraped_sav=scrape_title2
                        path = "recipes"
                        source = "recipes/scraper.txt"
                        destination = f"recipes/{scraped_sav}.txt"
                        dest = shutil.copyfile(source, destination)
                        path = "shopping_list"
                        source = "shopping_list/scr_shoppinglist.txt"
                        destination = f"shopping_list/{scraped_sav}shp.txt"
                        dest = shutil.copyfile(source, destination)
                        self.scrape_int -= 1
                        print(self.scrape_int)
                        print(len(self.used_urls))
                        print("USED URLS",self.used_urls)
                        #self.file_handling_scraper(self, self.used_urls, urls_pre_filter1, *args, **kwargs)
                        urls_pre_filter2 = []
                        with open("datafiles/usedurls1.txt", "r") as prev_urls2:
                            urls_preload2 = prev_urls2.readlines()
                            print(len(urls_preload2))
                        if len(urls_preload2) != 0:
                            self.urls_pre_filter2 = urls_preload2[0]
                            self.urls_pre_filter2 = self.urls_pre_filter2.split(",")
                            self.used_urls.extend(urls_pre_filter2)
                            print("filter 2")
                        print(self.used_urls)

                        if len(self.urls_pre_filter1) != 0:
                            print(self.urls_pre_filter1, "<><><><><><><")
                            self.used_urls.extend(self.urls_pre_filter1)
                            self.used_urls = set(self.used_urls)
                            self.used_urls = list(self.used_urls)
                        print("used urls")
                        print(len(self.used_urls))
                        print(self.used_urls)
                        url_filter = open("datafiles/workingurls.txt", "w")
                        # for url_filter in self.used_urls:
                        writeiter = len(self.used_urls)
                        index_loc = 0
                        while writeiter != 0:
                            url_filter.write(str(self.used_urls[index_loc]))
                            url_filter.write(",")
                            index_loc += 1
                            writeiter -= 1
                        url_filter.close()
                        path = "datafiles"
                        source = "datafiles/workingurls.txt"
                        destination = "datafiles/usedurls1.txt"
                        dest = shutil.copyfile(source, destination)

                    except Exception as error_catch:
                        print(error_catch)
                        continue

                    else:
                        print("secondary loop completed")


                else:
                    print("first loop completed")
                    #implement backup scrapers here
                    Clock.schedule_once(self.tick_loader, .5)
                    return
            except:
                print("connection error or general scraper error")

        except:
            print("connection error, or possible webscrape break")

class RecipeBookBuilder(Screen,MDApp):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        Clock.start_clock()
        self.tick_loader2 = Clock.schedule_interval(self.prog_bar2, .02)
        Clock.unschedule(self.tick_loader2)
        self.p_bar_z2 = Clock.schedule_once(self.prog_bar_cleanup2, 2)
        self.n_scr2 = Clock.schedule_once(self.nxt_scr2, 1)
        Clock.unschedule(self.n_scr2)


    def recipe_b_args(self):
        print("passing args")
        self.recipe_book_builder(every_gen_entree, every_gen_breakfast, ent_rec_comp, side_rec_comp, brd_rec_comp,
                            brk_rec_comp, salad_rec_comp, mex_rec_comp, fsh_rec_comp, des_rec_comp)
    def recipe_book_builder(self,every_gen_entree, every_gen_breakfast, ent_rec_comp, side_rec_comp, brd_rec_comp,
                            brk_rec_comp, salad_rec_comp, mex_rec_comp, fsh_rec_comp, des_rec_comp):
        #recipe lists that require a recipe scraped
        self.ent_rec_scrape=[]
        self.side_rec_scrape=[]
        self.brd_rec_scrape=[]
        self.brk_rec_scrape=[]
        self.sld_rec_scrape=[]
        self.fsh_rec_scrape=[]
        self.des_rec_scrape=[]
        self.mex_rec_scrape=[]
        self.total_recipe_loaded=[]
        #recipe lists to pair with recipes
        ent_rec_list=[]
        side_rec_list = []
        brk_rec_list = []
        brd_rec_list = []
        des_rec_list = []
        sld_rec_list = []
        mex_rec_list = []
        fsh_rec_list = []
        # this stage identifies everything by category
        for item_chk in every_gen_entree:
            if item_chk in ent_rec_comp:
                item_chk=item_chk.strip('"')
                ent_rec_list.append(item_chk)
        for item_chk2 in every_gen_entree:
            if item_chk2 in side_rec_comp:
                item_chk2 = item_chk2.strip('"')
                side_rec_list.append(item_chk2)
        for item_chk3 in every_gen_entree:
            if item_chk3 in des_rec_comp:
                item_chk3 = item_chk3.strip('"')
                des_rec_list.append(item_chk3)
        for item_chk4 in every_gen_entree:
            if item_chk4 in brd_rec_comp:
                item_chk4 = item_chk4.strip('"')
                brd_rec_list.append(item_chk4)
        for item_chk5 in every_gen_breakfast:
            if item_chk5 in brk_rec_comp:
                item_chk5 = item_chk5.strip('"')
                brk_rec_list.append(item_chk5)
        for item_chk6 in every_gen_entree:
            if item_chk6 in salad_rec_comp:
                item_chk6 = item_chk6.strip('"')
                sld_rec_list.append(item_chk6)
        for item_chk7 in every_gen_entree:
            if item_chk7 in mex_rec_comp:
                item_chk7 = item_chk7.strip('"')
                mex_rec_list.append(item_chk7)
        for item_chk8 in every_gen_entree:
            if item_chk8 in fsh_rec_comp:
                item_chk8 = item_chk8.strip('"')
                fsh_rec_list.append(item_chk8)
        # this stage will first filter duplicates
        # then sort alphabetically
        ent_rec_list = set(ent_rec_list)
        ent_rec_list = list(ent_rec_list)
        ent_rec_list.sort()

        side_rec_list = set(side_rec_list)
        side_rec_list = list(side_rec_list)
        side_rec_list.sort()

        des_rec_list = set(des_rec_list)
        des_rec_list = list(des_rec_list)
        des_rec_list.sort()

        brd_rec_list = set(brd_rec_list)
        brd_rec_list = list(brd_rec_list)
        brd_rec_list.sort()

        brk_rec_list = set(brk_rec_list)
        brk_rec_list = list(brk_rec_list)
        brk_rec_list.sort()

        sld_rec_list = set(sld_rec_list)
        sld_rec_list = list(sld_rec_list)
        sld_rec_list.sort()

        mex_rec_list = set(mex_rec_list)
        mex_rec_list = list(mex_rec_list)
        mex_rec_list.sort()

        fsh_rec_list = set(fsh_rec_list)
        fsh_rec_list = list(fsh_rec_list)
        fsh_rec_list.sort()
        self.total_recipe_loaded.extend(ent_rec_list)
        self.total_recipe_loaded.extend(side_rec_list)
        self.total_recipe_loaded.extend(des_rec_list)
        self.total_recipe_loaded.extend(brd_rec_list)
        self.total_recipe_loaded.extend(brk_rec_list)
        self.total_recipe_loaded.extend(sld_rec_list)
        self.total_recipe_loaded.extend(mex_rec_list)

        rec_book_ref=open("recipebooks/recbookrefwork.txt","w")

        for rec_ref in self.total_recipe_loaded:
            rec_ref.strip('"')
            rec_book_ref.write(rec_ref)
            print(",",file=rec_book_ref)
        rec_book_ref.close()

        working_rb = open("recipebooks/workingrb.txt", "w")
        print("entlist", ent_rec_list)
        print("Entree Recipes", file=working_rb)
        print("\n", file=working_rb)
        for recipe_get in ent_rec_list:
            try:
                with open(f"recipes/{recipe_get}.txt", "r") as recipe_pull:
                    recipe_book_as_list = recipe_pull.readlines()
                    for recipe_line in recipe_book_as_list:
                        working_rb.writelines(recipe_line)
                        continue
                    else:
                        print("end of recipe")
                        print("\n", file=working_rb)

            except Exception as recipe_error:
                self.ent_rec_scrape.append(recipe_get)
                ent_rec_list.remove(recipe_get)
                print("failed to get recipe")
                # recipe web scraper resolver goes here
                print(recipe_error)
                continue
        print("Side Recipes", file=working_rb)
        print("\n", file=working_rb)
        for recipe_get in side_rec_list:
            try:
                with open(f"recipes/{recipe_get}.txt", "r") as recipe_pull:
                    recipe_book_as_list = recipe_pull.readlines()
                    for recipe_line in recipe_book_as_list:
                        working_rb.writelines(recipe_line)
                        continue
                    else:
                        print("end of recipe")
                        print("\n", file=working_rb)

            except Exception as recipe_error:
                self.side_rec_scrape.append(recipe_get)
                print("failed to get recipe")
                # recipe web scraper resolver goes here
                print(recipe_error)
                continue
        print("Bread Item Recipes", file=working_rb)
        print("\n", file=working_rb)
        for recipe_get in brd_rec_list:
            try:
                with open(f"recipes/{recipe_get}.txt", "r") as recipe_pull:
                    recipe_book_as_list = recipe_pull.readlines()
                    for recipe_line in recipe_book_as_list:
                        working_rb.writelines(recipe_line)
                        continue
                    else:
                        print("end of recipe")
                        print("\n", file=working_rb)

            except Exception as recipe_error:
                self.brd_rec_scrape.append(recipe_get)
                print("failed to get recipe")
                # recipe web scraper resolver goes here
                print(recipe_error)
                continue
        print("Salad Recipes", file=working_rb)
        print("\n", file=working_rb)
        for recipe_get in sld_rec_list:
            try:
                with open(f"recipes/{recipe_get}.txt", "r") as recipe_pull:
                    recipe_book_as_list = recipe_pull.readlines()
                    for recipe_line in recipe_book_as_list:
                        working_rb.writelines(recipe_line)
                        continue
                    else:
                        print("end of recipe")
                        print("\n", file=working_rb)

            except Exception as recipe_error:
                self.sld_rec_scrape.append(recipe_get)
                print("failed to get recipe")
                # recipe web scraper resolver goes here
                print(recipe_error)
                continue
        print("Breakfast Recipes", file=working_rb)
        print("\n", file=working_rb)
        for recipe_get in brk_rec_list:
            try:
                with open(f"recipes/{recipe_get}.txt", "r") as recipe_pull:
                    recipe_book_as_list = recipe_pull.readlines()
                    for recipe_line in recipe_book_as_list:
                        working_rb.writelines(recipe_line)
                        continue
                    else:
                        print("end of recipe")
                        print("\n", file=working_rb)

            except Exception as recipe_error:
                self.brk_rec_scrape.append(recipe_get)
                print("failed to get recipe")
                # recipe web scraper resolver goes here
                print(recipe_error)
                continue
        print("Mexican Food Recipes", file=working_rb)
        print("\n", file=working_rb)
        for recipe_get in mex_rec_list:
            try:
                with open(f"recipes/{recipe_get}.txt", "r") as recipe_pull:
                    recipe_book_as_list = recipe_pull.readlines()
                    for recipe_line in recipe_book_as_list:
                        working_rb.writelines(recipe_line)
                        continue
                    else:
                        print("end of recipe")
                        print("\n", file=working_rb)

            except Exception as recipe_error:
                self.mex_rec_scrape.append(recipe_get)
                print("failed to get recipe")
                # recipe web scraper resolver goes here
                print(recipe_error)
                continue
        print("Fish and Seafood Recipes", file=working_rb)
        print("\n", file=working_rb)
        for recipe_get in fsh_rec_list:
            try:
                with open(f"recipes/{recipe_get}.txt", "r") as recipe_pull:
                    recipe_book_as_list = recipe_pull.readlines()
                    for recipe_line in recipe_book_as_list:
                        working_rb.writelines(recipe_line)
                        continue
                    else:
                        print("end of recipe")
                        print("\n", file=working_rb)

            except Exception as recipe_error:
                self.fsh_rec_scrape.append(recipe_get)
                print("failed to get recipe")
                # recipe web scraper resolver goes here
                print(recipe_error)
                continue
        print("Dessert Recipes", file=working_rb)
        print("\n", file=working_rb)
        for recipe_get in des_rec_list:
            try:
                with open(f"recipes/{recipe_get}.txt", "r") as recipe_pull:
                    recipe_book_as_list = recipe_pull.readlines()
                    for recipe_line in recipe_book_as_list:
                        working_rb.writelines(recipe_line)
                        continue
                    else:
                        print("end of recipe")
                        print("\n", file=working_rb)

            except Exception as recipe_error:
                self.des_rec_scrape.append(recipe_get)
                print("failed to get recipe")
                # recipe web scraper resolver goes here
                print(recipe_error)
                continue
        working_rb.close()
        recipe_pull.close()
        if self.ent_rec_scrape!=0:
            self.recipe_webscraper()
        if self.side_rec_scrape!=0:
            self.recipe_webscraper()
        if self.brd_rec_scrape!=0:
            self.recipe_webscraper()
        if self.brk_rec_scrape!=0:
            self.recipe_webscraper()
        if self.sld_rec_scrape!=0:
            self.recipe_webscraper()
        if self.fsh_rec_scrape!=0:
            self.recipe_webscraper()
        if self.des_rec_scrape!=0:
            self.recipe_webscraper()
        if self.mex_rec_scrape!=0:
            self.recipe_webscraper()
        else:
            ent_rec_list.clear()
            side_rec_list.clear()
            brd_rec_list.clear()
            brk_rec_list.clear()
            des_rec_list.clear()
            sld_rec_list.clear()
            mex_rec_list.clear()
            fsh_rec_list.clear()

            return
    def recipe_webscraper(self):
        self.lists_to_search = []
        if self.ent_rec_scrape != 0:
            self.lists_to_search.extend(self.ent_rec_scrape)
        if self.side_rec_scrape != 0:
            self.lists_to_search.extend(self.side_rec_scrape)
        if self.brd_rec_scrape != 0:
            self.lists_to_search.extend(self.brd_rec_scrape)
        if self.brk_rec_scrape != 0:
            self.lists_to_search.extend(self.brk_rec_scrape)
        if self.sld_rec_scrape != 0:
            self.lists_to_search.extend(self.sld_rec_scrape)
        if self.fsh_rec_scrape != 0:
            self.lists_to_search.extend(self.fsh_rec_scrape)
        if self.des_rec_scrape != 0:
            self.lists_to_search.extend(self.des_rec_scrape)
        if self.mex_rec_scrape != 0:
            self.lists_to_search.extend(self.mex_rec_scrape)
        run_iter=len(self.lists_to_search)
        try:

            urls_search = "https://www.allrecipes.com/search?q="

            rec_filter_1=[]
            rec_filter_2=[]
            url_pull = []
            working_week
            ing_list=[]



            for i in self.lists_to_search:
                print("list search",self.lists_to_search)
                try:
                    while run_iter!=0:
                        print(run_iter)
                        if run_iter==0:
                            self.recipe_book_builder(self, every_gen_entree, every_gen_breakfast, ent_rec_comp,
                        side_rec_comp, brd_rec_comp,brk_rec_comp, salad_rec_comp, mex_rec_comp, fsh_rec_comp, des_rec_comp)
                            return
                        i = i.strip('"')
                        i=i.strip('"')
                        search_i=i.replace(" ","+")
                        print(i)
                        req_url = requests.get(f"https://www.allrecipes.com/search?q={search_i}").text
                        url_parsed = BeautifulSoup(req_url, "html.parser")
                        #print(url_parsed)
                        # finds first instance of provided argument
                        tags = (url_parsed.find_all("a"))
                        rec_filter_1=((tags[187]))
                        #rec_filter_1=list(rec_filter_1)
                        rec_filter_1=str(rec_filter_1)
                        rec_filter_2=rec_filter_1.split(" ")
                        rec_filter_3=rec_filter_2[10]
                        rec_filter_3=rec_filter_3.strip("href=")
                        rec_filter_3 = rec_filter_3.strip('""')
                        rec_filter_3 = rec_filter_3.strip('""')
                        scraper = (scrape_me(rec_filter_3, wild_mode=True))
                        scrap = open("recipes/scraper.txt", 'w')
                        shp_list = open("shopping_list/scr_shoppinglist.txt", "w")
                        print(i, file=scrap)
                        print("\n", file=scrap)
                        print(scraper.ingredients())
                        encode_iter_ing = len(ing_list)
                        ing_list_encoded = [""]
                        print("Ingredients", file=scrap)
                        while encode_iter_ing != 0:
                            encode_me = ing_list[-1]
                            encode_me = encode_me.encode("utf-8").decode("cp1252")
                            ing_list_encoded.append(encode_me)
                            ing_list.pop(-1)
                            encode_iter_ing -= 1
                        writeiter = len(ing_list_encoded)

                        while writeiter != 0:
                            scrap.write(str(ing_list_encoded[-1]))
                            scrap.write("\n")
                            shp_list.write(str(ing_list_encoded[-1]))
                            shp_list.write(",")
                            ing_list_encoded.pop(-1)
                            writeiter -= 1
                        print("Cooking Instructions", file=scrap)
                        instr_list = scraper.instructions()
                        instr_list_encoded = [""]
                        textwrap_iter = len(instr_list)
                        text_wrapped_instr = []
                        wrap_proc = textwrap.TextWrapper(width=60)
                        wrap_me = (wrap_proc.wrap(instr_list))
                        encode_iter_instr = len(wrap_me)
                        index_loc = int(0)
                        while encode_iter_instr != 0:
                            encode_me = wrap_me[index_loc]
                            encode_me = encode_me.encode("utf-8").decode("cp1252")
                            instr_list_encoded.append(encode_me)
                            index_loc += 1
                            encode_iter_instr -= 1
                        writeiter = len(instr_list_encoded)
                        index_loc = 0
                        while writeiter != 0:
                            scrap.write(str(instr_list_encoded[index_loc]))
                            scrap.write("\n")
                            index_loc += 1
                            writeiter -= 1
                        print("Source", "\n", file=scrap)
                        print(scraper.canonical_url(), "\n", file=scrap)
                        print("Reference Video", "\n", file=scrap)
                        print(f"https://www.youtube.com/results?search_query={scraper.title()}", file=scrap)
                        scrap.close()
                        shp_list.close()
                        scraped_sav = i
                        scraped_sav=scraped_sav.strip('"')
                        path = "recipes"
                        source = "recipes/scraper.txt"
                        destination = f"recipes/{scraped_sav}.txt"
                        dest = shutil.copyfile(source, destination)
                        path = "shopping_list"
                        source = "shopping_list/scr_shoppinglist.txt"
                        destination = f"shopping_list/{scraped_sav}shp.txt"
                        dest = shutil.copyfile(source, destination)
                        run_iter-=1
                        break
                        if Exception== "list index out of range":
                            print("recipe not found")
                except Exception as error:
                        print("main",error)
                        scrap = open("recipes/scraper.txt", 'w')
                        shp_list = open("shopping_list/scr_shoppinglist.txt", "w")
                        print(i, file=scrap)
                        print("\n", file=scrap)
                        print("recipe not found for this",file=scrap)
                        print(f"ingredients not found for {i}",file=shp_list)
                        scrap.close()
                        shp_list.close()
                        scraped_sav = i
                        scraped_sav = scraped_sav.strip('"')
                        path = "recipes"
                        source = "recipes/scraper.txt"
                        destination = f"recipes/{scraped_sav}.txt"
                        dest = shutil.copyfile(source, destination)
                        path = "shopping_list"
                        source = "shopping_list/scr_shoppinglist.txt"
                        destination = f"shopping_list/{scraped_sav}shp.txt"
                        dest = shutil.copyfile(source, destination)
                        run_iter -= 1
                        continue

            #TODO integrate loading bar
            else:
                print("RAN ALL")
                self.ent_rec_scrape.clear()
                self.side_rec_scrape.clear()
                self.brk_rec_scrape.clear()
                self.brd_rec_scrape.clear()
                self.sld_rec_scrape.clear()
                self.des_rec_scrape.clear()
                self.mex_rec_scrape.clear()
                self.fsh_rec_scrape.clear()

                Clock.schedule_once(self.tick_loader2)
                return


        except Exception as error:
            run_iter -= 1
            print("outer")
            print(error)

    def prog_bar2(self,*args,**kwargs):
        self.progress_bar2.max=(len(self.total_recipe_loaded))
        self.progress_bar2.value +=  1
        if self.progress_bar2.value==self.progress_bar2.max:
            Clock.unschedule(self.tick_loader2)
            Clock.schedule_once(self.p_bar_z2,2)
            Clock.schedule_once(self.n_scr2,0)

        return self.ids.progress_bar2.value
    def prog_bar_cleanup2(self,*args,**kwargs):
        Clock.unschedule(self.p_bar_z2)
        self.progress_bar2.value = 0

        if self.progress_bar2.value==0:
            self.progress_bar2.value = 0
            print(self.progress_bar2.value)
            print((self.progress_bar2.max))


        return self.ids.progress_bar2.value
    def nxt_scr2(self,*args):
        self.parent.current = "SaveSlotSelect"
        self.progress_bar2.value = 1
        self.progress_bar2.max = 300

class Tools(Screen,MDApp):
    def popup_test(self):
        pass

class RecipeBookOne(Screen,MDApp):
    index_loc = 0
    recipe_reference=[]
    def prep_recipe_list(self):
        rec_ref=open("recipebooks/mp1recbookref.txt","r")
        for read_in in rec_ref.readlines():
            read_in=str(read_in)
            filter_pre_rec1=read_in.split(',\n')
            filter_pre_rec1.pop(-1)
            filter_pre_rec2=str(filter_pre_rec1)
            filter_pre_rec3=filter_pre_rec2.replace("[","")
            filter_pre_rec4=filter_pre_rec3.replace("]", "")
            filter_pre_rec5=filter_pre_rec4.replace("'", "")
            filter_pre_rec6 = filter_pre_rec5.replace('"', "")
            filter_pre_rec7 = filter_pre_rec6.strip(' ')
            print(filter_pre_rec7)
            self.recipe_reference.append(str(filter_pre_rec7))
        print(self.recipe_reference)
        rec_ref.close()
        self.page_view_initial()
    def page_view_initial(self):
        try:
            start_page=self.recipe_reference[0]
            with open(f"recipes/{start_page}.txt","r")as page:
                page_in=str(page.read())
                self.ids.textview.text=page_in
        except:
            self.ids.textview.text=f"Recipe for {start_page} not found "
    def page_view_next(self):
        try:
            backstop=len(self.recipe_reference)
            self.index_loc += 1
            if self.index_loc==backstop:
                self.index_loc=0
            next_page=self.recipe_reference[self.index_loc]
            with open(f"recipes/{next_page}.txt","r")as page:
                page_in=str(page.read())
                self.ids.textview.text=page_in
        except:
            backstop = len(self.recipe_reference)
            self.index_loc += 1
            if self.index_loc == backstop:
                self.index_loc = 0
                print("loop completed")
            self.ids.textview.text=f"Recipe for {next_page} not found "
    def page_view_previous(self):
        try:
            self.index_loc -= 1
            if self.index_loc==-1:
                self.index_loc=0
            prev_page = self.recipe_reference[self.index_loc]
            with open(f"recipes/{prev_page}.txt", "r") as page:
                page_out = str(page.read())
                self.ids.textview.text = page_out
        except:
            backstop = len(self.recipe_reference)
            self.index_loc -= 1
            if self.index_loc == backstop:
                self.index_loc = 0
                print("loop completed")
            self.ids.textview.text=f"Recipe for {prev_page} not found "
class RecipeBookOneSearch(Screen,MDApp):
    search=ObjectProperty(None)
    search_results=[]
    def search_rec(self):
        self.search_results.clear
        query = self.search.text
        print(type(query))
        print(query)

        for check in RecipeBookOne.recipe_reference:
            check.lower
            check_filter2=check.split(" ")
            print(check_filter2)
            for second_chk in check_filter2:
                if query in second_chk:
                    print("found")
                    self.search_results.append(check)
                    print(self.search_results)
        else:
            if len(self.search_results)!=0:
                print("search done")
                print(self.search_results)
                self.parent.current = "RecipeBookOneSearchResults"

            if len(self.search_results)<=1:
                self.ids.textview.text = """No Results
            Try Capitalizing The First
            Letter of Your Search, Try
            To Limit it To One Keyword"""
class RecipeBookOneSearchResults(Screen,MDApp):
    index_loc=0
    def page_view_initial(self):
        try:
            start_page=RecipeBookOneSearch.search_results[0]
            with open(f"recipes/{start_page}.txt","r")as page:
                page_in=str(page.read())
                self.ids.textview.text=page_in
        except:
            self.ids.textview.text=f"Recipe for {start_page} not found "
    def page_view_next(self):
        try:
            backstop=len(RecipeBookOneSearch.search_results)
            self.index_loc += 1
            if self.index_loc==backstop:
                self.index_loc=0
                self.ids.textview.text = "End Of Results"
            next_page=RecipeBookOneSearch.search_results[self.index_loc]
            with open(f"recipes/{next_page}.txt","r")as page:
                page_in=str(page.read())
                self.ids.textview.text=page_in
        except:
            backstop = len(RecipeBookOneSearch.search_results)
            self.index_loc += 1
            if self.index_loc == backstop:
                self.index_loc = 0
                self.ids.textview.text="End Of Results"
            self.ids.textview.text = f"Recipe for {next_page} not found "
    def page_view_previous(self):
        try:
            self.index_loc -= 1
            if self.index_loc==-1:
                self.index_loc=0
            prev_page = RecipeBookOneSearch.search_results[self.index_loc]
            with open(f"recipes/{prev_page}.txt", "r") as page:
                page_out = str(page.read())
                self.ids.textview.text = page_out
        except:
            backstop = len(RecipeBookOneSearch.search_results)
            self.index_loc -= 1
            if self.index_loc == backstop:
                self.index_loc = 0
                print("loop completed")
            self.ids.textview.text=f"Recipe for {prev_page} not found "
    def clear_search(self):
        RecipeBookOneSearch.search_results.clear()

class RecipeBookTwo(Screen,MDApp):
    index_loc = 0
    recipe_reference = []

    def prep_recipe_list(self):
        rec_ref = open("recipebooks/mp2recbookref.txt", "r")
        for read_in in rec_ref.readlines():
            read_in = str(read_in)
            filter_pre_rec1 = read_in.split(',\n')
            filter_pre_rec1.pop(-1)
            filter_pre_rec2 = str(filter_pre_rec1)
            filter_pre_rec3 = filter_pre_rec2.replace("[", "")
            filter_pre_rec4 = filter_pre_rec3.replace("]", "")
            filter_pre_rec5 = filter_pre_rec4.replace("'", "")
            filter_pre_rec6 = filter_pre_rec5.replace('"', "")
            filter_pre_rec7 = filter_pre_rec6.strip(' ')
            print(filter_pre_rec7)
            self.recipe_reference.append(str(filter_pre_rec7))
        print(self.recipe_reference)
        rec_ref.close()
        self.page_view_initial()

    def page_view_initial(self):
        try:
            start_page = self.recipe_reference[0]
            with open(f"recipes/{start_page}.txt", "r") as page:
                page_in = str(page.read())
                self.ids.textview.text = page_in
        except:
            self.ids.textview.text=f"Recipe for {start_page} not found "

    def page_view_next(self):
        try:
            backstop = len(self.recipe_reference)
            self.index_loc += 1
            if self.index_loc == backstop:
                self.index_loc = 0
            next_page = self.recipe_reference[self.index_loc]
            with open(f"recipes/{next_page}.txt", "r") as page:
                page_in = str(page.read())
                self.ids.textview.text = page_in
        except:
            backstop = len(self.recipe_reference)
            self.index_loc += 1
            if self.index_loc == backstop:
                self.index_loc = 0
                print("loop completed")
            self.ids.textview.text=f"Recipe for {next_page} not found "

    def page_view_previous(self):
        try:
            self.index_loc -= 1
            if self.index_loc == -1:
                self.index_loc = 0
            prev_page = self.recipe_reference[self.index_loc]
            with open(f"recipes/{prev_page}.txt", "r") as page:
                page_out = str(page.read())
                self.ids.textview.text = page_out
        except:
            backstop = len(self.recipe_reference)
            self.index_loc -= 1
            if self.index_loc == backstop:
                self.index_loc = 0
                print("loop completed")
            self.ids.textview.text=f"Recipe for {prev_page} not found "

class RecipeBookTwoSearch(Screen,MDApp):
    search=ObjectProperty(None)
    search_results=[]
    def search_rec(self):
        self.search_results.clear
        query = self.search.text
        print(type(query))
        print(query)

        for check in RecipeBookTwo.recipe_reference:
            check.lower
            check_filter2=check.split(" ")
            print(check_filter2)
            for second_chk in check_filter2:
                if query in second_chk:
                    print("found")
                    self.search_results.append(check)
                    print(self.search_results)
        else:
            if len(self.search_results)!=0:
                print("search done")
                print(self.search_results)
                self.parent.current = "RecipeBookTwoSearchResults"

            if len(self.search_results)<=1:
                self.ids.textview.text = """No Results
            Try Capitalizing The First
            Letter of Your Search, Try
            To Limit it To One Keyword"""

class RecipeBookTwoSearchResults(Screen,MDApp):
    index_loc=0
    def page_view_initial(self):
        try:
            start_page=RecipeBookTwoSearch.search_results[0]
            with open(f"recipes/{start_page}.txt","r")as page:
                page_in=str(page.read())
                self.ids.textview.text=page_in
        except:
            self.ids.textview.text=f"Recipe for {start_page} not found "
    def page_view_next(self):
        try:
            backstop=len(RecipeBookTwoSearch.search_results)
            self.index_loc += 1
            if self.index_loc==backstop:
                self.index_loc=0
                self.ids.textview.text = "End Of Results"
            next_page=RecipeBookTwoSearch.search_results[self.index_loc]
            with open(f"recipes/{next_page}.txt","r")as page:
                page_in=str(page.read())
                self.ids.textview.text=page_in
        except:
            backstop = len(RecipeBookTwoSearch.search_results)
            self.index_loc += 1
            if self.index_loc == backstop:
                self.index_loc = 0
                self.ids.textview.text="End Of Results"
            self.ids.textview.text=f"Recipe for {next_page} not found "
    def page_view_previous(self):
        try:
            self.index_loc -= 1
            if self.index_loc==-1:
                self.index_loc=0
            prev_page = RecipeBookTwoSearch.search_results[self.index_loc]
            with open(f"recipes/{prev_page}.txt", "r") as page:
                page_out = str(page.read())
                self.ids.textview.text = page_out
        except:
            backstop = len(RecipeBookTwoSearch.search_results)
            self.index_loc -= 1
            if self.index_loc == backstop:
                self.index_loc = 0
                print("loop completed")
            self.ids.textview.text = f"Recipe for {prev_page} not found "
    def clear_search(self):
        RecipeBookTwoSearch.search_results.clear()

class RecipeBookThree(Screen,MDApp):
    index_loc = 0
    recipe_reference = []

    def prep_recipe_list(self):
        rec_ref = open("recipebooks/mp3recbookref.txt", "r")
        for read_in in rec_ref.readlines():
            read_in = str(read_in)
            filter_pre_rec1 = read_in.split(',\n')
            filter_pre_rec1.pop(-1)
            filter_pre_rec2 = str(filter_pre_rec1)
            filter_pre_rec3 = filter_pre_rec2.replace("[", "")
            filter_pre_rec4 = filter_pre_rec3.replace("]", "")
            filter_pre_rec5 = filter_pre_rec4.replace("'", "")
            filter_pre_rec6 = filter_pre_rec5.replace('"', "")
            filter_pre_rec7 = filter_pre_rec6.strip(' ')
            print(filter_pre_rec7)
            self.recipe_reference.append(str(filter_pre_rec7))
        print(self.recipe_reference)
        rec_ref.close()
        self.page_view_initial()

    def page_view_initial(self):
        try:
            start_page = self.recipe_reference[0]
            with open(f"recipes/{start_page}.txt", "r") as page:
                page_in = str(page.read())
                self.ids.textview.text = page_in
        except:
            self.ids.textview.text=f"Recipe for {start_page} not found "

    def page_view_next(self):
        try:
            backstop = len(self.recipe_reference)
            self.index_loc += 1
            if self.index_loc == backstop:
                self.index_loc = 0
            next_page = self.recipe_reference[self.index_loc]
            with open(f"recipes/{next_page}.txt", "r") as page:
                page_in = str(page.read())
                self.ids.textview.text = page_in
        except:
            backstop = len(self.recipe_reference)
            self.index_loc += 1
            if self.index_loc == backstop:
                self.index_loc = 0
                print("loop completed")
            self.ids.textview.text=f"Recipe for {next_page} not found "

    def page_view_previous(self):
        try:
            self.index_loc -= 1
            if self.index_loc == -1:
                self.index_loc = 0
            prev_page = self.recipe_reference[self.index_loc]
            with open(f"recipes/{prev_page}.txt", "r") as page:
                page_out = str(page.read())
                self.ids.textview.text = page_out
        except:
            backstop = len(self.recipe_reference)
            self.index_loc -= 1
            if self.index_loc == backstop:
                self.index_loc = 0
                print("loop completed")
            self.ids.textview.text=f"Recipe for {prev_page} not found "

class RecipeBookThreeSearch(Screen,MDApp):
    search=ObjectProperty(None)
    search_results=[]
    def search_rec(self):
        self.search_results.clear
        query = self.search.text
        print(type(query))
        print(query)

        for check in RecipeBookThree.recipe_reference:
            check.lower
            check_filter2=check.split(" ")
            print(check_filter2)
            for second_chk in check_filter2:
                if query in second_chk:
                    print("found")
                    self.search_results.append(check)
                    print(self.search_results)
        else:
            if len(self.search_results)!=0:
                print("search done")
                print(self.search_results)
                self.parent.current = "RecipeBookThreeSearchResults"

            if len(self.search_results)<=1:
                self.ids.textview.text = """No Results
            Try Capitalizing The First
            Letter of Your Search, Try
            To Limit it To One Keyword"""

class RecipeBookThreeSearchResults(Screen,MDApp):
    index_loc=0
    def page_view_initial(self):
        try:
            start_page=RecipeBookThreeSearch.search_results[0]
            with open(f"recipes/{start_page}.txt","r")as page:
                page_in=str(page.read())
                self.ids.textview.text=page_in
        except:
            self.ids.textview.text=f"Recipe for {start_page} not found "
    def page_view_next(self):
        try:
            backstop=len(RecipeBookThreeSearch.search_results)
            self.index_loc += 1
            if self.index_loc==backstop:
                self.index_loc=0
                self.ids.textview.text = "End Of Results"
            next_page=RecipeBookThreeSearch.search_results[self.index_loc]
            with open(f"recipes/{next_page}.txt","r")as page:
                page_in=str(page.read())
                self.ids.textview.text=page_in
        except:
            backstop = len(RecipeBookThreeSearch.search_results)
            self.index_loc += 1
            if self.index_loc == backstop:
                self.index_loc = 0
                self.ids.textview.text="End Of Results"
            self.ids.textview.text=f"Recipe for {next_page} not found "
    def page_view_previous(self):
        try:
            self.index_loc -= 1
            if self.index_loc==-1:
                self.index_loc=0
            prev_page = RecipeBookThreeSearch.search_results[self.index_loc]
            with open(f"recipes/{prev_page}.txt", "r") as page:
                page_out = str(page.read())
                self.ids.textview.text = page_out
        except:
            backstop = len(RecipeBookThreeSearch.search_results)
            self.index_loc -= 1
            if self.index_loc == backstop:
                self.index_loc = 0
                print("loop completed")
            self.ids.textview.text=f"Recipe for {prev_page} not found "
    def clear_search(self):
        RecipeBookThreeSearch.search_results.clear()

class RecipeBookFour(Screen,MDApp):
    index_loc = 0
    recipe_reference = []

    def prep_recipe_list(self):
        rec_ref = open("recipebooks/mp4recbookref.txt", "r")
        for read_in in rec_ref.readlines():
            read_in = str(read_in)
            filter_pre_rec1 = read_in.split(',\n')
            filter_pre_rec1.pop(-1)
            filter_pre_rec2 = str(filter_pre_rec1)
            filter_pre_rec3 = filter_pre_rec2.replace("[", "")
            filter_pre_rec4 = filter_pre_rec3.replace("]", "")
            filter_pre_rec5 = filter_pre_rec4.replace("'", "")
            filter_pre_rec6 = filter_pre_rec5.replace('"', "")
            filter_pre_rec7 = filter_pre_rec6.strip(' ')
            print(filter_pre_rec7)
            self.recipe_reference.append(str(filter_pre_rec7))
        print(self.recipe_reference)
        rec_ref.close()
        self.page_view_initial()

    def page_view_initial(self):
        try:
            start_page = self.recipe_reference[0]
            with open(f"recipes/{start_page}.txt", "r") as page:
                page_in = str(page.read())
                self.ids.textview.text = page_in
        except:
            self.ids.textview.text=f"Recipe for {start_page} not found "

    def page_view_next(self):
        try:
            backstop = len(self.recipe_reference)
            self.index_loc += 1
            if self.index_loc == backstop:
                self.index_loc = 0
            next_page = self.recipe_reference[self.index_loc]
            with open(f"recipes/{next_page}.txt", "r") as page:
                page_in = str(page.read())
                self.ids.textview.text = page_in
        except:
            backstop = len(self.recipe_reference)
            self.index_loc += 1
            if self.index_loc == backstop:
                self.index_loc = 0
                print("loop completed")
            self.ids.textview.text=f"Recipe for {next_page} not found "

    def page_view_previous(self):
        try:
            self.index_loc -= 1
            if self.index_loc == -1:
                self.index_loc = 0
            prev_page = self.recipe_reference[self.index_loc]
            with open(f"recipes/{prev_page}.txt", "r") as page:
                page_out = str(page.read())
                self.ids.textview.text = page_out
        except:
            backstop = len(self.recipe_reference)
            self.index_loc -= 1
            if self.index_loc == backstop:
                self.index_loc = 0
                print("loop completed")
            self.ids.textview.text=f"Recipe for {prev_page} not found "

class RecipeBookFourSearch(Screen,MDApp):
    search=ObjectProperty(None)
    search_results=[]
    def search_rec(self):
        self.search_results.clear
        query = self.search.text
        print(type(query))
        print(query)

        for check in RecipeBookFour.recipe_reference:
            check.lower
            check_filter2=check.split(" ")
            print(check_filter2)
            for second_chk in check_filter2:
                if query in second_chk:
                    print("found")
                    self.search_results.append(check)
                    print(self.search_results)
        else:
            if len(self.search_results)!=0:
                print("search done")
                print(self.search_results)
                self.parent.current = "RecipeBookFourSearchResults"

            if len(self.search_results)<=1:
                self.ids.textview.text = """No Results
            Try Capitalizing The First
            Letter of Your Search, Try
            To Limit it To One Keyword"""

class RecipeBookFourSearchResults(Screen,MDApp):
    index_loc=0
    def page_view_initial(self):
        try:
            start_page=RecipeBookFourSearch.search_results[0]
            with open(f"recipes/{start_page}.txt","r")as page:
                page_in=str(page.read())
                self.ids.textview.text=page_in
        except:
            self.ids.textview.text=f"Recipe for {start_page} not found "
    def page_view_next(self):
        try:
            backstop=len(RecipeBookFourSearch.search_results)
            self.index_loc += 1
            if self.index_loc==backstop:
                self.index_loc=0
                self.ids.textview.text = "End Of Results"
            next_page=RecipeBookFourSearch.search_results[self.index_loc]
            with open(f"recipes/{next_page}.txt","r")as page:
                page_in=str(page.read())
                self.ids.textview.text=page_in
        except:
            backstop = len(RecipeBookFourSearch.search_results)
            self.index_loc += 1
            if self.index_loc == backstop:
                self.index_loc = 0
                self.ids.textview.text="End Of Results"
            self.ids.textview.text=f"Recipe for {next_page} not found "
    def page_view_previous(self):
        try:
            self.index_loc -= 1
            if self.index_loc==-1:
                self.index_loc=0
            prev_page = RecipeBookFourSearch.search_results[self.index_loc]
            with open(f"recipes/{prev_page}.txt", "r") as page:
                page_out = str(page.read())
                self.ids.textview.text = page_out
        except:
            backstop = len(RecipeBookFourSearch.search_results)
            self.index_loc -= 1
            if self.index_loc == backstop:
                self.index_loc = 0
                print("loop completed")
            self.ids.textview.text=f"Recipe for {prev_page} not found "
    def clear_search(self):
        RecipeBookFourSearch.search_results.clear()

class RecipeBookFive(Screen,MDApp):
    index_loc = 0
    recipe_reference = []

    def prep_recipe_list(self):
        rec_ref = open("recipebooks/mp5recbookref.txt", "r")
        for read_in in rec_ref.readlines():
            read_in = str(read_in)
            filter_pre_rec1 = read_in.split(',\n')
            filter_pre_rec1.pop(-1)
            filter_pre_rec2 = str(filter_pre_rec1)
            filter_pre_rec3 = filter_pre_rec2.replace("[", "")
            filter_pre_rec4 = filter_pre_rec3.replace("]", "")
            filter_pre_rec5 = filter_pre_rec4.replace("'", "")
            filter_pre_rec6 = filter_pre_rec5.replace('"', "")
            filter_pre_rec7 = filter_pre_rec6.strip(' ')
            print(filter_pre_rec7)
            self.recipe_reference.append(str(filter_pre_rec7))
        print(self.recipe_reference)
        rec_ref.close()
        self.page_view_initial()

    def page_view_initial(self):
        try:
            start_page = self.recipe_reference[0]
            with open(f"recipes/{start_page}.txt", "r") as page:
                page_in = str(page.read())
                self.ids.textview.text = page_in
        except:
            self.ids.textview.text=f"Recipe for {start_page} not found "

    def page_view_next(self):
        try:
            backstop = len(self.recipe_reference)
            self.index_loc += 1
            if self.index_loc == backstop:
                self.index_loc = 0
            next_page = self.recipe_reference[self.index_loc]
            with open(f"recipes/{next_page}.txt", "r") as page:
                page_in = str(page.read())
                self.ids.textview.text = page_in
        except:
            backstop = len(self.recipe_reference)
            self.index_loc += 1
            if self.index_loc == backstop:
                self.index_loc = 0
                print("loop completed")
            self.ids.textview.text=f"Recipe for {next_page} not found "

    def page_view_previous(self):
        try:
            self.index_loc -= 1
            if self.index_loc == -1:
                self.index_loc = 0
            prev_page = self.recipe_reference[self.index_loc]
            with open(f"recipes/{prev_page}.txt", "r") as page:
                page_out = str(page.read())
                self.ids.textview.text = page_out
        except:
            backstop = len(self.recipe_reference)
            self.index_loc -= 1
            if self.index_loc == backstop:
                self.index_loc = 0
                print("loop completed")
            self.ids.textview.text=f"Recipe for {prev_page} not found "

class RecipeBookFiveSearch(Screen,MDApp):
    search=ObjectProperty(None)
    search_results=[]
    def search_rec(self):
        self.search_results.clear
        query = self.search.text
        print(type(query))
        print(query)

        for check in RecipeBookFive.recipe_reference:
            check.lower
            check_filter2=check.split(" ")
            print(check_filter2)
            for second_chk in check_filter2:
                if query in second_chk:
                    print("found")
                    self.search_results.append(check)
                    print(self.search_results)
        else:
            if len(self.search_results)!=0:
                print("search done")
                print(self.search_results)
                self.parent.current = "RecipeBookFiveSearchResults"

            if len(self.search_results)<=1:
                self.ids.textview.text = """No Results
            Try Capitalizing The First
            Letter of Your Search, Try
            To Limit it To One Keyword"""

class RecipeBookFiveSearchResults(Screen,MDApp):
    index_loc=0
    def page_view_initial(self):
        try:
            start_page=RecipeBookFiveSearch.search_results[0]
            with open(f"recipes/{start_page}.txt","r")as page:
                page_in=str(page.read())
                self.ids.textview.text=page_in
        except:
            self.ids.textview.text=f"Recipe for {start_page} not found "
    def page_view_next(self):
        try:
            backstop=len(RecipeBookFiveSearch.search_results)
            self.index_loc += 1
            if self.index_loc==backstop:
                self.index_loc=0
                self.ids.textview.text = "End Of Results"
            next_page=RecipeBookFiveSearch.search_results[self.index_loc]
            with open(f"recipes/{next_page}.txt","r")as page:
                page_in=str(page.read())
                self.ids.textview.text=page_in
        except:
            backstop = len(RecipeBookFiveSearch.search_results)
            self.index_loc += 1
            if self.index_loc == backstop:
                self.index_loc = 0
                self.ids.textview.text="End Of Results"
            self.ids.textview.text=f"Recipe for {next_page} not found "
    def page_view_previous(self):
        try:
            self.index_loc -= 1
            if self.index_loc==-1:
                self.index_loc=0
            prev_page = RecipeBookFiveSearch.search_results[self.index_loc]
            with open(f"recipes/{prev_page}.txt", "r") as page:
                page_out = str(page.read())
                self.ids.textview.text = page_out
        except:
            backstop = len(RecipeBookFiveSearch.search_results)
            self.index_loc -= 1
            if self.index_loc == backstop:
                self.index_loc = 0
                print("loop completed")
            self.ids.textview.text=f"Recipe for {prev_page} not found "
    def clear_search(self):
        RecipeBookFiveSearch.search_results.clear()

class EntreeLimitPop(Popup):
    pass
class SidesEntreesPop(Popup):
    pass
class WebScrapeLimitPop(Popup):
    pass
class WebScrapeReportPop(Popup):
    pass

Builder.load_file("morekivy.kv")
class Meal_Planner(MDApp):


    def build(self):

        sm = ScreenManager()
        self.window = GridLayout()
        self.window.size_hint = (0.01, 0.02)
        sm.add_widget(LoginWindow(name="StartScreen"))
        sm.add_widget(PageOne(name="Day Select"))
        sm.add_widget(DayWeek(name="Day Week"))
        sm.add_widget(EntSideGen(name="EntSideGen"))
        sm.add_widget(FishFrQuest(name="FishFrQuest"))
        sm.add_widget(FishFrYes(name="FishFrYes"))
        sm.add_widget(TacoTueQuest(name="TacoTueQuest"))
        sm.add_widget(TacoTueYes(name="TacoTueYes"))
        sm.add_widget(SetDaysQuest(name="SetDaysQuest"))
        sm.add_widget(SetDaysDay1(name="SetDaysDay1"))
        sm.add_widget(SetDaysMealL1(name="SetDaysMealL1"))
        sm.add_widget(SetDaysMealD1(name="SetDaysMealD1"))
        sm.add_widget(SetDaysQuest2(name="SetDaysQuest2"))
        sm.add_widget(SetDaysDay2(name="SetDaysDay2"))
        sm.add_widget(SetDaysMealL2(name="SetDaysMealL2"))
        sm.add_widget(SetDaysMealD2(name="SetDaysMealD2"))
        sm.add_widget(GeneratorScreen(name="GeneratorScreen"))
        sm.add_widget(AddNewItem(name="AddNewItem"))
        sm.add_widget(AddNewEntree(name="AddNewEntree"))
        sm.add_widget(AddNewSide(name="AddNewSide"))
        sm.add_widget(AddNewBrd(name="AddNewBrd"))
        sm.add_widget(AddNewSld(name="AddNewSld"))
        sm.add_widget(AddNewBrk(name="AddNewBrk"))
        sm.add_widget(AddNewDes(name="AddNewDes"))
        sm.add_widget(AddNewMex(name="AddNewMex"))
        sm.add_widget(AddNewFsh(name="AddNewFsh"))
        sm.add_widget(SaveSlotSelect(name="SaveSlotSelect"))
        sm.add_widget(MealCheck(name="MealCheck"))
        sm.add_widget(ViewMP1(name="ViewMP1"))
        sm.add_widget(ViewMP2(name="ViewMP2"))
        sm.add_widget(ViewMP3(name="ViewMP3"))
        sm.add_widget(ViewMP4(name="ViewMP4"))
        sm.add_widget(ViewMP5(name="ViewMP5"))
        sm.add_widget(HelpScreen(name="HelpScreen"))
        sm.add_widget(WebScraperConfig(name="WebScraperConfig"))
        sm.add_widget(WebScraper(name="WebScraper"))
        sm.add_widget(WebScraperQty(name="WebScraperQty"))
        sm.add_widget(Tools(name="Tools"))
        sm.add_widget(RecipeBookBuilder(name="RecipeBookBuilder"))
        sm.add_widget(RecipeBookOne(name="RecipeBookOne"))
        sm.add_widget(RecipeBookOneSearch(name="RecipeBookOneSearch"))
        sm.add_widget(RecipeBookOneSearchResults(name="RecipeBookOneSearchResults"))
        sm.add_widget(RecipeBookTwo(name="RecipeBookTwo"))
        sm.add_widget(RecipeBookTwoSearch(name="RecipeBookTwoSearch"))
        sm.add_widget(RecipeBookTwoSearchResults(name="RecipeBookTwoSearchResults"))
        sm.add_widget(RecipeBookThree(name="RecipeBookThree"))
        sm.add_widget(RecipeBookThreeSearch(name="RecipeBookThreeSearch"))
        sm.add_widget(RecipeBookThreeSearchResults(name="RecipeBookThreeSearchResults"))
        sm.add_widget(RecipeBookFour(name="RecipeBookFour"))
        sm.add_widget(RecipeBookFourSearch(name="RecipeBookFourSearch"))
        sm.add_widget(RecipeBookFourSearchResults(name="RecipeBookFourSearchResults"))
        sm.add_widget(RecipeBookFive(name="RecipeBookFive"))
        sm.add_widget(RecipeBookFiveSearch(name="RecipeBookFiveSearch"))
        sm.add_widget(RecipeBookFiveSearchResults(name="RecipeBookFiveSearchResults"))
        return sm

if __name__ == "__main__":
    Meal_Planner().run()




