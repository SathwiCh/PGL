import sys
from PyQt5.QtWidgets import QVBoxLayout
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
from PyQt5.QtWebEngineWidgets import QWebEngineView
import pandas as pd

df_ec02_ec03=pd.read_csv('C:\\Users\\20339181\\OneDrive - L&T Construction\\Desktop\\Dashboards-Analytics\\PyQt5-Dashboard-Main\\Dashboard Template\\ec02_ec03.csv')
df_ec02_ec03['Time column 1'] = df_ec02_ec03['Time column 1'].astype(str)
df_ec02_ec03['Time column 1'] = pd.to_datetime(df_ec02_ec03['Time column 1'],format = '%d.%m.%Y %H:%M:%S.%f')
df_all_buildings = df_ec02_ec03[(df_ec02_ec03["building"] == 'TC-1') | (df_ec02_ec03["building"] == 'TC&MEDICAL') | (df_ec02_ec03["building"] == 'TC3-TOWER A') | (df_ec02_ec03["building"] == 'TC3-TOWER B') | (df_ec02_ec03["building"] == 'TC3 HVAC')]
last_date = pd.to_datetime('2022-09-28')
home_df = df_all_buildings[df_all_buildings['Time column 1'].dt.date == last_date.date()]

class HomePlotter:
    def __init__(self, ui):
        self.ui=ui
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
