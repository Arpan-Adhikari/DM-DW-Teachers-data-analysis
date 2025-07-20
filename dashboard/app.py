import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set Streamlit page config
st.set_page_config(page_title='Teacher Distribution Dashboard', layout='wide')

st.title('📊 Teacher Distribution in Community Schools (2074 BS)')

# Short description
st.markdown("""
This dashboard explores the distribution of approved and Rahat teacher positions across community schools in Nepal (2074 BS). 
Use the filters on the left to explore data by province.
""")

# Load data
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
    df['Approved_Primary'].fillna(0, inplace=True)
    df['Total_Approved_Teachers'] = (
        df['Approved_Primary'] + df['Approved_LowerSecondary'] + df['Approved_Secondary']
    )
    df['Total_Rahat_Teachers'] = (
        df['Rahat_Primary'] + df['Rahat_LowerSecondary'] + df['Rahat_Secondary']
    )
    # Remove rows where Province is "ALL" if such exists
    df = df[df['Province'] != 'ALL']
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter")
provinces = st.sidebar.multiselect("Select Province(s):", options=df['Province'].unique(), default=df['Province'].unique())
filtered_df = df[df['Province'].isin(provinces)]

# Show summary metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Districts Selected", filtered_df['District'].nunique())
col2.metric("Total Approved Teachers", f"{filtered_df['Total_Approved_Teachers'].sum():,.0f}")
col3.metric("Total Rahat Teachers", f"{filtered_df['Total_Rahat_Teachers'].sum():,.0f}")

# Extra stats
avg = filtered_df['Total_Approved_Teachers'].mean()
max_value = filtered_df['Total_Approved_Teachers'].max()
min_value = filtered_df['Total_Approved_Teachers'].min()

col4, col5, col6 = st.columns(3)
col4.metric("Avg Approved Teachers per District", f"{avg:.0f}")
col5.metric("Max Approved Teachers in a District", f"{max_value}")
col6.metric("Min Approved Teachers in a District", f"{min_value}")

# Plot 1: Distribution
st.subheader('Distribution of Total Approved Teachers by District')
fig1, ax1 = plt.subplots(figsize=(8,4))
sns.histplot(filtered_df['Total_Approved_Teachers'], bins=20, kde=True, color='skyblue', ax=ax1)
ax1.set_title('Distribution of Total Approved Teachers', fontsize=14)
ax1.set_xlabel('Number of Approved Teachers', fontsize=12)
ax1.set_ylabel('Number of Districts', fontsize=12)
st.pyplot(fig1, use_container_width=True)

# Plot 2: Top 10 districts
st.subheader('Top 10 Districts by Number of Approved Teachers')
top10 = filtered_df.sort_values('Total_Approved_Teachers', ascending=False).head(10)
fig2, ax2 = plt.subplots(figsize=(8,4))
sns.barplot(y='District', x='Total_Approved_Teachers', data=top10, palette='Blues_d', ax=ax2)
ax2.set_title('Top 10 Districts', fontsize=14)
ax2.set_xlabel('Approved Teachers', fontsize=12)
ax2.set_ylabel('District', fontsize=12)
st.pyplot(fig2, use_container_width=True)

# Plot 3: Bottom 10 districts
st.subheader('Bottom 10 Districts by Number of Approved Teachers')
bottom10 = filtered_df.sort_values('Total_Approved_Teachers', ascending=True).head(10)
fig3, ax3 = plt.subplots(figsize=(8,4))
sns.barplot(y='District', x='Total_Approved_Teachers', data=bottom10, palette='Reds_d', ax=ax3)
ax3.set_title('Bottom 10 Districts', fontsize=14)
ax3.set_xlabel('Approved Teachers', fontsize=12)
ax3.set_ylabel('District', fontsize=12)
st.pyplot(fig3, use_container_width=True)

# Plot 4: Boxplot
st.subheader('Boxplot of Total Approved Teachers')
fig4, ax4 = plt.subplots(figsize=(8,2))
sns.boxplot(x='Total_Approved_Teachers', data=filtered_df, color='lightgreen', ax=ax4)
ax4.set_title('Boxplot of Total Approved Teachers', fontsize=14)
st.pyplot(fig4, use_container_width=True)

# Pie chart: Approved teachers by province
st.subheader('Share of Approved Teachers by Province')
province_totals = filtered_df.groupby('Province')['Total_Approved_Teachers'].sum()
fig5, ax5 = plt.subplots(figsize=(6,6))
ax5.pie(province_totals, labels=province_totals.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
ax5.set_title('Approved Teachers by Province', fontsize=14)
ax5.axis('equal')
st.pyplot(fig5, use_container_width=True)

# Compare Approved vs Rahat Teachers by District
st.subheader('Approved vs. Rahat Teachers by District')
long_df = filtered_df.melt(
    id_vars=['District'],
    value_vars=['Total_Approved_Teachers', 'Total_Rahat_Teachers'],
    var_name='Teacher_Type',
    value_name='Count'
)
# Clean up labels
long_df['Teacher_Type'] = long_df['Teacher_Type'].replace({
    'Total_Approved_Teachers': 'Approved',
    'Total_Rahat_Teachers': 'Rahat'
})
# Sort by total approved teachers
sorted_districts = filtered_df.sort_values('Total_Approved_Teachers', ascending=False)['District']
long_df['District'] = pd.Categorical(long_df['District'], categories=sorted_districts, ordered=True)
long_df = long_df.sort_values('District')

fig6, ax6 = plt.subplots(figsize=(10,6))
sns.barplot(y='District', x='Count', hue='Teacher_Type', data=long_df, ax=ax6)
ax6.set_title('Approved vs. Rahat Teachers', fontsize=14)
ax6.set_xlabel('Number of Teachers', fontsize=12)
ax6.set_ylabel('District', fontsize=12)
ax6.legend(title='Teacher Type')
st.pyplot(fig6, use_container_width=True)

# Show raw data if needed
with st.expander("Show Raw Data"):
    st.dataframe(filtered_df)
