import gradio as gr


def positive(text):
    print('submit is clicked')
    print(text)
    return text

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
    
    submit_button.click(positive,input_box,input_box)
    clear_button.click(negative,input_box,input_box)

demo.launch()
    