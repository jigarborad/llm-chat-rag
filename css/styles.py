custom_css = """
    <style>
        body {
            background-color: #f0f2f6;
            font-family: 'Helvetica Neue', sans-serif;
            color: #333;
        }
        .main {
            background: linear-gradient(to right, #ece9e6, #ffffff);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .stTextInput>div>div>input {
            border-radius: 5px;
            border: 1px solid #ccc;
            padding: 10px;
            width: 100%;
        }
        .stButton>button {
            background-color: #2e7bcf;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 16px;
        }
        .stButton>button:hover {
            background-color: #1e5bbf;
        }
        .sidebar .sidebar-content {
            background-color: #2e7bcf;
            color: white;
        }
        .sidebar .sidebar-content a {
            color: white;
        }
        h1 {
            color: #2e7bcf;
        }
        .card {
            background-color: white;
            padding: 20px;
            margin: 20px 0;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .stSpinner {
            border-top-color: #2e7bcf;
        }
    </style>
"""

upload_banner="""
        <div class="card fade-in">
            <h2>Upload your PDF</h2>
            <p>Upload a PDF file and ask questions related to its content.</p>
        </div>
    """

header = """<h1 class="fade-in">Chat with LLM &#x1F916;</h1>"""