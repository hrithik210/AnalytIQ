import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import asyncio
import json
import os
import sys
from io import StringIO
import tempfile
from pathlib import Path

# The agents are in the current directory, so we don't need to add anything to the path

# Import your agents
from data_interpreter import DataInterpreter
from wrangler_agent import DataWranglerAgent
from analyst import Analyst
from visualizer import Visualizer

# Configure Streamlit page
st.set_page_config(
    page_title="AnalytIQ - Agentic Data Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .agent-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Check for Gemini API key
    if not os.getenv("GEMINI_API"):
        st.error("❌ The GEMINI_API environment variable is not set. Please set it before running the app.")
        st.info("You can set it by running: `export GEMINI_API=your_api_key` in your terminal or adding it to your .env file.")
        return
    
    # Header
    st.markdown('<h1 class="main-header">📊 AnalytIQ</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #7f8c8d;">Agentic Data Analysis System</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🚀 Analysis Pipeline")
        st.markdown("""
        **Our AI Agents:**
        1. 🔍 **Data Interpreter** - Schema analysis
        2. 🧹 **Data Wrangler** - Data cleaning
        3. 📈 **Analyst** - Statistical insights
        4. 📊 **Visualizer** - Chart generation
        """)
        
        st.markdown("---")
        st.markdown("### 📋 Requirements")
        st.markdown("""
        - CSV file upload
        - Automated processing
        - Downloadable cleaned data
        - Interactive visualizations
        """)

    # Main content area
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="section-header">📁 Upload Your Data</div>', unsafe_allow_html=True)
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=['csv'],
            help="Upload your CSV file to start the analysis"
        )
        
        if uploaded_file is not None:
            # Display file info
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            st.info(f"📊 File size: {uploaded_file.size / 1024:.2f} KB")
            
            # Preview the data
            try:
                df_preview = pd.read_csv(uploaded_file)
                st.markdown("### 👀 Data Preview")
                st.dataframe(df_preview.head(), use_container_width=True)
                st.info(f"Shape: {df_preview.shape[0]} rows × {df_preview.shape[1]} columns")
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
                return

    with col2:
        st.markdown('<div class="section-header">🤖 AI Analysis</div>', unsafe_allow_html=True)
        
        if uploaded_file is not None:
            # Process button
            if st.button("🚀 Start AI Analysis", type="primary", use_container_width=True):
                process_data(uploaded_file)
        else:
            st.info("👆 Please upload a CSV file to begin analysis")

def process_data(uploaded_file):
    """Process the uploaded CSV file through the agentic pipeline"""
    
    # Create a temporary file
    try:
        with tempfile.NamedTemporaryFile(mode='w+b', suffix='.csv', delete=False) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        # Verify the CSV file can be read
        try:
            test_df = pd.read_csv(tmp_file_path)
        except Exception as e:
            st.error(f"❌ Could not read the CSV file: {str(e)}")
            return
    except Exception as e:
        st.error(f"❌ Error creating temporary file: {str(e)}")
        return
    
    try:
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Initialize session state for results
        if 'analysis_results' not in st.session_state:
            st.session_state.analysis_results = {}
        
        # Step 1: Data Interpretation
        status_text.text("🔍 Step 1/4: Interpreting data schema...")
        progress_bar.progress(25)
        
        with st.expander("🔍 Data Interpreter Results", expanded=False):
            interpreter_results = run_async_agent(DataInterpreter(), 'analyze', tmp_file_path)
            if interpreter_results:
                st.json(interpreter_results.model_dump())
                st.session_state.analysis_results['interpreter'] = interpreter_results
            else:
                st.error("❌ Data interpretation failed")
                return
        
        # Step 2: Data Wrangling
        status_text.text("🧹 Step 2/4: Cleaning and processing data...")
        progress_bar.progress(50)
        
        with st.expander("🧹 Data Wrangler Results", expanded=False):
            wrangler_results = run_async_agent(DataWranglerAgent(), 'wrangle', tmp_file_path)
            if wrangler_results:
                st.json(wrangler_results)
                st.session_state.analysis_results['wrangler'] = wrangler_results
                
                # Show cleaning summary
                st.markdown("### 📋 Cleaning Summary")
                original_shape = wrangler_results.get('original_shape', [0, 0])
                final_shape = wrangler_results.get('final_shape', [0, 0])
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Original Rows", original_shape[0])
                with col2:
                    st.metric("Final Rows", final_shape[0], delta=final_shape[0] - original_shape[0])
                with col3:
                    st.metric("Columns", final_shape[1])
            else:
                st.error("❌ Data wrangling failed")
                return
        
        # Step 3: Analysis
        status_text.text("📈 Step 3/4: Performing statistical analysis...")
        progress_bar.progress(75)
        
        with st.expander("📈 Analyst Results", expanded=True):
            analyst_results = run_async_agent(Analyst(), 'run_analysis', tmp_file_path)
            if analyst_results:
                st.session_state.analysis_results['analyst'] = analyst_results
                display_analyst_results(analyst_results)
            else:
                st.error("❌ Analysis failed")
                return
        
        # Step 4: Visualization
        status_text.text("📊 Step 4/4: Generating visualizations...")
        progress_bar.progress(100)
        
        with st.expander("📊 Visualizer Results", expanded=True):
            visualizer_results = run_async_agent(Visualizer(), 'create_visualization', tmp_file_path)
            if visualizer_results:
                st.session_state.analysis_results['visualizer'] = visualizer_results
                display_visualizations(visualizer_results, wrangler_results['cleaned_csv_path'])
            else:
                st.error("❌ Visualization generation failed")
                return
        
        # Final success message
        status_text.text("✅ Analysis complete!")
        st.success("🎉 All agents have completed their analysis successfully!")
        
        # Download section
        display_download_section(wrangler_results)
        
    except Exception as e:
        st.error(f"❌ Error during processing: {str(e)}")
        st.exception(e)
    finally:
        # Clean up temporary file
        if os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)

