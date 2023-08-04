import sys
from PyQt5.QtWidgets import QVBoxLayout
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
from PyQt5.QtWebEngineWidgets import QWebEngineView
import pandas as pd

#Read the Dataframes from the local
#df--this variable refers to the dataset of Energy Center-2 (EC02)
df=pd.read_csv('C:\\Users\\20339181\\L&T Construction\\PT&D Digital Solutions - Incubation - Documents\\Incubation\\DSIDIB Team\\Sathwika\\PGL-Analytics-Insights-Final - Copy\\Dashboard Template\\new_ec02.csv')

#df1--this variable refers to the dataset of Energy Center-3 (EC03)
df1=pd.read_csv('C:\\Users\\20339181\\L&T Construction\\PT&D Digital Solutions - Incubation - Documents\\Incubation\\DSIDIB Team\\Sathwika\\PGL-Analytics-Insights-Final - Copy\\Dashboard Template\\new_ec03.csv')

#df2--this variable refers to the combined dataset of Energy Center-2 & 3 (whole dataset)
df2=pd.read_csv('C:\\Users\\20339181\\L&T Construction\\PT&D Digital Solutions - Incubation - Documents\\Incubation\\DSIDIB Team\\Sathwika\\PGL-Analytics-Insights-Final - Copy\\Dashboard Template\\ec02_ec03.csv')
print("Loading...")

#Converting the Time column to the pandas datetime object
df['Time column 1'] = df['Time column 1'].astype(str)
df['Time column 1'] = pd.to_datetime(df['Time column 1'],format = '%d.%m.%Y %H:%M:%S.%f')
df1['Time column 1'] = df1['Time column 1'].astype(str)
df1['Time column 1'] = pd.to_datetime(df1['Time column 1'],format = '%d.%m.%Y %H:%M:%S.%f')
df2['Time column 1'] = df2['Time column 1'].astype(str)
df2['Time column 1'] = pd.to_datetime(df2['Time column 1'],format = '%d.%m.%Y %H:%M:%S.%f')

#create a Varible to store buildings data of ec03
ec03_buildings = df1[df1['building'].isin(['TC3-TOWER A', 'TC3-TOWER B', 'TC3 HVAC'])]

