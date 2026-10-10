#!/usr/bin/env python3
import os
import subprocess
import random
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    subprocess.run(["pip", "install", "Pillow"], check=True)
    from PIL import Image, ImageDraw, ImageFont

# Ensure directories exist
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "fileshare", "data", "repo", "classified_assets_2048")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_image(filename, text, size=(800, 600)):
    # Create a dark background image
    img = Image.new('RGB', size, color=(10, 12, 16))
    draw = ImageDraw.Draw(img)
    
    # Draw some random telemetry lines
    for _ in range(20):
        x1, y1 = random.randint(0, size[0]), random.randint(0, size[1])
        x2, y2 = random.randint(0, size[0]), random.randint(0, size[1])
        color = (random.randint(0, 100), random.randint(100, 255), random.randint(50, 150))
        draw.line((x1, y1, x2, y2), fill=color, width=2)
        
    # Draw text
    try:
        font = ImageFont.truetype("DejavuSansMono.ttf", 24)
    except:
        font = ImageFont.load_default()
        
    draw.text((50, 50), text, fill=(0, 255, 136), font=font)
    
    # Add random grid
    for i in range(0, size[0], 50):
        draw.line((i, 0, i, size[1]), fill=(30, 30, 30), width=1)
    for i in range(0, size[1], 50):
        draw.line((0, i, size[0], i), fill=(30, 30, 30), width=1)

    img.save(filename, format='JPEG', quality=95)
    print(f"Generated {filename}")

def generate():
    flag_stage4 = os.environ.get("FLAG_STAGE4", "BP{steghide_payload_extracted}")
    
    # 1. Generate decoy images
    create_image("telemetry_node_1.jpg", "NODE 1: SIGNAL ACQUIRED\nSTATUS: NOMINAL")
    create_image("telemetry_node_2.jpg", "NODE 2: SIGNAL ACQUIRED\nSTATUS: NOMINAL")
    create_image("telemetry_node_4.jpg", "NODE 4: SIGNAL ACQUIRED\nSTATUS: OFFLINE")
    
    # 2. Generate target image
    target_img = "payload_telemetry.jpg"
    create_image(target_img, "NODE 3: ANOMALY DETECTED\nWARNING: PAYLOAD EMBEDDED")
    
    # 3. Create payload text file
    payload_text = f"""[CLASSIFIED EXTRACTION SUCCESSFUL]

FLAG: {flag_stage4}

Next Step:
The injection tool needed to override the SOVEREIGN core is located at:
/tools/sovereign_inject_x86

Proceed to the root of this file share to locate it.
"""
    with open("payload.txt", "w") as f:
        f.write(payload_text)
        
    print("Payload text generated.")
    
    # 4. Embed payload using dockerized steghide
    print("Embedding payload using Steghide via Docker...")
    pwd = os.path.abspath(os.getcwd())
    steghide_cmd = [
        "docker", "run", "--rm",
        "-v", f"{pwd}:/work",
        "-w", "/work",
        "ubuntu:22.04",
        "sh", "-c",
        f"apt-get update && apt-get install -y steghide && steghide embed -cf {target_img} -ef payload.txt -p sovereign_override_991"
    ]
    
    subprocess.run(steghide_cmd, check=True)
    print("Payload embedded successfully.")
    
    # 5. Move images to output directory
    os.rename("telemetry_node_1.jpg", os.path.join(OUTPUT_DIR, "telemetry_node_1.jpg"))
    os.rename("telemetry_node_2.jpg", os.path.join(OUTPUT_DIR, "telemetry_node_2.jpg"))
    os.rename("telemetry_node_4.jpg", os.path.join(OUTPUT_DIR, "telemetry_node_4.jpg"))
    os.rename(target_img, os.path.join(OUTPUT_DIR, target_img))
    
    # Cleanup
    os.remove("payload.txt")
    print(f"All artifacts moved to {OUTPUT_DIR}")

if __name__ == "__main__":
    generate()
