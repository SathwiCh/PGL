import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton,QVBoxLayout,QFrame,QWidget
from PyQt5.QtCore import QFile, QTextStream
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtWidgets
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

# import the generated UI code
from GUI_1 import Ui_MainWindow

#import the classes from python files
from Home_Tab import HomePlotter
from Energy import EnergyPlotter
from Incomer import IncomerPlotter
from EC02 import EC02Plotter
from EC03 import EC03Plotter

#Read the Dataframes from the local
df_ec02=pd.read_csv('C:\\Users\\20339181\\OneDrive - L&T Construction\\Desktop\\Dashboards-Analytics\\PyQt5-Dashboard-Main\\Dashboard Template\\new_ec02.csv')
df_ec03=pd.read_csv('C:\\Users\\20339181\\OneDrive - L&T Construction\\Desktop\\Dashboards-Analytics\\PyQt5-Dashboard-Main\\Dashboard Template\\new_ec03.csv')
df_ec02_ec03=pd.read_csv('C:\\Users\\20339181\\OneDrive - L&T Construction\\Desktop\\Dashboards-Analytics\\PyQt5-Dashboard-Main\\Dashboard Template\\ec02_ec03.csv')
print("datasets Loaded")

#Converting the Time column to the pandas datetime object
df_ec02['Time column 1'] = df_ec02['Time column 1'].astype(str)
df_ec02['Time column 1'] = pd.to_datetime(df_ec02['Time column 1'],format = '%d.%m.%Y %H:%M:%S.%f')
df_ec03['Time column 1'] = df_ec03['Time column 1'].astype(str)
df_ec03['Time column 1'] = pd.to_datetime(df_ec03['Time column 1'],format = '%d.%m.%Y %H:%M:%S.%f')
df_ec02_ec03['Time column 1'] = df_ec02_ec03['Time column 1'].astype(str)
df_ec02_ec03['Time column 1'] = pd.to_datetime(df_ec02_ec03['Time column 1'],format = '%d.%m.%Y %H:%M:%S.%f')
print("Timestamp changed")

#create a Varible to store buildings data of ec02 
ec02_buildings = df_ec02[df_ec02['building'].isin(['TC-1','TC&MEDICAL'])]
#create a Varible to store buildings data of ec03
ec03_buildings = df_ec03[df_ec03['building'].isin(['TC3-TOWER A', 'TC3-TOWER B', 'TC3 HVAC'])]
#Create a variable to store all the building data
df_all_buildings = df_ec02_ec03[(df_ec02_ec03["building"] == 'TC-1') | (df_ec02_ec03["building"] == 'TC&MEDICAL') | (df_ec02_ec03["building"] == 'TC3-TOWER A') | (df_ec02_ec03["building"] == 'TC3-TOWER B') | (df_ec02_ec03["building"] == 'TC3 HVAC')]
#Create a variable to store all the meters data
df_meters=df_ec02_ec03[(df_ec02_ec03["meter"] == '11kv_415Vtrafo') | (df_ec02_ec03["meter"] == '33kV trafo-1') | (df_ec02_ec03["meter"] == '33kV trafo-2') | (df_ec02_ec03["meter"] == '33kV trafo-3') |
        (df_ec02_ec03["meter"] == '33kV trafo-4') | (df_ec02_ec03["meter"] == '33kV trafo-5') | (df_ec02_ec03["meter"] == 'EC02 MFM 11KV TRAFO') | (df_ec02_ec03["meter"] == '33KV Incomer')]

