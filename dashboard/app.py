import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Set Streamlit page config
st.set_page_config(page_title='Teacher Distribution Dashboard', layout='wide')

st.title('📊 Teacher Distribution in Community Schools (2074 BS)')

# Load and preprocess data
@st.cache_data
def load_data():
    df = pd.read_csv('../data/data.csv')
    df.rename(columns={
        'Province No': 'Province',
        'Approved Teacher Posts Primary': 'Approved_Primary',
        'Approved Teacher Posts Lower Secondary': 'Approved_LowerSecondary',
        'Approved Teacher Posts Secondary': 'Approved_Secondary',
        'Rahat Teacher Posts Primary': 'Rahat_Primary',
        'Rahat Teacher Posts Lower Secondary': 'Rahat_LowerSecondary',
        'Rahat Teacher Posts Secondary': 'Rahat_Secondary'
    }, inplace=True)

    # Handle missing values
    df['Approved_Primary'].fillna(0, inplace=True)

    # Remove rows with 'ALL' totals
    df = df[df['District'] != 'ALL']
    df = df[df['Province'] != 'ALL']

    # Compute total approved & Rahat teachers
    df['Total_Approved_Teachers'] = (
        df['Approved_Primary'] + df['Approved_LowerSecondary'] + df['Approved_Secondary']
    )
    df['Total_Rahat_Teachers'] = (
        df['Rahat_Primary'] + df['Rahat_LowerSecondary'] + df['Rahat_Secondary']
    )

    # Clustering based on total approved teachers
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df['Cluster'] = kmeans.fit_predict(df[['Total_Approved_Teachers']])

    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter")
provinces = st.sidebar.multiselect("Select Province(s):", options=df['Province'].unique(), default=df['Province'].unique())
filtered_df = df[df['Province'].isin(provinces)]

# Summary metrics
st.subheader('Summary')
st.write(f"Total Districts Selected: {filtered_df['District'].nunique()}")
st.write(f"Total Approved Teachers: {filtered_df['Total_Approved_Teachers'].sum():,.0f}")
st.write(f"Total Rahat Teachers: {filtered_df['Total_Rahat_Teachers'].sum():,.0f}")

avg = filtered_df['Total_Approved_Teachers'].mean()
max_value = filtered_df['Total_Approved_Teachers'].max()
min_value = filtered_df['Total_Approved_Teachers'].min()

st.write(f"Average Approved Teachers per District: {avg:.0f}")
st.write(f"Max Approved Teachers in a District: {max_value}")
st.write(f"Min Approved Teachers in a District: {min_value}")

# Plot 1: Distribution
st.subheader('Distribution of Total Approved Teachers by District')
fig1, ax1 = plt.subplots(figsize=(8,4))
sns.histplot(filtered_df['Total_Approved_Teachers'], bins=20, kde=True, color='skyblue', ax=ax1)
st.pyplot(fig1)

# Plot 2: Top 10 districts
st.subheader('Top 10 Districts by Number of Approved Teachers')
top10 = filtered_df.sort_values('Total_Approved_Teachers', ascending=False).head(10)
fig2, ax2 = plt.subplots(figsize=(8,4))
sns.barplot(y='District', x='Total_Approved_Teachers', data=top10, palette='Blues_d', ax=ax2)
st.pyplot(fig2)

# Plot 3: Bottom 10 districts
st.subheader('Bottom 10 Districts by Number of Approved Teachers')
bottom10 = filtered_df.sort_values('Total_Approved_Teachers').head(10)
fig3, ax3 = plt.subplots(figsize=(8,4))
sns.barplot(y='District', x='Total_Approved_Teachers', data=bottom10, palette='Reds_d', ax=ax3)
st.pyplot(fig3)

# Plot 4: Boxplot
st.subheader('Boxplot of Total Approved Teachers')
fig4, ax4 = plt.subplots(figsize=(8,2))
sns.boxplot(x='Total_Approved_Teachers', data=filtered_df, color='lightgreen', ax=ax4)
st.pyplot(fig4)

# Plot 5: Pie chart of total approved teachers by province
st.subheader('Share of Approved Teachers by Province')
province_totals = filtered_df.groupby('Province')['Total_Approved_Teachers'].sum()
fig5, ax5 = plt.subplots(figsize=(6,6))
ax5.pie(province_totals, labels=province_totals.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
ax5.axis('equal')
st.pyplot(fig5)

# Plot 6: Compare total Rahat vs Approved teachers per district
st.subheader('Approved vs. Rahat Teachers by District')
long_df = filtered_df.melt(
    id_vars=['District'],
    value_vars=['Total_Approved_Teachers', 'Total_Rahat_Teachers'],
    var_name='Teacher_Type',
    value_name='Count'
)
fig6, ax6 = plt.subplots(figsize=(10,6))
sns.barplot(y='District', x='Count', hue='Teacher_Type', data=long_df, ax=ax6)
ax6.legend(title='Teacher Type')
st.pyplot(fig6)

# Plot 7: Clustering scatter plot
st.subheader('Clusters of Districts by Total Approved Teachers')
fig7, ax7 = plt.subplots(figsize=(8,6))
sns.scatterplot(
    x='Total_Approved_Teachers',
    y='Total_Rahat_Teachers',
    hue='Cluster',
    data=filtered_df,
    palette='Set2',
    s=100
)
ax7.set_xlabel('Total Approved Teachers')
ax7.set_ylabel('Total Rahat Teachers')
st.pyplot(fig7)

# Show raw data if needed
with st.expander("Show Raw Data"):
    st.dataframe(filtered_df)
