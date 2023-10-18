#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import *
from PyQt6.QtWidgets import QFileDialog, QTreeView, QVBoxLayout, QHBoxLayout, QSplitter, QLabel, QPushButton, QLineEdit, QComboBox, QMessageBox
from PyQt6.QtWidgets import QWidget

from src.gui.sharedcomnponets.sharedcomponets import (WorkAreaTabWidget,
                                                      GUIToolKit)
from src.simpleFOCConnector import SimpleFOCDevice


from datetime import datetime

supportedMCUS = {
  'generic': "Generic MCU",
  'atmega328':"Arduino UNO/Nano/Pro Mini (atmega328)",
  'atmega32u4':"Arduino Leonardo (atmega32u)",
  'atmega2560':"Arduino MEGA (atmega2560)",
  'due':"Arduino DUE (SAM3XBE)",
  'stm32': "Generic STM32",
  'stm32g4':"STM32  B-G431B-ESC1",
  'esp32':"Generic ESP32", 
  'esp8266':"Generic ESP8266", 
  'teensy':"Generic Teensy", 
  'samd21' :"Generic SAMD21", 
  'samd51':"Generic SAMD51", 
  'portenta':"Arduino Portenta H7",
  'rp2040': "Raspberry Pi Pico (rp2040)"
  }

driverMCUFiles = {
  'generic': ["generic_mcu.cpp"],
  'atmega328': ["atmega328_mcu.cpp"],
  'atmega32u4':["atmega32u4_mcu.cpp"],
  'atmega2560': ["atmega2560_mcu.cpp"],
  'due':["due_mcu.cpp"],
  'stm32': ["stm32_mcu.cpp"],
  'stm32g4': ["stm32_mcu.cpp"],
  'esp32':["esp32_mcu.cpp"], 
  'esp8266':["esp8266_mcu.cpp"], 
  'teensy': ["teensy_mcu.cpp"], 
  'samd21' :["samd_mcu.h","samd_mcu.cpp","samd21_mcu.cpp"], 
  'samd51':["samd_mcu.h","samd_mcu.cpp","samd51_mcu.cpp"], 
  'portenta':["portenta_h7_mcu.cpp"],
  'rp2040':["rp2040_mcu.cpp"]
  }

currentsenseMCUFiles = {
  'generic': ["generic_mcu.cpp"],
  'atmega328': ["atmega_mcu.cpp"],
  'atmega32u4':["atmega_mcu.cpp"],
  'atmega2560': ["atmega_mcu.cpp"],
  'due':["due_mcu.cpp"],
  'stm32': ["stm32_mcu.cpp"],
  'stm32g4': ["stm32g4_hal.cpp","stm32g4_hal.h","stm32g4_mcu.cpp"],
  'esp32':["esp32_mcu.cpp","esp32_adc_driver.h","esp32_adc_driver.cpp"], 
  'esp8266':["generic_mcu.cpp"], 
  'teensy': ["teensy_mcu.cpp"], 
  'samd21' :["samd_mcu.cpp","samd21_mcu.h","samd21_mcu.cpp"], 
  'samd51':["samd_mcu.cpp"], 
  'portenta':["generic_mcu.cpp"],
  'rp2040':["generic_mcu.cpp"]
  }


class MinimalCodeDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Generate minimal strcture")
        self.setWindowIcon(GUIToolKit.getIconByName('gen'))


        self.motorSelsctionLayout = QVBoxLayout()

        self.motorLable = IconLabel('add','Motors',  hyperlink='https://docs.simplefoc.com/motors_config', link_label='Docs') 

        self.checkBoxBLDCMotor = QtWidgets.QCheckBox()
        self.checkBoxBLDCMotor.setObjectName('BLDC_motor')
        self.checkBoxBLDCMotor.setText("BLDC Motor")

        self.checkBoxStepperMotor = QtWidgets.QCheckBox()
        self.checkBoxStepperMotor.setObjectName('Stepper_motor')
        self.checkBoxStepperMotor.setText("Stepper Motor")

        self.motorSelsctionLayout.addWidget(self.motorLable)
        self.motorSelsctionLayout.addWidget(self.checkBoxBLDCMotor)
        self.motorSelsctionLayout.addWidget(self.checkBoxStepperMotor)
        self.motorSelsctionLayout.addStretch()
        

        self.driverSelsctionLayout = QVBoxLayout()

        self.driverLabel =  IconLabel('add','Drivers',  hyperlink='https://docs.simplefoc.com/drivers_config', link_label='Docs') 


        self.checkBoxBLDCDriver3PWM = QtWidgets.QCheckBox()
        self.checkBoxBLDCDriver3PWM.setObjectName('BLDC_Driver_3PWM')
        self.checkBoxBLDCDriver3PWM.setText("BLDC Driver 3PWM")

        self.checkBoxBLDCDriver6PWM = QtWidgets.QCheckBox()
        self.checkBoxBLDCDriver6PWM.setObjectName('BLDC_Driver_6PWM')
        self.checkBoxBLDCDriver6PWM.setText("BLDC Driver 6PWM")

        self.checkBoxStepperDriver2PWM = QtWidgets.QCheckBox()
        self.checkBoxStepperDriver2PWM.setObjectName('Stepper_Driver_2PWM')
        self.checkBoxStepperDriver2PWM.setText("Stepper Driver 2PWM")

        self.checkBoxStepperDriver4PWM = QtWidgets.QCheckBox()
        self.checkBoxStepperDriver4PWM.setObjectName('Stepper_Driver_4PWM')
        self.checkBoxStepperDriver4PWM.setText("Stepper Driver 2PWM")

        self.driverSelsctionLayout.addWidget(self.driverLabel)
        self.driverSelsctionLayout.addWidget(self.checkBoxBLDCDriver3PWM)
        self.driverSelsctionLayout.addWidget(self.checkBoxBLDCDriver6PWM)
        self.driverSelsctionLayout.addWidget(self.checkBoxStepperDriver2PWM)
        self.driverSelsctionLayout.addWidget(self.checkBoxStepperDriver4PWM)
        self.driverSelsctionLayout.addStretch()


        self.sensorSelsctionLayout = QVBoxLayout()

        self.sensorLabel = IconLabel('add','Position Sensors', hyperlink='https://docs.simplefoc.com/sensors', link_label='Docs') 

        self.checkBoxEncoder = QtWidgets.QCheckBox()
        self.checkBoxEncoder.setObjectName('Encoder')
        self.checkBoxEncoder.setText("Encoder")

        self.checkBoxHallSensor = QtWidgets.QCheckBox()
        self.checkBoxHallSensor.setObjectName('Hall_Sensor')
        self.checkBoxHallSensor.setText("Hall Sensor")

        self.checkBoxMagneticSPI = QtWidgets.QCheckBox()
        self.checkBoxMagneticSPI.setObjectName('MagSPI')
        self.checkBoxMagneticSPI.setText("Magnetic SPI")

        self.checkBoxMagneticI2C = QtWidgets.QCheckBox()
        self.checkBoxMagneticI2C.setObjectName('MagI2C')
        self.checkBoxMagneticI2C.setText("Magnetic I2C")

        self.checkBoxMagneticPWM = QtWidgets.QCheckBox()
        self.checkBoxMagneticPWM.setObjectName('MagPWM')
        self.checkBoxMagneticPWM.setText("Magnetic PWM")

        self.checkBoxMagneticAnalog = QtWidgets.QCheckBox()
        self.checkBoxMagneticAnalog.setObjectName('MagAnalog')
        self.checkBoxMagneticAnalog.setText("Magnetic Analog")

        self.sensorSelsctionLayout.addWidget(self.sensorLabel)
        self.sensorSelsctionLayout.addWidget(self.checkBoxEncoder)
        self.sensorSelsctionLayout.addWidget(self.checkBoxHallSensor)
        self.sensorSelsctionLayout.addWidget(self.checkBoxMagneticSPI)
        self.sensorSelsctionLayout.addWidget(self.checkBoxMagneticI2C)
        self.sensorSelsctionLayout.addWidget(self.checkBoxMagneticPWM)
        self.sensorSelsctionLayout.addWidget(self.checkBoxMagneticAnalog)
        self.sensorSelsctionLayout.addStretch()
        
        

        self.csSelsctionLayout = QVBoxLayout()
        self.csLable = IconLabel('add','Current Senses', hyperlink='https://docs.simplefoc.com/current_sense', link_label='Docs')

        self.checkBoxCSInline = QtWidgets.QCheckBox()
        self.checkBoxCSInline.setObjectName('Inline')
        self.checkBoxCSInline.setText("In-line")

        self.checkBoxCSLowside = QtWidgets.QCheckBox()
        self.checkBoxCSLowside.setObjectName('lowside')
        self.checkBoxCSLowside.setText("Low-Side")

        self.csSelsctionLayout.addWidget(self.csLable)
        self.csSelsctionLayout.addWidget(self.checkBoxCSInline)
        self.csSelsctionLayout.addWidget(self.checkBoxCSLowside)
        self.csSelsctionLayout.addStretch()
        


        self.commSelsctionLayout = QVBoxLayout()

        self.csLable = IconLabel('add','Communications', hyperlink='https://docs.simplefoc.com/communication', link_label='Docs')

        self.checkBoxCommander = QtWidgets.QCheckBox()
        self.checkBoxCommander.setObjectName('Commander')
        self.checkBoxCommander.setText("Commander")

        self.checkBoxCommStepDir = QtWidgets.QCheckBox()
        self.checkBoxCommStepDir.setObjectName('Step-Dir')
        self.checkBoxCommStepDir.setText("Step-Dir")

        self.commSelsctionLayout.addWidget(self.csLable)
        self.commSelsctionLayout.addWidget(self.checkBoxCommander)
        self.commSelsctionLayout.addWidget(self.checkBoxCommStepDir)
        self.commSelsctionLayout.addStretch()


        self.pathLable = IconLabel('gear','Project settings')
        self.folderPath = SimplePathWidget()
        self.projectNameLabel = QLabel('Project Name')
        self.projectNameEdit = QLineEdit('minimal_project')
        self.projectNameLayout = QHBoxLayout()
        self.projectNameLayout.addWidget(self.projectNameLabel)
        self.projectNameLayout.addWidget(self.projectNameEdit)
        


        self.mcuLable = IconLabel('sensor','Microcontroller type', hyperlink='https://docs.simplefoc.com/microcontrollers', link_label='Supported mcus')
        self.dropDownMCU = QComboBox()
        for family in supportedMCUS:
          self.dropDownMCU.addItem(supportedMCUS[family], family)

        QBtn = QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        text = "<h1>Arduino Minimal Project Code Generation</h1>"
        text += "Generating minimal arduino project using the <i>Simple<b>FOC</b>Studio</i>, based on the <i>Simple<b>FOC</b>library</i> <small>v2.2</small> <br><br>"
        text += "This code will generate a minimal stand alone arduino project which can help you reduce the overall library footprint and isolate only<br> the library code that you actually use in your application.<br>"
        text += "<h4>Choose the library components that you need:</h4>"

        self.layout = QtWidgets.QVBoxLayout()
        message1 = QtWidgets.QLabel(text)
        self.layout.addWidget(message1)
        layoutCheck = QtWidgets.QHBoxLayout()
        layoutCheck.addLayout(self.motorSelsctionLayout)
        layoutCheck.addLayout(self.driverSelsctionLayout)
        layoutCheck.addLayout(self.sensorSelsctionLayout)
        layoutCheck.addLayout(self.csSelsctionLayout)
        layoutCheck.addLayout(self.commSelsctionLayout)
        self.layout.addLayout(layoutCheck)
        self.layout.addWidget(self.mcuLable)
        self.layout.addWidget(self.dropDownMCU)
        self.layout.addWidget(self.pathLable)
        self.layout.addWidget(self.folderPath)
        self.layout.addLayout(self.projectNameLayout)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
    
