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

#Finding the total energy consumtion of center wise
def total_energy_consumption(self,from_ts, to_ts):
    gdf = df[['Time column 1','actual_kwh']]
    grouped_df = gdf.groupby('Time column 1').sum()
    gdf1 = df1[['Time column 1','actual_kwh']]
    grouped_df1 = gdf1.groupby('Time column 1').sum()
    grouped_df = grouped_df.reset_index()
    grouped_df1 = grouped_df1.reset_index()
    grouped_df['cum']=grouped_df['actual_kwh'].cumsum(axis = 0)
    grouped_df1['cum']=grouped_df1['actual_kwh'].cumsum(axis = 0)
    fig = go.Figure()
    mask2 = (grouped_df['Time column 1']>= from_ts) & (grouped_df['Time column 1']<= to_ts)
    mask3 = (grouped_df1['Time column 1']>= from_ts) & (grouped_df1['Time column 1']<= to_ts)
    fig.add_trace(go.Scatter(x=grouped_df.loc[mask2, 'Time column 1'], y=grouped_df.loc[mask2, 'cum'], name='EC02'))
    fig.add_trace(go.Scatter(x=grouped_df1.loc[mask3, 'Time column 1'], y=grouped_df1.loc[mask3, 'cum'], name='EC03'))
    fig.update_layout(title={'text': 'Energy Consumption','font': {'size': 20,'family': 'Arial','color': 'black'}}, yaxis_title='kWh',plot_bgcolor='white',paper_bgcolor='white')
    # x=fig.show()
    # return x
    plot1 = QWebEngineView()
    plot1.setHtml(fig.to_html(include_plotlyjs='cdn',full_html=True))
    frame_layout = self.ui.fram.layout()
    if frame_layout is not None:
        for i in reversed(range(frame_layout.count())):
            frame_layout.itemAt(i).widget().setParent(None)
    else:
        frame_layout = QVBoxLayout(self.ui.fram)
    frame_layout.addWidget(plot1) 
    print("no prblm")

#Displaying the consumption of centers in pie chart
def centerwise_piechart(self,from_ts, to_ts):
    m1 = df2.groupby(['center','Time column 1']).sum()
    m1 = m1.reset_index()
    mask = (m1['Time column 1']>= from_ts) & (m1['Time column 1']<= to_ts)
    m1=m1.loc[mask]
    fig = px.pie(m1, values='kwh', names='center',title= 'Energy Consumption')
    # fig = go.Figure(data=data)
    plot1 = QWebEngineView()
    plot1.setHtml(fig.to_html(include_plotlyjs='cdn',full_html=True))

    frame_layout = self.ui.frame_3.layout()
    if frame_layout is not None:
        for i in reversed(range(frame_layout.count())):
            frame_layout.itemAt(i).widget().setParent(None)
    else:
        frame_layout = QVBoxLayout(self.ui.frame_3)
    frame_layout.addWidget(plot1)

#weekly total energy consumption 
def weekly_graph(self,from_ts, to_ts):
    mask = (df2['Time column 1']>= to_ts-pd.Timedelta('7 days')) & (df2['Time column 1']<= to_ts)
    m=df2.loc[mask]
    m1 = m.pivot_table(index='days_of_week', columns=['time_of_day'], values=['kwh'], aggfunc='count')
    m1 = m1.melt(ignore_index=False)
    m1.reset_index(inplace=True)
    fig = px.bar(data_frame=m1,
    x="days_of_week",
    y="value",
    color='time_of_day',
    category_orders={'time_of_day':['morning', 'afternoon', 'evening', 'night']},
    orientation='v',
    barmode='relative',
    opacity=0.8,
    # plot_bgcolor='white',
    # paper_bgcolor='white',
    color_discrete_map={'morning':'#ffff00','afternoon':'#f26517','evening':'#69b2f4','night':'#b2b2b2'})
    # fig.update_layout(title={'text': 'Energy Consumption','font': {'size': 20,'family': 'Arial','color': 'black'}}, yaxis_title='kWh',plot_bgcolor='white',paper_bgcolor='white')
    plot1 = QWebEngineView()
    plot1.setHtml(fig.to_html(include_plotlyjs='cdn',full_html=True))

    frame_layout = self.ui.frame_2.layout()
    if frame_layout is not None:
        for i in reversed(range(frame_layout.count())):
            frame_layout.itemAt(i).widget().setParent(None)
    else:
        frame_layout = QVBoxLayout(self.ui.frame_2)
    frame_layout.addWidget(plot1)   