class EC03Plotter:
    def __init__(self, df2,df1,df, ui):
        self.df2 = df2
        self.df1=df1
        self.df=df
        self.ui=ui
    #total energy consumption of energy center- 2 
    def ec03_energy_consumption(self,from_ts, to_ts):
        color=["red","blue","lightgreen","#f0920e","#f71302","#f00e8e","#f0f00e","#0ef083","#0e83f0"]
        i=0
        M = ['INCOMER-EC03','Trafo-1','Trafo-2','Trafo-3','Trafo-4','Trafo-5']
        data=[]
        title="EC03 For each Building"
        grouped1 = df1.groupby(['building','Time column 1']).sum()
        grouped1['cum'] = grouped1['actual_kwh'].cumsum(axis = 0)
        grouped1 = grouped1.reset_index()
        mask3 = (grouped1['Time column 1']>= from_ts) & (grouped1['Time column 1']<= to_ts)
        for b in grouped1.building.unique():
            if b not in M:
                x=[]
                y=[]
                x=grouped1.loc[(grouped1["building"]==b)& mask3,"Time column 1"]
                y=grouped1.loc[(grouped1["building"]==b)& mask3,"cum"]
                trace=go.Scatter(x=x,y=y,mode='lines',line=dict(color=color[i],width=2),name=str(b))
                data.append(trace)
                i+=1
        fig = go.Figure(data=data)
        fig.update_layout(title={'text':'EC03 Energy Consumption','font': {'size': 20,'family': 'Arial','color': 'black'}}, yaxis_title='kWh',plot_bgcolor='white',paper_bgcolor='white')

        plot1 = QWebEngineView()
        plot1.setHtml(fig.to_html(include_plotlyjs='cdn',full_html=True))
        frame_layout = self.ui.ec03_kwh_frame.layout()
        if frame_layout is not None:
            for i in reversed(range(frame_layout.count())):
                frame_layout.itemAt(i).widget().setParent(None)
        else:
            frame_layout = QVBoxLayout(self.ui.ec03_kwh_frame)
        frame_layout.addWidget(plot1)

    #Total energy consumption of each meter of ec02 in pie chart
    def ec03_meter_piechart(self,from_ts,to_ts):
        b=self.ui.ec03_building_cb.currentText()
        b3 = ec03_buildings[ec03_buildings['building']==b]
        mask = (b3['Time column 1']>= from_ts) & (b3['Time column 1']<= to_ts)
        b3= b3.loc[mask]
        meter_counts = b3.groupby('meter').sum().reset_index()
        fig = px.pie( meter_counts, values='kwh', names='meter', title='Total Energy Consumpution')

        plot1 = QWebEngineView()
        plot1.setHtml(fig.to_html(include_plotlyjs='cdn',full_html=True))

        frame_layout = self.ui.ec03_piechart_frame.layout()
        if frame_layout is not None:
            for i in reversed(range(frame_layout.count())):
                frame_layout.itemAt(i).widget().setParent(None)
        else:
            frame_layout = QVBoxLayout(self.ui.ec03_piechart_frame)
        frame_layout.addWidget(plot1)

    #frequency Deviations
    def ec03_fre_deviations(self,from_ts,to_ts):
        meter=self.ui.ec03_meter_cb.currentText()
        data = ec03_buildings[ec03_buildings['meter']==meter]
        mask2 = (data['Time column 1']>= from_ts) & (data['Time column 1']<= to_ts)
        count = len(data.loc[mask2 &(data['F']<49)])
        fig = px.bar(x=[count], y=[meter], title=f"Frequency Deviation Count")
        fig.update_traces(width=0.2)
        plot1 = QWebEngineView()
        plot1.setHtml(fig.to_html(include_plotlyjs='cdn',full_html=True))

        frame_layout = self.ui.ec03_Fdev_frame.layout()
        if frame_layout is not None:
            for i in reversed(range(frame_layout.count())):
                frame_layout.itemAt(i).widget().setParent(None)
        else:
            frame_layout = QVBoxLayout(self.ui.ec03_Fdev_frame)
        frame_layout.addWidget(plot1)

    #Power Factor Deviations
    def ec03_PF_deviations(self,from_ts,to_ts):
        meter=self.ui.ec03_meter_cb.currentText()
        data = ec03_buildings[ec03_buildings['meter']==meter]
        mask2 = (data['Time column 1']>= from_ts) & (data['Time column 1']<= to_ts)
        count = len(data.loc[mask2 &(data['PF']<0.85)])
        fig = px.bar(x=[count], y=[meter], title=f"Power Factor Deviation Count")
        fig.update_traces(width=0.2)
        plot1 = QWebEngineView()
        plot1.setHtml(fig.to_html(include_plotlyjs='cdn',full_html=True))

        frame_layout = self.ui.ec03_PFdev_frame.layout()
        if frame_layout is not None:
            for i in reversed(range(frame_layout.count())):
                frame_layout.itemAt(i).widget().setParent(None)
        else:
            frame_layout = QVBoxLayout(self.ui.ec03_PFdev_frame)
        frame_layout.addWidget(plot1)   

    #voltage swell and sags
    def ec03_Vswell_Vsag(self,from_ts,to_ts):
        meter=self.ui.ec03_meter_cb.currentText()
        data = ec03_buildings[ec03_buildings['meter']==meter]
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

        frame_layout = self.ui.ec03_Vswellsag_frame.layout()
        if frame_layout is not None:
            for i in reversed(range(frame_layout.count())):
                frame_layout.itemAt(i).widget().setParent(None)
        else:
            frame_layout = QVBoxLayout(self.ui.ec03_Vswellsag_frame)
        frame_layout.addWidget(plot1)