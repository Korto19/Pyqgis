# -*- coding: utf-8 -*-

"""
***************************************************************************
*   GF 09.11.2019                                                                      *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

from PyQt5.QtCore import QCoreApplication, QVariant
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsFeature,
                       QgsField,
                       QgsLayerItem,
                       QgsProcessingParameterString,
                       QgsProcessingParameterNumber, 
                       QgsProcessingParameterVectorLayer,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterEnum,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterField,
                       QgsFeatureRequest,
                       )
import datetime


class CalcolatriceProcessingAlgorithm(QgsProcessingAlgorithm):
    """
   Algorithm that generate progressive sum for a field in layer
    """
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    OPTIONAL_START_VALUE = 'optional_start_value'
    OPERATION_FIELD_NAME = 'operation_field_name'
    RESULT_FIELD_NAME = 'result_field_name'
    OUTPUT_OPERATION = 'output_operation'

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return CalcolatriceProcessingAlgorithm()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'Calc_by_field'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Calcoli su campo')

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
        return self.tr("Replica il layer aggiungendo un nuovo campo con: \n- progressiva,\
        \n- percentuale, \n- media mobile, \n- variazione \n- variazione % \ncalcolata con ordinamento per id.\
        \nIl campo generato ha lo stesso nome dell'origine più un suffisso che richiama il calcolo\
        \nIl nuovo layer ha nome Calc_  più il timestamp\
        \nLa variazione % da 0 a un qualsiasi valore è indicata con 9999999\
        \nLa variazione e la variazione % necessitano di layer non temporanei.")

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
        # We add the input vector features source. It can have any kind of geometry.
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr('Input layer'),
                [QgsProcessing.TypeVector]
            )
        )
        
        self.addParameter(QgsProcessingParameterNumber(self.OPTIONAL_START_VALUE,
                                                       self.tr('Optional start value for progressive (default = 0)'), QgsProcessingParameterNumber.Double,
                                                       0, False, 0))
        
        self.addParameter(QgsProcessingParameterField(self.OPERATION_FIELD_NAME,
                                                       'Choose operation field',
                                                       'N',
                                                       self.INPUT
                                                       ))
        
        self.addParameter(QgsProcessingParameterEnum(self.OUTPUT_OPERATION, 'Option Calc: Progressiva, Percentuale, Media Mobile, Variazione, Variazione %',
                                                        options=['PROGRESSIVA','PERCENTUALE','MEDIA MOBILE','VARIAZIONE','VARIAZIONE %'],
                                                        allowMultiple=False, defaultValue=None))
        
        self.addParameter(QgsProcessingParameterString(self.RESULT_FIELD_NAME,
                                                       self.tr('optional new Field name suffix'),' ',
                                                       ))
        
        # self.addParameter(QgsProcessingParameterBoolean('A', 'A', optional=True, defaultValue=False))
        # We add a feature sink in which to store our processed features (this
        # usually takes the form of a newly created vector layer when the
        # algorithm is run in QGIS).
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Calc_' + str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        source = self.parameterAsSource(
            parameters,
            self.INPUT,
            context)
        optional_start_value = self.parameterAsDouble(
            parameters,
            self.OPTIONAL_START_VALUE,
            context)
        operation_field_name = self.parameterAsString(
            parameters,
            self.OPERATION_FIELD_NAME,
            context)
        output_operation = self.parameterAsString(
            parameters,
            self.OUTPUT_OPERATION,
            context)
        result_field_name = self.parameterAsString(
            parameters,
            self.RESULT_FIELD_NAME,
            context)
        
        if result_field_name == " ":
            result_field_name = ""
        else :
            result_field_name = "_" + result_field_name 
            
        if output_operation == '0':
            result_field_name = "_prog" + result_field_name
        if output_operation == '1':
            result_field_name = "_perc" + result_field_name
        if output_operation == '2':
            result_field_name = "_mo_m" + result_field_name
        if output_operation == '3':
            result_field_name = "_delta" + result_field_name
        if output_operation == '4':
            result_field_name = "_delta%" + result_field_name
        
        fields = source.fields()
        result_field_name = operation_field_name + result_field_name
        fields.append(QgsField(result_field_name,QVariant.Double,'',20,3))
        #fields.append(QgsField('test',QVariant.Double,'',20,3))
        
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context, fields, source.wkbType(), source.sourceCrs())
           
        feedback.pushInfo('Get features')
        features = source.getFeatures()


        # Running the processing algorithm
        feedback.pushInfo('Calculate ' + output_operation +": "+ result_field_name)
        
        if output_operation == '0':
            k = 0
            partial = optional_start_value
        
        if output_operation == '1':
            k = 1
            partial = 0
            sum_values = 0
            for f in source.getFeatures():
                sum_values = sum_values + f[operation_field_name]
            
        if output_operation == '2':
            k = 1
            partial = 0
            
        if output_operation == '3'or output_operation == '4':
            k = 0
            partial = 0
            
        # Read the layer and create output features
        for f in source.getFeatures():
            new_feature = QgsFeature()
            new_feature.setGeometry(f.geometry())
            new_f = f.attributes()
            
            
            if output_operation == '0':
                partial = partial + f[operation_field_name]
            
            if output_operation == '1':
                if f[operation_field_name] != 0:
                    partial = f[operation_field_name] / sum_values
                
            if output_operation == '2':
                partial = (partial * (k-1) + f[operation_field_name])/(k)
            
            if output_operation == '3':
                if k != 0:
                    request = QgsFeatureRequest().setFilterFid(k-1)
                    feat = next(source.getFeatures(request))
                    partial = f[operation_field_name] - feat[operation_field_name]
                    #feedback.pushInfo(str(k) +" -- " +str(feat[operation_field_name])+"  "+str(f[operation_field_name])+"  "+str(partial))
                else:
                    partial  = 0
                    feedback.pushInfo(str(k) + "  " +str(partial))
            
            
            if output_operation == '4':
                if k != 0:
                    request = QgsFeatureRequest().setFilterFid(k-1)
                    feat = next(source.getFeatures(request))
                    if feat[operation_field_name] != 0:
                        partial = (f[operation_field_name] - feat[operation_field_name])/ feat[operation_field_name]
                    else:
                        partial  = 9999999
                        #feedback.pushInfo(str(k) +" -- " +str(feat[operation_field_name])+"  "+str(f[operation_field_name])+"  "+str(partial))
                else:
                    partial  = 0
            
            k = k + 1
            
            new_f.append(partial)
            #new_f.append(10.99)
            new_feature.setAttributes(new_f)
            sink.addFeature(new_feature, QgsFeatureSink.FastInsert)
            
        return {self.OUTPUT: dest_id}