last_date = pd.to_datetime('2022-09-28')
home_df = df_all_buildings[df_all_buildings['Time column 1'].dt.date == last_date.date()]

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #create an instances for the classes
        self.home_plotter=HomePlotter(self.ui)
        self.energy_plotter=EnergyPlotter(self.ui)
        self.incomer_plotter=IncomerPlotter(self.ui)
        self.ec02_plotter=EC02Plotter(self.ui)
        self.ec03_plotter=EC03Plotter(self.ui)

        #Hide the icon widget when Intial display of Dashboard
        self.ui.icon_only_widget.hide()
        self.ui.stackedWidget.setCurrentIndex(3)
        self.ui.stackedWidget_3.setCurrentIndex(0)
        #Display the home tab when initial display of Dashboard
        self.ui.home_btn_2.setChecked(True)
        #Display the Energy tab inside home tab, when initial display of Dashboard
        self.ui.energy_btn_3.setChecked(True)

        #Fetch the date from the dateEdit and convert into pandas Datetime object type for the Analytics Tab
        from_date = self.ui.From_date.date().toPyDate()
        to_date = self.ui.To_date.date().toPyDate()
        from_ts = pd.Timestamp(from_date)
        to_ts = pd.Timestamp(to_date)

        #Fetch the date from the dateEdit and convert into pandas Datetime object type for the Insights Tab
        from_date1 = self.ui.From_date_Insights.date().toPyDate()
        to_date1 = self.ui.To_date_Insights.date().toPyDate()
        from_ts1 = pd.Timestamp(from_date1)
        to_ts1 = pd.Timestamp(to_date1)

        #Add unique meters list of ec02 to the meters dropdown in ec02 tab
        ec02_meter_values = ec02_buildings["meter"].unique().tolist()
        self.ui.ec02_meter_cb.addItems(ec02_meter_values)

        #Add unique meters list of ec03 to the meters dropdown in ec03 tab
        ec03_meter_values = ec03_buildings["meter"].unique().tolist()
        self.ui.ec03_meter_cb.addItems(ec03_meter_values)

        #Add unique Buildings list of ec02 to the Buildings dropdown in ec02 tab- Analytics tab
        ec02_building_names = ec02_buildings["building"].unique().tolist()
        self.ui.ec02_building_cb.addItems(ec02_building_names)
        #call the update_ec02_meter_combobox function when the building name is changed and update the meter names
        self.ui.ec02_building_cb.currentIndexChanged.connect(self.update_ec02_meter_combobox)

        #Add unique Buildings list of ec03 to the Buildings dropdown in ec03 tab- Analytics tab
        ec03_building_names = ec03_buildings["building"].unique().tolist()
        self.ui.ec03_building_cb.addItems(ec03_building_names)
        #call the update_ec03_meter_combobox function when the building name is changed and update the meter names
        self.ui.ec03_building_cb.currentIndexChanged.connect(self.update_ec03_meter_combobox)

        #Add Incomer meters list to the meters dropdown in the Incomer tab- Analytics tab
        Incomer_names = df_meters["meter"].unique()
        self.ui.incomer_cb.addItems(Incomer_names)
        
        #Add Incomer meters list to the meters dropdown - Insights tab 
        Incomer_names = df_meters["meter"].unique()
        self.ui.In_insights_cb.addItems(Incomer_names)
        #Call the update_incomer_chords function when the dropdown value changed
        self.ui.In_insights_cb.currentIndexChanged.connect(self.update_incomer_chords)

        #Add centers list to the dropdown- Insights tab 
        center_names = df_all_buildings["center"].unique()
        self.ui.BI_insights_cb.addItems(center_names)
        #Call the update_building_chords function when the dropdown value changed
        self.ui.BI_insights_cb.currentIndexChanged.connect(self.update_building_chords)

        self.home_plotter.home_piechart()
        self.home_plotter.home_meterchart()
        self.home_plotter.home_buildingchart()

        #Default plotting of graphs for the Energy tab- Analytics tab
        self.energy_plotter.total_energy_consumption(from_ts, to_ts)
        self.energy_plotter.weekly_graph(from_ts, to_ts)
        self.energy_plotter.centerwise_piechart(from_ts, to_ts)

        #Default plotting of graphs for the Incomers tab- Analytics tab
        self.incomer_plotter.total_incomer_supply(from_ts, to_ts)

        #Default plotting of graphs for the EC02 tab- Analytics tab
        self.ec02_plotter.ec02_energy_consumption(from_ts, to_ts)
        self.ec02_plotter.ec02_meter_piechart(from_ts, to_ts)
        self.ec02_plotter.ec02_fre_deviations(from_ts,to_ts)
        self.ec02_plotter.ec02_PF_deviations(from_ts,to_ts)
        self.ec02_plotter.ec02_Vswell_Vsag(from_ts,to_ts)
        
        #Default plotting of graphs for the EC03 tab- Analytics tab
        self.ec03_plotter.ec03_energy_consumption(from_ts, to_ts)
        self.ec03_plotter.ec03_meter_piechart(from_ts,to_ts)
        self.ec03_plotter.ec03_fre_deviations(from_ts,to_ts)
        self.ec03_plotter.ec03_PF_deviations(from_ts,to_ts)
        self.ec03_plotter.ec03_Vswell_Vsag(from_ts,to_ts)

        #Create the variable to store the returned values for the home tab pf and frequeny deviations
        Home_PfD=self.home_plotter.home_pf_deviation()
        Home_FrD=self.home_plotter.home_fre_deviation()
        self.ui.Home_pf_lb.setText(Home_PfD)
        self.ui.Home_freq_lb.setText(Home_FrD)

        #Create the variable to store the returned values from the "Main Incomer" Functions
        MI_kwh11,MI_kwh33 = self.MI_kwh(from_ts1, to_ts1)
        MI_freq_11,MI_freq_33= self.MI_frequency(from_ts1,to_ts1)
        MI_pf_11,MI_pf_33=self.MI_powerfactor(from_ts1,to_ts1)
        MI_high_kwh=self.MI_high_kwh(from_ts1,to_ts1)
        MI_33VswellR,MI_33VswellY,MI_33VswellB,MI_33VsagR,MI_33VsagY,MI_33VsagB=self.MI_33kv_Vswell_Vsag(from_ts1,to_ts1)
        MI_11VswellR,MI_11VswellY,MI_11VswellB,MI_11VsagR,MI_11VsagY,MI_11VsagB=self.MI_11kv_Vswell_Vsag(from_ts1,to_ts1)
        MI_11kvidlehours,MI_33kvidlehours=self.MI_idlehours(from_ts1,to_ts1)

        #Create the variable to store the returned values from the "Incomer" Functions
        In_kwh=self.In_kwh(from_ts1, to_ts1)
        In_freq=self.In_frequency(from_ts1,to_ts1)
        In_pf=self.In_powerfactor(from_ts1,to_ts1)
        In_VswellR,In_VswellY,In_VswellB,In_VsagR,In_VsagY,In_VsagB=self.In_Vswell_Vsag(from_ts1,to_ts1)
        In_idlehrs=self.In_idlehours(from_ts1,to_ts1)

        #Create the variable to store the returned values from the "Buildings" Functions
        BI_kwh=self.BI_kwh(from_ts1,to_ts1)
        BI_idlehrs=self.BI_idlehours(from_ts1, to_ts1)
        BI_kwhMax=self.BI_kwh_max(from_ts1,to_ts1)
        BI_kwhMin=self.BI_kwh_min(from_ts1,to_ts1)

        #Set the return text to the referred lables and display
        self.ui.MI_kwh_lb.setText(f"{MI_kwh11}<br>{MI_kwh33}") 
        self.ui.MI_feq_lb.setText(f"{MI_freq_11}<br>{MI_freq_33}")
        self.ui.MI_pf_lb.setText(f"{MI_pf_11}<br>{MI_pf_33}")
        self.ui.MI_33VSwellR_lb.setText(MI_33VswellR)
        self.ui.MI_33VSwellY_lb.setText(MI_33VswellY)
        self.ui.MI_33VSwellB_lb.setText(MI_33VswellB)
        self.ui.MI_33VSagR_lb.setText(MI_33VsagR)
        self.ui.MI_33VSagY_lb.setText(MI_33VsagY)
        self.ui.MI_33VSagB_lb.setText(MI_33VsagB)
        self.ui.MI_11VSwellR_lb.setText(MI_11VswellR)
        self.ui.MI_11VSwellY_lb.setText(MI_11VswellY)
        self.ui.MI_11VSwellB_lb.setText(MI_11VswellB)
        self.ui.MI_11VSagR_lb.setText(MI_11VsagR)
        self.ui.MI_11VSagY_lb.setText(MI_11VsagY)
        self.ui.MI_11VSagB_lb.setText(MI_11VsagB)
        self.ui.MI_idlehours_lb.setText(f"{MI_11kvidlehours}<br>{MI_33kvidlehours}")
        self.ui.MI_highkwh_lb.setText(MI_high_kwh)

        #Set the return text to the referred lables and display 
        self.ui.In_kwh_lb.setText(In_kwh)
        self.ui.In_freq_lb.setText(In_freq)
        self.ui.In_pf_lb.setText(In_pf)
        self.ui.In_VswellR_lb.setText(In_VswellR)
        self.ui.In_VswellY_lb.setText(In_VswellY)
        self.ui.In_VswellB_lb.setText(In_VswellB)
        self.ui.In_VsagR_lb.setText(In_VsagR)
        self.ui.In_VsagY_lb.setText(In_VsagY)
        self.ui.In_VsagB_lb.setText(In_VsagB)
        self.ui.In_idlehours_lb.setText(In_idlehrs)

        #Set the return text to the referred lables and display
        self.ui.BI_kwh_lb.setText(BI_kwh)
        self.ui.BI_idlehours_lb.setText('\n'.join(BI_idlehrs))
        self.ui.BI_highkwh_lb.setText(f"{BI_kwhMax}<br>{BI_kwhMin}")
        print("Default plotting done")
        #Call the Change_voltage_graphs Function when the meter name is changed from the drop down
        self.ui.incomer_cb.currentTextChanged.connect(self.change_voltage_graphs)
        self.ui.ec02_meter_cb.currentTextChanged.connect(self.change_voltage_graphs)
        self.ui.ec03_meter_cb.currentTextChanged.connect(self.change_voltage_graphs)

        #Call the Change_current_graphs Function when the meter name is changed from the drop down
        self.ui.incomer_cb.currentTextChanged.connect(self.change_current_graphs)
        self.ui.ec02_meter_cb.currentTextChanged.connect(self.change_current_graphs)
        self.ui.ec03_meter_cb.currentTextChanged.connect(self.change_current_graphs)

        #Call the Change_pf_graphs Function when the meter name is changed from the drop down
        self.ui.incomer_cb.currentTextChanged.connect(self.change_pf_graphs)
        self.ui.ec02_meter_cb.currentTextChanged.connect(self.change_pf_graphs)
        self.ui.ec03_meter_cb.currentTextChanged.connect(self.change_pf_graphs)

        #Call the Change_fre_graphs Function when the meter name is changed from the drop down
        self.ui.incomer_cb.currentTextChanged.connect(self.change_fre_graphs)
        self.ui.ec02_meter_cb.currentTextChanged.connect(self.change_fre_graphs)
        self.ui.ec03_meter_cb.currentTextChanged.connect(self.change_fre_graphs)

        # Connect the single slot function to both dateChanged signals for Analytics
        self.ui.From_date.dateChanged.connect(self.call_graphs)
        self.ui.To_date.dateChanged.connect(self.call_graphs)
        # Connect the single slot function to both dateChanged signals for Insights
        self.ui.From_date_Insights.dateChanged.connect(self.update_all_chords)
        self.ui.To_date_Insights.dateChanged.connect(self.update_all_chords)

