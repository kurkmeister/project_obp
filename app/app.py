import streamlit as st
import pandas as pd
import os
from sidebar import global_sidebar
try:
    from solver import dash_solver
except ImportError:
    pass

st.title("Shift Scheduling Decision Support System")

global_sidebar()

# Function to load data from file
def load_data_from_file(filepath):
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        st.error(f"File not found: {filepath}")
        return pd.DataFrame()  # Return empty DataFrame
    except pd.errors.ParserError as e:
        st.error(f"Error parsing CSV: {filepath}. Error: {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"An unexpected error occurred while loading {filepath}: {e}")
        return pd.DataFrame()

# File Uploaders
st.subheader("Upload Input Data")
uploaded_shifts = st.file_uploader("Upload Shifts CSV", type=["csv"])
uploaded_tasks = st.file_uploader("Upload Tasks CSV", type=["csv"])

# Load from file buttons
st.subheader("Load Data from Files")
col_load1, col_load2 = st.columns(2)

shifts_filepath = os.path.join(os.path.dirname(__file__), "data/shifts.csv")
tasks_filepath = os.path.join(os.path.dirname(__file__), "data/tasks.csv")

with col_load1:
    if st.button("Load Shifts from File"):
        shifts_df = load_data_from_file(shifts_filepath)
        if not shifts_df.empty: #Only show success if data was loaded
            st.success(f"Shifts loaded from: {shifts_filepath}")
        st.session_state['shifts_df'] = shifts_df # Store the shifts in the session state

with col_load2:
    if st.button("Load Tasks from File"):
        tasks_df = load_data_from_file(tasks_filepath)
        if not tasks_df.empty: #Only show success if data was loaded
            st.success(f"Tasks loaded from: {tasks_filepath}")
        st.session_state['tasks_df'] = tasks_df # Store the tasks in the session state

# Use session state to persist the dataframes
if 'shifts_df' in st.session_state:
    shifts_df = st.session_state['shifts_df']
else:
    shifts_df = pd.DataFrame()

if 'tasks_df' in st.session_state:
    tasks_df = st.session_state['tasks_df']
else:
    tasks_df = pd.DataFrame()

if uploaded_shifts is not None:
    try:
        shifts_df = pd.read_csv(uploaded_shifts)
        st.session_state['shifts_df'] = shifts_df
    except pd.errors.ParserError as e:
        st.error(f"Error parsing shifts CSV: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

if uploaded_tasks is not None:
    try:
        tasks_df = pd.read_csv(uploaded_tasks)
        st.session_state['tasks_df'] = tasks_df
    except pd.errors.ParserError as e:
        st.error(f"Error parsing tasks CSV: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")


# Data Display (modified to show columns under each other)
st.subheader("Uploaded Data")
st.subheader("Shifts:")

if not shifts_df.empty:
    st.dataframe(shifts_df)
else:
    st.write("No shifts data available.")

st.subheader("Tasks:")
if not tasks_df.empty:
    st.dataframe(tasks_df)
else:
    st.write("No tasks data available.")

# Solve Button (same as before)
st.subheader("Solve")
if st.button("Generate Schedule"):
    if shifts_df.empty or tasks_df.empty:
        st.warning("Please upload or load both shifts and tasks data.")
    else:
        with st.spinner("Solving..."):
            try:
                results_df = dash_solver(shifts_df, tasks_df)
                st.session_state['results'] = results_df
            except Exception as e:
                st.error(f"An error occurred during solving: {e}")
                st.session_state['results'] = pd.read_csv('data/tasks_output.csv')
            

# Result Display
st.subheader("Schedule Results")

if 'results' in st.session_state:
    results_df = st.session_state['results']

    st.write(results_df)

else:
    st.write("No schedule generated yet. Click 'Generate Schedule'.")