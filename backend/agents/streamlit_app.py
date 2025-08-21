# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# import asyncio
# import json
# import os
# import sys
# from io import StringIO
# import tempfile
# from pathlib import Path

# # The agents are in the current directory, so we don't need to add anything to the path

# # Import the orchestrator
# from backend.orchestrator.runner import start as orchestrator_start

# # Configure Streamlit page
# st.set_page_config(
#     page_title="AnalytIQ - Agentic Data Analysis",
#     page_icon="📊",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS for better styling
# st.markdown("""
# <style>
#     .main-header {
#         font-size: 3rem;
#         font-weight: bold;
#         color: #1f77b4;
#         text-align: center;
#         margin-bottom: 2rem;
#     }
#     .section-header {
#         font-size: 1.5rem;
#         font-weight: bold;
#         color: #2c3e50;
#         margin-top: 2rem;
#         margin-bottom: 1rem;
#     }
#     .agent-card {
#         background-color: #f8f9fa;
#         padding: 1rem;
#         border-radius: 10px;
#         border-left: 4px solid #1f77b4;
#         margin: 1rem 0;
#     }
#     .success-message {
#         background-color: #d4edda;
#         color: #155724;
#         padding: 1rem;
#         border-radius: 5px;
#         border: 1px solid #c3e6cb;
#     }
#     .error-message {
#         background-color: #f8d7da;
#         color: #721c24;
#         padding: 1rem;
#         border-radius: 5px;
#         border: 1px solid #f5c6cb;
#     }
# </style>
# """, unsafe_allow_html=True)

# def main():
#     # Check for Gemini API key
#     if not os.getenv("GEMINI_API"):
#         st.error("❌ The GEMINI_API environment variable is not set. Please set it before running the app.")
#         st.info("You can set it by running: `export GEMINI_API=your_api_key` in your terminal or adding it to your .env file.")
#         return
    
#     # Header
#     st.markdown('<h1 class="main-header">📊 AnalytIQ</h1>', unsafe_allow_html=True)
#     st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #7f8c8d;">Agentic Data Analysis System</p>', unsafe_allow_html=True)
    
#     # Sidebar
#     with st.sidebar:
#         st.markdown("## 🚀 Orchestrated Analysis Pipeline")
#         st.markdown("""
#         **Our AI Agent Pipeline:**
#         1. 🔍 **Data Interpreter** - Schema analysis
#         2. 🧹 **Data Wrangler** - Data cleaning
#         3. 📈 **Analyst** - Statistical insights
#         4. 📊 **Visualizer** - Chart generation
#         5. 🎨 **Chart Renderer** - JSON-based visualization
        
#         *All agents work together through an orchestrated pipeline*
#         """)
        
#         st.markdown("---")
#         st.markdown("### 📋 Requirements")
#         st.markdown("""
#         - CSV file upload
#         - Automated orchestrated processing
#         - Downloadable cleaned data
#         - Pre-generated JSON chart visualizations
#         """)

#     # Main content area
#     col1, col2 = st.columns([1, 2])
    
#     with col1:
#         st.markdown('<div class="section-header">📁 Upload Your Data</div>', unsafe_allow_html=True)
        
#         # File uploader
#         uploaded_file = st.file_uploader(
#             "Choose a CSV file",
#             type=['csv'],
#             help="Upload your CSV file to start the analysis"
#         )
        
#         if uploaded_file is not None:
#             # Display file info
#             st.success(f"✅ File uploaded: {uploaded_file.name}")
#             st.info(f"📊 File size: {uploaded_file.size / 1024:.2f} KB")
            
#             # Preview the data
#             try:
#                 df_preview = pd.read_csv(uploaded_file)
#                 st.markdown("### 👀 Data Preview")
#                 st.dataframe(df_preview.head(), use_container_width=True)
#                 st.info(f"Shape: {df_preview.shape[0]} rows × {df_preview.shape[1]} columns")
#             except Exception as e:
#                 st.error(f"Error reading file: {str(e)}")
#                 return

#     with col2:
#         st.markdown('<div class="section-header">🤖 AI Analysis</div>', unsafe_allow_html=True)
        
