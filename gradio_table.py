import pandas as pd
import gradio as gr

# Create a sample DataFrame
data = {
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "city": ["New York", "London", "Paris"]
}
df = pd.DataFrame(data)

# Define a Gradio interface with a table output
def show_dataframe(df):
    return df.style.hide_index().set_table_attributes('class="table"').render()

iface = gr.Interface(
    fn=show_dataframe,
    inputs=gr.inputs.Dataframe(),
    outputs=gr.outputs.HTML(),
    title="Display Pandas DataFrame as a Table",
    description="This app displays a Pandas DataFrame as an HTML table using Gradio.",
    theme="default"
)

# Launch the interface
iface.launch()