#Connecting Signals to the buttons      
    def on_home_btn_1_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(3)
    def on_analytics_btn_1_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    def on_insights_btn_1_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(1)
    def on_prediction_btn_1_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(2)

#Connecting Signals to the buttons  
    def on_home_btn_2_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(3)
    def on_analytics_btn_2_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    def on_insights_btn_2_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(1)
    def on_prediction_btn_2_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(2)

#Connecting Signals to the buttons          
    def on_energy_btn_3_clicked(self):
        self.ui.stackedWidget_3.setCurrentIndex(0)
    def on_incomer_btn_3_clicked(self):
        self.ui.stackedWidget_3.setCurrentIndex(1)
    def on_ec02_btn_3_clicked(self):
        self.ui.stackedWidget_3.setCurrentIndex(2)
    def on_ec03_btn_3_clicked(self):
        self.ui.stackedWidget_3.setCurrentIndex(3)   
    def on_stackedWidget_currentChanged(self, index):
        btn_list = self.ui.icon_only_widget.findChildren(QPushButton) \
                    + self.ui.full_menu_widget.findChildren(QPushButton)
        
        for btn in btn_list:
            if index in [5, 6]:
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)   

#Update the dropdown box of meters when the building name is changed for the tabs ec02 & ec03   
    def update_ec02_meter_combobox(self):
        selected_building = self.ui.ec02_building_cb.currentText()
        building_df = ec02_buildings[ec02_buildings["building"] == selected_building]
        meter_names = building_df["meter"].unique().tolist()
        self.ui.ec02_meter_cb.clear()
        self.ui.ec02_meter_cb.addItems(meter_names)
    def update_ec03_meter_combobox(self):
        selected_building = self.ui.ec03_building_cb.currentText()
        building_df = ec03_buildings[ec03_buildings["building"] == selected_building]
        meter_names = building_df["meter"].unique().tolist()
        self.ui.ec03_meter_cb.clear()
        self.ui.ec03_meter_cb.addItems(meter_names)

#Update all the plots when the date is changed    
    def call_graphs(self,selected_meter):
        self.update_all_graphs()
        self.change_voltage_graphs(selected_meter)
        self.change_current_graphs(selected_meter)
        self.change_pf_graphs(selected_meter)
        self.change_fre_graphs(selected_meter)
    def update_all_graphs(self):
        # Get the updated values of from_date and to_date from the dateEdit widgets
        from_date = self.ui.From_date.date().toPyDate()
        to_date = self.ui.To_date.date().toPyDate()
        from_ts = pd.Timestamp(from_date)
        to_ts = pd.Timestamp(to_date)
        #energy centers graphs
        self.energy_plotter.total_energy_consumption(from_ts, to_ts)
        self.energy_plotter.centerwise_piechart(from_ts, to_ts)
        self.energy_plotter.weekly_graph(from_ts, to_ts)
        #Incomers Graphs
        self.incomer_plotter.total_incomer_supply(from_ts, to_ts)
        #EC02 graphs
        self.ec02_plotter.ec02_energy_consumption(from_ts, to_ts)
        self.ec02_plotter.ec02_meter_piechart(from_ts, to_ts)
        self.ec02_plotter.ec02_fre_deviations(from_ts,to_ts)
        self.ec02_plotter.ec02_PF_deviations(from_ts,to_ts)
        self.ec02_plotter.ec02_Vswell_Vsag(from_ts,to_ts)
        #EC03 graphs
        self.ec03_plotter.ec03_energy_consumption(from_ts, to_ts)
        self.ec03_plotter.ec03_meter_piechart(from_ts,to_ts)
        self.ec03_plotter.ec03_fre_deviations(from_ts,to_ts)
        self.ec03_plotter.ec03_PF_deviations(from_ts,to_ts)    
        self.ec03_plotter.ec03_Vswell_Vsag(from_ts,to_ts)   
    def change_voltage_graphs(self, selected_meter):
        from_date = self.ui.From_date.date().toPyDate()
        to_date = self.ui.To_date.date().toPyDate()
        from_ts = pd.Timestamp(from_date)
        to_ts = pd.Timestamp(to_date)
        sender = self.sender()
        if sender == self.ui.incomer_cb:
            frame = self.ui.incomer_V_frame
        elif sender == self.ui.ec02_meter_cb:
            frame = self.ui.ec02_V_frame
        elif sender == self.ui.ec03_meter_cb:
            frame = self.ui.ec03_V_frame
        else:
            frame = None
        self.voltage(from_ts, to_ts, selected_meter,frame)
    def change_current_graphs(self, selected_meter):
        from_date = self.ui.From_date.date().toPyDate()
        to_date = self.ui.To_date.date().toPyDate()
        from_ts = pd.Timestamp(from_date)
        to_ts = pd.Timestamp(to_date)
        sender = self.sender()
        if sender == self.ui.incomer_cb:
            frame = self.ui.incomer_I_frame
        elif sender == self.ui.ec02_meter_cb:
            frame = self.ui.ec02_I_frame
        elif sender == self.ui.ec03_meter_cb:
            frame = self.ui.ec03_I_frame
        else:
            frame = None
        self.current(from_ts, to_ts, selected_meter,frame)
    def change_pf_graphs(self, selected_meter):
        from_date = self.ui.From_date.date().toPyDate()
        to_date = self.ui.To_date.date().toPyDate()
        from_ts = pd.Timestamp(from_date)
        to_ts = pd.Timestamp(to_date)
        sender = self.sender()
        if sender == self.ui.incomer_cb:
            frame = self.ui.incomer_PF_frame
        elif sender == self.ui.ec02_meter_cb:
            frame = self.ui.ec02_PF_frame
        elif sender == self.ui.ec03_meter_cb:
            frame = self.ui.ec03_PF_frame
        else:
            frame = None
        self.powerfactor(from_ts, to_ts, selected_meter,frame)
    def change_fre_graphs(self, selected_meter):
        from_date = self.ui.From_date.date().toPyDate()
        to_date = self.ui.To_date.date().toPyDate()
        from_ts = pd.Timestamp(from_date)
        to_ts = pd.Timestamp(to_date)
        sender = self.sender()
        if sender == self.ui.incomer_cb:
            frame = self.ui.incomer_Freq_frame
        elif sender == self.ui.ec02_meter_cb:
            frame = self.ui.ec02_Freq_frame
        elif sender == self.ui.ec03_meter_cb:
            frame = self.ui.ec03_Freq_frame
        else:
            frame = None
        self.frequency(from_ts, to_ts, selected_meter,frame)

