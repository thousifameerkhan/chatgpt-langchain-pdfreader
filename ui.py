import gradio as gr
import pandas as pd

# Example DataFrame
data = {
    'Name': ['John', 'Alice', 'Bob'],
    'Age': [25, 30, 35],
    'City': ['New York', 'London', 'Paris']
}
df = pd.DataFrame(data)
df1 = pd.DataFrame()

papers = gr.DataFrame(
      headers = ["Name", "age","city"],
      datatype = ["str", "str","str"],
      value = df,
      visible = False   
        )

def positive1():
    return df

def positive(text):
    print('submit is clicked')
    print(df)
    table_html = df.to_html()  # Generate HTML table code
    return e = False   
        )

def negative(text):
    print('clear is clicked')
    text=""
    return text

with gr.Blocks() as demo:
    with gr.Row():
        input_box = gr.Textbox(lines=1)
    with gr.Row():
        submit_button = gr.Button("Submit")
        clear_button = gr.Button("Clear")
    
        submit_button.click(positive, inputs=[input_box],outputs=papers)
        clear_button.click(negative, inputs=[input_box], outputs=[input_box])

demo.launch()
    