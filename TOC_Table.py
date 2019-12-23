# -*-coding: utf-8 -*-

"""
***************************************************************************
*                                                                         *
*	Giulio Fattori 23.12.2019         TOCTable v 1.20                 *
*	                                                                  *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

from PyQt5.QtCore import *
from qgis.utils import iface
from qgis.core import (QgsRasterLayer,
                       QgsVectorLayer,
                       QgsMapLayer,
                       QgsMapLayerType,
                       QgsCoordinateReferenceSystem,
                       QgsExpression,
                       QgsField,
                       QgsFields,
                       QgsProject,
                       QgsFeature,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsWkbTypes,
                       QgsProcessing,
                       QgsProcessingUtils,
                       QgsLayerTreeGroup,
                       QgsLayerTreeLayer,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameters,
                       QgsProcessingParameterDefinition,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterVectorLayer,
                       QgsProcessingParameterCrs,
                       QgsProcessingParameterPoint,
                       QgsProcessingParameterExtent,
                       QgsProcessingParameterExpression,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterField,
                       QgsProcessingParameterVectorDestination,
                       QgsProcessingParameterFileDestination,
                       QgsProcessingParameterString,
                       QgsProcessingParameterMapLayer,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterNumber)

import datetime

class TOCTABLEProcessingAlgorithm(QgsProcessingAlgorithm):
    """
    TOC algorithm retrieve info from Metadata and some 
	attributes of each layer and collect it's in a table.
    """
    #INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'


    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return TOCTABLEProcessingAlgorithm()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'TOCTable'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('TOC Table')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('FGscripts')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'FGscripts'

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr("The algorithm retrieves some properties and metadata of the project layers and \
                        inserts them in a table so that they can be inserted in the prints. Keeps track\
                        of the order of layers in the project and any groups\n \
                        Questo algoritmo recupera alcuni metadati e proprietà dei layer del progetto e\
                        li raccoglie in una tabella così da poterli inserire nelle stampe.\
                        Tiene traccia dell'ordine dei layer nel progetto e degli eventuali gruppi")
				

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
       
		# We add a feature sink in which to store our processed features (this
        # usually takes the form of a newly created vector layer when the
        # algorithm is run in QGIS).
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Project_Layers_Table ' + str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
			 
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        
        #CREA TABELLA CONTENUTI PROGETTO
        #per altri campi occorre vedere quali si serve aggiungere
        
        #funzione iterativa per posizione layer nella TOC
        def get_group_layers(group, level):
            level = level + group.name() + ' - '#' >> '
            for child in group.children():
                if isinstance(child, QgsLayerTreeGroup):
                    get_group_layers(child, level)
                else:
                    TOC_dict [child.name()] = level
                    #print(lev)
                    
        #dizionario delle posizioni
        TOC_dict ={}
        
        root = QgsProject.instance().layerTreeRoot()
        for child in root.children():
            level = 'root - ' #' >> '
            if isinstance(child, QgsLayerTreeGroup):
                get_group_layers(child, level)
            elif isinstance(child, QgsLayerTreeLayer):
                #lev = level #+ child.name())
                TOC_dict[child.name()] = level
        
        #abort if TOC is empty
        #feedback.pushInfo (str(TOC_dict))
        #feedback.pushInfo (str(not bool(TOC_dict)))
        
        if not bool(TOC_dict):
            raise QgsProcessingException('Invalid input value: EMPY PROJECT')
            
        
        #parametro denominazione tabella risultante
        report = 'Project_Layers_Table'
		
        fields = QgsFields()
        fields.append(QgsField("Layer_N", QVariant.Int))                    # AA
        fields.append(QgsField("Layer_Group_Level", QVariant.String))       # O
        fields.append(QgsField("Layer_Name", QVariant.String))              # A
        fields.append(QgsField("Feature_Not_Valid", QVariant.Int))          # P
        fields.append(QgsField("Layer_Crs", QVariant.String))               # B
        fields.append(QgsField("Layer_Type", QVariant.Int))                 # C
        fields.append(QgsField("Layer_Type_Name", QVariant.String))         # D
        fields.append(QgsField("Layer_Source", QVariant.String))            # E
        fields.append(QgsField("Layer_Feature_Count", QVariant.Int))        # F
        fields.append(QgsField("Layer_Meta_Parent_Id", QVariant.String))    # G
        fields.append(QgsField("Layer_Meta_Identifier", QVariant.String))   # H
        fields.append(QgsField("Layer_Meta_Title", QVariant.String))        # I
        fields.append(QgsField("Layer_Meta_Type", QVariant.String))         # L
        fields.append(QgsField("Layer_Meta_Language", QVariant.String))     # M
        fields.append(QgsField("Layer_Meta_Abstract", QVariant.String))     # N
        
        
		
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context, fields)
        
        # If sink was not created, throw an exception to indicate that the algorithm
        # encountered a fatal error. The exception text can be any string, but in this
        # case we use the pre-built invalidSinkError method to return a standard
        # helper text for when a sink cannot be evaluated
        if sink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT)) 
            
        feat = QgsFeature()
        count = 1
        
        for layer in QgsProject.instance().mapLayers().values():
            if layer.name().find("Project_Layers_Table") == -1:
                AA = count
                count += 1
                A = layer.name()
                B = layer.crs().authid()
                E = layer.source()
                G = layer.metadata().parentIdentifier()
                H = layer.metadata().identifier()
                I = layer.metadata().title()
                L = layer.metadata().type()
                M = layer.metadata().language()
                N = layer.metadata().abstract()
                   
                    
                if layer.type() is not QgsMapLayerType.RasterLayer:
                    F = layer.featureCount()
                    C = layer.wkbType()
                    D = QgsWkbTypes.displayString(layer.wkbType())
                    
                    P = 0
                    for f in layer.getFeatures():
                        if not f.geometry().isGeosValid():
                            P += 1
                    
                else:
                    C = (0)
                    D = QgsMapLayerType.RasterLayer.name
                    F = (-1)
                    P = 0
                    
                feat.setAttributes([AA,TOC_dict.get(A),A,P,B,C,D,E,F,G,H,I,L,M,N])
                sink.addFeature(feat, QgsFeatureSink.FastInsert)
        
        feedback.pushInfo ('By GF')
        
        return {self.OUTPUT: dest_id}
