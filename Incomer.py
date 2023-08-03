import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton,QVBoxLayout,QFrame,QWidget
from PyQt5.QtCore import pyqtSlot, QFile, QTextStream
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtWidgets
import pandas as pd

df2=pd.read_csv('C:\\Users\\20339181\\L&T Construction\\PT&D Digital Solutions - Incubation - Documents\\Incubation\\DSIDIB Team\\Sathwika\\PGL-Analytics-Insights-Final - Copy\\Dashboard Template\\ec02_ec03.csv')
print("Loading...")
df2['Time column 1'] = df2['Time column 1'].astype(str)
df2['Time column 1'] = pd.to_datetime(df2['Time column 1'],format = '%d.%m.%Y %H:%M:%S.%f')

def total_incomer_supply(self,from_ts, to_ts):
        color=["red","blue","lightgreen","#f0920e","#f71302","#f00e8e","#f0f00e","#0ef083","#0e83f0"]
        i=0
        M = ['INCOMER-EC03','Trafo-1','Trafo-2','Trafo-3','Trafo-4','Trafo-5','trafo-1','INCOMER']
        data=[]
        title="INCOMERS For entrie Centers"
        grouped1 = df2.groupby(['building','Time column 1']).sum()
        grouped1 = grouped1.reset_index()
        mask = (grouped1['Time column 1']>= from_ts) & (grouped1['Time column 1']<= to_ts)
        for b in grouped1.building.unique():
            if b in M:
                x=[]
                y=[]
                x=grouped1.loc[(grouped1["building"]==b)& mask,"Time column 1"]
                y=grouped1.loc[(grouped1["building"]==b)& mask,"kwh"]
                trace=go.Scatter(x=x,y=y,mode='lines',line=dict(color=color[i],width=2),name=str(b))
                data.append(trace)
                i+=1
        fig = go.Figure(data=data)
        fig.update_layout(title={'text': 'Incomers','font': {'size': 20,'family': 'Arial','color': 'black'}}, yaxis_title='kWh',plot_bgcolor='white',paper_bgcolor='white')
        plot1 = QWebEngineView()
        plot1.setHtml(fig.to_html(include_plotlyjs='cdn',full_html=True))
        frame_layout = self.ui.frame_4.layout()
        if frame_layout is not None:
            for i in reversed(range(frame_layout.count())):
                frame_layout.itemAt(i).widget().setParent(None)
        else:
            frame_layout = QVBoxLayout(self.ui.frame_4)
        frame_layout.addWidget(plot1)  