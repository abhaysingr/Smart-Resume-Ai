import requests
from utils.logger import setup_logger

logger = setup_logger(__name__)

def compile_latex_online(latex_code):
    """
    Compile LaTeX to PDF using latex.online service
    
    Args:
        latex_code: String containing LaTeX code
    
    Returns:
        bytes: PDF file content or None if compilation fails
    """
    try:
        # Use latex.online API
        url = "https://latexonline.cc/compile"
        
        files = {
            'filecontents[]': ('document.tex', latex_code.encode('utf-8'), 'text/plain')
        }
        
        data = {
            'command': 'pdflatex'
        }
        
        logger.info("Sending LaTeX to online compiler...")
        response = requests.post(url, files=files, data=data, timeout=60)
        
        if response.status_code == 200:
            logger.info("PDF compiled successfully online")
            return response.content
        else:
            logger.error(f"Online compilation failed: {response.status_code}")
            logger.error(f"Response: {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"Error with online LaTeX compilation: {str(e)}", exc_info=True)
        return None