import pandas as pd
import streamlit as st 
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pickle

#Changing backround color of a webpage
bg_color = 'dbe5d3' # This color code taken from HTML color codes 
st.markdown(f"""<style>.stApp {{background-color: {bg_color};}}</style>""",unsafe_allow_html=True)

#Title and logo
st.title("Crop Production Prediction🌾")
col1, col2 = st.columns([0.9, 0.19]) 

with col1:
    st.markdown("<h1 style='font-family: Times New Roman; color: white;'>   Crop Production Prediction</h1>", unsafe_allow_html=True)
with col2:
    st.image(r"D:\\Projects\\Guvi_Project3\\crops.jpg")

#data collection
data=pd.read_csv(r'D:\\Projects\\Guvi_Project3\\Cleaned_Data_final.csv')
#data.drop(columns='Unnamed: 0',inplace=True)


#Creating radio button 
options=st.sidebar.radio("",['Home🏠','Analyze Crop Distribution🏭','Temporal Analysis📈','Input-Output Relationships🔧',
                             'Comparative Analysis📊','Outliers detection⚠️','Predict💡'
                             ])

#Displaying EDA charts
if options=='Home🏠':
    st.header('About')
    st.write("Agriculture is a key contributor to the economy, and accurately predicting crop production is essential for improving planning and decision-making. This project aims to develop a regression model that forecasts crop production (in tons) based on agricultural factors such as area harvested (in hectares), yield (in kg/ha), and the year, for various crops grown in a specific region.")

    st.header('1️⃣ Top Crops by Total Production Insights') 
    st.write("1. Sugar cane is the most produced crop, followed by Maize, Rice, and Wheat.")
    st.write("2. Oil palm fruit and Cassava are also among the high-production crops.")

    st.header('2️⃣ Top Crops by Yield  Insights') 
    st.write("1. Vegetables (Cucumbers, Tomatoes, and Eggplants) have the highest yield per hectare.")
    st.write("2. Sugar cane and Sugar beet also have extremely high productivity.")

    st.header('3️⃣ Outlier Analysis') 
    st.metric(label="Area Harvested", value='7,245 records')
    st.metric(label="Yield", value='3,307 records')
    st.metric(label="Production", value='7,231  records')
    st.write("1. The Area Harvested and Production columns have the most anomalies, suggesting large variations in agricultural practices across regions")
    st.write("2. Yield has fewer outliers, meaning its distribution is more stable.")
    
    st.header('4️⃣ Yearly Trend of Total Crop Production')
    st.write("1. Crop production has steadily increased from 2019 to 2023.")
    st.write("2. The highest production was in 2023 (~11.69 billion tons), showing an upward trend in agriculture.")

if options == 'Analyze Crop Distribution🏭':
    ct=data['Item'].value_counts(ascending=False).reset_index(name='Cultivation_count')
    top10_max=ct.head(10)
    ct_min=data['Item'].value_counts(ascending=True).reset_index(name='Cultivation_count')
    top10_min=ct_min.head(10)
    max_crop=px.bar(top10_max,x='Item',y='Cultivation_count')
    max_crop.update_layout(title='Max cultivated items during the year 2019 to 2023')
    st.plotly_chart(max_crop)
    min_crop=px.bar(top10_min,x='Item',y='Cultivation_count')
    min_crop.update_layout(title='Min cultivated items during the year 2019 to 2023')
    st.plotly_chart(min_crop)
    gd=data[['Area','Item']]
    gd_analysis=gd.value_counts().reset_index(name='cultivated_count')
    gd_most = gd_analysis.loc[gd_analysis.groupby("Area")["cultivated_count"].idxmax()] 
    gdc = px.scatter_geo(gd_most, 
                     locations="Area", 
                     locationmode="country names", 
                     hover_data={'Item','cultivated_count'},
                     title="Geographical Distribution by Country",
                     projection="orthographic")
    st.plotly_chart(gdc)

if options=='Temporal Analysis📈':
    yt=data[['Area','Year','Area harvested','Yield','Production']]
    year_Area_harvested = yt.groupby(["Area", "Year"])["Area harvested"].sum().reset_index()
    year_Yield=yt.groupby(["Area", "Year"])["Yield"].sum().reset_index()
    year_Production=yt.groupby(["Area", "Year"])["Production"].sum().reset_index()
    fig_Area = px.line(year_Area_harvested, x="Year", y="Area harvested", color="Area", markers=True, 
              title="Yearly Trends in Area harvested across the Countries")
    st.plotly_chart(fig_Area)
    fig_yield = px.line(year_Yield, x="Year", y="Yield", color="Area", markers=True, 
              title="Yearly Trends in Yield across the Countries")
    st.plotly_chart(fig_yield)
    fig_production = px.line(year_Production, x="Year", y="Production", color="Area", markers=True, 
              title="Yearly Trends in Production(tons) across the Countries")
    st.plotly_chart(fig_production)

