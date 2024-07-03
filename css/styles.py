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
        .st-emotion-cache-svoq73 {
            height: 400px;
            overflow: auto;
            display: flex;
            flex-direction: column-reverse;
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
        .user-message-container {
            display: flex; 
            justify-content: flex-end; 
            margin-bottom: 10px;
        }
        
        .assistant-message-container {
            display: flex; 
            justify-content: flex-start; 
            margin-bottom: 10px;
            
        }

        /* User message styles */
        .user-message {
            padding: 5px; 
            background-color: #2E4053; 
            border-radius: 10px; 
            max-width: 80%; 
            color: white;
            box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
        }

        /* Assistant message styles */
        .assistant-message {
            justify-content: flex-start; 
            background-color: #E0E0E0; /* Light gray background */
            color: #262730; /* Dark text color */
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
            max-width: 80%;
            word-wrap: break-word;
            box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
        }

        .icons-images {
            vertical-align: middle; 
            width: 30px; 
            height: 30px; 
            margin-right: 10px; 
            margin-left: 10px;
        }
    </style>
"""

upload_banner = """
    <div class="card fade-in">
        <h2>Upload your PDF</h2>
        <p>Upload a PDF file and ask questions related to its content.</p>
    </div>
"""

header = """<h1 class="fade-in">Chat with PDF &#x1F916;</h1>"""
