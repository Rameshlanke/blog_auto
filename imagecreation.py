from PIL import Image, ImageDraw, ImageFont
import os
import textwrap

# Get the current working directory
path = os.getcwd()

# Set the image template file name
template_filename = "template1.png"

# Set the template path by joining the current working directory and the template filename
template_path = os.path.join(path, template_filename)

# Load the image template
template = Image.open(template_path)

text = "WHAT IS WEB DEVELOPMENT IN TODAYS KING"
font_size = 100
text_color = (0, 0, 0)  # Black


# Load the font (adjust the path if needed)
font_path = "Roboto-Black_1.ttf"
font = ImageFont.truetype(font_path, font_size)

# Create a new ImageDraw object
draw = ImageDraw.Draw(template)

# Calculate the maximum width and height for the text
max_text_width = template.width - 100  # Adjust the padding as needed
max_text_height = template.height - 100  # Adjust the padding as needed

# Wrap the text to fit within the maximum width
wrapped_text = textwrap.fill(text, width=int(max_text_width / (font_size * 0.6)))

# Calculate the text bounding box
text_bbox = draw.textbbox((0, 0), wrapped_text, font=font)

# Calculate the text width and height
text_width = text_bbox[2] - text_bbox[0]
text_height = text_bbox[3] - text_bbox[1]

# Calculate the position to center and middle-align the text
text_x = (template.width - text_width) // 2
text_y = (template.height - text_height) // 2 - int(text_height * 0.15)  # Move the text up by 15% of its height

# Draw the wrapped text on the image
draw.text((text_x, text_y), wrapped_text, font=font, fill=text_color)

# Save the modified image
template.save("modified_image.png")
