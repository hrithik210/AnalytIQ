from data_interpreter import DataInterpreter
from wrangler_agent import DataWranglerAgent
from visualizer import Visualizer
from analyst import Analyst


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