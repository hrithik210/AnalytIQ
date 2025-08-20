from ..agents.data_interpreter import DataInterpreter
from ..agents.wrangler_agent import DataWranglerAgent
from ..agents.visualizer import Visualizer
from ..agents.analyst import Analyst
from ..agents.qa import QAAgent
from ..agents.storyteller_agent import StoryTeller
import pandas as pd
import json
import traceback
import uuid


async def start(csv : str ):
    report_id = f"cli-{uuid.uuid4()}" # Generate for CLI/testing
    
    #interpreter 
    interpreter = DataInterpreter()
    interpreter_output = await interpreter.analyze(csv)
    interpreter_dict = interpreter_output.model_dump()
    
    
    #wrangler 
    wrangler = DataWranglerAgent()
    wrangler_output = await wrangler.wrangle(csv, interpreter_dict)
    print("wrangler_output:", wrangler_output)
    cleaned_csv_path = wrangler_output['cleaned_csv_path']
        
    
    df = pd.read_csv(cleaned_csv_path)
    
    
    df_sample = df.head(5).to_dict()
    

    
    #analyst
    analyst = Analyst()
    analyst_res = await analyst.run_analysis(cleaned_csv_path , interpreter_dict, wrangler_output['wrangling_report'])
    
    analyst_output = analyst_res.model_dump()
    print("analyst_output:", analyst_output)

    
    #visualizer
    visualizer = Visualizer()
    visualization_output = await visualizer.create_visualization(cleaned_csv_path , analyst_output)
    
    visualizer_res =  visualization_output.model_dump()
    
    plotly_code_snippets = visualizer_res.get("plotly_code_snippets")
    
    print("visualizer_res:", visualizer_res)
    print(f"visualizer code : {plotly_code_snippets}")
    
    print("Executing Plotly code snippets and generating JSON...")
    
    chart_data_objects = [] 
    
    for i, code_snippet in enumerate(plotly_code_snippets):
        try:
            print(f"executing snippet {i+1}")
            print(f"Code snippet: {code_snippet}")
            local_scope = {
                "pd": pd,
                "px": __import__('plotly.express', fromlist=['']), # Import plotly.express as px
                "go": __import__('plotly.graph_objects', fromlist=['']), # Import plotly.graph_objects as go (in case used)
                "pio": __import__('plotly.io', fromlist=['']), # Import plotly.io as pio
                "df": df,
                "json": json
            }
            
            exec(code_snippet, globals(), local_scope)
            fig = local_scope.get('fig')
            pio = local_scope.get('pio')
            if fig is not None:
                chart_json_dict = json.loads(pio.to_json(fig))
                chart_data_objects.append(chart_json_dict)
                print(f"    Success: Chart {i+1} JSON generated.")
            else:
                error_msg = f"Snippet {i+1} did not create a 'fig' object."
                print(f"    Warning: {error_msg}")
                chart_data_objects.append({"error": error_msg})
    
        except Exception as e:
            # Handle errors in code execution
            error_details = f"Error executing snippet {i+1}: {str(e)}"
            tb_details = traceback.format_exc()
            print(f"    Error: {error_details}")
            print(f"    Code snippet that failed: {code_snippet}")
            print(f"    DataFrame columns available: {list(df.columns)}")
            # Optionally print traceback for debugging (remove in production)
            print(f"    Traceback: {tb_details}")
            chart_data_objects.append({
                "error": error_details,
                "failed_code": code_snippet,
                "available_columns": list(df.columns)
                # "traceback": tb_details # Include traceback if needed for debugging
            })
    
    qa_agent = QAAgent()
    qa_response = await qa_agent.run_qa_review(interpreter_output=interpreter_dict,
                           wrangler_output = wrangler_output['wrangling_report'],
                           analyst_output=analyst_output,
                           visualizer_output=visualizer_res,
                           cleaned_csv_sample=df_sample
                        )
    
    qa_output = qa_response.model_dump()
    print("QA Report:", json.dumps(qa_output, indent=2))
    
    storyteller = StoryTeller()
    storyteller_res =  await storyteller.createNarrative(
        interpreter_output=interpreter_dict,
        analyst_output=analyst_output,
        visualizer_output=visualizer_res,
        qa_report=qa_output
    )
    
    storyteller_output = storyteller_res.model_dump()
    print(f"storyteller_output : {storyteller_output}")
    
    return {
        "interpreter_output": interpreter_output,
        "wrangler_output": wrangler_output,
        "analyst_output": analyst_output,
        "visualizer_output": visualizer_res,
        "qa_output" : qa_output,
        "storyteller_output" : storyteller_output,
        "chart_data": chart_data_objects
    }


if __name__ == "__main__":
    import asyncio
    import sys
    csv_path = sys.argv[1]
    
    asyncio.run(start(csv_path))