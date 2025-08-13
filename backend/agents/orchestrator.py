from data_interpreter import DataInterpreter
from wrangler_agent import DataWranglerAgent
from visualizer import Visualizer
from analyst import Analyst
from qa import QAAgent
import pandas as pd
import json

async def start(csv : str):
    interpreter = DataInterpreter()
    
    interpreter_output = await interpreter.analyze(csv)
    interpreter_dict = interpreter_output.model_dump()
    print("interpreter_output:", interpreter_output)
    wrangler = DataWranglerAgent()
    wrangler_output = await wrangler.wrangle(csv)
    print("wrangler_output:", wrangler_output)
    cleaned_csv_path = wrangler_output['cleaned_csv_path']
    
    
    analyst = Analyst()
    analyst_res = await analyst.run_analysis(cleaned_csv_path , interpreter_dict, wrangler_output['wrangling_report'])
    
    analyst_output = analyst_res.model_dump()
    print("analyst_output:", analyst_output)
    visualizer = Visualizer()
    visualization_output = await visualizer.create_visualization(cleaned_csv_path , analyst_output)
    
    visualizer_res =  visualization_output.model_dump()
    
    print("visualizer_res:", visualizer_res)
    
    df = pd.read_csv(cleaned_csv_path)
    
    df_sample = df.head(5).to_dict()
    
    qa_agent = QAAgent()
    qa_response = await qa_agent.run_qa_review(interpreter_output=interpreter_dict,
                           wrangler_output = wrangler_output['wrangling_report'],
                           analyst_output=analyst_output,
                           visualizer_output=visualizer_res,
                           cleaned_csv_sample=df_sample
                        )
    
    qa_output = qa_response.model_dump()
    print("QA Report:", json.dumps(qa_output, indent=2))
    return {
        "interpreter_output": interpreter_output,
        "wrangler_output": wrangler_output,
        "analyst_output": analyst_output,
        "visualizer_output": visualizer_res
    }


if __name__ == "__main__":
    import asyncio
    import sys
    csv_path = sys.argv[1]
    
    asyncio.run(start(csv_path))