#Update all the chords when the date is changed
    def update_all_chords(self):
        from_date = self.ui.From_date_Insights.date().toPyDate()
        to_date = self.ui.To_date_Insights.date().toPyDate()
        from_ts1 = pd.Timestamp(from_date)
        to_ts1 = pd.Timestamp(to_date)

        MI_kwh11,MI_kwh33 = self.MI_kwh(from_ts1, to_ts1)
        MI_freq_11,MI_freq_33= self.MI_frequency(from_ts1,to_ts1)
        MI_pf_11,MI_pf_33=self.MI_powerfactor(from_ts1,to_ts1)
        MI_high_kwh=self.MI_high_kwh(from_ts1,to_ts1)
        MI_33VswellR,MI_33VswellY,MI_33VswellB,MI_33VsagR,MI_33VsagY,MI_33VsagB=self.MI_33kv_Vswell_Vsag(from_ts1,to_ts1)
        MI_11VswellR,MI_11VswellY,MI_11VswellB,MI_11VsagR,MI_11VsagY,MI_11VsagB=self.MI_11kv_Vswell_Vsag(from_ts1,to_ts1)
        MI_11kvidlehours,MI_33kvidlehours=self.MI_idlehours(from_ts1,to_ts1)

        In_kwh=self.In_kwh(from_ts1, to_ts1)
        In_freq=self.In_frequency(from_ts1,to_ts1)
        In_pf=self.In_powerfactor(from_ts1,to_ts1)
        In_VswellR,In_VswellY,In_VswellB,In_VsagR,In_VsagY,In_VsagB=self.In_Vswell_Vsag(from_ts1,to_ts1)
        In_idlehrs=self.In_idlehours(from_ts1,to_ts1)


        BI_kwh=self.BI_kwh(from_ts1,to_ts1)
        BI_idlehrs=self.BI_idlehours(from_ts1, to_ts1)
        BI_kwhMax=self.BI_kwh_max(from_ts1,to_ts1)
        BI_kwhMin=self.BI_kwh_min(from_ts1,to_ts1)

        self.ui.MI_kwh_lb.setText(f"{MI_kwh11}<br>{MI_kwh33}") 
        self.ui.MI_feq_lb.setText(f"{MI_freq_11}<br>{MI_freq_33}")
        self.ui.MI_pf_lb.setText(f"{MI_pf_11}<br>{MI_pf_33}")
        self.ui.MI_33VSwellR_lb.setText(MI_33VswellR)
        self.ui.MI_33VSwellY_lb.setText(MI_33VswellY)
        self.ui.MI_33VSwellB_lb.setText(MI_33VswellB)
        self.ui.MI_33VSagR_lb.setText(MI_33VsagR)
        self.ui.MI_33VSagY_lb.setText(MI_33VsagY)
        self.ui.MI_33VSagB_lb.setText(MI_33VsagB)
        self.ui.MI_11VSwellR_lb.setText(MI_11VswellR)
        self.ui.MI_11VSwellY_lb.setText(MI_11VswellY)
        self.ui.MI_11VSwellB_lb.setText(MI_11VswellB)
        self.ui.MI_11VSagR_lb.setText(MI_11VsagR)
        self.ui.MI_11VSagY_lb.setText(MI_11VsagY)
        self.ui.MI_11VSagB_lb.setText(MI_11VsagB)
        self.ui.MI_idlehours_lb.setText(f"{MI_11kvidlehours}<br>{MI_33kvidlehours}")
        self.ui.MI_highkwh_lb.setText(MI_high_kwh)

        self.ui.In_kwh_lb.setText(In_kwh)
        self.ui.In_freq_lb.setText(In_freq)
        self.ui.In_pf_lb.setText(In_pf)
        self.ui.In_VswellR_lb.setText(In_VswellR)
        self.ui.In_VswellY_lb.setText(In_VswellY)
        self.ui.In_VswellB_lb.setText(In_VswellB)
        self.ui.In_VsagR_lb.setText(In_VsagR)
        self.ui.In_VsagY_lb.setText(In_VsagY)
        self.ui.In_VsagB_lb.setText(In_VsagB)
        self.ui.In_idlehours_lb.setText(In_idlehrs)

        self.ui.BI_kwh_lb.setText(BI_kwh)
        self.ui.BI_idlehours_lb.setText('\n'.join(BI_idlehrs))
        self.ui.BI_highkwh_lb.setText(f"{BI_kwhMax}<br>{BI_kwhMin}")
    def update_incomer_chords(self):
        from_date = self.ui.From_date_Insights.date().toPyDate()
        to_date = self.ui.To_date_Insights.date().toPyDate()
        from_ts1 = pd.Timestamp(from_date)
        to_ts1 = pd.Timestamp(to_date)

        In_kwh=self.In_kwh(from_ts1, to_ts1)
        In_freq=self.In_frequency(from_ts1,to_ts1)
        In_pf=self.In_powerfactor(from_ts1,to_ts1)
        In_VswellR,In_VswellY,In_VswellB,In_VsagR,In_VsagY,In_VsagB=self.In_Vswell_Vsag(from_ts1,to_ts1)
        In_idlehrs=self.In_idlehours(from_ts1,to_ts1)

        self.ui.In_kwh_lb.setText(In_kwh)
        self.ui.In_freq_lb.setText(In_freq)
        self.ui.In_pf_lb.setText(In_pf)
        self.ui.In_VswellR_lb.setText(In_VswellR)
        self.ui.In_VswellY_lb.setText(In_VswellY)
        self.ui.In_VswellB_lb.setText(In_VswellB)
        self.ui.In_VsagR_lb.setText(In_VsagR)
        self.ui.In_VsagY_lb.setText(In_VsagY)
        self.ui.In_VsagB_lb.setText(In_VsagB)
        self.ui.In_idlehours_lb.setText(In_idlehrs)
    def update_building_chords(self):
        from_date = self.ui.From_date_Insights.date().toPyDate()
        to_date = self.ui.To_date_Insights.date().toPyDate()
        from_ts1 = pd.Timestamp(from_date)
        to_ts1 = pd.Timestamp(to_date)

        BI_kwh=self.BI_kwh(from_ts1,to_ts1)
        BI_idlehrs=self.BI_idlehours(from_ts1, to_ts1)
        BI_kwhMax=self.BI_kwh_max(from_ts1,to_ts1)
        BI_kwhMin=self.BI_kwh_min(from_ts1,to_ts1)


        self.ui.BI_kwh_lb.setText(BI_kwh)
        self.ui.BI_idlehours_lb.setText('\n'.join(BI_idlehrs))
        self.ui.BI_highkwh_lb.setText(f"{BI_kwhMax}<br>{BI_kwhMin}")  