#         if uploaded_file is not None:
#             # Process button
#             if st.button("🚀 Start AI Analysis", type="primary", use_container_width=True):
#                 process_data(uploaded_file)
#         else:
#             st.info("👆 Please upload a CSV file to begin analysis")

# def process_data(uploaded_file):
#     """Process the uploaded CSV file through the agentic pipeline using orchestrator"""
    
#     # Create a temporary file
#     try:
#         with tempfile.NamedTemporaryFile(mode='w+b', suffix='.csv', delete=False) as tmp_file:
#             tmp_file.write(uploaded_file.getvalue())
#             tmp_file_path = tmp_file.name
        
#         # Verify the CSV file can be read
#         try:
#             test_df = pd.read_csv(tmp_file_path)
#         except Exception as e:
#             st.error(f"❌ Could not read the CSV file: {str(e)}")
#             return
#     except Exception as e:
#         st.error(f"❌ Error creating temporary file: {str(e)}")
#         return
    
#     try:
#         # Progress tracking
#         progress_bar = st.progress(0)
#         status_text = st.empty()
        
#         # Initialize session state for results
#         if 'analysis_results' not in st.session_state:
#             st.session_state.analysis_results = {}
        
#         # Run the orchestrator pipeline
#         status_text.text("🚀 Running AI Analysis Pipeline...")
#         progress_bar.progress(50)
        
#         # Execute the orchestrator
#         results = run_orchestrator(tmp_file_path)
        
#         if not results:
#             st.error("❌ Orchestrator pipeline failed")
#             return
        
#         progress_bar.progress(100)
#         status_text.text("✅ Analysis complete!")
        
#         # Store results in session state
#         st.session_state.analysis_results = results
        
#         # Display results from each agent
#         display_orchestrator_results(results)
        
#         # Final success message
#         st.success("🎉 All agents have completed their analysis successfully!")
        
#         # Download section
#         display_download_section(results['wrangler_output'])
        
#     except Exception as e:
#         st.error(f"❌ Error during processing: {str(e)}")
#         st.exception(e)
#     finally:
#         # Clean up temporary file
#         if os.path.exists(tmp_file_path):
#             os.unlink(tmp_file_path)

# def run_orchestrator(csv_path):
#     """Run the orchestrator pipeline"""
#     try:
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
#         result = loop.run_until_complete(orchestrator_start(csv_path))
#         loop.close()
#         return result
#     except Exception as e:
#         st.error(f"Error running orchestrator: {str(e)}")
#         return None

# def display_orchestrator_results(results):
#     """Display results from the orchestrator pipeline"""
#     if not results:
#         st.error("No results available to display")
#         return
    
#     # Display Story Teller Results
#     st.markdown('<h2 class="section-header">📖 Data Story</h2>', unsafe_allow_html=True)
#     if 'storyteller_output' in results:
#         storyteller_output = results['storyteller_output']
        
#         # Display the narrative in a nice format
#         if isinstance(storyteller_output, dict):
#             if 'narrative' in storyteller_output:
#                 st.markdown(storyteller_output['narrative'])
#             elif 'story' in storyteller_output:
#                 st.markdown(storyteller_output['story'])
#             else:
#                 # If structure is different, display the whole output
#                 for key, value in storyteller_output.items():
#                     if isinstance(value, str) and len(value) > 50:  # Likely narrative text
#                         st.markdown(f"**{key.title()}:**")
#                         st.markdown(value)
#         else:
#             st.markdown(str(storyteller_output))
#     else:
#         st.info("No story narrative available")
    
#     # Display and Execute Visualizer Results
#     st.markdown('<h2 class="section-header">📊 Data Visualizations</h2>', unsafe_allow_html=True)
#     if 'chart_data' in results and results['chart_data']:
#         display_chart_visualizations(results['chart_data'], results.get('visualizer_output', {}))
#     else:
#         st.info("No visualizations available")

# def display_analyst_results(analyst_results):
#     """Display analyst results in a formatted way"""
#     if analyst_results is None:
#         st.error("No analyst results available to display")
#         return
    
