import sys
# import PySide2
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton,QVBoxLayout,QFrame,QWidget
from PyQt5.QtCore import pyqtSlot, QFile, QTextStream
import numpy as np
# import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.express as px
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtWidgets
import pandas as pd

# import the generated UI code
from GUI_1 import Ui_MainWindow
from Energy import total_energy_consumption,centerwise_piechart,weekly_graph
from Incomer import total_incomer_supply
from EC02 import ec02_energy_consumption,ec02_meter_piechart,ec02_fre_deviations,ec02_PF_deviations,ec02_Vswell_Vsag
from EC03 import ec03_energy_consumption,ec03_meter_piechart,ec03_fre_deviations,ec03_PF_deviations,ec03_Vswell_Vsag
df=pd.read_csv('C:\\Users\\20339181\\L&T Construction\\PT&D Digital Solutions - Incubation - Documents\\Incubation\\DSIDIB Team\\Sathwika\\PGL-Analytics-Insights-Final - Copy\\Dashboard Template\\new_ec02.csv')
# print("df loaded")
df1=pd.read_csv('C:\\Users\\20339181\\L&T Construction\\PT&D Digital Solutions - Incubation - Documents\\Incubation\\DSIDIB Team\\Sathwika\\PGL-Analytics-Insights-Final - Copy\\Dashboard Template\\new_ec03.csv')
# print("df1 loaded")
df2=pd.read_csv('C:\\Users\\20339181\\L&T Construction\\PT&D Digital Solutions - Incubation - Documents\\Incubation\\DSIDIB Team\\Sathwika\\PGL-Analytics-Insights-Final - Copy\\Dashboard Template\\ec02_ec03.csv')
# print("df2 Loaded")
df['Time column 1'] = df['Time column 1'].astype(str)
df['Time column 1'] = pd.to_datetime(df['Time column 1'],format = '%d.%m.%Y %H:%M:%S.%f')
df1['Time column 1'] = df1['Time column 1'].astype(str)
df1['Time column 1'] = pd.to_datetime(df1['Time column 1'],format = '%d.%m.%Y %H:%M:%S.%f')
df2['Time column 1'] = df2['Time column 1'].astype(str)
df2['Time column 1'] = pd.to_datetime(df2['Time column 1'],format = '%d.%m.%Y %H:%M:%S.%f')
print("timestamp changed")
building2 = df[df['building'].isin(['TC-1','TC&MEDICAL'])]
building3 = df1[df1['building'].isin(['TC3-TOWER A', 'TC3-TOWER B', 'TC3 HVAC'])]
df3 = df2[(df2["building"] == 'TC-1') | (df2["building"] == 'TC&MEDICAL') | (df2["building"] == 'TC3-TOWER A') | (df2["building"] == 'TC3-TOWER B') | (df2["building"] == 'TC3 HVAC')]
print("df3 Loaded")
df4=df2[(df2["meter"] == '11kv_415Vtrafo') | (df2["meter"] == '33kV trafo-1') | (df2["meter"] == '33kV trafo-2') | (df2["meter"] == '33kV trafo-3') |
        (df2["meter"] == '33kV trafo-4') | (df2["meter"] == '33kV trafo-5') | (df2["meter"] == 'EC02 MFM 11KV TRAFO') | (df2["meter"] == '33KV Incomer')]