from git import Repo
import git
import os
import shutil

class MinimalCodeDisplay(WorkAreaTabWidget):

    def __init__(self, parent=None ):
        super().__init__(parent)
        
        self.device = SimpleFOCDevice.getInstance()
        dlg = MinimalCodeDialog()  # If you pass self, the dialog will be centered over the main window as before.
        if not dlg.exec():
          return
          
        # get the version of the library from te github
        try:
          repo = Repo('lib_src')
          QMessageBox.about(self, "INFO", "Using already cloned <i>Simple<b>FOC</b>library</i> files from <i>lib_src</i> folder!")
        except git.exc.NoSuchPathError:
          QMessageBox.about(self, "INFO", "Cloning the <i>Siimple<b>FOC</b>library</i> files to th <i>lib_src</i> folder!<br> This could take few mmoments.")
          repo = Repo.clone_from(
              "https://github.com/simplefoc/Arduino-FOC.git",
              "lib_src",
              single_branch=True,
              branch='v2.2'
          )
          QMessageBox.about(self, "INFO", "Cloning done.")


        folder_path = os.path.join(dlg.folderPath.box.text(),dlg.projectNameEdit.text())
        project_name = dlg.projectNameEdit.text()
        # checking whether folder exists or not
        if os.path.exists(folder_path):
            # checking whether the folder is empty or not
            if len(os.listdir(folder_path)) != 0:
                # messaging saying folder not empty
                QMessageBox.about(self, "ERROR", "Folder is not empty. Project may already exist! <br><br>Rewritig the project files not supported, please choose different project name.")
                return
        else:
            # file not found message
            os.mkdir(folder_path)


        """
        create the ino file
        """
        start_comment = "/* \n* SimpleFOCStudio generated example \n"+ \
                "* at "+datetime.now().strftime("%d/%m/%Y %H:%M:%S"+"\n")+ \
                "*\n*\n"+ \
                "* Chosen components:\n" \

        ino_includes = ""
        start_inc = '#include "src/'
        end_inc = "\" \n"
        
        """
        building the minimal example structure
        """
        # add the source folder
        os.mkdir(os.path.join(folder_path,'src'))

        # common files
        shutil.copytree(os.path.join("lib_src","src/common"), os.path.join(folder_path,"src/common"))

        """ 
        motors
        """
        if dlg.checkBoxBLDCMotor.isChecked():
          shutil.copy(os.path.join('lib_src','src/BLDCMotor.cpp'),os.path.join(folder_path,'src/'))
          shutil.copy(os.path.join('lib_src','src/BLDCMotor.h'),os.path.join(folder_path,'src/'))
          start_comment +="*\t - BLDCMotor\n"
          ino_includes += start_inc+"BLDCMotor.h"+end_inc

        if dlg.checkBoxStepperMotor.isChecked():
          shutil.copy(os.path.join('lib_src','src/StepperMotor.cpp'),os.path.join(folder_path,'src/'))
          shutil.copy(os.path.join('lib_src','src/StepperMotor.h'),os.path.join(folder_path,'src/'))
          start_comment +="*\t - StepperMotor\n"
          ino_includes += start_inc+"StepperMotor.h"+end_inc

        """ 
        drivers
        """
        src_drivers = os.path.join('lib_src','src/drivers')
        target_drivers = os.path.join(folder_path,'src/drivers')

        if  dlg.checkBoxBLDCDriver3PWM.isChecked() or  dlg.checkBoxBLDCDriver6PWM.isChecked() or  dlg.checkBoxStepperDriver2PWM.isChecked() or  dlg.checkBoxStepperDriver4PWM.isChecked():
          os.mkdir(os.path.join(folder_path,'src/drivers'))
          shutil.copy(os.path.join(src_drivers,'hardware_api.h'),target_drivers)
          # add hardware specific stuff
          target_hardware_specific = os.path.join(target_drivers,'hardware_specific')
          src_hardware_specific = os.path.join(src_drivers,'hardware_specific')

          # create hardware specific folder
          os.mkdir(target_hardware_specific)
          # for now coppy the generic as well - this might change in future
          shutil.copy(os.path.join(src_hardware_specific,'generic_mcu.cpp'), target_hardware_specific)    

          # find selected mcu
          mcu = dlg.dropDownMCU.currentData()
          # coppy necessary files
          for file_name in driverMCUFiles[mcu]:
            shutil.copy(os.path.join(src_hardware_specific,file_name), target_hardware_specific)          
   



        if dlg.checkBoxBLDCDriver3PWM.isChecked():
          shutil.copy(os.path.join(src_drivers,'BLDCDriver3PWM.cpp'),target_drivers)
          shutil.copy(os.path.join(src_drivers,'BLDCDriver3PWM.h'),target_drivers)
          start_comment +="*\t - BLDCDriver3PWM\n"
          ino_includes += start_inc+"drivers/BLDCDriver3PWM.h"+end_inc

        if dlg.checkBoxBLDCDriver6PWM.isChecked():
          shutil.copy(os.path.join(src_drivers,'BLDCDriver6PWM.cpp'),target_drivers)
          shutil.copy(os.path.join(src_drivers,'BLDCDriver6PWM.h'),target_drivers)
          start_comment +="*\t - BLDCDriver6PWM\n"
          ino_includes += start_inc+"drivers/BLDCDriver6PWM.h"+end_inc
          
        if dlg.checkBoxStepperDriver2PWM.isChecked():
          shutil.copy(os.path.join(src_drivers,'StepperDriver2PWM.cpp'),target_drivers)
          shutil.copy(os.path.join(src_drivers,'StepperDriver2PWM.h'),target_drivers)
          start_comment +="*\t - StepperDriver2PWM\n"
          ino_includes += start_inc+"drivers/StepperDriver2PWM.h"+end_inc

        if dlg.checkBoxStepperDriver4PWM.isChecked():
          shutil.copy(os.path.join(src_drivers,'StepperDriver4PWM.cpp'),target_drivers)
          shutil.copy(os.path.join(src_drivers,'StepperDriver4PWM.h'),target_drivers)
          start_comment +="*\t - StepperDriver4PWM\n"
          ino_includes += start_inc+"drivers/StepperDriver4PWM.h"+end_inc

        # driver mcu specific

        
        """ 
        sensors
        """
        src_sensors = os.path.join('lib_src','src/sensors')
        target_sensors = os.path.join(folder_path,'src/sensors')

        if dlg.checkBoxEncoder.isChecked() or dlg.checkBoxHallSensor.isChecked() or dlg.checkBoxMagneticAnalog.isChecked() or dlg.checkBoxMagneticSPI.isChecked() or dlg.checkBoxMagneticI2C.isChecked() or dlg.checkBoxMagneticPWM.isChecked():
          os.mkdir(os.path.join(folder_path,'src/sensors'))

        if dlg.checkBoxEncoder.isChecked():
          shutil.copy(os.path.join(src_sensors, 'Encoder.cpp'),target_sensors)
          shutil.copy(os.path.join(src_sensors, 'Encoder.h'),target_sensors)
          start_comment +="*\t - Encoder\n"
          ino_includes += start_inc+"sensors/Encoder.h"+end_inc
          
        if dlg.checkBoxHallSensor.isChecked():
          shutil.copy(os.path.join(src_sensors, 'HallSensor.cpp'),target_sensors)
          shutil.copy(os.path.join(src_sensors, 'HallSensor.h'),target_sensors)
          start_comment +="*\t - HallSensor\n"
          ino_includes += start_inc+"sensors/HallSensor.h"+end_inc
        
        if dlg.checkBoxMagneticSPI.isChecked():
          shutil.copy(os.path.join(src_sensors, 'MagneticSensorSPI.cpp'),target_sensors)
          shutil.copy(os.path.join(src_sensors, 'MagneticSensorSPI.h'),target_sensors)
          start_comment +="*\t - MagneticSensorSPI\n"
          ino_includes += start_inc+"sensors/MagneticSensorSPI.h"+end_inc

        if dlg.checkBoxMagneticI2C.isChecked():
          shutil.copy(os.path.join(src_sensors, 'MagneticSensorI2C.cpp'),target_sensors)
          shutil.copy(os.path.join(src_sensors, 'MagneticSensorI2C.h'),target_sensors)
          start_comment +="*\t - MagneticSensorI2C\n"
          ino_includes += start_inc+"sensors/MagneticSensorSPI.h"+end_inc
             
        if dlg.checkBoxMagneticPWM.isChecked():
          shutil.copy(os.path.join(src_sensors, 'MagneticSensorPWM.cpp'),target_sensors)
          shutil.copy(os.path.join(src_sensors, 'MagneticSensorPWM.h'),target_sensors)
          start_comment +="*\t - MagneticSensorPWM\n"
          ino_includes += start_inc+"sensors/MagneticSensorPWM.h"+end_inc
             
        if dlg.checkBoxMagneticAnalog.isChecked():
          shutil.copy(os.path.join(src_sensors, 'MagneticSensorAnalog.cpp'),target_sensors)
          shutil.copy(os.path.join(src_sensors, 'MagneticSensorAnalog.h'),target_sensors)
          start_comment +="*\t - MagneticSensorAnalog\n"
          ino_includes += start_inc+"sensors/MagneticSensorAnalog.h"+end_inc
             
        """
        current sense 
        """
        src_currentsense = os.path.join('lib_src','src/current_sense')
        target_currentsense = os.path.join(folder_path,'src/current_sense')

        if  dlg.checkBoxCSInline.isChecked() or  dlg.checkBoxCSLowside.isChecked():
          os.mkdir(target_currentsense)
          shutil.copy(os.path.join(src_currentsense,'hardware_api.h'),target_currentsense)

          # add hardware specific stuff
          target_hardware_specific = os.path.join(target_currentsense,'hardware_specific')
          src_hardware_specific = os.path.join(src_currentsense,'hardware_specific')

          # create hardware specific folder
          os.mkdir(target_hardware_specific)
          # for now coppy the generic as well - this might change in future
          shutil.copy(os.path.join(src_hardware_specific,'generic_mcu.cpp'), target_hardware_specific)    

          # find selected mcu
          mcu = dlg.dropDownMCU.currentData()
          # coppy necessary files
          for file_name in currentsenseMCUFiles[mcu]:
            shutil.copy(os.path.join(src_hardware_specific,file_name), target_hardware_specific)  
   


        if dlg.checkBoxCSInline.isChecked():
          shutil.copy(os.path.join(src_currentsense,'InlineCurrentSense.cpp'),target_currentsense)
          shutil.copy(os.path.join(src_currentsense,'InlineCurrentSense.h'),target_currentsense)
          start_comment +="*\t - InlineCurrentSense\n"
          ino_includes += start_inc+"current_sense/InlineCurrentSense.h"+end_inc

        if dlg.checkBoxCSLowside.isChecked():
          shutil.copy(os.path.join(src_currentsense,'LowsideCurrentSense.cpp'),target_currentsense)
          shutil.copy(os.path.join(src_currentsense,'LowsideCurrentSense.h'),target_currentsense)
          start_comment +="*\t - LowsideCurrentSense\n"
          ino_includes += start_inc+"current_sense/LowsideCurrentSense.h"+end_inc
        # current sense specific
        
        """
        communication
        """
        src_communication = os.path.join('lib_src','src/communication')
        target_communication = os.path.join(folder_path,'src/communication')

        if  dlg.checkBoxCommander.isChecked() or  dlg.checkBoxCommStepDir.isChecked():
          os.mkdir(os.path.join(folder_path,'src/communication'))

        if dlg.checkBoxCommander.isChecked():
          shutil.copy(os.path.join(src_communication,'Commander.cpp'),target_communication)
          shutil.copy(os.path.join(src_communication,'Commander.h'),target_communication)
          shutil.copy(os.path.join(src_communication,'commands.h'),target_communication)
          start_comment +="*\t - Commander\n"
          ino_includes += start_inc+"communication/Commander.h"+end_inc

        if dlg.checkBoxCommStepDir.isChecked():
          shutil.copy(os.path.join(src_communication,'StepDirListener.cpp'),target_communication)
          shutil.copy(os.path.join(src_communication,'StepDirListener.h'),target_communication)
          start_comment +="*\t - StepDirListener\n"
          ino_includes += start_inc+"communication/StepDirListener.h"+end_inc

        
        # include file ( maybe )

        # finish the ino file
        f = open(os.path.join(folder_path,project_name+'.ino'), "w")
        start_comment +="*\n* Microcontroller type:\n"
        start_comment +="*\t -"+dlg.dropDownMCU.currentText() +"\n*\n"
        start_comment +="*/\n\n"
        ino_includes += "\n\n"
        f.write(start_comment)
        f.write(ino_includes)
        f.writelines(["void setup(){\n\t\n\t\n",
                "}\n\n",
                "void loop(){\n\t\n\t\n",
                "}\n\n",])
        f.close()

        QMessageBox.about(self, "INFO", "Project generated successfully!")
        
        self.layout = QVBoxLayout()
        
        text = "<h1>Arduino Minimal Project Code Generation</h1>"
        text += "Generated minimal stand alone arduino project using the <i>Simple<b>FOC</b>Studio</i>, based on the <i>Simple<b>FOC</b>library</i> <small>v2.2</small> <br><br>"
        text += "In this window you can simply navigate and familiarise yourself with the code structure.<br>"
        text += "Your project is saved on the disk at the desired path: <b>" + folder_path+"</b><br>"
        text += "<br>"

        message = QtWidgets.QLabel(text)
        self.layout.addWidget(message)
        self.layout.addWidget(QLabel("<h2>Generated project structure:</h2>"))

        self.model = QFileSystemModel()
        self.model.setIconProvider(FileIconProvider())
        self.model.setRootPath(folder_path)
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(folder_path))
        
        self.tree.setAnimated(False)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)
        
        self.tree.setWindowTitle("Project View")
        

        self.codeDisplay = QtWidgets.QTextEdit()
        self.codeDisplay.setObjectName('codeDisplay')
        self.codeDisplay.setText("")
        self.codeDisplay.setReadOnly(True)

        h = Highlighter(self.codeDisplay)
        self.separatedView = QHBoxLayout()
        self.separatedView.addWidget(self.tree)
        self.separatedView.addWidget(self.codeDisplay)

        self.layout.addLayout(self.separatedView)
        self.setLayout(self.layout)

        self.tree.clicked.connect(self.on_treeView_clicked)
        # display ino file on startup
        self.tree.setCurrentIndex(self.model.index(os.path.join(folder_path,project_name+'.ino')))
        self.on_treeView_clicked( self.model.index(os.path.join(folder_path,project_name+'.ino')))

    def getTabIcon(self):
        return GUIToolKit.getIconByName('gen')

    def getTabName(self):
        return 'Generated Code'

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def on_treeView_clicked(self, index):
        indexItem = self.model.index(index.row(), 0, index.parent())
        fileName = self.model.fileName(indexItem)
        filePath = self.model.filePath(indexItem)
        if 'ino' in fileName or 'cpp' in fileName  or 'h' in fileName:
          data = ""
          with open (filePath, "r") as myfile:
            data += myfile.read()
          self.codeDisplay.setText(data)

