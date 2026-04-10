<style>
    /* Main background and global text color */
    .stApp { 
        background-color: #f4ecd8; 
        font-family: 'Courier New', Courier, monospace;
        color: #000000 !important; 
    }
    
    /* Ensure all markdown text (including chat) is black */
    .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, span {
        color: #000000 !important;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] { 
        background-color: #3e2723; 
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important; /* Keep sidebar text white for contrast */
    }

    /* Header styling */
    h1 { 
        color: #3e2723 !important; 
        text-align: center; 
        border-bottom: 2px solid #3e2723; 
        font-variant: small-caps; 
    }

    /* Chat message boxes */
    .stChatMessage { 
        background-color: #ffffffcc !important; 
        border-radius: 0px; 
        border-left: 5px solid #3e2723; 
        margin-bottom: 10px;
    }
    </style>