#     if isinstance(analyst_results, dict):
#         results = analyst_results
#     else:
#         results = analyst_results.model_dump()
    
#     # Key insights
#     st.markdown("### 🔍 Key Insights")
#     if 'data_summary' in results:
#         st.markdown(results['data_summary'])
    
#     # Trends
#     if 'trends' in results and results['trends']:
#         st.markdown("### 📈 Identified Trends")
#         for i, trend in enumerate(results['trends'], 1):
#             st.markdown(f"{i}. {trend}")
    
#     # Correlations
#     if 'correlation' in results and results['correlation']:
#         st.markdown("### 🔗 Correlations")
#         correlation_df = pd.DataFrame(results['correlation'], columns=['Column 1', 'Column 2', 'Correlation'])
#         st.dataframe(correlation_df, use_container_width=True)
    
#     # Outliers
#     if 'outliers' in results and results['outliers']:
#         st.markdown("### ⚠️ Outliers Detected")
#         for outlier in results['outliers']:
#             st.warning(f"**{outlier['column']}**: {outlier['count']} outliers detected")

# def display_chart_visualizations(chart_data, visualizer_results):
#     """Display visualizations from JSON chart data"""
#     if not chart_data:
#         st.error("No chart data available to display")
#         return
    
#     st.markdown("### 📊 Generated Visualizations")
    
#     # Display chart recommendations if available
#     if visualizer_results and 'chart_recommendations' in visualizer_results:
#         for i, rec in enumerate(visualizer_results['chart_recommendations']):
#             if i < len(chart_data):  # Only show recommendations for available charts
#                 st.markdown(f"#### Chart {i+1}: {rec['title']}")
#                 st.markdown(f"**Type**: {rec['chart_type']}")
#                 st.markdown(f"**Reason**: {rec['reason']}")
#                 st.markdown(f"**Columns**: {', '.join(rec['data_columns'])}")
    
#     # Display each chart from JSON data
#     for i, chart_json in enumerate(chart_data):
#         try:
#             if 'error' in chart_json:
#                 st.error(f"❌ Chart {i+1} failed to generate: {chart_json['error']}")
#                 if 'failed_code' in chart_json:
#                     with st.expander(f"📝 View Failed Code for Chart {i+1}"):
#                         st.code(chart_json['failed_code'], language='python')
#                 continue
            
#             # Create plotly figure from JSON
#             fig = go.Figure(chart_json)
            
#             # Display the chart
#             if not visualizer_results or 'chart_recommendations' not in visualizer_results or i >= len(visualizer_results['chart_recommendations']):
#                 st.markdown(f"#### Visualization {i+1}")
            
#             st.plotly_chart(fig, use_container_width=True)
            
#         except Exception as e:
#             st.error(f"❌ Error displaying chart {i+1}: {str(e)}")
#             # Show raw JSON data for debugging if needed
#             with st.expander(f"🔍 Debug Chart {i+1} JSON Data"):
#                 st.json(chart_json)

# def display_download_section(wrangler_results):
#     """Display download options for cleaned data"""
#     st.markdown("### 💾 Download Results")
    
#     if 'cleaned_csv_path' in wrangler_results:
#         try:
#             # Read the cleaned CSV
#             cleaned_df = pd.read_csv(wrangler_results['cleaned_csv_path'])
            
#             # Convert to CSV string
#             csv_string = cleaned_df.to_csv(index=False)
            
#             # Download button
#             st.download_button(
#                 label="📥 Download Cleaned CSV",
#                 data=csv_string,
#                 file_name="cleaned_data.csv",
#                 mime="text/csv",
#                 use_container_width=True
#             )
            
#             # Show preview of cleaned data
#             with st.expander("👀 Preview Cleaned Data"):
#                 st.dataframe(cleaned_df.head(10), use_container_width=True)
#                 st.info(f"Cleaned dataset shape: {cleaned_df.shape[0]} rows × {cleaned_df.shape[1]} columns")
                
#         except Exception as e:
#             st.error(f"Error preparing download: {str(e)}")

# if __name__ == "__main__":
#     main()
