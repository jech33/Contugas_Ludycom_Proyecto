import re
import arcpy
import os
import datetime
word = "CAL.SN hoaladkf"

mystring = "SN"

print(mystring[0])
print(re.split(' |\.', word))
print(word[-2:])
print(word.upper().split(".")[1] in mystring.upper())

start_time = datetime.datetime.now()
contugasVias = "BACKUP_CONTUGAS_27-09-2021.gdb/Red_Vial_ICA_15_10_2021"
contugasViasFields = ["SHAPE@", 'NOMBREVIA', 'TIPOVIA', 'NOM_ALT_C']

print(None)

siglasVias = {
        "AL": ["AL", "01", "ALAMEDA"],
        "AV": ["AV", "02", "AVENIDA", "AVENIDIA", "AV", "AVENDIA"],	
        "BA": ["BA", "03", "BAJADA"],	
        "CR": ["CR", "04", "CARRETERA"],
        "CJ": ["CJ", "05", "CALLEJON", "CALLEJ\xd3N"],
        "CA": ["CA", "06", "CALLE", "CL", "CAL"],	
        "GA": ["GA", "07", "GALERIA"],	
        "JR": ["JR", "08", "JIRON", "JR", "JIR\xd3N"],	
        "ML": ["ML", "09", "MALECON", "MALEC\xd3N"],	
        "OV": ["OV", "10", "OVALO"],	
        "PJ": ["PJ", "11", "PASAJE", "PSJ", "PSJE", "PJE"],	
        "PL": ["PL", "12", "PLAZA", ],	
        "PQ": ["PQ", "13", "PARQUE"],	
        "PR": ["PR", "14", "PROLONGACION", "PROLONG", "PROLONGACI\xd3N", "PROL"],	
        "PZ": ["PZ", "16", "PLAZUELA"],
        "PS": ["PS", "15", "PASEO"],	
        "CM": ["CM", "17", "CAMINO"],	
        "CU": ["CU", "18", "CUESTA"],	
        "SE": ["SE", "19", "SENDERO"],	
        "PU": ["PU", "20", "PUENTE"],	
        "BO": ["BO", "21", "BOULEVARD", ],
        "RI": ["RI", "22", "RINCONADA"],
        "AU": ["AU", "23", "AUTOPISTA"],
        "CI": ["CI", "24", "CIRCVUNVALACION", "CIRCUNVALACI\xd3N"],
        "VI": ["VI", "25", "AUTOPISTA"]
    }

def get_key(val, dictionary):
    for key, value in dictionary.items():
        for element in value:
            if val.upper() == element:
                return key

tipoVia = {
    "00": ["S/N", "SN"],
    "01": ["ALAMEDA",   "AL"],
    "02": ["AVENIDA",   "AV"],
    "03": ["BAJADA",    "BA"],
    "04": ["CARRETERA", "CR"],
    "05": ["CALLEJON",  "CJ"],
    "06": ["CALLE",     "CA"],
    "07": ["GALERIA",   "GA"],
    "08": ["JIRON",     "JR"],
    "09": ["MALECON",   "ML"],
    "10": ["OVALO",     "OV"],
    "11": ["PASAJE",    "PJ"],
    "12": ["PLAZA",     "PL"],
    "13": ["PARQUE",    "PQ"],
    "14": ["PROLONGACION",  "PR"],
    "15": ["PASEO",     "PS"],
    "16": ["PLAZUELA",	"PZ"],
    "17": ["CAMINO",	"CM"],
    "18": ["CUESTA",	"CU"],
    "19": ["SENDERO",	"SE"],
    "20": ["PUENTE",	"PU"],
    "21": ["BOULEVARD",	"BL"],
    "22": ["CALZADA",	"CL"],
    "23": ["RINCONADA",	"RI"],
    "24": ["AUTOPISTA",	"AU"],
    "25": ["CIRCUNVALACION",    "CI"],
    "26": ["VIADUCTO",  "VI"]
}

print("UBIGEOIZQUIERDA LIKE '{0}%' OR UBIGEODERECHA LIKE '{0}%'".format(1103))
print("12".upper())

import unicodedata

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

print(" ".join(" prueba  dos   tres espacios".split()))

def shapeVertex(layer, fields):
    with arcpy.da.SearchCursor(layer, fields) as cursorVias:
        vias = [list(rowVias) for rowVias in cursorVias]
    print(vias[0][0].firstPoint, vias[0][0].lastPoint)
# shapeVertex(contugasVias, contugasViasFields)

codigos = {
    1: {
        'code': 1,
        'name': "VICTOR RAUL HAYA DE LA TORRE",
        'points': []
    },
    2: {
        'code': 1,
        'name': "panamericana",
        'points': []
    },
}

try:
    if codigos[3]["name"] == "huacachica":
        codigos[3]['code'] == "prueb"
    else:
        pass
except:
    codigos[3] = {}
    codigos[3]["name"] = "huacachica" 

print(any('huacachica' in d.values() for d in codigos.values()))
for codigo in codigos:
    print(codigos[codigo])
print(len(codigos))

def editorTracking(gdb_fc):
    # Create a Describe object from the feature class
    desc = arcpy.Describe(gdb_fc)

    # If the feature class has editor tracking enabled, then
    #   list how many features were last edited by each user.
    #
    if desc.editorTrackingEnabled:
        #
        # Get the editorFieldName from the describe object
        whoField = desc.editorFieldName
        #
        # Use a cursor to search through all the features
        userDictionary = {}
        cur = arcpy.da.SearchCursor(gdb_fc, [whoField])
        for row in cur:
            featureEditedBy = row[0]
            if featureEditedBy in userDictionary:
                userDictionary[featureEditedBy] += 1
            else:
                userDictionary[featureEditedBy] = 1
        #
        # Print the results
        for user in userDictionary.keys():
            if user == None:
                print('Last edited before editor tracking was enabled: '+ \
                    str(userDictionary[user]))
            else:
                print("Last edited by " + user + ": " + str(userDictionary[user]))
    else:
        print('Editor tracking not enabled for '+gdb_fc)

mallavialEditor = "BACKUP_CONTUGAS_27-09-2021.gdb/MALLAVIAL"
editorTracking(mallavialEditor)

import socket
print(socket.gethostname())