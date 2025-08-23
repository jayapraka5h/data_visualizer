import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title='CSV/Excel Data Visualizer', layout='wide')

st.title('📊 Professional Data Visualizer')
st.write("Upload your CSV or Excel file and visualize your data interactively.")

# Upload CSV or Excel file
uploaded_file = st.file_uploader("Upload File", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Read file depending on type
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader('Data Preview')
    st.dataframe(df.head())

    # Select chart type
    chart_type = st.sidebar.selectbox('Select Chart Type', 
                                      ['Bar', 'Line', 'Pie', 'Scatter', 'Area', 'Histogram', 'Box', 'Bubble'])

    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    all_columns = df.columns.tolist()

    x_axis = None
    y_axis = None
    size_col = None

    if chart_type in ['Bar', 'Line', 'Area']:
        x_axis = st.sidebar.selectbox('X-axis', all_columns)
        y_axis = st.sidebar.selectbox('Y-axis', numeric_columns)

    elif chart_type == 'Pie':
        x_axis = st.sidebar.selectbox('Category Column', all_columns)
        y_axis = st.sidebar.selectbox('Value Column', numeric_columns)

    elif chart_type == 'Scatter':
        x_axis = st.sidebar.selectbox('X-axis', numeric_columns)
        y_axis = st.sidebar.selectbox('Y-axis', numeric_columns)

    elif chart_type == 'Histogram':
        x_axis = st.sidebar.selectbox('Select Column', numeric_columns)

    elif chart_type == 'Box':
        y_axis = st.sidebar.selectbox('Select Column', numeric_columns)
        x_axis = st.sidebar.selectbox('Optional Categorical Column', [None] + all_columns)

    elif chart_type == 'Bubble':
        x_axis = st.sidebar.selectbox('X-axis', numeric_columns)
        y_axis = st.sidebar.selectbox('Y-axis', numeric_columns)
        size_col = st.sidebar.selectbox('Size Column', numeric_columns)

    # Plotting
    fig, ax = plt.subplots(figsize=(12, 6))

    if chart_type == 'Bar':
        sns.barplot(data=df, x=x_axis, y=y_axis, ax=ax)
    elif chart_type == 'Line':
        sns.lineplot(data=df, x=x_axis, y=y_axis, ax=ax)
    elif chart_type == 'Area':
        ax.fill_between(df[x_axis], df[y_axis], color='skyblue', alpha=0.4)
        ax.plot(df[x_axis], df[y_axis], color='Slateblue', alpha=0.6)
    elif chart_type == 'Pie':
        pie_data = df.groupby(x_axis)[y_axis].sum()
        ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
    elif chart_type == 'Scatter':
        sns.scatterplot(data=df, x=x_axis, y=y_axis, ax=ax)
    elif chart_type == 'Histogram':
        sns.histplot(df[x_axis], kde=True, ax=ax)
    elif chart_type == 'Box':
        if x_axis:
            sns.boxplot(data=df, x=x_axis, y=y_axis, ax=ax)
        else:
            sns.boxplot(y=df[y_axis], ax=ax)
    elif chart_type == 'Bubble':
        sns.scatterplot(data=df, x=x_axis, y=y_axis, size=size_col, ax=ax, sizes=(50, 500), alpha=0.6)

    st.subheader(f'{chart_type} Chart')
    st.pyplot(fig)