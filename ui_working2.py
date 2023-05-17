import gradio as gr
import pandas as pd

# Example DataFrame
data = {
    'Name': ['John', 'Alice', 'Bob'],
    'Age': [25, 30, 35],
    'City': ['New York', 'London', 'Paris']
}
df = pd.DataFrame(data)

def positive1():
    return df.values.tolist()


def positive(text):
    print('submit is clicked')
    print(df)
    table_html = df.to_html()  # Generate HTML table code
    return table_html

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
    with gr.Row():
         output_html = gr.outputs.HTML()

    submit_button.click(positive, inputs=[input_box],outputs=[output_html])
    clear_button.click(negative, inputs=[input_box], outputs=[input_box])

demo.launch()
    