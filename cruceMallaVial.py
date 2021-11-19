import arcpy
import os
import datetime
import re
import pprint
import unicodedata

start_time = datetime.datetime.now()
contugasVias = "BACKUP_CONTUGAS_27-09-2021.gdb/Red_Vial_ICA_29_10_2021"
contugasViasFields = ["SHAPE@", "NOMBREVIA", 'TIPOVIA', 'UBIGEOIZQUIERDA', 'UBIGEODERECHA', 'CODIGOSEGMENTOVIA', 'CODIGOVIA']
viasToInsert = "BACKUP_CONTUGAS_27-09-2021.gdb/MALLAVIAL"
viasClause = "UBIGEOIZQUIERDA LIKE '110%' OR UBIGEODERECHA LIKE '110%'"
cruceMallaVial = "BACKUP_CONTUGAS_27-09-2021.gdb/CRUCEMALLAVIAL"

############ Lista todos los campos de la tabla ##########
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

siglas = {
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

def insertRow():
    with arcpy.da.SearchCursor(contugasVias, ["SHAPE@", "NOMBREVIA", 'TIPOVIA', 'UBIGEOIZQUIERDA', 
        'UBIGEODERECHA', 'CODIGOSEGMENTOVIA', 'CODIGOVIA'], where_clause=(viasClause)) as cursorVias:
        # Recorrer cada fila de la tabla contugasVias
        vias = [list(rowVias) for rowVias in cursorVias]
    
    print(vias[0])

    with arcpy.da.InsertCursor(viasToInsert, ["SHAPE@", "NOMBREVIA", 'TIPOVIA', 'UBIGEOIZQUIERDA', 
        'UBIGEODERECHA', 'CODIGOSEGMENTOVIA', 'CODIGOVIA']) as cursor:
        for row in vias:
            # print(row)
            if get_key(row[2], siglas) == None:
                row[2] = "00"
            else: 
                row[2] = siglas[row[2]][1]
            cursor.insertRow(row)

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def calculateName(layer):
    counter=0
    with arcpy.da.UpdateCursor(layer, ['NOMBRETENTATIVO', 'TEXTOVIAL', 'name']) as cursorVias:
        for rowVias in cursorVias:            
            if rowVias[1] != None and rowVias[1] != " ":
                nomenclaturaGis = remove_accents(rowVias[1].upper())
                if nomenclaturaGis[-2:] != "SN":
                    rowVias[0] = nomenclaturaGis
                else:
                    if rowVias[2] != None and rowVias[2] != " ":
                        name = remove_accents(rowVias[2].upper())
                        if name[-2:] != "SN":
                            rowVias[0] = name
                    elif nomenclaturaGis[-2:] == "SN":
                        rowVias[0] = nomenclaturaGis
                    else:
                        rowVias[0] = "SN"
                        counter += 1
            else:
                if rowVias[2] != None and rowVias[2] != " ":
                    name = remove_accents(rowVias[2].upper())
                    if name[-2:] != "SN":
                        rowVias[0] = name
                    else:
                        rowVias[0] = "SN"
                        counter += 1 
                else:
                    rowVias[0] = "SN"
                    counter += 1

            cursorVias.updateRow(rowVias)
    print("Registros actualizados. Vias no encontradas en ningun registro (SN): {0:,}".format(counter))

####### Tipos de via
def updateTipoDeVia(layer):
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

    with arcpy.da.UpdateCursor(layer, ["NOMBRETENTATIVO", 'NOMBREVIA', 'TIPOVIA', 'NOM_ALT_C']) as cursorVias:
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
            

def changeName(layer):
    with arcpy.da.UpdateCursor(layer, ['NOMBREVIA']) as cursorVias:
        for rowVias in cursorVias:
            tipo = re.split(' |\.', rowVias[0])
            if (get_key(tipo[0], siglas) != None) and (tipo[0] != "SN"):
                tipo.remove(tipo[0])
                rowVias[0] = " ".join(tipo)
                ##### Incluir los casos en los que el nombre es igual a " "
                if rowVias[0] == " " or rowVias[0] == "":
                    rowVias[0] = "SN"
                if rowVias[0] == None:
                    rowVias[0] = "SN"
                ##### Quitar espacio al inicio del nombre de la via
                if rowVias[0][0] == " ":
                    rowVias[0] = rowVias[0][1:]
                cursorVias.updateRow(rowVias)

def updateCodigoSegmentoVia(layer):
    provincias = ['1101', '1102', '1103', '1105']
    for provincia in provincias:
        clause = "UBIGEOIZQUIERDA LIKE '{0}%' OR UBIGEODERECHA LIKE '{0}%'".format(provincia)
        with arcpy.da.UpdateCursor(layer, ['CODIGOSEGMENTOVIA'], where_clause=(clause)) as cursorVias:
            counter = 1
            for rowVias in cursorVias:
                rowVias[0] = provincia + str(counter)
                counter +=1
                cursorVias.updateRow(rowVias)
    print("Registros actualizados en archivo {0}".format(layer))

def updateCodigoLineasAdyacentes(layer):
    provincias = ['1101', '1102', '1103', '1105']
    # provincias = ['1103']

    ######## Llenar diccionario viasPorNombreProvincia
    viasPorNombreProvincia = {}
    for provincia in provincias:
        clause = "UBIGEOIZQUIERDA LIKE '{0}%' OR UBIGEODERECHA LIKE '{0}%'".format(provincia)
        with arcpy.da.UpdateCursor(layer, ['NOMBREVIA', 'CODIGOVIA', 'TIPOVIA', 'SHAPE@'], where_clause=(clause), sql_clause=(None, "ORDER BY NOMBREVIA, nombprov")) as cursorVias:
            for rowVias in cursorVias:
                name = str(provincia) + " " + rowVias[0]
                startPoint = (rowVias[3].firstPoint.X, rowVias[3].firstPoint.Y)
                endPoint = (rowVias[3].lastPoint.X, rowVias[3].lastPoint.Y)
                if name not in viasPorNombreProvincia:
                    viasPorNombreProvincia[name] = [(rowVias[0], rowVias[2], startPoint, endPoint)]
                else:
                    viasPorNombreProvincia[name].append((rowVias[0], rowVias[2], startPoint, endPoint))
                
                # cursorVias.updateRow(rowVias)

    ######## Inicializar diccionario codigosVertices
    codigosVertices = {}
    i = 1
    ######## Funcion recursiva para comparar todas las vias cuando haya alguna coincidencia
    def comparaEncontrado(listCodigos, code, listVias, value):
        if value[2] in listCodigos[code]["vertex"]:
            listCodigos[code]["vertex"].append(value[3])
            listCodigos[code]["vias"].append(value)
        elif value[3] in listCodigos[code]["vertex"]:
            listCodigos[code]["vertex"].append(value[2])
            listCodigos[code]["vias"].append(value)
        else:
            return
        for element in listVias:
            if element == value:
                continue
            elif element in listCodigos[code]["vias"]:
                continue
            elif (element[2] in listCodigos[code]["vertex"]) or (element[3] in listCodigos[code]["vertex"]):
                comparaEncontrado(listCodigos, code, listVias, element)
        return listCodigos
        
    ######## Asignar codigo a cada via que comparta nombre y coordenadas
    for key in viasPorNombreProvincia:
        code = str(key[:4]) + str(i)
        codigosVertices[code] = {"name": "", "vertex":[], "vias": []}
        for viaAComparar in viasPorNombreProvincia[key]:
            nombre = viaAComparar[0]
            if key[-2:] == "SN" or "SN" in key:
                code = str(key[:4]) + str(i)
                codigosVertices[code] = {"name": "", "vertex":[], "vias": []}
                codigosVertices[code]["name"] =  nombre
                codigosVertices[code]["vertex"].append( viaAComparar[2])
                codigosVertices[code]["vertex"].append(viaAComparar[3])
                codigosVertices[code]["vias"].append(viaAComparar)
                i += 1
            elif codigosVertices[code]["vertex"] == []:
                code = str(key[:4]) + str(i)
                codigosVertices[code] = {"name": "", "vertex":[], "vias": []}
                codigosVertices[code]["name"] =  nombre
                codigosVertices[code]["vertex"].append(viaAComparar[2])
                codigosVertices[code]["vertex"].append(viaAComparar[3])
                comparaEncontrado(codigosVertices, code, viasPorNombreProvincia[key], viaAComparar)
                i += 1
            else:
                haveCode = False
                for element in codigosVertices:
                    if viaAComparar in codigosVertices[element]["vias"]:
                        haveCode = True
                        break
                if haveCode == False:
                    code = str(key[:4]) + str(i)
                    codigosVertices[code] = {"name": "", "vertex":[], "vias": []}
                    codigosVertices[code]["name"] =  nombre
                    codigosVertices[code]["vertex"].append(viaAComparar[2])
                    codigosVertices[code]["vertex"].append(viaAComparar[3])
                    comparaEncontrado(codigosVertices, code, viasPorNombreProvincia[key], viaAComparar)
                    i += 1
    
    ######## Buscar codigo en diccionario codigosVertices y asignarlo en la base de datos
    counterFinal = 0
    for provincia in provincias:
        clause = "UBIGEOIZQUIERDA LIKE '{0}%' OR UBIGEODERECHA LIKE '{0}%'".format(provincia)
        with arcpy.da.UpdateCursor(layer, ['NOMBREVIA', 'CODIGOVIA', 'TIPOVIA', 'SHAPE@'], where_clause=(clause), sql_clause=(None, "ORDER BY NOMBREVIA, nombprov")) as cursorVias:
            for rowVias in cursorVias:
                nombre = rowVias[0]
                startPoint = (rowVias[3].firstPoint.X, rowVias[3].firstPoint.Y)
                endPoint = (rowVias[3].lastPoint.X, rowVias[3].lastPoint.Y)
                viaTipoPuntos = (nombre, rowVias[2], startPoint, endPoint)
                for codigo in codigosVertices.keys():
                    if codigosVertices[codigo]["name"] == nombre and viaTipoPuntos in codigosVertices[codigo]["vias"]:
                        counterFinal += 1 
                        print("Si")
                        rowVias[1] = codigo
                        cursorVias.updateRow(rowVias)
                        break

    print(counterFinal)
    

    pprint.pprint({k: codigosVertices[k] for k in codigosVertices.keys()[:3]})
    # pprint.pprint({k: viasPorNombreProvincia[k] for k in viasPorNombreProvincia.keys()[:1]})
    print("Registros actualizados en archivo {0}".format(layer))

def updateCodigoNombreTipo(layer):
    provincias = ['1101', '1102', '1103', '1105']
    for provincia in provincias:
        codigos = {}
        clause = "UBIGEOIZQUIERDA LIKE '{0}%' OR UBIGEODERECHA LIKE '{0}%'".format(provincia)
        with arcpy.da.UpdateCursor(layer, ['NOMBREVIA', 'CODIGOVIA', 'TIPOVIA', 'SHAPE@'], where_clause=(clause)) as cursorVias:
            counter = 1
            for rowVias in cursorVias:
                key = rowVias[2] + " " + rowVias[0]
                if key in codigos and key[-2:] != "SN":
                    rowVias[1] = codigos[key]
                elif key[-2:] == "SN":
                    rowVias[1] = provincia + str(counter)
                    counter += 1
                else:
                    rowVias[1] = provincia + str(counter)
                    codigos[key] = rowVias[1]
                    counter += 1
                cursorVias.updateRow(rowVias)
    print(codigos)
    print("Registros actualizados en archivo {0}".format(layer))


def insertCruceMallaVial():
    with arcpy.da.SearchCursor(viasToInsert, [
        'SHAPE@', 'NOMBREVIA', 'TIPOVIA', 'UBIGEOIZQUIERDA', 'UBIGEODERECHA', 'CODIGOVIA', 'TIPVIA'
    ]) as cursor:
        vias = [list(rowVias) for rowVias in cursor]

    with arcpy.da.InsertCursor(cruceMallaVial, [
        'SHAPE@', 'NOMBREVIA', 'TIPOVIA', 'UBIGEO', 'CODIGOVIA', 'TIPVIA'
    ]) as cursorCruce:
        for via in vias:
            izquierda = [via[0], via[1], via[2], via[3], via[5], via[6]]
            derecha = [via[0], via[1], via[2], via[4], via[5], via[6]]
            if izquierda[3] == derecha[3]:
                cursorCruce.insertRow(izquierda)
            else:
                cursorCruce.insertRow(izquierda)
                cursorCruce.insertRow(derecha)
    print("Registros insertados en CRUCEMALLAVIAL")

def dissolveCruceMallaVial():
    # Set local variables
    inFeatures = viasToInsert
    outFeatureClass = "BACKUP_CONTUGAS_27-09-2021.gdb/CRUCEMALLAVIAL2"
    dissolveFields = ["CODIGOVIA", "NOMBREVIA"]
    statistics = [["TIPOVIA", "MAX"]]

    arcpy.Delete_management(outFeatureClass)
    
    # Execute Dissolve using CODIGOVIA and NOMBREVIA as Dissolve Fields
    arcpy.Dissolve_management(inFeatures, outFeatureClass, dissolveFields, statistics, 
                            "MULTI_PART", "DISSOLVE_LINES")

    with arcpy.da.SearchCursor(outFeatureClass, [
        'SHAPE@', 'CODIGOVIA', 'NOMBREVIA', 'MAX_TIPOVIA'
    ]) as cursor:
        vias = [list(rowVias) for rowVias in cursor]

    # Delete all current rows to empty layer
    with arcpy.da.UpdateCursor(cruceMallaVial, [
        'SHAPE@', 'CODIGOVIA', 'NOMBREVIA', 'TIPOVIA'
    ]) as cursorCruce:
        for row in cursorCruce:
            cursorCruce.deleteRow()
    
    # Insert new rows based on dissolved features (multipart)
    with arcpy.da.InsertCursor(cruceMallaVial, [
        'SHAPE@', 'CODIGOVIA', 'NOMBREVIA', 'TIPOVIA'
    ]) as cursorCruce:
        for via in vias:
            cursorCruce.insertRow(via)

    print("Registros insertados en CRUCEMALLAVIAL")

def estadisticasMallaVial():
    countSN = 0.0
    countCodigoUnico = 0.0
    codigos = {}
    queryProvincia = "UBIGEOIZQUIERDA LIKE '110%' OR UBIGEODERECHA LIKE '110%'"

    with arcpy.da.SearchCursor(viasToInsert, [
        'SHAPE@', 'NOMBREVIA', 'TIPOVIA', 'UBIGEOIZQUIERDA', 'UBIGEODERECHA', 'CODIGOSEGMENTOVIA', 'CODIGOVIA'
    ], where_clause=(queryProvincia)) as cursor:
        vias = [list(rowVias) for rowVias in cursor]
        
    for via in vias:
        if via[1] == "SN":
            countSN += 1
        if via[6] not in codigos:
            codigos[via[6]] = {"times":1, "name": via[1]}
            countCodigoUnico += 1
        else:
            codigos[via[6]]["times"] += 1

    sortedCodigos = sorted(codigos.items(), key=lambda x: (x[1]['times'], x[1]['name']), reverse=True)

    print("Vias totales registradas: {0:,}".format(len(vias)))
    print("Vias sin nombre (SN): {0:,.0f} ---> porcentaje: {1:.2f}%".format(countSN, (countSN/len(vias))*100))
    print("Codigos de via registrados (CODIGOVIA): {0:,.0f} ---> porcentaje: {1:.2f}%".format(countCodigoUnico, (countCodigoUnico/len(vias))*100))
    
    for i in sortedCodigos[:5]:
        print(i)
    print("")


##################################################################################################

### Establecer nombre de las vias prioridad: TABLAOSWALDO -> NOMENCLATURA -> OSM
# calculateName(contugasVias)

### Actualizar el tipo de via
# updateTipoDeVia(contugasVias)

### Cambiar nombre a las vias para quitar el prefijo (e.g. "AVENIDA")
# changeName(contugasVias)

### Actualizar el campo CODIGOSEGMENTOVIA
# updateCodigoSegmentoVia(contugasVias)

### Actualizar el campo CODIGOVIA
# updateCodigoNombreTipo(contugasVias)
# updateCodigoLineasAdyacentes(contugasVias)

### Insertar filas nuevas MALLAVIAL
# insertRow()

### Ver estadisticas del proceso
estadisticasMallaVial()

### Crear CRUCEMALLAVIAL
# insertCruceMallaVial()
# dissolveCruceMallaVial()