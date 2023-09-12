import os
import tkinter as tk
from tkinter import filedialog
import subprocess

def create_gif(input_video, start_time, end_time, output_gif):
    # Get the original video's frame rate
    original_fps = get_original_frame_rate(input_video)
    
    cmd = [
        'ffmpeg',
        '-ss', start_time,     # Start time in HH:MM:SS format
        '-to', end_time,       # End time in HH:MM:SS format
        '-i', input_video,     # Input video file
        '-vf', f'fps={original_fps},scale=-1:-1;',  # Use original FPS and scale
        '-c:v', 'gif',         # Output format is GIF
        '-b:v', '100M',        # Set a high bitrate for the best quality
        '-loop', '0',          # Loop
        '-y',                  # Overwrite output file if it exists
        output_gif             # Output GIF file
    ]

    subprocess.run(cmd)

def get_original_frame_rate(input_video):
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=r_frame_rate',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        input_video
    ]

    output = subprocess.check_output(cmd, universal_newlines=True)
    numerator, denominator = output.strip().split('/')
    return int(numerator) / int(denominator)

def browse_video():
    input_video = filedialog.askopenfilename(filetypes=[("Video files", "*.m4v *.wmv *.mp4 *.avi *.mkv")])
    input_video_entry.delete(0, tk.END)
    input_video_entry.insert(0, input_video)

def browse_output_dir():
    output_gif = filedialog.asksaveasfilename(defaultextension=".gif", filetypes=[("GIF files", "*.gif")])
    output_gif_entry.delete(0, tk.END)
    output_gif_entry.insert(0, output_gif)

def create_gif_button():
    input_video = input_video_entry.get()
    start_time = start_time_entry.get()
    end_time = end_time_entry.get()
    output_gif = output_gif_entry.get()

    create_gif(input_video, start_time, end_time, output_gif)
    result_label.config(text="GIF created successfully!  Sure hope nothing super bad happens in your life after this.")

app = tk.Tk()
app.title("GIF OF THE MAGI")

# Input Video
input_video_label = tk.Label(app, text="Input Video:")
input_video_label.pack()
input_video_entry = tk.Entry(app)
input_video_entry.pack()
browse_video_button = tk.Button(app, text="Browse", command=browse_video)
browse_video_button.pack()

# Start Time
start_time_label = tk.Label(app, text="Start Time (HH:MM:SS):")
start_time_label.pack()
start_time_entry = tk.Entry(app)
start_time_entry.pack()

# End Time
end_time_label = tk.Label(app, text="End Time (HH:MM:SS):")
end_time_label.pack()
end_time_entry = tk.Entry(app)
end_time_entry.pack()

# Output GIF File Name
output_gif_label = tk.Label(app, text="Output GIF File Name:")
output_gif_label.pack()
output_gif_entry = tk.Entry(app)
output_gif_entry.pack()
browse_output_gif_button = tk.Button(app, text="Browse", command=browse_output_dir)
browse_output_gif_button.pack()

# Create GIF Button
create_gif_button = tk.Button(app, text="Create GIF", command=create_gif_button)
create_gif_button.pack()

# Result Label
result_label = tk.Label(app, text="")
result_label.pack()

app.mainloop()
