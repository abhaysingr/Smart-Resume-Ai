import os
import base64
from ui_components import about_section

def render_about():
    """Render the about page with updated light theme"""
    
    def get_image_as_base64(file_path):
        try:
            with open(file_path, "rb") as image_file:
                encoded = base64.b64encode(image_file.read()).decode()
                return f"data:image/jpeg;base64,{encoded}"
        except:
            return None
    
    # Note: The original code had image_path logic but didn't seem to use image_base64 in the about_section call.
    # I'll keep the logic just in case, but it seems unused in the original snippet provided.
    # Actually, looking at the original code, image_path was constructed relative to __file__.
    # Since we moved this file to views/, we need to adjust the path to assets.
    # assets is in the root, so it's ../assets
    
    image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "124852522.jpeg")
    image_base64 = get_image_as_base64(image_path)
    
    # Updated CSS: light backgrounds (#f7f7f7) with dark text (#333333)
    
    about_section(
        title="About Smart Resume AI",
        description="""
            "Smart Resume AI represents my vision of democratizing career advancement through technology. 
            By combining cutting-edge AI with intuitive design, this platform empowers job seekers at 
            every career stage to showcase their true potential and stand out in today's competitive job market."
        """
    )