class IconLabel(QWidget):

    IconSize = QSize(13, 13)
    FontSize = 13

    def __init__(self, icon_name, text, final_stretch=True, hyperlink=None, link_label='More info'):
        super(QWidget, self).__init__()

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        icon = QLabel()
        icon.setPixmap(GUIToolKit.getIconByName(icon_name).pixmap(self.IconSize))

        layout.addWidget(icon)
        a = QLabel(text)
        f = a.font()
        f.setPointSize(self.FontSize)
        f.setBold(True)
        a.setFont(f)
        layout.addWidget(a)

        if hyperlink is not None:
          link = QLabel()
          link.setText('<a href="'+hyperlink+'">'+link_label+'</a>')
          link.setOpenExternalLinks(True)
          layout.addWidget(link) 

        if final_stretch:
            layout.addStretch(1)

class SimplePathWidget(QWidget):

    def __init__(self):
        super().__init__()
        lab = QLabel('Directory')
        btn = QPushButton('Browse')
        btn.clicked.connect(self.open)
        self.box = QLineEdit()
        self.box.setText(os.getcwd())
        vbox = QHBoxLayout(self)
        vbox.addWidget(lab)
        vbox.addWidget(self.box)
        vbox.addWidget(btn)
        vbox.setContentsMargins(0,0,0,0)
        

    def open(self):
        name = QFileDialog.getExistingDirectory(self, "Select Directory")
        if name:
            self.box.setText(name)



