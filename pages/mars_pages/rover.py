import streamlit as st
import asyncio
import aiohttp
from PIL import Image
from io import BytesIO

# Async function to fetch image
async def fetch_image(session, url):
    async with session.get(url) as response:
        img_data = await response.read()
        img = Image.open(BytesIO(img_data))
        return img

# Async function to fetch photos
async def fetch_photos_async(rover, sol, camera):
    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos"
    params = {
        "sol": sol,
        "camera": camera,
        "api_key": "DEMO_KEY"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                photos = await response.json()
                return photos.get("photos", [])
            else:
                return []

def display():
    st.title("NASA Mars Rover Photos Viewer")

    # Dropdowns and inputs for user parameters
    rovers = ["Curiosity", "Opportunity", "Spirit"]
    selected_rover = st.selectbox("Select Rover", rovers).lower()
    
    sol = st.number_input("Enter Martian Sol (Martian day)", min_value=0, value=1000, step=1)
    
    camera_options = ["FHAZ", "RHAZ", "MAST", "CHEMCAM", "NAVCAM", "PANCAM", "MINITES"]
    selected_camera = st.selectbox("Select Camera", camera_options).lower()

    # Button to fetch photos
    if st.button("Get Photos"):
        with st.spinner("Fetching photos..."):
            photos = asyncio.run(fetch_photos_async(selected_rover, sol, selected_camera))
        
        if photos:
            st.success(f"Found {len(photos)} photos.")
            
            # Fetch images concurrently
            async def display_images():
                async with aiohttp.ClientSession() as session:
                    tasks = []
                    num_photos = len(photos)
                    for i in range(0, num_photos, 2):
                        cols = st.columns(2)
                        
                        for j in range(2):
                            if i + j < num_photos:
                                photo = photos[i + j]
                                img_url = photo["img_src"]
                                tasks.append(fetch_image(session, img_url))
                                
                    images = await asyncio.gather(*tasks)

                    for idx, img in enumerate(images):
                        cols[idx % 2].image(img, caption=f"{photos[idx]['rover']['name']} - {photos[idx]['camera']['full_name']} (Sol {photos[idx]['sol']})", use_column_width=True)

            asyncio.run(display_images())
        else:
            st.warning("No photos found for the given parameters.")

# Run the app
if __name__ == "__main__":
    display()