print("df4 Loaded")

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.icon_only_widget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.stackedWidget_3.setCurrentIndex(0)
        self.ui.home_btn_2.setChecked(True)
        self.ui.energy_btn_3.setChecked(True)

        from_date = self.ui.dateEdit.date().toPyDate()
        to_date = self.ui.dateEdit_6.date().toPyDate()
        from_ts = pd.Timestamp(from_date)
        to_ts = pd.Timestamp(to_date)

        from_date1 = self.ui.dateEdit_3.date().toPyDate()
        to_date1 = self.ui.dateEdit_4.date().toPyDate()
        from_ts1 = pd.Timestamp(from_date1)
        to_ts1 = pd.Timestamp(to_date1)

        ec02_meter_values = building2["meter"].unique().tolist()
        self.ui.ec02_meter_cb.addItems(ec02_meter_values)

        ec03_meter_values = building3["meter"].unique().tolist()
        self.ui.ec03_meter_cb.addItems(ec03_meter_values)

        ec02_building_names = building2["building"].unique().tolist()
        self.ui.ec02_building_cb.addItems(ec02_building_names)
        self.ui.ec02_building_cb.currentIndexChanged.connect(self.update_ec02_meter_combobox)

        ec03_building_names = building3["building"].unique().tolist()
        self.ui.ec03_building_cb.addItems(ec03_building_names)
        self.ui.ec03_building_cb.currentIndexChanged.connect(self.update_ec03_meter_combobox)

        Incomer_names = df4["meter"].unique()
        self.ui.incomer_cb.addItems(Incomer_names)
        
        Incomer_names = df4["meter"].unique()
        self.ui.In_insights_cb.addItems(Incomer_names)
        self.ui.In_insights_cb.currentIndexChanged.connect(self.update_incomer_chords)

        center_names = df3["center"].unique()
        self.ui.BI_insights_cb.addItems(center_names)
        self.ui.BI_insights_cb.currentIndexChanged.connect(self.update_building_chords)

        self.ui.incomer_cb.currentTextChanged.connect(self.change_voltage_graphs)
        self.ui.ec02_meter_cb.currentTextChanged.connect(self.change_voltage_graphs)
        self.ui.ec03_meter_cb.currentTextChanged.connect(self.change_voltage_graphs)

        self.ui.incomer_cb.currentTextChanged.connect(self.change_current_graphs)
        self.ui.ec02_meter_cb.currentTextChanged.connect(self.change_current_graphs)
        self.ui.ec03_meter_cb.currentTextChanged.connect(self.change_current_graphs)

        self.ui.incomer_cb.currentTextChanged.connect(self.change_pf_graphs)
        self.ui.ec02_meter_cb.currentTextChanged.connect(self.change_pf_graphs)
        self.ui.ec03_meter_cb.currentTextChanged.connect(self.change_pf_graphs)

        self.ui.incomer_cb.currentTextChanged.connect(self.change_fre_graphs)
        self.ui.ec02_meter_cb.currentTextChanged.connect(self.change_fre_graphs)
        self.ui.ec03_meter_cb.currentTextChanged.connect(self.change_fre_graphs)


        total_energy_consumption(self,from_ts, to_ts)
        weekly_graph(self,from_ts, to_ts)
        centerwise_piechart(self,from_ts, to_ts)

        total_incomer_supply(self,from_ts, to_ts)

        ec02_energy_consumption(self,from_ts, to_ts)
        ec02_meter_piechart(self,from_ts, to_ts)
        ec02_fre_deviations(self,from_ts,to_ts)
        ec02_PF_deviations(self,from_ts,to_ts)
        ec02_Vswell_Vsag(self,from_ts,to_ts)

        # self.voltage(from_ts, to_ts)
        # self.current(from_ts, to_ts)
        # self.powerfactor(from_ts, to_ts)
        # self.frequeny(from_ts, to_ts)
        
        ec03_energy_consumption(self,from_ts, to_ts)
        ec03_meter_piechart(self,from_ts,to_ts)
        ec03_fre_deviations(self,from_ts,to_ts)
        ec03_PF_deviations(self,from_ts,to_ts)
        ec03_Vswell_Vsag(self,from_ts,to_ts)
        print("Default plotting done")

        # self.change_voltage_graphs(self.ui.incomer_cb.currentText())
        # self.change_voltage_graphs(self.ui.ec02_meter_cb.currentText())
        # self.change_voltage_graphs(self.ui.ec03_meter_cb.currentText())

        # self.change_current_graphs(self.ui.incomer_cb.currentText())
        # self.change_current_graphs(self.ui.ec02_meter_cb.currentText())
        # self.change_current_graphs(self.ui.ec03_meter_cb.currentText())

        # self.change_pf_graphs(self.ui.incomer_cb.currentText())
        # self.change_pf_graphs(self.ui.ec02_meter_cb.currentText())
        # self.change_pf_graphs(self.ui.ec03_meter_cb.currentText())

        # self.change_fre_graphs(self.ui.incomer_cb.currentText())
        # self.change_fre_graphs(self.ui.ec02_meter_cb.currentText())
        # self.change_fre_graphs(self.ui.ec03_meter_cb.currentText())

        # Connect the single slot function to both dateChanged signals
        self.ui.dateEdit.dateChanged.connect(self.call_graphs)
        self.ui.dateEdit_6.dateChanged.connect(self.call_graphs)

        r1,r2 = self.MI_kwh(from_ts1, to_ts1)
        r3,r4= self.MI_frequency(from_ts1,to_ts1)
        r5,r6=self.MI_powerfactor(from_ts1,to_ts1)
        r21=self.MI_high_kwh(from_ts1,to_ts1)
        r7,r8,r9,r10,r11,r12=self.MI_33kv_Vswell_Vsag(from_ts1,to_ts1)
        r13,r14,r15,r16,r17,r18=self.MI_11kv_Vswell_Vsag(from_ts1,to_ts1)
        r19,r20=self.MI_idlehours(from_ts1,to_ts1)
        
        r22=self.In_kwh(from_ts1, to_ts1)
        r23=self.In_frequency(from_ts1,to_ts1)
        r24=self.In_powerfactor(from_ts1,to_ts1)
        r25,r26,r27,r28,r29,r30=self.In_Vswell_Vsag(from_ts1,to_ts1)
        r31=self.In_idlehours(from_ts1,to_ts1)

        r32=self.BI_kwh(from_ts1,to_ts1)
        r33=self.BI_idlehours(from_ts1, to_ts1)
        r34=self.BI_kwh_max(from_ts1,to_ts1)
        r35=self.BI_kwh_min(from_ts1,to_ts1)

        self.ui.MI_kwh_lb.setText(f"{r1}<br>{r2}")
        self.ui.MI_feq_lb.setText(f"{r3}<br>{r4}")
        self.ui.MI_pf_lb.setText(f"{r5}<br>{r6}")
        self.ui.MI_33VSwellR_lb.setText(r7)
        self.ui.MI_33VSwellY_lb.setText(r8)
        self.ui.MI_33VSwellB_lb.setText(r9)
        self.ui.MI_33VSagR_lb.setText(r10)
        self.ui.MI_33VSagY_lb.setText(r11)
        self.ui.MI_33VSagB_lb.setText(r12)
        self.ui.MI_11VSwellR_lb.setText(r13)
        self.ui.MI_11VSwellY_lb.setText(r14)
        self.ui.MI_11VSwellB_lb.setText(r15)
        self.ui.MI_11VSagR_lb.setText(r16)
        self.ui.MI_11VSagY_lb.setText(r17)
        self.ui.MI_11VSagB_lb.setText(r18)
        self.ui.MI_idlehours_lb.setText(f"{r19}<br>{r20}")
        self.ui.MI_highkwh_lb.setText(r21)
        self.ui.In_kwh_lb.setText(r22)
        self.ui.In_freq_lb.setText(r23)
        self.ui.In_pf_lb.setText(r24)

        self.ui.In_VswellR_lb.setText(r25)
        self.ui.In_VswellY_lb.setText(r26)
        self.ui.In_VswellB_lb.setText(r27)
        self.ui.In_VsagR_lb.setText(r28)
        self.ui.In_VsagY_lb.setText(r29)
        self.ui.In_VsagB_lb.setText(r30)
        self.ui.In_idlehours_lb.setText(r31)

        self.ui.BI_kwh_lb.setText(r32)
        self.ui.BI_idlehours_lb.setText('\n'.join(r33))
        self.ui.BI_highkwh_lb.setText(f"{r34}<br>{r35}")

        self.ui.dateEdit_3.dateChanged.connect(self.update_all_chords)
        self.ui.dateEdit_4.dateChanged.connect(self.update_all_chords)
      

    def call_graphs(self,selected_meter):
        self.update_all_graphs()
        self.change_voltage_graphs(selected_meter)
        self.change_current_graphs(selected_meter)
        self.change_pf_graphs(selected_meter)
        self.change_fre_graphs(selected_meter)
    def update_all_graphs(self):
        # Get the updated values of from_date and to_date from the dateEdit widgets
        from_date = self.ui.dateEdit.date().toPyDate()
        to_date = self.ui.dateEdit_6.date().toPyDate()
        from_ts = pd.Timestamp(from_date)
        to_ts = pd.Timestamp(to_date)
        #energy centers graphs
        total_energy_consumption(self,from_ts, to_ts)
        centerwise_piechart(self,from_ts, to_ts)
        weekly_graph(self,from_ts, to_ts)
        #Incomers Graphs
        total_incomer_supply(self,from_ts, to_ts)
        #EC02 graphs
        ec02_energy_consumption(self,from_ts, to_ts)
        ec02_meter_piechart(self,from_ts, to_ts)
        ec02_fre_deviations(self,from_ts,to_ts)
        ec02_PF_deviations(self,from_ts,to_ts)
        ec02_Vswell_Vsag(self,from_ts,to_ts)
        #EC03 graphs
        ec03_energy_consumption(self,from_ts, to_ts)
        ec03_meter_piechart(self,from_ts,to_ts)
        ec03_fre_deviations(self,from_ts,to_ts)
        ec03_PF_deviations(self,from_ts,to_ts)    
        ec03_Vswell_Vsag(self,from_ts,to_ts)   
    def change_voltage_graphs(self, selected_meter):
        from_date = self.ui.dateEdit.date().toPyDate()
        to_date = self.ui.dateEdit_6.date().toPyDate()
        from_ts = pd.Timestamp(from_date)
        to_ts = pd.Timestamp(to_date)
        sender = self.sender()
        if sender == self.ui.incomer_cb:
            frame = self.ui.frame_5
            print("frame5")
        elif sender == self.ui.ec02_meter_cb:
            frame = self.ui.frame_12
            print("frame12")
        elif sender == self.ui.ec03_meter_cb:
            frame = self.ui.frame_16
            print("frame16")
        else:
            frame = None
        self.voltage(from_ts, to_ts, selected_meter,frame)
    def change_current_graphs(self, selected_meter):
        from_date = self.ui.dateEdit.date().toPyDate()
        to_date = self.ui.dateEdit_6.date().toPyDate()
        from_ts = pd.Timestamp(from_date)
        to_ts = pd.Timestamp(to_date)
        sender = self.sender()
        if sender == self.ui.incomer_cb:
            frame = self.ui.frame_6
            print("frame6")
        elif sender == self.ui.ec02_meter_cb:
            frame = self.ui.frame_13
            print("frame13")
        elif sender == self.ui.ec03_meter_cb:
            frame = self.ui.frame_17
            print("frame17")
        else:
            frame = None
        self.current(from_ts, to_ts, selected_meter,frame)
    def change_pf_graphs(self, selected_meter):
        from_date = self.ui.dateEdit.date().toPyDate()
        to_date = self.ui.dateEdit_6.date().toPyDate()
        from_ts = pd.Timestamp(from_date)
        to_ts = pd.Timestamp(to_date)
        sender = self.sender()
        if sender == self.ui.incomer_cb:
            frame = self.ui.frame_7
            print("frame6")
        elif sender == self.ui.ec02_meter_cb:
            frame = self.ui.frame_14
            print("frame13")
        elif sender == self.ui.ec03_meter_cb:
            frame = self.ui.frame_18
            print("frame17")
        else:
            frame = None
        self.powerfactor(from_ts, to_ts, selected_meter,frame)
    def change_fre_graphs(self, selected_meter):
        from_date = self.ui.dateEdit.date().toPyDate()
        to_date = self.ui.dateEdit_6.date().toPyDate()
        from_ts = pd.Timestamp(from_date)
        to_ts = pd.Timestamp(to_date)
        sender = self.sender()
        if sender == self.ui.incomer_cb:
            frame = self.ui.frame_8
            print("frame6")
        elif sender == self.ui.ec02_meter_cb:
            frame = self.ui.frame_19
            print("frame13")
        elif sender == self.ui.ec03_meter_cb:
            frame = self.ui.frame_23
            print("frame17")
        else:
            frame = None
        self.frequency(from_ts, to_ts, selected_meter,frame)

    def update_ec02_meter_combobox(self):
        selected_building = self.ui.ec02_building_cb.currentText()
        building_df = building2[building2["building"] == selected_building]
        meter_names = building_df["meter"].unique().tolist()
        self.ui.ec02_meter_cb.clear()
        self.ui.ec02_meter_cb.addItems(meter_names)
    def update_ec03_meter_combobox(self):
        selected_building = self.ui.ec03_building_cb.currentText()
        building_df = building3[building3["building"] == selected_building]
        meter_names = building_df["meter"].unique().tolist()
        self.ui.ec03_meter_cb.clear()
        self.ui.ec03_meter_cb.addItems(meter_names)
    
    def update_all_chords(self):
        from_date = self.ui.dateEdit_3.date().toPyDate()
        to_date = self.ui.dateEdit_4.date().toPyDate()
        from_ts = pd.Timestamp(from_date)
        to_ts = pd.Timestamp(to_date)

        r1,r2 = self.MI_kwh(from_ts, to_ts)
        r3,r4= self.MI_frequency(from_ts,to_ts)
        r5,r6=self.MI_powerfactor(from_ts,to_ts)
        r21=self.MI_high_kwh(from_ts,to_ts)
        r7,r8,r9,r10,r11,r12=self.MI_33kv_Vswell_Vsag(from_ts,to_ts)
        r13,r14,r15,r16,r17,r18=self.MI_11kv_Vswell_Vsag(from_ts,to_ts)
        r19,r20=self.MI_idlehours(from_ts,to_ts)
       
        r22=self.In_kwh(from_ts, to_ts)
        r23=self.In_frequency(from_ts,to_ts)
        r24=self.In_powerfactor(from_ts,to_ts)
        r25,r26,r27,r28,r29,r30=self.In_Vswell_Vsag(from_ts,to_ts)
        r31=self.In_idlehours(from_ts,to_ts)

        r32=self.BI_kwh(from_ts,to_ts)
        r33=self.BI_idlehours(from_ts, to_ts)
        r34=self.BI_kwh_max(from_ts,to_ts)
        r35=self.BI_kwh_min(from_ts,to_ts)

        self.ui.MI_kwh_lb.setText(f"{r1}<br>{r2}")
        self.ui.MI_feq_lb.setText(f"{r3}<br>{r4}")
        self.ui.MI_pf_lb.setText(f"{r5}<br>{r6}")
        self.ui.MI_33VSwellR_lb.setText(r7)
        self.ui.MI_33VSwellY_lb.setText(r8)
        self.ui.MI_33VSwellB_lb.setText(r9)
        self.ui.MI_33VSagR_lb.setText(r10)
        self.ui.MI_33VSagY_lb.setText(r11)
        self.ui.MI_33VSagB_lb.setText(r12)
        self.ui.MI_11VSwellR_lb.setText(r13)
        self.ui.MI_11VSwellY_lb.setText(r14)
        self.ui.MI_11VSwellB_lb.setText(r15)
        self.ui.MI_11VSagR_lb.setText(r16)
        self.ui.MI_11VSagY_lb.setText(r17)
        self.ui.MI_11VSagB_lb.setText(r18)
        self.ui.MI_idlehours_lb.setText(f"{r19}<br>{r20}")
        self.ui.MI_highkwh_lb.setText(r21)
        self.ui.In_kwh_lb.setText(r22)
        self.ui.In_freq_lb.setText(r23)
        self.ui.In_pf_lb.setText(r24)

        self.ui.In_VswellR_lb.setText(r25)
        self.ui.In_VswellY_lb.setText(r26)
        self.ui.In_VswellB_lb.setText(r27)
        self.ui.In_VsagR_lb.setText(r28)
        self.ui.In_VsagY_lb.setText(r29)
        self.ui.In_VsagB_lb.setText(r30)

        self.ui.In_idlehours_lb.setText(r31)
        self.ui.BI_kwh_lb.setText(r32)
        self.ui.BI_idlehours_lb.setText('\n'.join(r33))
        self.ui.BI_highkwh_lb.setText(f"{r34}<br>{r35}")

    def update_incomer_chords(self):
        from_date = self.ui.dateEdit_3.date().toPyDate()
        to_date = self.ui.dateEdit_4.date().toPyDate()
        from_ts = pd.Timestamp(from_date)
        to_ts = pd.Timestamp(to_date)

        r22=self.In_kwh(from_ts, to_ts)
        r23=self.In_frequency(from_ts,to_ts)
        r24=self.In_powerfactor(from_ts,to_ts)
        r25,r26,r27,r28,r29,r30=self.In_Vswell_Vsag(from_ts,to_ts)
        r31=self.In_idlehours(from_ts,to_ts)

        self.ui.In_kwh_lb.setText(r22)
        self.ui.In_freq_lb.setText(r23)
        self.ui.In_pf_lb.setText(r24)
        self.ui.In_VswellR_lb.setText(r25)
        self.ui.In_VswellY_lb.setText(r26)
        self.ui.In_VswellB_lb.setText(r27)
        self.ui.In_VsagR_lb.setText(r28)
        self.ui.In_VsagY_lb.setText(r29)
        self.ui.In_VsagB_lb.setText(r30)
        self.ui.In_idlehours_lb.setText(r31)

    def update_building_chords(self):
        from_date = self.ui.dateEdit_3.date().toPyDate()
        to_date = self.ui.dateEdit_4.date().toPyDate()
        from_ts = pd.Timestamp(from_date)
        to_ts = pd.Timestamp(to_date)

        r32=self.BI_kwh(from_ts,to_ts)
        r33=self.BI_idlehours(from_ts, to_ts)
        r34=self.BI_kwh_max(from_ts,to_ts)
        r35=self.BI_kwh_min(from_ts,to_ts)

        self.ui.BI_kwh_lb.setText(r32)
        self.ui.BI_idlehours_lb.setText('\n'.join(r33))
        self.ui.BI_highkwh_lb.setText(f"{r34}<br>{r35}")
    
    def on_home_btn_1_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    def on_analytics_btn_1_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    def on_insights_btn_1_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(1)
    def on_prediction_btn_1_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def on_home_btn_2_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    def on_analytics_btn_2_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    def on_insights_btn_2_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(1)
    def on_prediction_btn_2_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(3)
       
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

    # def total_energy_consumption(self,from_ts, to_ts):
    #     gdf = df[['Time column 1','actual_kwh']]
    #     grouped_df = gdf.groupby('Time column 1').sum()
    #     gdf1 = df1[['Time column 1','actual_kwh']]
    #     grouped_df1 = gdf1.groupby('Time column 1').sum()
    #     grouped_df = grouped_df.reset_index()
    #     grouped_df1 = grouped_df1.reset_index()
    #     grouped_df['cum']=grouped_df['actual_kwh'].cumsum(axis = 0)
    #     grouped_df1['cum']=grouped_df1['actual_kwh'].cumsum(axis = 0)
    #     fig = go.Figure()
    #     mask2 = (grouped_df['Time column 1']>= from_ts) & (grouped_df['Time column 1']<= to_ts)
    #     mask3 = (grouped_df1['Time column 1']>= from_ts) & (grouped_df1['Time column 1']<= to_ts)
    #     fig.add_trace(go.Scatter(x=grouped_df.loc[mask2, 'Time column 1'], y=grouped_df.loc[mask2, 'cum'], name='EC02'))
    #     fig.add_trace(go.Scatter(x=grouped_df1.loc[mask3, 'Time column 1'], y=grouped_df1.loc[mask3, 'cum'], name='EC03'))
    #     fig.update_layout(title={'text': 'Energy Consumption','font': {'size': 20,'family': 'Arial','color': 'black'}}, yaxis_title='kWh',plot_bgcolor='white',paper_bgcolor='white')
    #     # x=fig.show()
    #     # return x
    #     plot1 = QWebEngineView()
    #     plot1.setHtml(fig.to_html(include_plotlyjs='cdn',full_html=True))
    #     frame_layout = self.ui.fram.layout()
    #     if frame_layout is not None:
    #         for i in reversed(range(frame_layout.count())):
    #             frame_layout.itemAt(i).widget().setParent(None)
    #     else:
    #         frame_layout = QVBoxLayout(self.ui.fram)
    #     frame_layout.addWidget(plot1) 
    #     print("no prblm")
    # def centerwise_piechart(self,from_ts, to_ts):
    #     m1 = df2.groupby(['center','Time column 1']).sum()
    #     m1 = m1.reset_index()
    #     mask = (m1['Time column 1']>= from_ts) & (m1['Time column 1']<= to_ts)
    #     m1=m1.loc[mask]
    #     fig = px.pie(m1, values='kwh', names='center',title= 'Energy Consumption')
    #     # fig = go.Figure(data=data)
    #     plot1 = QWebEngineView()
    #     plot1.setHtml(fig.to_html(include_plotlyjs='cdn',full_html=True))

    #     frame_layout = self.ui.frame_3.layout()
    #     if frame_layout is not None:
    #         for i in reversed(range(frame_layout.count())):
    #             frame_layout.itemAt(i).widget().setParent(None)
    #     else:
    #         frame_layout = QVBoxLayout(self.ui.frame_3)
    #     frame_layout.addWidget(plot1)
    # def weekly_graph(self,from_ts, to_ts):
    #     mask = (df2['Time column 1']>= to_ts-pd.Timedelta('7 days')) & (df2['Time column 1']<= to_ts)
    #     m=df2.loc[mask]
    #     m1 = m.pivot_table(index='days_of_week', columns=['time_of_day'], values=['kwh'], aggfunc='count')
    #     m1 = m1.melt(ignore_index=False)
    #     m1.reset_index(inplace=True)
    #     fig = px.bar(data_frame=m1,
    #     x="days_of_week",
    #     y="value",
    #     color='time_of_day',
    #     category_orders={'time_of_day':['morning', 'afternoon', 'evening', 'night']},
    #     orientation='v',
    #     barmode='relative',
    #     opacity=0.8,
    #     # plot_bgcolor='white',
    #     # paper_bgcolor='white',
    #     color_discrete_map={'morning':'#ffff00','afternoon':'#f26517','evening':'#69b2f4','night':'#b2b2b2'})
    #     # fig.update_layout(title={'text': 'Energy Consumption','font': {'size': 20,'family': 'Arial','color': 'black'}}, yaxis_title='kWh',plot_bgcolor='white',paper_bgcolor='white')
    #     plot1 = QWebEngineView()
    #     plot1.setHtml(fig.to_html(include_plotlyjs='cdn',full_html=True))

    #     frame_layout = self.ui.frame_2.layout()
    #     if frame_layout is not None:
    #         for i in reversed(range(frame_layout.count())):
    #             frame_layout.itemAt(i).widget().setParent(None)
    #     else:
    #         frame_layout = QVBoxLayout(self.ui.frame_2)
    #     frame_layout.addWidget(plot1)
    
    # def total_incomer_supply(self,from_ts, to_ts):
    #     color=["red","blue","lightgreen","#f0920e","#f71302","#f00e8e","#f0f00e","#0ef083","#0e83f0"]
    #     i=0
    #     M = ['INCOMER-EC03','Trafo-1','Trafo-2','Trafo-3','Trafo-4','Trafo-5','trafo-1','INCOMER']
    #     data=[]
    #     title="INCOMERS For entrie Centers"
    #     grouped1 = df2.groupby(['building','Time column 1']).sum()
    #     grouped1 = grouped1.reset_index()
    #     mask = (grouped1['Time column 1']>= from_ts) & (grouped1['Time column 1']<= to_ts)
    #     for b in grouped1.building.unique():
    #         if b in M:
    #             x=[]
    #             y=[]
    #             x=grouped1.loc[(grouped1["building"]==b)& mask,"Time column 1"]
    #             y=grouped1.loc[(grouped1["building"]==b)& mask,"kwh"]
    #             trace=go.Scatter(x=x,y=y,mode='lines',line=dict(color=color[i],width=2),name=str(b))
    #             data.append(trace)
    #             i+=1
    #     fig = go.Figure(data=data)
    #     fig.update_layout(title={'text': 'Incomers','font': {'size': 20,'family': 'Arial','color': 'black'}}, yaxis_title='kWh',plot_bgcolor='white',paper_bgcolor='white')
    #     plot1 = QWebEngineView()
    #     plot1.setHtml(fig.to_html(include_plotlyjs='cdn',full_html=True))
    #     frame_layout = self.ui.frame_4.layout()
    #     if frame_layout is not None:
    #         for i in reversed(range(frame_layout.count())):
    #             frame_layout.itemAt(i).widget().setParent(None)
    #     else:
    #         frame_layout = QVBoxLayout(self.ui.frame_4)
    #     frame_layout.addWidget(plot1)  
    
    # def ec02_energy_consumption(self,from_ts, to_ts):
    #     data=[]
    #     title="EC02 For each Building"
    #     grouped = df.groupby(['building','Time column 1']).sum()
    #     grouped['cum'] = grouped['actual_kwh'].cumsum(axis = 0)
    #     grouped = grouped.reset_index()
    #     mask2 = (grouped['Time column 1']>= from_ts) & (grouped['Time column 1']<= to_ts)
    #     for b in grouped.building.unique():
    #         if (b!='INCOMER') and (b !='trafo-1'):
    #             x=[]
    #             y=[]
    #             x=grouped.loc[(grouped["building"]==b)& mask2,"Time column 1"]
    #             y=grouped.loc[(grouped["building"]==b)& mask2,"cum"]
    #             trace=go.Scatter(x=x,y=y,mode='lines',line=dict(width=2),name=str(b))
    #             data.append(trace)
    #     fig=go.Figure(data=data)
    #     fig.update_layout(title={'text':'EC02 Energy Consumption','font': {'size': 20,'family': 'Arial','color': 'black'}}, yaxis_title='kWh',plot_bgcolor='white',paper_bgcolor='white')

    #     plot1 = QWebEngineView()
    #     plot1.setHtml(fig.to_html(include_plotlyjs='cdn',full_html=True))
    #     frame_layout = self.ui.frame_9.layout()
    #     if frame_layout is not None:
    #         for i in reversed(range(frame_layout.count())):
    #             frame_layout.itemAt(i).widget().setParent(None)
    #     else:
    #         frame_layout = QVBoxLayout(self.ui.frame_9)
    #     frame_layout.addWidget(plot1)
    # def ec02_meter_piechart(self,from_ts,to_ts):
    #     b=self.ui.ec02_building_cb.currentText()
    #     b2 = building2[building2['building']==b]
    #     mask = (b2['Time column 1']>= from_ts) & (b2['Time column 1']<= to_ts)
    #     b2= b2.loc[mask]
    #     meter_counts = b2.groupby('meter').sum().reset_index()
    #     fig = px.pie( meter_counts, values='kwh', names='meter', title='Total Energy Consumpution')
    #     plot1 = QWebEngineView()
    #     plot1.setHtml(fig.to_html(include_plotlyjs='cdn',full_html=True))

    #     frame_layout = self.ui.frame_11.layout()
    #     if frame_layout is not None:
    #         for i in reversed(range(frame_layout.count())):
    #             frame_layout.itemAt(i).widget().setParent(None)
    #     else:
    #         frame_layout = QVBoxLayout(self.ui.frame_11)
    #     frame_layout.addWidget(plot1)
    # def ec02_fre_deviations(self,from_ts,to_ts):
    #     meter=self.ui.ec02_meter_cb.currentText()
    #     data = building2[building2['meter']==meter]
    #     mask2 = (data['Time column 1']>= from_ts) & (data['Time column 1']<= to_ts)
    #     count = len(data.loc[mask2 &(data['F']<49)])
    #     fig = px.bar(x=[count], y=[meter], title=f"Frequency Deviation Count")
    #     fig.update_traces(width=0.2) # set the width of the bars
    #     plot1 = QWebEngineView()
    #     plot1.setHtml(fig.to_html(include_plotlyjs='cdn',full_html=True))

    #     frame_layout = self.ui.frame_21.layout()
    #     if frame_layout is not None:
    #         for i in reversed(range(frame_layout.count())):
    #             frame_layout.itemAt(i).widget().setParent(None)
    #     else:
    #         frame_layout = QVBoxLayout(self.ui.frame_21)
    #     frame_layout.addWidget(plot1)
    # def ec02_PF_deviations(self,from_ts,to_ts):
    #     meter=self.ui.ec02_meter_cb.currentText()
    #     data = building2[building2['meter']==meter]
    #     mask2 = (data['Time column 1']>= from_ts) & (data['Time column 1']<= to_ts)
    #     count = len(data.loc[mask2 &(data['PF']<0.85)])
    #     fig = px.bar(x=[count], y=[meter], title=f"Power Factor Deviation")
    #     fig.update_traces(width=0.2)
    #     plot1 = QWebEngineView()
    #     plot1.setHtml(fig.to_html(include_plotlyjs='cdn',full_html=True))

    #     frame_layout = self.ui.frame_22.layout()
    #     if frame_layout is not None:
    #         for i in reversed(range(frame_layout.count())):
    #             frame_layout.itemAt(i).widget().setParent(None)
    #     else:
    #         frame_layout = QVBoxLayout(self.ui.frame_22)
    #     frame_layout.addWidget(plot1)
    # def ec02_Vswell_Vsag(self,from_ts,to_ts):
    #     meter=self.ui.ec02_meter_cb.currentText()
    #     data = building2[building2['meter']==meter]
    #     voltage = data[['rv','yv','bv','Time column 1']]
    #     voltage.set_index('Time column 1', inplace=True)
    #     voltage = voltage.resample('30S').ffill()
    #     mask2 = (voltage.index>= from_ts) & (voltage.index<= to_ts)
    #     voltage = voltage.loc[mask2]
    #     # Nominal voltage level
    #     nominal_voltage = 230 
    #     threshold = 0.1  # 10% change
    #     # Find the voltage change from nominal voltage for each phase
    #     voltage_change_rv = voltage["rv"] / nominal_voltage - 1
    #     voltage_change_yv = voltage["yv"] / nominal_voltage - 1
    #     voltage_change_bv = voltage["bv"] / nominal_voltage - 1
    #     # Find the time duration between consecutive measurements
    #     time_diff = voltage.index.to_series().diff().dt.total_seconds()
    #     # Identify the voltage swells and sags based on criteria for each phase
    #     is_swell_rv = (voltage_change_rv >= threshold) & (time_diff <= 60)
    #     is_sag_rv = (voltage_change_rv <= -threshold) & (time_diff <= 60)
    #     is_swell_yv = (voltage_change_yv >= threshold) & (time_diff <= 60)
    #     is_sag_yv = (voltage_change_yv <= -threshold) & (time_diff <= 60)
    #     is_swell_bv = (voltage_change_bv >= threshold) & (time_diff <= 60)
    #     is_sag_bv = (voltage_change_bv <= -threshold) & (time_diff <= 60)
    #     # Count the number of voltage swells and sags for each phase
    #     num_swells_rv = is_swell_rv.sum()
    #     num_sags_rv = is_sag_rv.sum()
    #     num_swells_yv = is_swell_yv.sum()
    #     num_sags_yv = is_sag_yv.sum()
    #     num_swells_bv = is_swell_bv.sum()
    #     num_sags_bv = is_sag_bv.sum()
    #     fig = go.Figure(data=[
    #         go.Bar(name='Swells', x=['rv', 'yv', 'bv'], y=[num_swells_rv, num_swells_yv, num_swells_bv]),
    #         go.Bar(name='Sags', x=['rv', 'yv', 'bv'], y=[num_sags_rv, num_sags_yv, num_sags_bv])
    #     ])
    #     fig.update_layout(title='Voltage Swells and Sags')
    #     plot1 = QWebEngineView()
    #     plot1.setHtml(fig.to_html(include_plotlyjs='cdn',full_html=True))

    #     frame_layout = self.ui.frame_20.layout()
    #     if frame_layout is not None:
    #         for i in reversed(range(frame_layout.count())):
    #             frame_layout.itemAt(i).widget().setParent(None)
    #     else:
    #         frame_layout = QVBoxLayout(self.ui.frame_20)
    #     frame_layout.addWidget(plot1)
    
    def voltage(self, from_ts, to_ts, selected_meter, frame):
        dfir = df[(df['meter'] == selected_meter)]
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
        dfir = df[(df['meter'] == selected_meter)]
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
        dfir = df[(df['meter'] == selected_meter)]
        fig = go.Figure()
        mask2=(dfir['Time column 1']>=from_ts)&(dfir['Time column 1']<=to_ts)
        fig.add_trace(go.Scatter(x=dfir.loc[mask2,'Time column 1'],y=dfir.loc[mask2,'PF'],name = 'PF' ))
        fig.update_layout(title={'text':'Power Factor','font': {'size': 20,'family': 'Arial','color': 'black'}}, yaxis_title='Power Factor',plot_bgcolor='white',paper_bgcolor='white')

        plot1 = QWebEngineView()
        plot1.setHtml(fig.to_html(include_plotlyjs='cdn',full_html=True))
        frame_layout = self.ui.frame_14.layout()
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
        dfir = df[(df['meter'] == selected_meter)]
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
    
    # def ec03_energy_consumption(self,from_ts, to_ts):
    #     color=["red","blue","lightgreen","#f0920e","#f71302","#f00e8e","#f0f00e","#0ef083","#0e83f0"]
    #     i=0
    #     M = ['INCOMER-EC03','Trafo-1','Trafo-2','Trafo-3','Trafo-4','Trafo-5']
    #     data=[]
    #     title="EC03 For each Building"
    #     grouped1 = df1.groupby(['building','Time column 1']).sum()
    #     grouped1['cum'] = grouped1['actual_kwh'].cumsum(axis = 0)
    #     grouped1 = grouped1.reset_index()
    #     mask3 = (grouped1['Time column 1']>= from_ts) & (grouped1['Time column 1']<= to_ts)
    #     for b in grouped1.building.unique():
    #         if b not in M:
    #             x=[]
    #             y=[]
    #             x=grouped1.loc[(grouped1["building"]==b)& mask3,"Time column 1"]
    #             y=grouped1.loc[(grouped1["building"]==b)& mask3,"cum"]
    #             trace=go.Scatter(x=x,y=y,mode='lines',line=dict(color=color[i],width=2),name=str(b))
    #             data.append(trace)
    #             i+=1
    #     fig = go.Figure(data=data)
    #     fig.update_layout(title={'text':'EC03 Energy Consumption','font': {'size': 20,'family': 'Arial','color': 'black'}}, yaxis_title='kWh',plot_bgcolor='white',paper_bgcolor='white')

    #     plot1 = QWebEngineView()
    #     plot1.setHtml(fig.to_html(include_plotlyjs='cdn',full_html=True))
    #     frame_layout = self.ui.frame_10.layout()
    #     if frame_layout is not None:
    #         for i in reversed(range(frame_layout.count())):
    #             frame_layout.itemAt(i).widget().setParent(None)
    #     else:
    #         frame_layout = QVBoxLayout(self.ui.frame_10)
    #     frame_layout.addWidget(plot1)
    # def ec03_meter_piechart(self,from_ts,to_ts):
    #     b=self.ui.ec03_building_cb.currentText()
    #     b3 = building3[building3['building']==b]
    #     mask = (b3['Time column 1']>= from_ts) & (b3['Time column 1']<= to_ts)
    #     b3= b3.loc[mask]
    #     meter_counts = b3.groupby('meter').sum().reset_index()
    #     fig = px.pie( meter_counts, values='kwh', names='meter', title='Total Energy Consumpution')

    #     plot1 = QWebEngineView()
    #     plot1.setHtml(fig.to_html(include_plotlyjs='cdn',full_html=True))

    #     frame_layout = self.ui.frame_15.layout()
    #     if frame_layout is not None:
    #         for i in reversed(range(frame_layout.count())):
    #             frame_layout.itemAt(i).widget().setParent(None)
    #     else:
    #         frame_layout = QVBoxLayout(self.ui.frame_15)
    #     frame_layout.addWidget(plot1)
    # def ec03_fre_deviations(self,from_ts,to_ts):
    #     meter=self.ui.ec03_meter_cb.currentText()
    #     data = building3[building3['meter']==meter]
    #     mask2 = (data['Time column 1']>= from_ts) & (data['Time column 1']<= to_ts)
    #     count = len(data.loc[mask2 &(data['F']<49)])
    #     fig = px.bar(x=[count], y=[meter], title=f"Frequency Deviation Count")
    #     fig.update_traces(width=0.2)
    #     plot1 = QWebEngineView()
    #     plot1.setHtml(fig.to_html(include_plotlyjs='cdn',full_html=True))

    #     frame_layout = self.ui.frame_25.layout()
    #     if frame_layout is not None:
    #         for i in reversed(range(frame_layout.count())):
    #             frame_layout.itemAt(i).widget().setParent(None)
    #     else:
    #         frame_layout = QVBoxLayout(self.ui.frame_25)
    #     frame_layout.addWidget(plot1)
    # def ec03_PF_deviations(self,from_ts,to_ts):
    #     meter=self.ui.ec03_meter_cb.currentText()
    #     data = building2[building2['meter']==meter]
    #     mask2 = (data['Time column 1']>= from_ts) & (data['Time column 1']<= to_ts)
    #     count = len(data.loc[mask2 &(data['PF']<0.85)])
    #     fig = px.bar(x=[count], y=[meter], title=f"Power Factor Deviation Count")
    #     fig.update_traces(width=0.2)
    #     plot1 = QWebEngineView()
    #     plot1.setHtml(fig.to_html(include_plotlyjs='cdn',full_html=True))

    #     frame_layout = self.ui.frame_26.layout()
    #     if frame_layout is not None:
    #         for i in reversed(range(frame_layout.count())):
    #             frame_layout.itemAt(i).widget().setParent(None)
    #     else:
    #         frame_layout = QVBoxLayout(self.ui.frame_26)
    #     frame_layout.addWidget(plot1)   
    # def ec03_Vswell_Vsag(self,from_ts,to_ts):
        meter=self.ui.ec03_meter_cb.currentText()
        data = building3[building3['meter']==meter]
        voltage = data[['rv','yv','bv','Time column 1']]
        voltage.set_index('Time column 1', inplace=True)
        voltage = voltage.resample('30S').ffill()
        mask2 = (voltage.index>= from_ts) & (voltage.index<= to_ts)
        voltage = voltage.loc[mask2]
        # Nominal voltage level
        nominal_voltage = 230 
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
        fig = go.Figure(data=[
            go.Bar(name='Swells', x=['rv', 'yv', 'bv'], y=[num_swells_rv, num_swells_yv, num_swells_bv]),
            go.Bar(name='Sags', x=['rv', 'yv', 'bv'], y=[num_sags_rv, num_sags_yv, num_sags_bv])
        ])
        fig.update_layout(title='Voltage Swells and Sags')
        plot1 = QWebEngineView()
        plot1.setHtml(fig.to_html(include_plotlyjs='cdn',full_html=True))

        frame_layout = self.ui.frame_24.layout()
        if frame_layout is not None:
            for i in reversed(range(frame_layout.count())):
                frame_layout.itemAt(i).widget().setParent(None)
        else:
            frame_layout = QVBoxLayout(self.ui.frame_24)
        frame_layout.addWidget(plot1)

    def MI_kwh(self,from_ts, to_ts):
        main_incomer2 = df[df['meter']=='EC02 MFM 11KV TRAFO']
        main_incomer3 = df1[df1['meter']=='33KV Incomer']
        mask2 = (main_incomer2['Time column 1']>= from_ts) & (main_incomer2['Time column 1']<= to_ts)
        mask3 = (main_incomer3['Time column 1']>= from_ts) & (main_incomer3['Time column 1']<= to_ts)
        total2 = round(main_incomer2.loc[mask2, 'actual_kwh'].sum(),0)
        total3 = round(main_incomer3.loc[mask3, 'actual_kwh'].sum(),0)
        return f'11kV TRAFO: {total2} kWh',f'33kV TRAFO: {total3} kWh'
    def MI_powerfactor(self,from_ts,to_ts):
        main_incomer2 = df[(df['meter']=='EC02 MFM 11KV TRAFO')& (df['Vry']!=0)]
        main_incomer3 = df1[(df1['meter']=='33KV Incomer')&(df['Vry']!=0)]
        mask2 = (main_incomer2['Time column 1']>= from_ts) & (main_incomer2['Time column 1']<= to_ts)
        mask3 = (main_incomer3['Time column 1']>= from_ts) & (main_incomer3['Time column 1']<= to_ts)
        pf_limits = 0.85
        count = len(main_incomer2.loc[mask2 &(main_incomer2['PF']<0.85)])
        count1 = len(main_incomer3.loc[mask3 &(main_incomer3['PF']<0.85)])
        return f'11kV TRAFO: {count}',f'33kV TRAFO: {count1}'
    def MI_frequency(self,from_ts,to_ts):
        main_incomer2 = df[(df['meter']=='EC02 MFM 11KV TRAFO')]
        main_incomer3 = df1[(df1['meter']=='33KV Incomer')]
        mask2 = (main_incomer2['Time column 1']>= from_ts) & (main_incomer2['Time column 1']<= to_ts)
        mask3 = (main_incomer3['Time column 1']>= from_ts) & (main_incomer3['Time column 1']<= to_ts)
        count = len(main_incomer2.loc[mask2 &(main_incomer2['F']<49)])
        count1 = len(main_incomer3.loc[mask3 &(main_incomer3['F']<49)])
        return f'11kV TRAFO: {count}',f'33kV TRAFO: {count1}'
    def MI_high_kwh(self,from_ts, to_ts):
        main_incomer2 = df[df['meter']=='EC02 MFM 11KV TRAFO']
        main_incomer3 = df1[df1['meter']=='33KV Incomer']
        mask2 = (main_incomer2['Time column 1']>= from_ts) & (main_incomer2['Time column 1']<= to_ts)
        mask3 = (main_incomer3['Time column 1']>= from_ts) & (main_incomer3['Time column 1']<= to_ts)
        total2 = round(main_incomer2.loc[mask2, 'actual_kwh'].sum(),0)
        total3 = round(main_incomer3.loc[mask3, 'actual_kwh'].sum(),0)
        if total2 > total3:
            return f'11kV main incomer supplies more than 33kV main incomer'
        else:
            return f'33kV main incomer supplies more than 11kV main incomer'       
    def MI_idlehours(self,from_ts,to_ts):
        main_incomer2 = df[(df['meter']=='EC02 MFM 11KV TRAFO')]
        main_incomer3 = df1[(df1['meter']=='33KV Incomer')]
        mask2 = (main_incomer2['Time column 1']>= from_ts) & (main_incomer2['Time column 1']<= to_ts)
        mask3 = (main_incomer3['Time column 1']>= from_ts) & (main_incomer3['Time column 1']<= to_ts)
        count = len(main_incomer2.loc[mask2 &(main_incomer2['Vry']==0) & (main_incomer2['Vbr']==0) & (main_incomer2['Vyb']==0) & (main_incomer2['Ir']==0) & (main_incomer2['Iy']==0) & (main_incomer2['Ib']==0)])
        count1 = len(main_incomer3.loc[mask3&(main_incomer3['Vry']==0) & (main_incomer3['Vbr']==0) & (main_incomer3['Vyb']==0) & (main_incomer3['Ir']==0) & (main_incomer3['Iy']==0) & (main_incomer3['Ib']==0)])
        hour_count = count/4
        hour_count1 =count1/4
        return f'11kV TRAFO is idle for {hour_count} hours',f'33kV TRAFO is idle for {hour_count1} hours'
    def MI_33kv_Vswell_Vsag(self,from_ts,to_ts):
        main_incomer3 = df1[(df1['meter']=='33KV Incomer')]
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
    def MI_11kv_Vswell_Vsag(self,from_ts,to_ts):
        main_incomer2 = df[(df['meter']=='EC02 MFM 11KV TRAFO')]
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
    
    def In_kwh(self,from_ts, to_ts):
        selected_meter = self.ui.In_insights_cb.currentText()
        data = df4[df4['meter']==selected_meter]
        mask2 = (data['Time column 1']>= from_ts) & (data['Time column 1']<= to_ts)
        total = round(data.loc[mask2,'actual_kwh'].sum(),0)
        return f' {selected_meter}: {total} kWh'
    def In_frequency(self,from_ts,to_ts):
        selected_meter = self.ui.In_insights_cb.currentText()
        data = df4[df4['meter']==selected_meter]
        mask2 = (data['Time column 1']>= from_ts) & (data['Time column 1']<= to_ts)
        count = len(data.loc[mask2 &(data['F']<49)])
        return f' {selected_meter}: {count}'
    def In_powerfactor(self,from_ts,to_ts):
        selected_meter = self.ui.In_insights_cb.currentText()
        data = df4[df4['meter']==selected_meter]
        mask2 = (data['Time column 1']>= from_ts) & (data['Time column 1']<= to_ts)
        pf_limits = 0.85
        count = len(data.loc[mask2 &(data['PF']<0.85)])
        return f'{selected_meter}: {count}'
    def In_Vswell_Vsag(self,from_ts,to_ts):
        selected_meter = self.ui.In_insights_cb.currentText()
        main_incomer3 = df4[(df4['meter']==selected_meter)]
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
    def In_idlehours(self,from_ts,to_ts):
        selected_meter = self.ui.In_insights_cb.currentText()
        data = df4[df4['meter']==selected_meter]
        mask2 = (data['Time column 1']>= from_ts) & (data['Time column 1']<= to_ts)
        count = len(data.loc[mask2 &(data['Vry']==0) & (data['Vbr']==0) & (data['Vyb']==0) & (data['Ir']==0) & (data['Iy']==0) & (data['Ib']==0)])
        hour_count =count/4
        return f'{selected_meter} is idle hours for {hour_count} hours'
    
    def BI_kwh(self,from_ts,to_ts):
        selected_center = self.ui.BI_insights_cb.currentText()
        data = df3[df3['center']== selected_center]
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
    def BI_idlehours(self,from_ts, to_ts):
        selected_center = self.ui.BI_insights_cb.currentText()
        d = df3[df3['center']== selected_center]
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
    def BI_kwh_max(self,from_ts,to_ts):
        selected_center = self.ui.BI_insights_cb.currentText()
        data = df3[df3['center']== selected_center]
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
    def BI_kwh_min(self,from_ts,to_ts):
        selected_center = self.ui.BI_insights_cb.currentText()
        data = df3[df3['center']== selected_center]
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
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    style_file = QFile("style.qss")
    style_file.open(QFile.ReadOnly | QFile.Text)
    style_stream = QTextStream(style_file)
    app.setStyleSheet(style_stream.readAll())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