class FileIconProvider(QtWidgets.QFileIconProvider):
    def icon(self, parameter):
        if isinstance(parameter, QtCore.QFileInfo):
            info = parameter
            if info.suffix() == "ino":
                return GUIToolKit.getIconByName('ard')
        return super(FileIconProvider, self).icon(parameter)




class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)



        literals1Format = QTextCharFormat()
        literals1Format.setForeground(Qt.darkMagenta)
        literals1Format.setFontWeight(QFont.Bold)

        keyword1Format = QTextCharFormat()
        keyword1Format.setForeground(QColor(255, 140, 0,255))
        keyword1Format.setFontWeight(QFont.Bold)

        f = open(os.path.join('lib_src','keywords.txt'))
        keywords1 = []
        keywords2 = []
        keywords3 = []
        literals1 = []
        for line in f.readlines():
          line = line.strip()
          if len(line):
            line = line.split()
            if 'KEYWORD1' in line[1]:
              keywords1.append(line[0])
            elif 'KEYWORD2' in line[1]:
              keywords2.append(line[0])
            elif 'KEYWORD3' in line[1]:
              keywords3.append(line[0])
            elif 'LITERAL1' in line[1]:
              literals1.append(line[0])

        self.highlightingRules = [(QRegularExpression(pattern), keyword1Format)
                for pattern in keywords1]
                
        [self.highlightingRules.append((QRegularExpression(pattern), literals1Format))
                for pattern in literals1]


        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(Qt.darkCyan)
        keywordPatterns = ["\\bchar\\b", "\\bclass\\b", "\\bconst\\b",
                "\\bdouble\\b","\\bfloat\\b", "\\benum\\b", "\\bexplicit\\b", "\\bfriend\\b",
                "\\binline\\b", "\\bint\\b", "\\blong\\b", "\\bnamespace\\b",
                "\\boperator\\b", "\\bprivate\\b", "\\bprotected\\b",
                "\\bpublic\\b", "\\bshort\\b", "\\bsignals\\b", "\\bsigned\\b",
                "\\bslots\\b", "\\bstatic\\b", "\\bstruct\\b",
                "\\btemplate\\b", "\\btypedef\\b", "\\btypename\\b",
                "\\bunion\\b", "\\bunsigned\\b", "\\bvirtual\\b", "\\bvoid\\b",
                "\\bvolatile\\b","\\bbool\\b"]

        [self.highlightingRules.append((QRegularExpression(pattern), keywordFormat))
                for pattern in keywordPatterns]


        classFormat = QTextCharFormat()
        classFormat.setFontWeight(QFont.Bold)
        classFormat.setForeground(Qt.darkMagenta)
        self.highlightingRules.append((QRegularExpression("\\bQ[A-Za-z]+\\b"),
                classFormat))

        singleLineCommentFormat = QTextCharFormat()
        singleLineCommentFormat.setForeground(Qt.darkGray)
        self.highlightingRules.append((QRegularExpression("//[^\n]*"),
                singleLineCommentFormat))

        self.multiLineCommentFormat = QTextCharFormat()
        self.multiLineCommentFormat.setForeground(Qt.darkGray)

        quotationFormat = QTextCharFormat()
        quotationFormat.setForeground(QColor(255, 140, 0,255))
        quotationFormat.setFontWeight(QFont.Bold)
        self.highlightingRules.append((QRegularExpression("\".*\""), quotationFormat))

        functionFormat = QTextCharFormat()
        functionFormat.setFontItalic(True)
        functionFormat.setForeground(Qt.black)
        self.highlightingRules.append((QRegularExpression("\\b[A-Za-z0-9_]+(?=\\()"),
                functionFormat))

        self.commentStartExpression = QRegularExpression("/\\*")
        self.commentEndExpression = QRegularExpression("\\*/")


        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(Qt.darkGreen)
        keywordPatterns = ["\\bif\\b", "\\belse\\b", "\\breturn\\b", "\\bswitch\\b", "\\bcase\\b","\\bwhile\\b"]

        [self.highlightingRules.append((QRegularExpression(pattern), keywordFormat))
                for pattern in keywordPatterns]

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegularExpression(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        startIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.commentStartExpression.indexIn(text)

        while startIndex >= 0:
            endIndex = self.commentEndExpression.indexIn(text, startIndex)

            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIndex
            else:
                commentLength = endIndex - startIndex + self.commentEndExpression.matchedLength()

            self.setFormat(startIndex, commentLength,
                    self.multiLineCommentFormat)
            startIndex = self.commentStartExpression.indexIn(text,
                    startIndex + commentLength);