#Home Tab -- functions --    
    def home_piechart(self):
        m1 = home_df.groupby(['center','Time column 1']).sum()
        m1 = m1.reset_index()
        fig = px.pie(m1, values='kwh', names='center', title='CenterWise Energy Consumpution')
        # return fig

        plot1 = QWebEngineView()
        plot1.setHtml(fig.to_html(include_plotlyjs='cdn',full_html=True))

        frame_layout = self.ui.Home_Pie_frame.layout()
        if frame_layout is not None:
            for i in reversed(range(frame_layout.count())):
                frame_layout.itemAt(i).widget().setParent(None)
        else:
            frame_layout = QVBoxLayout(self.ui.Home_Pie_frame)
        frame_layout.addWidget(plot1)
    def home_meterchart(self):
        meter_counts = home_df.groupby('meter').sum().reset_index()
        fig = px.bar( meter_counts, y='kwh',x='meter', title='MeterWise Energy Consumpution')

        plot1 = QWebEngineView()
        plot1.setHtml(fig.to_html(include_plotlyjs='cdn',full_html=True))

        frame_layout = self.ui.Home_meter_frame.layout()
        if frame_layout is not None:
            for i in reversed(range(frame_layout.count())):
                frame_layout.itemAt(i).widget().setParent(None)
        else:
            frame_layout = QVBoxLayout(self.ui.Home_meter_frame)
        frame_layout.addWidget(plot1)
    def home_buildingchart(self):
        building_counts = home_df.groupby('building').sum().reset_index()
        fig = px.bar( building_counts, y='kwh',x='building', title='BuildingWise Energy Consumpution')
        plot1 = QWebEngineView()
        plot1.setHtml(fig.to_html(include_plotlyjs='cdn',full_html=True))

        frame_layout = self.ui.Home_Building_frame.layout()
        if frame_layout is not None:
            for i in reversed(range(frame_layout.count())):
                frame_layout.itemAt(i).widget().setParent(None)
        else:
            frame_layout = QVBoxLayout(self.ui.Home_Building_frame)
        frame_layout.addWidget(plot1)
    def home_pf_deviation(self):
        # pf_limits=0.85
        count=len(home_df[home_df['PF']<0.85])
        return f'Power Factor Deviation\nCount: {count}'
    def home_fre_deviation(self):
        count=len(home_df[home_df['F']<49])
        return f'Frequency Deviation\nCount: {count}'

#Analytics Tab -- V/I/PF/F functions --    
    def voltage(self, from_ts, to_ts, selected_meter, frame):
        dfir = df_ec02_ec03[(df_ec02_ec03['meter'] == selected_meter)]
        fig = go.Figure()
        mask2=(dfir['Time column 1']>=from_ts)&(dfir['Time column 1']<=to_ts)
        fig.add_trace(go.Scatter(x=dfir.loc[mask2,'Time column 1'],y=dfir.loc[mask2,'Vry'],name = 'Vry' ))
        fig.add_trace(go.Scatter(x=dfir.loc[mask2,'Time column 1'],y=dfir.loc[mask2,'Vyb'],name = 'Vyb' ))
        fig.add_trace(go.Scatter(x=dfir.loc[mask2,'Time column 1'],y=dfir.loc[mask2,'Vbr'],name = 'Vbr' ))
        fig.update_layout(title={'text':'Voltage','font': {'size': 20,'family': 'Arial','color': 'black'}}, yaxis_title='Voltage (V)',plot_bgcolor='white',paper_bgcolor='white')

        plot1 = QWebEngineView()
        plot1.setHtml(fig.to_html(include_plotlyjs='cdn',full_html=True))
        if frame is not None:
            frame_layout = frame.layout()
            if frame_layout is not None:
                for i in reversed(range(frame_layout.count())):
                    frame_layout.itemAt(i).widget().setParent(None)
            else:
                frame_layout = QVBoxLayout(frame)
            frame_layout.addWidget(plot1)
    def current(self,from_ts, to_ts, selected_meter,frame):
        # selected_meter = self.ui.comboBox_5.currentText()
        dfir = df_ec02_ec03[(df_ec02_ec03['meter'] == selected_meter)]
        fig = go.Figure()
        mask2=(dfir['Time column 1']>=from_ts)&(dfir['Time column 1']<=to_ts)
        fig.add_trace(go.Scatter(x=dfir.loc[mask2,'Time column 1'],y=dfir.loc[mask2,'Ir'],name = 'Ir' ))
        fig.add_trace(go.Scatter(x=dfir.loc[mask2,'Time column 1'],y=dfir.loc[mask2,'Iy'],name = 'Iy' ))
        fig.add_trace(go.Scatter(x=dfir.loc[mask2,'Time column 1'],y=dfir.loc[mask2,'Ib'],name = 'Ib' ))
        fig.update_layout(title={'text':'Current','font': {'size': 20,'family': 'Arial','color': 'black'}}, yaxis_title='Current (A)',plot_bgcolor='white',paper_bgcolor='white')
        # fig.show()

        plot1 = QWebEngineView()
        plot1.setHtml(fig.to_html(include_plotlyjs='cdn',full_html=True))
        if frame is not None:
            frame_layout = frame.layout()
            if frame_layout is not None:
                for i in reversed(range(frame_layout.count())):
                    frame_layout.itemAt(i).widget().setParent(None)
            else:
                frame_layout = QVBoxLayout(frame)
            frame_layout.addWidget(plot1)
    def powerfactor(self,from_ts, to_ts,selected_meter,frame):
        # selected_meter = self.ui.comboBox_5.currentText()
        dfir = df_ec02_ec03[(df_ec02_ec03['meter'] == selected_meter)]
        fig = go.Figure()
        mask2=(dfir['Time column 1']>=from_ts)&(dfir['Time column 1']<=to_ts)
        fig.add_trace(go.Scatter(x=dfir.loc[mask2,'Time column 1'],y=dfir.loc[mask2,'PF'],name = 'PF' ))
        fig.update_layout(title={'text':'Power Factor','font': {'size': 20,'family': 'Arial','color': 'black'}}, yaxis_title='Power Factor',plot_bgcolor='white',paper_bgcolor='white')

        plot1 = QWebEngineView()
        plot1.setHtml(fig.to_html(include_plotlyjs='cdn',full_html=True))
        # frame_layout = self.ui.frame_14.layout()
        if frame is not None:
            frame_layout = frame.layout()
            if frame_layout is not None:
                for i in reversed(range(frame_layout.count())):
                    frame_layout.itemAt(i).widget().setParent(None)
            else:
                frame_layout = QVBoxLayout(frame)
            frame_layout.addWidget(plot1)
    def frequency(self,from_ts, to_ts,selected_meter,frame):
        # selected_meter = self.ui.comboBox.currentText()
        dfir = df_ec02_ec03[(df_ec02_ec03['meter'] == selected_meter)]
        fig = go.Figure()
        mask2=(dfir['Time column 1']>=from_ts)&(dfir['Time column 1']<=to_ts)
        fig.add_trace(go.Scatter(x=dfir.loc[mask2,'Time column 1'],y=dfir.loc[mask2,'F'],name = 'F' ))
        fig.update_layout(title={'text':'Frequency','font': {'size': 20,'family': 'Arial','color': 'black'}}, yaxis_title='Frequency (Hz)',plot_bgcolor='white',paper_bgcolor='white')
        # fig.show()

        plot1 = QWebEngineView()
        plot1.setHtml(fig.to_html(include_plotlyjs='cdn',full_html=True))
        if frame is not None:
            frame_layout = frame.layout()
            if frame_layout is not None:
                for i in reversed(range(frame_layout.count())):
                    frame_layout.itemAt(i).widget().setParent(None)
            else:
                frame_layout = QVBoxLayout(frame)
            frame_layout.addWidget(plot1)

