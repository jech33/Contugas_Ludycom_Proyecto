import arcpy
import os
import time

start_time = time.time()
contugasVias = "BACKUP_CONTUGAS_27-09-2021.gdb/VCentros_Malla_Vial_ICA"
contugasClientes = "BACKUP_CONTUGAS_27-09-2021.gdb/arcgis_CTG_VW_GIS_CLIENTES"

def fields(tablePath):
    tableFieldsObject = arcpy.ListFields(tablePath)
    tableFieldsName = []
    for element in tableFieldsObject:
        tableFieldsName.append(element.name)
    return tableFieldsName

contugasClientesFields = ["OBJECTID", "NOMVIA2", "TIPOVIA", "NOMVIA", "COD_PROVINCIA", "COD_DISTRITO", "COD_MANZANA", "CARA"]
contugasViasFields = [
    "OBJECTID", "NOMBRETENTATIVO_12", 'NOM_ALT_C', 'NOMBREVIA', 
    "PROVINCIA", "DISTRITO", "CODIGOMANZ", "LADOMANZAN", 
    "ref"
    ]

print("Tabla de clientes PLSQL: "+contugasClientes)
print("Vias feature class: "+contugasVias)
print("")
print("Campos tabla de clientes PLSQL: ")
print(contugasClientesFields)
print("")
print("Campos Vias feature class: ")
print(contugasViasFields)
print("")


counter = 0
provincias = ['1101', '1102', '1103', '1105']

# clientesList = []
# # NAZCA: with arcpy.da.SearchCursor(contugasClientes, contugasClientesFields, where_clause=("COD_PROVINCIA = '1103'")) as cursorClientes:
# with arcpy.da.SearchCursor(contugasClientes, contugasClientesFields) as cursorClientes:
#     for row in cursorClientes:
#         clientesList.append(row)

# for element in provincias:
#     viasClause = "PROVINCIA = "+"'"+element+"'"
#     clientesClause = "COD_PROVINCIA = "+"'"+element+"'"
#     print(viasClause)
#     print(clientesClause)



for element in provincias:
    clientesList = []
    viasClause = "PROVINCIA = "+"'"+element+"'"
    clientesClause = "COD_PROVINCIA = "+"'"+element+"'"
    with arcpy.da.SearchCursor(contugasClientes, contugasClientesFields, where_clause=(clientesClause)) as cursorClientes:
        for row in cursorClientes:
            clientesList.append(row)

    # Create update cursor for feature class 
    # NAZCA: with arcpy.da.UpdateCursor(contugasVias, contugasViasFields, where_clause=("PROVINCIA = '1103'")) as cursorVias:
    with arcpy.da.UpdateCursor(contugasVias, contugasViasFields, where_clause=(viasClause)) as cursorVias:
        # Recorrer cada fila de la tabla VIAS
        for rowVias in cursorVias:
            # Recorrer cada fila de la tabla CLIENTES y Calcular TIPOVIA y NOMBREVIA para la tabla VIAS y asignar OBJECTID de CLIENTES
            for rowClientes in clientesList:

                # Verificar coincidencia por manzana
                if rowVias[6]!=None and rowClientes[6]!=None and rowVias[7]!=None and rowClientes[7]!=None:
                    if (
                        (int(rowVias[6]) == int(rowClientes[6])) 
                        and (int(rowVias[7]) == int(rowClientes[7])) 
                        and (rowVias[5]==rowClientes[5])
                        ):
                        # Verificar coincidencia de nombres
                        if rowClientes[3]!=None:
                            if rowVias[1]==None:
                                rowVias[8] = rowClientes[0]
                                rowVias[2] = rowClientes[2]
                                rowVias[3] = rowClientes[3]
                                counter += 1
                                print(
                                    "arcGIS:", 
                                    rowVias[0], rowVias[2], rowVias[3], rowVias[4], rowVias[5], rowVias[6], rowVias[7], rowVias[8]
                                    )
                                print(
                                    "PLSQL:", 
                                    rowClientes[0], rowClientes[2], rowClientes[3], rowClientes[4], rowClientes[5], rowClientes[6], rowClientes[7]
                                    )
                                print("")
                                cursorVias.updateRow(rowVias)
                                break
                            elif (rowClientes[3].upper() in rowVias[1].upper()):
                                rowVias[8] = rowClientes[0]
                                rowVias[2] = rowClientes[2]
                                rowVias[3] = rowClientes[3]
                                counter += 1
                                print(
                                    "arcGIS:", 
                                    rowVias[0], rowVias[2], rowVias[3], rowVias[4], rowVias[5], rowVias[6], rowVias[7], rowVias[8]
                                    )
                                print(
                                    "PLSQL:", 
                                    rowClientes[0], rowClientes[2], rowClientes[3], rowClientes[4], rowClientes[5], rowClientes[6], rowClientes[7]
                                    )
                                print("")
                                cursorVias.updateRow(rowVias)
                                break
                            else:
                                rowVias[8] = rowClientes[0]
                                rowVias[2] = rowClientes[2]
                                rowVias[3] = rowClientes[3]
                                counter += 1
                                print(
                                    "arcGIS:", 
                                    rowVias[0], rowVias[2], rowVias[3], rowVias[4], rowVias[5], rowVias[6], rowVias[7], rowVias[8]
                                    )
                                print(
                                    "PLSQL:", 
                                    rowClientes[0], rowClientes[2], rowClientes[3], rowClientes[4], rowClientes[5], rowClientes[6], rowClientes[7]
                                    )
                                print("")
                                cursorVias.updateRow(rowVias)
                                break
        
          
end_time = time.time()
print("Numero de registros cruzados: ", counter)
print("Inicio Script: ", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(start_time)))
print("Fin Script: ", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(end_time)))
print("Duracion_Script (h): ", time.strftime("%H:%M:%S", time.gmtime(end_time - start_time)))