def run_async_agent(agent, method_name, *args):
    """Run an async agent method"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        method = getattr(agent, method_name)
        result = loop.run_until_complete(method(*args))
        loop.close()
        return result
    except Exception as e:
        st.error(f"Error running {agent.__class__.__name__}: {str(e)}")
        return None

def display_analyst_results(analyst_results):
    """Display analyst results in a formatted way"""
    if analyst_results is None:
        st.error("No analyst results available to display")
        return
    
    if isinstance(analyst_results, dict):
        results = analyst_results
    else:
        results = analyst_results.model_dump()
    
    # Key insights
    st.markdown("### 🔍 Key Insights")
    if 'data_summary' in results:
        st.markdown(results['data_summary'])
    
    # Trends
    if 'trends' in results and results['trends']:
        st.markdown("### 📈 Identified Trends")
        for i, trend in enumerate(results['trends'], 1):
            st.markdown(f"{i}. {trend}")
    
    # Correlations
    if 'correlation' in results and results['correlation']:
        st.markdown("### 🔗 Correlations")
        correlation_df = pd.DataFrame(results['correlation'], columns=['Column 1', 'Column 2', 'Correlation'])
        st.dataframe(correlation_df, use_container_width=True)
    
    # Outliers
    if 'outliers' in results and results['outliers']:
        st.markdown("### ⚠️ Outliers Detected")
        for outlier in results['outliers']:
            st.warning(f"**{outlier['column']}**: {outlier['count']} outliers detected")

def display_visualizations(visualizer_results, cleaned_csv_path):
    """Display generated visualizations"""
    if visualizer_results is None:
        st.error("No visualization results available to display")
        return
        
    if isinstance(visualizer_results, dict):
        results = visualizer_results
    else:
        results = visualizer_results.model_dump()
    
    # Load the cleaned data
    try:
        df = pd.read_csv(cleaned_csv_path)
    except Exception as e:
        st.error(f"Could not load cleaned data: {str(e)}")
        return
    
    st.markdown("### 📊 Generated Visualizations")
    
    # Display chart recommendations
    if 'chart_recommendations' in results:
        for i, rec in enumerate(results['chart_recommendations']):
            st.markdown(f"#### Chart {i+1}: {rec['title']}")
            st.markdown(f"**Type**: {rec['chart_type']}")
            st.markdown(f"**Reason**: {rec['reason']}")
            st.markdown(f"**Columns**: {', '.join(rec['data_columns'])}")
    
    # Execute and display the plotly code
    if 'plotly_code_snippets' in results:
        for i, code in enumerate(results['plotly_code_snippets']):
            try:
                st.markdown(f"#### Visualization {i+1}")
                
                # Create a safe execution environment
                exec_globals = {
                    'px': px,
                    'go': go,
                    'df': df,
                    'pd': pd
                }
                
                # Execute the code
                exec(code, exec_globals)
                
                # Get the figure (assuming it's stored in 'fig')
                if 'fig' in exec_globals:
                    st.plotly_chart(exec_globals['fig'], use_container_width=True)
                
                # Show the code in a collapsible section
                if st.button(f"📝 View Code for Chart {i+1}", key=f"view_code_{i}"):
                    st.code(code, language='python')
                    
            except Exception as e:
                st.error(f"Error executing visualization code {i+1}: {str(e)}")
                if st.button(f"📝 View Failed Code for Chart {i+1}", key=f"failed_code_{i}"):
                    st.code(code, language='python')

def display_download_section(wrangler_results):
    """Display download options for cleaned data"""
    st.markdown("### 💾 Download Results")
    
    if 'cleaned_csv_path' in wrangler_results:
        try:
            # Read the cleaned CSV
            cleaned_df = pd.read_csv(wrangler_results['cleaned_csv_path'])
            
            # Convert to CSV string
            csv_string = cleaned_df.to_csv(index=False)
            
            # Download button
            st.download_button(
                label="📥 Download Cleaned CSV",
                data=csv_string,
                file_name="cleaned_data.csv",
                mime="text/csv",
                use_container_width=True
            )
            
            # Show preview of cleaned data
            with st.expander("👀 Preview Cleaned Data"):
                st.dataframe(cleaned_df.head(10), use_container_width=True)
                st.info(f"Cleaned dataset shape: {cleaned_df.shape[0]} rows × {cleaned_df.shape[1]} columns")
                
        except Exception as e:
            st.error(f"Error preparing download: {str(e)}")

if __name__ == "__main__":
    main()
