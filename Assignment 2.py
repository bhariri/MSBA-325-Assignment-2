# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 12:18:07 2022

@author: Basman
"""
#importing needed libraries
import os
import pandas as pd
import streamlit as st
import plotly.graph_objs as go
from plotly.offline import iplot
from PIL import Image
import bar_chart_race as bcr
import ffmpeg
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="The World University Rankings",
    page_icon="🏫",
    layout="centered"
)



# Creating the Side Bar Navigation Panel
navigate = st.sidebar.radio('Navigation Side Bar',
                 ('Home Page', 'Data Exploration','Plotly Visualizations'))
imgside=Image.open('2.jpg')
st.sidebar.image(imgside, use_column_width=True)

# Updating the Datset if needed
uploaded_file = st.file_uploader("Upload updated dataset")



if uploaded_file is None:
        df = pd.read_csv("universities.csv")
        if uploaded_file is not None:
                df = pd.read_csv(uploaded_file)
        
    
df.head()        
df.describe()

#checking for null values
df.isna().sum()

# Deleting rows that contain null values in any column
#df.dropna(inplace=True)
#features info
df.info()

# Creating the Home Page

if navigate == 'Home Page':
    
      
    # adding the home page image
    img=Image.open('1.jpg')
    st.image(img)
    
    # dashboard description
    st.header("Context")
    st.markdown("""In the context of rapidly growing demand for higher education, the relevance of the global rankings of the universities increases all over the world. Results of these rankings not only allow evaluation of the higher education quality, but also affect its competitiveness in the educational market. Recognition of the educational institution at the international level is becoming increasingly important for universities around the world..""")
    # dataset info
    st.header("Dataset Information")
    st.markdown("""The dataset contains 13 features that can be used to assess the universities performance . It includes 14 variables describing 2603 observations for 818 universities distributed around the world between 72 countries from year 2011 till year 2016.
    """)

if navigate == 'Data Exploration':
    if st.button('Show raw data'):
        st.subheader('Raw data')
        st.write(df)
            
    if st.button('Show a sample of the data'):
            st.subheader('Sample data')
            st.write(df.head())
            
    if st.button('Describe Data'):
            st.subheader('Data Descriptive Summary')
            st.write(df.describe())
    
    if st.button('Data Information'):
        st.subheader('Data Information')
        import io 
        buffer = io.StringIO()
        df.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)


if navigate == 'Plotly Visualizations':
    #Line Charts of Citation and Teaching vs World Rank of Top 50 Universities
    # will take only first top 50 universities of dataset
    df50 = df.iloc[:51,:]
    # Creating trace1
    trace1 = go.Scatter(
                        x = df50.world_rank,
                        y = df50.citations,
                        mode = "lines",
                        name = "citations",
                        marker = dict(color = 'rgba(16, 112, 2, 0.8)'),
                        text= df50.university_name)
    # Creating trace2
    trace2 = go.Scatter(
                        x = df50.world_rank,
                        y = df50.teaching,
                        mode = "lines+markers",
                        name = "teaching",
                        marker = dict(color = 'rgba(80, 26, 80, 0.8)'),
                        text= df50.university_name)
    data = [trace1, trace2]
    layout = dict(title = '<b>Line Charts of Citation and Teaching vs World Rank of Top 50 Universities year 2011',
                  xaxis= dict(title= 'World Rank',ticklen= 5,zeroline= False)
                 )
    fig = dict(data = data, layout = layout)
    st.markdown("<h1 style='text-align: center; color: blue;'>Data Visualization</h1>", unsafe_allow_html=True)
    st.plotly_chart(fig)
    st.markdown("As we can see from the chart Teaching is more corrolated than Citations in term of World Rank , however for some universities when the number of citations decrease the rank decrease even with high value of teaching.\n""")
    
    
    # Scatter plot of Citations vs World Rank of Top 50 Universities for last 3 years
    # will take only first top 50 universities of dataset
    df2014 = df[df.year == 2014].iloc[:50,:]
    df2015 = df[df.year == 2015].iloc[:50,:]
    df2016 = df[df.year == 2016].iloc[:50,:]
    
    # creating trace1
    trace1 =go.Scatter(
                        x = df2014.world_rank,
                        y = df2014.research,
                        mode = "markers",
                        name = "2014",
                        marker = dict(color = 'rgba(255, 128, 255, 0.8)'),
                        text= df2014.university_name)
    # creating trace2
    trace2 =go.Scatter(
                        x = df2015.world_rank,
                        y = df2015.research,
                        mode = "markers",
                        name = "2015",
                        marker = dict(color = 'rgba(255, 128, 2, 0.8)'),
                        text= df2015.university_name)
    # creating trace3
    trace3 =go.Scatter(
                        x = df2016.world_rank,
                        y = df2016.research,
                        mode = "markers",
                        name = "2016",
                        marker = dict(color = 'rgba(0, 255, 200, 0.8)'),
                        text= df2016.university_name)
    data = [trace1, trace2, trace3]
    layout = dict(title = '<b>Scatter plot of research vs world rank of top 50 universities for last 3 years',
                  xaxis= dict(title= 'World Rank',ticklen= 5,zeroline= False),
                  yaxis= dict(title= 'Research',ticklen= 5,zeroline= False)
                 )
    fig2 = dict(data = data, layout = layout)
    st.plotly_chart(fig2)
    st.markdown("As we can see from the scatter plot, number of researches is positively corrolated with the world rank, except in some cases were the values of citations and teaching are low")

    #Bar Plot of Citations and Teaching of top 5 universities including location in 2016
    # will take the top 5 universities for year 2016 of dataset
    df2016_2 = df[df.year == 2016].iloc[:5,:]

    # create trace1 
    trace1 = go.Bar(
                    x = df2016_2.university_name,
                    y = df2016_2.citations,
                    name = "citations",
                    marker = dict(color = 'rgba(255, 174, 255, 0.5)',
                                 line=dict(color='rgb(0,0,0)',width=1.5)),
                    text = df2016_2.country)
    # create trace2 
    trace2 = go.Bar(
                    x = df2016_2.university_name,
                    y = df2016_2.teaching,
                    name = "teaching",
                    marker = dict(color = 'rgba(255, 255, 128, 0.5)',
                                  line=dict(color='rgb(0,0,0)',width=1.5)),
                    text = df2016_2.country)
    data = [trace1, trace2]
    layout = go.Layout(title = "<b>Bar plot of Citations and Teaching of top 5 universities including location in 2016",barmode = "group")
    fig3 = go.Figure(data = data, layout = layout)
    st.plotly_chart(fig3)           
    
    # Pie Chart of Students rate of top 5 universities in 2016
    # will take the top 5 universities from the dataset
    df2016_3 = df[df.year == 2016].iloc[:5,:]
    pie1 = df2016_3.num_students
    pie1_list = [float(each.replace(',', '.')) for each in df2016_3.num_students]  
    labels = df2016_3.university_name
    # figure
    fig4 = {
      "data": [
        {
          "values": pie1_list,
          "labels": labels,
          "domain": {"x": [0, .5]},
          "name": "Number Of Students Rates",
          "hoverinfo":"label+percent+name",
          "hole": .3,
          "type": "pie"
        },],
      "layout": {
            "title":"<b>Top 5 Universities Number of Students rates Year 2016",
            "annotations": [
                { "font": { "size": 20},
                  "showarrow": False,
                  "text": "Number of Students",
                    "x": 0.20,
                    "y": 1
                },
            ]
        }
    }
    st.plotly_chart((fig4))
    
    #Bubble Chart of University world rank (Top 20) vs teaching score with number of students(size) and international score (color) in 2016
    st.markdown("<h6 style='text-align: center; color: black;'>Bubble chart of University world rank (Top 20) vs teaching score with number of students(size) and international score (color) in 2016</h1>", unsafe_allow_html=True)
    # will take the top 20 universities from the dataset
    df2016_4 = df[df.year == 2016].iloc[:20,:]
    
    num_students_size  = [float(each.replace(',', '.')) for each in df2016_4.num_students]
    international_color = [float(each) for each in df2016_4.international]
    
    fig5 = [
        {
            
            'y': df2016_4.teaching,
            'x': df2016_4.world_rank,
            'mode': 'markers',
            'marker': {
                'color': international_color,
                'size': num_students_size,
                'showscale': True,},
            "text" :  df2016_4.university_name,
            
        }
        
    ]
    
    st.plotly_chart(fig5)
    
    #Animated 
    import plotly.express as px
    dfa = df
    
    fig6=px.scatter(dfa, x="world_rank", y="teaching", animation_frame="year", animation_group="country",
               size="citations", color="country", hover_name="university_name",
               log_x=True, size_max=55, range_x=[1,100], range_y=[25,90])
    st.plotly_chart(fig6)
    
    # #Animated 2
    
    
    
   
    # dfa2=df
    # dfa2.drop(df.columns[[0,3,4,5,6,7,8,9,10,11,12,13,14]], axis=1, inplace=True)
    # dfa2.head()
    # dfa2.info()
    
    # #dfa2 = dfa2.pivot(index = "year", columns = "university_name", values = "num_of_students").reset_index().rename_axis(None, axis=1)
    
    
    # dfa2.set_index("year", inplace = True)
    # fig6=bcr.bar_chart_race(dfa2, filename=('race.mp4'),n_bars=3,filter_column_colors=True,title='test test')
    # st.plotly_chart(fig6)
