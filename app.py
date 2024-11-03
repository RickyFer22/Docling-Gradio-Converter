
import gradio as gr
from docling.document_converter import DocumentConverter
import json
import tempfile
import os

def convert_document(file, output_format):
    """
    Converts a document to Markdown or JSON format using Docling.
    Args:
        file: Uploaded file to convert.
        output_format: Desired output format (Markdown or JSON).
    Returns:
        Tuple containing the converted text, metadata, and downloadable file.
    """
    try:
        # Initialize the converter and load the document
        converter = DocumentConverter()
        result = converter.convert(file.name)
        
        # Create temporary file for download
        temp_dir = tempfile.gettempdir()
        
        if output_format == "Markdown":
            converted_text = result.document.export_to_markdown()
            file_extension = ".md"
        else:
            converted_text = result.document.export_to_json()
            file_extension = ".json"
            
        # Create output file
        output_filename = os.path.splitext(os.path.basename(file.name))[0] + file_extension
        output_path = os.path.join(temp_dir, output_filename)
        
        # Write content to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(converted_text)
            
        metadata = {
            "Filename": file.name,
            "File Size": f"{os.path.getsize(file.name) / 1024:.2f} KB",
            "Output Format": output_format,
            "Conversion Status": "Success"
        }
        
        return (
            converted_text,
            metadata,
            output_path,
            gr.update(visible=True),
            "✅ Document converted successfully!"
        )
        
    except Exception as e:
        error_metadata = {
            "Error": str(e),
            "Status": "Failed"
        }
        return (
            "",
            error_metadata,
            None,
            gr.update(visible=False),
            "❌ Error during conversion"
        )

# Custom CSS
custom_css = """
:root {
    --primary-color: #2563eb;
    --secondary-color: #1e40af;
    --background-color: #1e1e1e;
    --card-background: #262626;
    --text-color: #ffffff;
    --border-radius: 10px;
}

body {
    background-color: var(--background-color);
    color: var(--text-color);
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

.gr-button {
    background: var(--primary-color) !important;
    border: none !important;
    color: white !important;
    padding: 10px 20px !important;
    border-radius: var(--border-radius) !important;
    transition: all 0.3s ease !important;
}

.gr-button:hover {
    background: var(--secondary-color) !important;
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.gr-form {
    background-color: var(--card-background);
    padding: 2rem;
    border-radius: var(--border-radius);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.gr-input, .gr-textbox {
    background-color: #333333 !important;
    border: 1px solid #404040 !important;
    color: var(--text-color) !important;
    border-radius: var(--border-radius) !important;
}

.gr-padded {
    padding: 1rem;
}

.gr-header {
    margin-bottom: 2rem;
    text-align: center;
}

.gr-subtitle {
    color: #9ca3af;
    font-size: 1.1rem;
    margin-bottom: 1.5rem;
}
"""

# Create Gradio interface
with gr.Blocks(css=custom_css) as app:
    gr.HTML(
        """
        <div class="gr-header">
            <h1 style='font-size: 2.5rem; color: #2563eb; margin-bottom: 1rem;'>📄 Docling Document Converter</h1>
            <p class="gr-subtitle">Transform your documents into Markdown or JSON format with ease</p>
        </div>
        """
    )
    
    with gr.Row():
        with gr.Column(scale=1):
            with gr.Group():
                gr.Markdown("### Input Settings")
                file_input = gr.File(
                    label="Upload Your Document",
                    file_types=[".doc", ".docx", ".pdf", ".txt"],
                    elem_classes="gr-input"
                )
                format_input = gr.Radio(
                    choices=["Markdown", "JSON"],
                    label="Output Format",
                    value="Markdown",
                    elem_classes="gr-input"
                )
                convert_button = gr.Button(
                    "🔄 Convert Document",
                    variant="primary",
                    elem_classes=["gr-button"]
                )
                
            status_message = gr.Textbox(
                label="Status",
                interactive=False,
                visible=False,
                elem_classes="gr-padded"
            )
    
        with gr.Column(scale=2):
            with gr.Group():
                gr.Markdown("### Conversion Output")
                output_text = gr.Textbox(
                    label="Converted Content",
                    placeholder="The converted text will appear here...",
                    lines=15,
                    elem_classes="gr-textbox"
                )
                output_metadata = gr.JSON(
                    label="Document Metadata",
                    elem_classes="gr-input"
                )
                download_button = gr.File(
                    label="Download Converted File",
                    visible=False,
                    elem_classes="gr-padded"
                )
    
    # Event handlers
    convert_button.click(
        fn=convert_document,
        inputs=[file_input, format_input],
        outputs=[
            output_text,
            output_metadata,
            download_button,
            download_button,
            status_message
        ]
    )

# Launch the app with share=True
app.launch(debug=True, share=True)