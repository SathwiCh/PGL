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

#Converting the Time column to the pandas datetime object
ec02_buildings = df[df['building'].isin(['TC-1','TC&MEDICAL'])]

#total energy consumption of energy center- 2 
def ec02_energy_consumption(self,from_ts, to_ts):
    data=[]
    title="EC02 For each Building"
    grouped = df.groupby(['building','Time column 1']).sum()
    grouped['cum'] = grouped['actual_kwh'].cumsum(axis = 0)
    grouped = grouped.reset_index()
    mask2 = (grouped['Time column 1']>= from_ts) & (grouped['Time column 1']<= to_ts)
    for b in grouped.building.unique():
        if (b!='INCOMER') and (b !='trafo-1'):
            x=[]
            y=[]
            x=grouped.loc[(grouped["building"]==b)& mask2,"Time column 1"]
            y=grouped.loc[(grouped["building"]==b)& mask2,"cum"]
            trace=go.Scatter(x=x,y=y,mode='lines',line=dict(width=2),name=str(b))
            data.append(trace)
    fig=go.Figure(data=data)
    fig.update_layout(title={'text':'EC02 Energy Consumption','font': {'size': 20,'family': 'Arial','color': 'black'}}, yaxis_title='kWh',plot_bgcolor='white',paper_bgcolor='white')

    plot1 = QWebEngineView()
    plot1.setHtml(fig.to_html(include_plotlyjs='cdn',full_html=True))
    frame_layout = self.ui.frame_9.layout()
    if frame_layout is not None:
        for i in reversed(range(frame_layout.count())):
            frame_layout.itemAt(i).widget().setParent(None)
    else:
        frame_layout = QVBoxLayout(self.ui.frame_9)
    frame_layout.addWidget(plot1)

#Total energy consumption of each meter of ec02 in pie chart
def ec02_meter_piechart(self,from_ts,to_ts):
    b=self.ui.ec02_building_cb.currentText()
    b2 = ec02_buildings[ec02_buildings['building']==b]
    mask = (b2['Time column 1']>= from_ts) & (b2['Time column 1']<= to_ts)
    b2= b2.loc[mask]
    meter_counts = b2.groupby('meter').sum().reset_index()
    fig = px.pie( meter_counts, values='kwh', names='meter', title='Total Energy Consumpution')
    plot1 = QWebEngineView()
    plot1.setHtml(fig.to_html(include_plotlyjs='cdn',full_html=True))

    frame_layout = self.ui.frame_11.layout()
    if frame_layout is not None:
        for i in reversed(range(frame_layout.count())):
            frame_layout.itemAt(i).widget().setParent(None)
    else:
        frame_layout = QVBoxLayout(self.ui.frame_11)
    frame_layout.addWidget(plot1)

#frequency Deviations
def ec02_fre_deviations(self,from_ts,to_ts):
    meter=self.ui.ec02_meter_cb.currentText()
    data = ec02_buildings[ec02_buildings['meter']==meter]
    mask2 = (data['Time column 1']>= from_ts) & (data['Time column 1']<= to_ts)
    count = len(data.loc[mask2 &(data['F']<49)])
    fig = px.bar(x=[count], y=[meter], title=f"Frequency Deviation Count")
    fig.update_traces(width=0.2) # set the width of the bars
    plot1 = QWebEngineView()
    plot1.setHtml(fig.to_html(include_plotlyjs='cdn',full_html=True))

    frame_layout = self.ui.frame_21.layout()
    if frame_layout is not None:
        for i in reversed(range(frame_layout.count())):
            frame_layout.itemAt(i).widget().setParent(None)
    else:
        frame_layout = QVBoxLayout(self.ui.frame_21)
    frame_layout.addWidget(plot1)

#Power Factor Deviations
def ec02_PF_deviations(self,from_ts,to_ts):
    meter=self.ui.ec02_meter_cb.currentText()
    data = ec02_buildings[ec02_buildings['meter']==meter]
    mask2 = (data['Time column 1']>= from_ts) & (data['Time column 1']<= to_ts)
    count = len(data.loc[mask2 &(data['PF']<0.85)])
    fig = px.bar(x=[count], y=[meter], title=f"Power Factor Deviation")
    fig.update_traces(width=0.2)
    plot1 = QWebEngineView()
    plot1.setHtml(fig.to_html(include_plotlyjs='cdn',full_html=True))

    frame_layout = self.ui.frame_22.layout()
    if frame_layout is not None:
        for i in reversed(range(frame_layout.count())):
            frame_layout.itemAt(i).widget().setParent(None)
    else:
        frame_layout = QVBoxLayout(self.ui.frame_22)
    frame_layout.addWidget(plot1)

#voltage swell and sags
def ec02_Vswell_Vsag(self,from_ts,to_ts):
    meter=self.ui.ec02_meter_cb.currentText()
    data = ec02_buildings[ec02_buildings['meter']==meter]
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

    frame_layout = self.ui.frame_20.layout()
    if frame_layout is not None:
        for i in reversed(range(frame_layout.count())):
            frame_layout.itemAt(i).widget().setParent(None)
    else:
        frame_layout = QVBoxLayout(self.ui.frame_20)
    frame_layout.addWidget(plot1)