#Insights tab -- functions --

## Main Incomer
    #Total energy consumption of the Main Incomer- 11kv & 33kv
    def MI_kwh(self,from_ts, to_ts):
        main_incomer2 = df_ec02[df_ec02['meter']=='EC02 MFM 11KV TRAFO']
        main_incomer3 = df_ec03[df_ec03['meter']=='33KV Incomer']
        mask2 = (main_incomer2['Time column 1']>= from_ts) & (main_incomer2['Time column 1']<= to_ts)
        mask3 = (main_incomer3['Time column 1']>= from_ts) & (main_incomer3['Time column 1']<= to_ts)
        total2 = round(main_incomer2.loc[mask2, 'actual_kwh'].sum(),0)
        total3 = round(main_incomer3.loc[mask3, 'actual_kwh'].sum(),0)
        return f'11kV TRAFO: {total2} kWh',f'33kV TRAFO: {total3} kWh'
    #Power factor of 11kv & 33kv Main incomer
    def MI_powerfactor(self,from_ts,to_ts):
        main_incomer2 = df_ec02[(df_ec02['meter']=='EC02 MFM 11KV TRAFO')& (df_ec02['Vry']!=0)]
        main_incomer3 = df_ec03[(df_ec03['meter']=='33KV Incomer')&(df_ec03['Vry']!=0)]
        mask2 = (main_incomer2['Time column 1']>= from_ts) & (main_incomer2['Time column 1']<= to_ts)
        mask3 = (main_incomer3['Time column 1']>= from_ts) & (main_incomer3['Time column 1']<= to_ts)
        pf_limits = 0.85
        count = len(main_incomer2.loc[mask2 &(main_incomer2['PF']<0.85)])
        count1 = len(main_incomer3.loc[mask3 &(main_incomer3['PF']<0.85)])
        return f'11kV TRAFO: {count}',f'33kV TRAFO: {count1}'
    #Frequency of 11kv & 33Kv Main incomer
    def MI_frequency(self,from_ts,to_ts):
        main_incomer2 = df_ec02[(df_ec02['meter']=='EC02 MFM 11KV TRAFO')]
        main_incomer3 = df_ec03[(df_ec03['meter']=='33KV Incomer')]
        mask2 = (main_incomer2['Time column 1']>= from_ts) & (main_incomer2['Time column 1']<= to_ts)
        mask3 = (main_incomer3['Time column 1']>= from_ts) & (main_incomer3['Time column 1']<= to_ts)
        count = len(main_incomer2.loc[mask2 &(main_incomer2['F']<49)])
        count1 = len(main_incomer3.loc[mask3 &(main_incomer3['F']<49)])
        return f'11kV TRAFO: {count}',f'33kV TRAFO: {count1}'
    #Max energy consumtion  over 11kv & 33kv Main incomer
    def MI_high_kwh(self,from_ts, to_ts):
        main_incomer2 = df_ec02[df_ec02['meter']=='EC02 MFM 11KV TRAFO']
        main_incomer3 = df_ec03[df_ec03['meter']=='33KV Incomer']
        mask2 = (main_incomer2['Time column 1']>= from_ts) & (main_incomer2['Time column 1']<= to_ts)
        mask3 = (main_incomer3['Time column 1']>= from_ts) & (main_incomer3['Time column 1']<= to_ts)
        total2 = round(main_incomer2.loc[mask2, 'actual_kwh'].sum(),0)
        total3 = round(main_incomer3.loc[mask3, 'actual_kwh'].sum(),0)
        if total2 > total3:
            return f'11kV main incomer supplies more than 33kV main incomer'
        else:
            return f'33kV main incomer supplies more than 11kV main incomer'       
    #Idle hours of 11kv & 33kv Main incomer
    def MI_idlehours(self,from_ts,to_ts):
        main_incomer2 = df_ec02[(df_ec02['meter']=='EC02 MFM 11KV TRAFO')]
        main_incomer3 = df_ec03[(df_ec03['meter']=='33KV Incomer')]
        mask2 = (main_incomer2['Time column 1']>= from_ts) & (main_incomer2['Time column 1']<= to_ts)
        mask3 = (main_incomer3['Time column 1']>= from_ts) & (main_incomer3['Time column 1']<= to_ts)
        count = len(main_incomer2.loc[mask2 &(main_incomer2['Vry']==0) & (main_incomer2['Vbr']==0) & (main_incomer2['Vyb']==0) & (main_incomer2['Ir']==0) & (main_incomer2['Iy']==0) & (main_incomer2['Ib']==0)])
        count1 = len(main_incomer3.loc[mask3&(main_incomer3['Vry']==0) & (main_incomer3['Vbr']==0) & (main_incomer3['Vyb']==0) & (main_incomer3['Ir']==0) & (main_incomer3['Iy']==0) & (main_incomer3['Ib']==0)])
        hour_count = count/4
        hour_count1 =count1/4
        return f'11kV TRAFO is idle for {hour_count} hours',f'33kV TRAFO is idle for {hour_count1} hours'
    #Voltage swell and sag for 33kv Main incomer
    def MI_33kv_Vswell_Vsag(self,from_ts,to_ts):
        main_incomer3 = df_ec03[(df_ec03['meter']=='33KV Incomer')]
        voltage = main_incomer3[['rv','yv','bv','Time column 1']]
        voltage.set_index('Time column 1', inplace=True)
        voltage = voltage.resample('30S').ffill()
        mask2 = (voltage.index>= from_ts) & (voltage.index<= to_ts)
        voltage = voltage.loc[mask2]
        # Nominal voltage level
        nominal_voltage = 19.05 
        threshold = 0.1  # 10% change
        # Find the voltage change from nominal voltage for each phase
        voltage_change_rv = voltage["rv"] / nominal_voltage - 1
        voltage_change_yv = voltage["yv"] / nominal_voltage - 1
        voltage_change_bv = voltage["bv"] / nominal_voltage - 1
        # Find the time duration between consecutive measurements
        time_diff = voltage.index.to_series().diff().dt.total_seconds()
        # Identify the voltage swells and sags based on criteria for each phase
        is_swell_rv = (voltage_change_rv >= threshold) & (time_diff <= 60)
        is_sag_rv = (voltage_change_rv <= -threshold) & (time_diff <= 60)
        is_swell_yv = (voltage_change_yv >= threshold) & (time_diff <= 60)
        is_sag_yv = (voltage_change_yv <= -threshold) & (time_diff <= 60)
        is_swell_bv = (voltage_change_bv >= threshold) & (time_diff <= 60)
        is_sag_bv = (voltage_change_bv <= -threshold) & (time_diff <= 60)
        # Count the number of voltage swells and sags for each phase
        num_swells_rv = is_swell_rv.sum()
        num_sags_rv = is_sag_rv.sum()
        num_swells_yv = is_swell_yv.sum()
        num_sags_yv = is_sag_yv.sum()
        num_swells_bv = is_swell_bv.sum()
        num_sags_bv = is_sag_bv.sum()
        # result_str = f"RV: Swells={num_swells_rv}, Sags={num_sags_rv}; "\
        #     f"YV: Swells={num_swells_yv}, Sags={num_sags_yv}; "\
        #     f"BV: Swells={num_swells_bv}, Sags={num_sags_bv}"
        # return result_str
        # return f"- R-V swells: {num_swells_rv}\n- R-v sags: {num_sags_rv}\n- Y-V swells: {num_swells_yv}\n- Y-V sags: {num_sags_yv}\n- B-V swells: {num_swells_bv}\n- B-V sags: {num_sags_bv}"
        return f'{num_swells_rv}',f'{num_swells_yv}',f'{num_swells_bv}',f'{num_sags_rv}',f'{num_sags_yv}',f'{num_sags_bv}'
    #Voltage swell and sag for 11kv Main incomer
    def MI_11kv_Vswell_Vsag(self,from_ts,to_ts):
        main_incomer2 = df_ec02[(df_ec02['meter']=='EC02 MFM 11KV TRAFO')]
        voltage = main_incomer2[['rv','yv','bv','Time column 1']]
        voltage.set_index('Time column 1', inplace=True)
        voltage = voltage.resample('30S').ffill()
        mask2 = (voltage.index>= from_ts) & (voltage.index<= to_ts)
        voltage = voltage.loc[mask2]
        # Nominal voltage level
        nominal_voltage = 6.5 
        threshold = 0.1  # 10% change
        # Find the voltage change from nominal voltage for each phase
        voltage_change_rv = voltage["rv"] / nominal_voltage - 1
        voltage_change_yv = voltage["yv"] / nominal_voltage - 1
        voltage_change_bv = voltage["bv"] / nominal_voltage - 1
        # Find the time duration between consecutive measurements
        time_diff = voltage.index.to_series().diff().dt.total_seconds()
        # Identify the voltage swells and sags based on criteria for each phase
        is_swell_rv = (voltage_change_rv >= threshold) & (time_diff <= 60)
        is_sag_rv = (voltage_change_rv <= -threshold) & (time_diff <= 60)
        is_swell_yv = (voltage_change_yv >= threshold) & (time_diff <= 60)
        is_sag_yv = (voltage_change_yv <= -threshold) & (time_diff <= 60)
        is_swell_bv = (voltage_change_bv >= threshold) & (time_diff <= 60)
        is_sag_bv = (voltage_change_bv <= -threshold) & (time_diff <= 60)
        # Count the number of voltage swells and sags for each phase
        num_swells_rv = is_swell_rv.sum()
        num_sags_rv = is_sag_rv.sum()
        num_swells_yv = is_swell_yv.sum()
        num_sags_yv = is_sag_yv.sum()
        num_swells_bv = is_swell_bv.sum()
        num_sags_bv = is_sag_bv.sum()
        # result_str1 = f"RV: Swells={num_swells_rv}, Sags={num_sags_rv}; "\
        #     f"YV: Swells={num_swells_yv}, Sags={num_sags_yv}; "\
        #     f"BV: Swells={num_swells_bv}, Sags={num_sags_bv}"
        # return result_str1
        # return f"\u2022 R-V swells: {num_swells_rv}\n \u2022 R-V sags: {num_sags_rv}\n \u2022 T-V swells: {num_swells_yv}\n \u2022 Y-V sags: {num_sags_yv}\n \u2022 B-V swells: {num_swells_bv}\n \u2022 B-V sags: {num_sags_bv}"
        return f'{num_swells_rv}',f'{num_swells_yv}',f'{num_swells_bv}',f'{num_sags_rv}',f'{num_sags_yv}',f'{num_sags_bv}'
 
