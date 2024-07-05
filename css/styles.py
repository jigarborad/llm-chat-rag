custom_css = """
    <style>
    
        body {
            background-color: #f0f2f6;
            font-family: 'Helvetica Neue', sans-serif;
            color: #333;
        }
        .main {
            background-color: #ece9e6;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .st-emotion-cache-svoq73 {
            height: 400px;
            overflow: auto;
            display: flex;
            flex-direction: column-reverse;
        }
        .st-emotion-cache-12fmjuu {
            position: fixed;
            top: 0px;
            left: 0px;
            right: 0px;
            height: 0;
            background: rgb(255, 255, 255);
            outline: none;
            z-index: 999990;
            display: block;
        }
        [data-testid=stSidebar] {
            background-color: #f9f9f9;
            border-right: solid 0.1em;
            border-right-color: black;
            width: auto;
            color: black;
        }
        [data-testid=stExpander] {
            background-color: #ededed;
            color: black;
        }
        .sidebar .sidebar-content a {
            color: white;
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
        .header-container {
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
        }
        .blank-header-container {
            position: fixed;
            left: 0;
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #ece9e6;
            padding: 62px 300px;
            z-index: 1001;
        }
        .blank-footer-container {
            position: fixed;
            bottom: 0px;
            left: 0;
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #ece9e6;
            padding: 35px 300px;
            z-index: 1001;
        }
        .header-title {
            margin-right: 10px;
        }
        .info-button {
            font-size: 24px;
            cursor: pointer;
            fill: #1a5276;
            margin-left: 5px;
            color: white;
            
        }
        .info-button:hover {
            fill: #3e92cc;
            color: black;
        }
        /* Tooltip container */
        .tooltip {
            position: sticky;
            display: inline-block;
        }
        /* Tooltip text */
        .tooltip .tooltiptext {
            visibility: hidden;
            width: max-content;  /* Adjust width as needed */
            background-color: #333;
            color: #fff;
            text-align: center;
            border-radius: 6px;
            padding: 5px 10px;  /* Adjust padding as needed */
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -calc(50% + 10px);  /* Adjust margin based on padding */
            opacity: 0;
            transition: opacity 0.3s;
            
            
        }
        /* Tooltip text visibility on hover */
        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 70%;
        }
        div.block-container{
            padding-top:2rem;
        }
    </style>
"""

header = """<div class="header-container"><h3 class="header-title">Chat with PDF &#x1F916;</h3><div class="tooltip"><svg class="info-button" viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg><span class="tooltiptext">Enter the relevant API keys and upload PDFs on the left sidebar.</span></div></div>"""
blank_header = """<div class="blank-header-container"></div>"""
blank_footer = """<div class="blank-footer-container"></div>"""