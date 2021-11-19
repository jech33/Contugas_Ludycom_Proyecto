import arcpy
import os
import datetime
import re

start_time = datetime.datetime.now()
contugasVias = "BACKUP_CONTUGAS_27-09-2021.gdb/Red_Vial_ICA_29_10_2021"
contugasViasFields = ["NOMBRETENTATIVO", 'NOMBREVIA', 'TIPOVIA', 'NOM_ALT_C']
viasClause = "NOMBREVIA <> 'S/N'"

############ Lista todos los camops de la tabla ##########
def fields(tablePath):
    tableFieldsObject = arcpy.ListFields(tablePath)
    tableFieldsName = []
    for element in tableFieldsObject:
        tableFieldsName.append(element.name)
    return tableFieldsName

def get_key(val, dictionary):
    for key, value in dictionary.items():
        for element in value:
            if val.upper() == element:
                return key

print("Vias feature class: "+contugasVias)
print("Campos totales: ")
print(fields(contugasVias))
print("Campos Vias feature class: {0}".format(contugasViasFields))
print("")

def estadisticasNombres():
    ######### Ejecutar script ###########
    count = 0
    with arcpy.da.SearchCursor(contugasVias, contugasViasFields, where_clause=(viasClause)) as cursorVias:
        # Recorrer cada fila de la tabla contugasVias
        count += 1
        vias = [list(rowVias) for rowVias in cursorVias]

    nombresCorrectos = 0.0
    nombresErrados = 0.0
    nombresSn = 0
    tipoVia = []
    for row in vias:

        ## Encontrar vias coincidentes
        if ("SIN NOMBRE" in row[1]) or ("SN" in row[1]):
            row[1] = "SN"
        if row[0] != None:
            ## separar en listas los nombres
            tipo = re.split(' |\.', row[0])
            tipoVia.append(tipo[0])
            if row[0][-2:] == "SN":
                row[0] = "SN"
            # verificar si nombrevia esta en nombre tentativo
            if (row[1] in row[0]):
                nombresCorrectos += 1
                if row[1] != "SN":
                    nombresSn += 1
                continue
        nombresErrados += 1

    ########### Operaciones para porcentajes
    porcentajeCorrecto = nombresCorrectos/len(vias)*100
    porcentajeErrado = nombresErrados/len(vias)*100

    print("Diferentes a SIN NOMBRE: {0}".format(nombresSn))
    print("Vias registradas: {0}".format(len(vias)))
    print("Porcentaje de nombres coincidentes: {0:.2f}%".format(porcentajeCorrecto))

    end_time = datetime.datetime.now()
    diff = end_time - start_time

    print ("Inicio Script:   {}".format(start_time.strftime("%Y-%m-%d %H:%M:%S")))
    print ("Fin Script:      {}".format(end_time.strftime("%Y-%m-%d %H:%M:%S")))
    print ("Duracion_Script: {}".format(diff))


####### Tipos de via
def updateTipoDeVia():
    # print [
    #     "JR", "PROLONG", "PASAJE", "MALECON", "AVENIDIA", "OVALO", "PROLONGACI\xd3N", "BOULEVARD",
    #     "PLAZA", "PSJ", "PROL", "PSJE", "MALEC\xd3N", "CL", "JIR\xd3N", "CALLE", "CAL", "CARRETERA", 
    #     "AV", "AVENDIA", "AVENIDA", "PLAZUELA"
    # ]

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

    with arcpy.da.UpdateCursor(contugasVias, contugasViasFields) as cursorVias:
        # Recorrer cada fila de la tabla contugasVias
        for row in cursorVias:
            if row[0] != None:
                ## Poner en listas los nombres separandolos por puntos y espacios
                tipo = re.split(' |\.', row[0])
                siglaPLSQL = row[3]
                siglaCorregida = get_key(tipo[0], siglasVias)
                if (siglaCorregida == None and siglaPLSQL == "S/N"):
                    row[2] = "SN"
                elif (siglaCorregida == None and siglaPLSQL == None):
                    row[2] = "SN"
                elif (siglaCorregida == None and siglaPLSQL != "S/N"):
                    if get_key(siglaPLSQL, siglasVias) != None:
                        row[2] = get_key(siglaPLSQL[:10], siglasVias)
                    else:
                        row[2] = "SN"
                else:
                    row[2] = str(siglaCorregida)
            else:
                if(row[3] == "S/N"):
                    row[2] = "SN"
                elif row[3] != None:
                    siglaNone = get_key(row[3], siglasVias)
                    if siglaNone != None:
                        row[2] = siglaNone
                    else: 
                        row[2] = "SN"
            cursorVias.updateRow(row)
updateTipoDeVia()

def estadisticasTipoVia():
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
    count = 0.0
    tipoCorrecto = 0.0
    with arcpy.da.SearchCursor(contugasVias, contugasViasFields) as cursorVias:
        for row in cursorVias:
            if row[0] != None:
                tipo = re.split(' |\.', row[0])
                siglaCorregida = get_key(tipo[0], siglasVias)
                count += 1
                if row[2] == siglaCorregida:
                    tipoCorrecto += 1
        
    porcentajeCorrectoTipo = (tipoCorrecto/count)*100

    print("Porcentaje de tipos coincidentes: {0:.2f}%".format(porcentajeCorrectoTipo))