if options=='Input-Output Relationships🔧':
    correlation_check = data[['Area harvested','Yield','Production']]
    import seaborn as sns
    st.subheader('Correlation between Area harvested & Yield & Production ')
    # Plot heatmap
    plt.figure(figsize=(6,4))
    sns.heatmap(correlation_check.corr(), annot=True,vmax=1,vmin=-1)
    plt.title("Correlation Heatmap")
    st.pyplot(plt)

if options=='Comparative Analysis📊':
    com_analysis_yield=data[['Item','Yield']]
    total_yield=com_analysis_yield.groupby('Item')['Yield'].sum().reset_index()
    high_yield=total_yield.sort_values(by="Yield", ascending=False)
    low_yield=total_yield.sort_values(by="Yield", ascending=True)
    fig_hyc=px.bar(high_yield.head(10),x='Item',y='Yield',color="Item", title="Highest yield Crops")
    st.plotly_chart(fig_hyc)
    fig_lyc=px.bar(low_yield.head(10),x='Item',y='Yield',color="Item", title="Lowest yield Crops")
    st.plotly_chart(fig_lyc)
    productive_analysis=data[['Area','Production']]
    total_Production=productive_analysis.groupby('Area')['Production'].sum().reset_index()
    high_production=total_Production.sort_values(by="Production", ascending=False)
    fig_hpr=px.bar(high_production.head(10),x='Area',y='Production',color="Area", title="Highly Productive Regions(2019-2023)")
    st.plotly_chart(fig_hpr)
    fig_ghpr=px.scatter_geo(high_production,locations='Area',locationmode='country names',hover_data='Production',size='Production',color='Area',
                   title="Highly Productive Regions(2019-2023)", projection="orthographic")
    st.plotly_chart(fig_ghpr)
    yield_analysis=data[['Area','Item','Yield']]
    yield_analysis_total=yield_analysis.groupby(['Area','Item'])['Yield'].sum().reset_index()
    productive_analysis_yield=yield_analysis_total.sort_values(by="Yield", ascending=False)
    fig_cr = px.bar(productive_analysis_yield.head(10), x="Item", y="Yield", color="Area", title="High yield by Crop & Region")
    st.plotly_chart(fig_cr)
    pd_data=data[['Area', 'Item','Area harvested', 'Production']]
    # Calculate Productivity Ratio
    pd_data['Productivity_Ratio'] = pd_data['Production'] / pd_data['Area harvested']
    pd_data['Productivity_Percentage'] = pd_data['Productivity_Ratio'] * 100
    fig_geo_pr=px.scatter_geo(pd_data,locations='Area',locationmode='country names',hover_data=['Productivity_Percentage','Productivity_Ratio'],color='Area',
                   title="Crops and Regions Based on Productivity Ratio", projection="orthographic")
    st.plotly_chart(fig_geo_pr)

if options=='Outliers detection⚠️':
    st.subheader('Outlier values present in Area harvested & Yield & Production ')
    fig, axes = plt.subplots(1, 3, figsize=(10, 4))

    axes[0].boxplot(data['Area harvested'])
    axes[0].set_title('Outlier Area harvested')

    axes[1].boxplot(data['Yield'])
    axes[1].set_title('Outlier Yield')

    axes[2].boxplot(data['Production'])
    axes[2].set_title('Outlier Production')

    plt.tight_layout()
    st.pyplot(plt)

if options == 'Predict💡':

    Area = st.selectbox('Area',data['Area'].unique())

    area_fil= data[data['Area']==Area]

    item_fill=area_fil['Item'].unique()
    
    Item = st.selectbox("Item",item_fill)
 
    Year = st.selectbox("Year",2024)

    Area_harvested = st.number_input("Area harvested")

    Yield = st.number_input("Yield")

    submitted = st.button('Predict')
    
    if submitted:
        features={'Area': Area, 'Item' : Item , 'Year' : Year, 'Area harvested' : Area_harvested, 'Yield' : Yield}

        pre_freatures=pd.DataFrame([features])


        with open(r'D:\Projects\Guvi_Project3\LabelEncoder_Area.pkl','rb') as enco:
            encoder_area=pickle.load(enco)
        pre_freatures['Area']=encoder_area.transform(pre_freatures['Area'])
        with open(r'D:\Projects\Guvi_Project3\LabelEncoder_Item.pkl','rb') as enco:
            encoder_item=pickle.load(enco)
        pre_freatures['Item']=encoder_item.transform(pre_freatures['Item'])

        with open(r'D:\Projects\Guvi_Project3\RandomForestRegressor.pkl','rb') as model:
            rfc_model=pickle.load(model)
        
        prediction=rfc_model.predict(pre_freatures)

        st.header('🔮Expected production in 2024')

        st.subheader(f"{prediction[0]} Tons")





