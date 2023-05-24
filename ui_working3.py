import gradio as gr
import pandas as pd

# Example DataFrame
data = {
    'Name': ['John', 'Alice', 'Bob'],
    'Age': [25, 30, 35],
    'City': ['New York', 'London', 'Paris']
}
df = pd.DataFrame(data)


def load_env_variables():
    # Declare Global Variables
    global class_name
    global weaviate_client

    # Loading API Key
    load_dotenv()
    
    print('\n##########################################################')
    print('>>>>>>>>>>>>>  Displaying Environment Variables <<<<<<<<<<')
    print('##########################################################')
    print('Loaded OpenAI API Key     -> '+os.getenv("OPENAI_API_KEY"))
    print('Loaded Weaviate URL       -> '+os.getenv("WEAVIATE_URL"))
    print('Loaded CSV Location       -> '+os.getenv("CSV_FILE_LOCATION"))
    print('Loaded Master ClassName   -> '+os.getenv("MASTER_CLASS_NAME"))
    print('##########################################################\n')

    class_name = os.getenv("MASTER_CLASS_NAME")
    weaviate_url = os.getenv("WEAVIATE_URL")
    weaviate_client = weaviate.Client(
                                        weaviate_url
                                     )

def positive1(text):
    print('submit is clicked')
    print(df)
    table_html = df.to_html()  # Generate HTML table code
    return df


def positive(text):
    print('submit is clicked')
    print(df)
    table_html = df.to_html()  # Generate HTML table code
    return table_html

def negative(text):
    print('clear is clicked')
    text=""
    df = pd.DataFrame()
    return text,df

def main():
    with gr.Blocks(title="OFSLL DataMapper) as demo:
        with gr.Row():
            input_box = gr.Textbox(lines=1)
        with gr.Row():
            submit_button = gr.Button("Submit")
            clear_button = gr.Button("Clear")
        with gr.Row():
             output_html = gr.outputs.Dataframe(type='pandas')

        submit_button.click(positive1, inputs=[input_box],outputs=[output_html])
        clear_button.click(negative, inputs=[input_box], outputs=[input_box,output_html])

demo.launch()

if __name__ == '__main__':
    main()
    