##Incomer
    #Total energy consumption of Incomers
    def In_kwh(self,from_ts, to_ts):
        selected_meter = self.ui.In_insights_cb.currentText()
        data = df_meters[df_meters['meter']==selected_meter]
        mask2 = (data['Time column 1']>= from_ts) & (data['Time column 1']<= to_ts)
        total = round(data.loc[mask2,'actual_kwh'].sum(),0)
        return f' {selected_meter}: {total} kWh'
    #Frequency
    def In_frequency(self,from_ts,to_ts):
        selected_meter = self.ui.In_insights_cb.currentText()
        data = df_meters[df_meters['meter']==selected_meter]
        mask2 = (data['Time column 1']>= from_ts) & (data['Time column 1']<= to_ts)
        count = len(data.loc[mask2 &(data['F']<49)])
        return f' {selected_meter}: {count}'
    #Power factor
    def In_powerfactor(self,from_ts,to_ts):
        selected_meter = self.ui.In_insights_cb.currentText()
        data = df_meters[df_meters['meter']==selected_meter]
        mask2 = (data['Time column 1']>= from_ts) & (data['Time column 1']<= to_ts)
        pf_limits = 0.85
        count = len(data.loc[mask2 &(data['PF']<0.85)])
        return f'{selected_meter}: {count}'
    #Voltage swell and sag
    def In_Vswell_Vsag(self,from_ts,to_ts):
        selected_meter = self.ui.In_insights_cb.currentText()
        main_incomer3 = df_meters[(df_meters['meter']==selected_meter)]
        voltage = main_incomer3[['rv','yv','bv','Time column 1']]
        voltage.set_index('Time column 1', inplace=True)
        voltage = voltage.resample('30S').ffill()
        mask2 = (voltage.index>= from_ts) & (voltage.index<= to_ts)
        voltage = voltage.loc[mask2]
        # Nominal voltage level
        if selected_meter =='11kv_415Vtrafo':
            nominal_voltage = 6.5
        else:
            nominal_voltage = 19.05 
        threshold = 0.1  # 10% change
        # Find the voltage change from nominal voltage for each phase
        voltage_change_rv = voltage["rv"] / nominal_voltage - 1
        voltage_change_yv = voltage["yv"] / nominal_voltage - 1
        voltage_change_bv = voltage["bv"] / nominal_voltage - 1
        # Find the time duration between consecutive measurements
        time_diff = voltage.index.to_series().diff().dt.total_seconds()
        # Identify the voltage swells and sags based on criteria for each phase
        is_swell_rv = (voltage_change_rv >= threshold) & (time_diff <= 60)
        is_sag_rv = (voltage_change_rv <= -threshold) & (time_diff <= 60)
        is_swell_yv = (voltage_change_yv >= threshold) & (time_diff <= 60)
        is_sag_yv = (voltage_change_yv <= -threshold) & (time_diff <= 60)
        is_swell_bv = (voltage_change_bv >= threshold) & (time_diff <= 60)
        is_sag_bv = (voltage_change_bv <= -threshold) & (time_diff <= 60)
        # Count the number of voltage swells and sags for each phase
        num_swells_rv = is_swell_rv.sum()
        num_sags_rv = is_sag_rv.sum()
        num_swells_yv = is_swell_yv.sum()
        num_sags_yv = is_sag_yv.sum()
        num_swells_bv = is_swell_bv.sum()
        num_sags_bv = is_sag_bv.sum()
        # return f"- R-V swells: {num_swells_rv}\n- R-v sags: {num_sags_rv}\n- Y-V swells: {num_swells_yv}\n- Y-V sags: {num_sags_yv}\n- B-V swells: {num_swells_bv}\n- B-V sags: {num_sags_bv}"
        return f'{num_swells_rv}',f'{num_swells_yv}',f'{num_swells_bv}',f'{num_sags_rv}',f'{num_sags_yv}',f'{num_sags_bv}'
    #Idle hours
    def In_idlehours(self,from_ts,to_ts):
        selected_meter = self.ui.In_insights_cb.currentText()
        data = df_meters[df_meters['meter']==selected_meter]
        mask2 = (data['Time column 1']>= from_ts) & (data['Time column 1']<= to_ts)
        count = len(data.loc[mask2 &(data['Vry']==0) & (data['Vbr']==0) & (data['Vyb']==0) & (data['Ir']==0) & (data['Iy']==0) & (data['Ib']==0)])
        hour_count =count/4
        return f'{selected_meter} is idle hours for {hour_count} hours'
    
##Building Wise
    #Total energy consumption of each building  
    def BI_kwh(self,from_ts,to_ts):
        selected_center = self.ui.BI_insights_cb.currentText()
        data = df_all_buildings[df_all_buildings['center']== selected_center]
        mask2 = (data['Time column 1']>= from_ts) & (data['Time column 1']<= to_ts)
        value = data.loc[mask2]
        value = value.groupby(['building']).sum()
        building_names = list(value.index)
        # Compare the summed values of all the rows
        for i in range(len(building_names)):
            for j in range(i+1, len(building_names)):
                if value.loc[building_names[i], 'actual_kwh'] > value.loc[building_names[j], 'actual_kwh']:
                    return (f"{building_names[i]} building consumed more energy")
                else:
                    return (f"{building_names[j]} building consumed more energy")
    #Idle hours - Top5 meters of each center
    def BI_idlehours(self,from_ts, to_ts):
        selected_center = self.ui.BI_insights_cb.currentText()
        d = df_all_buildings[df_all_buildings['center']== selected_center]
        idle_hours = []
        for meter in d['meter'].unique():
            data = d[d['meter']==meter]
            mask2 = (data['Time column 1']>= from_ts) & (data['Time column 1']<= to_ts)
            count = len(data.loc[mask2 &(data['Vry']==0) & (data['Vbr']==0) & (data['Vyb']==0) & (data['Ir']==0) & (data['Iy']==0) & (data['Ib']==0)])
            hour_count = count / 4
            idle_hours.append((meter, hour_count))
        top_5 = sorted(idle_hours, key=lambda x: x[1], reverse=True)[:5]
        res=[]
        for meter, hours in top_5:
            res.append(f"{meter} is idle for {hours} hours")
        return res
    #Determaining Max Energy consumption - Morning/Afternoon/Evening/Night
    def BI_kwh_max(self,from_ts,to_ts):
        selected_center = self.ui.BI_insights_cb.currentText()
        data = df_all_buildings[df_all_buildings['center']== selected_center]
        mask2 = (data['Time column 1']>= from_ts) & (data['Time column 1']<= to_ts)
        value = data.loc[mask2]
        value = value.groupby(['time_of_day']).sum()
        building_names = list(value.index)
        # Compare the summed values of all the rows
        for i in range(len(building_names)):
            for j in range(i+1, len(building_names)):
                if value.loc[building_names[i], 'actual_kwh'] > value.loc[building_names[j], 'actual_kwh']:
                    return (f"{building_names[i]} {selected_center} consumed more energy")
                else:
                    return (f"{building_names[j]}  {selected_center} consumed more energy")
    #Determaining Min Energy consumption - Morning/Afternoon/Evening/Night
    def BI_kwh_min(self,from_ts,to_ts):
        selected_center = self.ui.BI_insights_cb.currentText()
        data = df_all_buildings[df_all_buildings['center']== selected_center]
        mask2 = (data['Time column 1']>= from_ts) & (data['Time column 1']<= to_ts)
        value = data.loc[mask2]
        value = value.groupby(['time_of_day']).sum()
        building_names = list(value.index)
        # Compare the summed values of all the rows
        for i in range(len(building_names)):
            for j in range(i+1, len(building_names)):
                if value.loc[building_names[i], 'kwh'] < value.loc[building_names[j], 'kwh']:
                    return (f"{building_names[i]}  {selected_center} consumed less energy")
                else:
                    return (f"{building_names[j]} {selected_center} consumed less energy")
    
    

#main function
if __name__ == "__main__":
    app = QApplication(sys.argv)
    style_file = QFile("style.qss")
    style_file.open(QFile.ReadOnly | QFile.Text)
    style_stream = QTextStream(style_file)
    app.setStyleSheet(style_stream.readAll())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
