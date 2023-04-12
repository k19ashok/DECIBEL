
from views import video_names

def downloadVideo(result_video_names):

    import cv2
    import numpy as np
    videos = []
    for i in result_video_names:
        file_id = video_names.get(i, '')
        if not file_id:
            continue

        # Replace with the file URL you want to download
        file_url = "https://drive.google.com/uc?export=download&id={file_id}"


        # Send a GET request to the file URL
        response = requests.get(file_url)

    np_data = np.frombuffer(response, dtype=np.uint8)

    # Decode the numpy array into an OpenCV frame
    frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)

    # Create a VideoCapture object from the OpenCV frame
    cap = cv2.VideoCapture()
    cap.open(frame)
    
    # Open the video file
    # video_path = "example.mp4"
    # cap = cv2.VideoCapture(video_path)

    # # Get the video properties
    # frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # fps = int(cap.get(cv2.CAP_PROP_FPS))

    # # Create a VideoWriter object to save the output video
    # output_path = "output.avi"
    # fourcc = cv2.VideoWriter_fourcc(*"XVID")
    # out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    # # Loop through the frames in the video
    # while cap.isOpened():
    #     # Read a frame from the video
    #     ret, frame = cap.read()

    #     # Stop the loop if we have reached the end of the video
    #     if not ret:
    #         break

    #     # Process the frame (for example, convert it to grayscale)
    #     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #     # Write the processed frame to the output video
    #     out.write(gray)

    #     # Display the processed frame (optional)
    #     cv2.imshow("Frame", gray)
    #     if cv2.waitKey(1) & 0xFF == ord("q"):
    #         break

    # # Release the resources
    # cap.release()
    # out.release()
    # cv2.destroyAllWindows()

    # import requests
    

    #     # Get the download URL from the response cookies
    #     confirm_cookie = response.cookies.get('download_warning')
    #     if confirm_cookie:
    #         confirm_url = f'{file_url}&confirm={confirm_cookie}'
    #         response = requests.get(confirm_url)
        
    #     # Write the file contents to a file on disk
    #     with open(i + '.mp4', 'wb') as f:
    #         f.write(response.content)
        
    #     clip = VideoFileClip(i+'.mp4')
    #     videos.append(clip)
    #     os.unlink(i+'.mp4')
    # print(videos)
    # print('DONE')
    # return HttpResponse('<h1>Done</h1>')


    # videos = []
    # for i in result_video_names:
    #     file_id = video_names.get(i, '')
    #     if not file_id:
    #         continue
    #     file_url = "https://drive.google.com/uc?export=download&id={file_id}"

    #     # Send a GET request to the file URL
    #     response = requests.get(file_url)

    #     _, file_extension = os.path.splitext(file_url)

    #     # Load the video file into a VideoFileClip object
    #     clip = VideoFileClip(response.content)
    #     videos.append(clip)

    #     # Delete the temporary file
    #     os.unlink(f.name)

    # print("final_list",videos)
    # final_result = concatenate_videoclips(videos).without_audio()
    # out = HttpResponse(content_type='video/mp4')
    # final_result.write_videofile(out, codec='libx264', audio_codec='aac')

    # return response








# Load the file contents into a BytesIO object

# Load the video file into a VideoFileClip object

# Use the clip object as desired
# For example, you can display the video using clip.preview()



# from PIL import Image, ImageSequence

# # Load the images
# def make_animation(images):
#     images = [Image.open(f'image{i}.jpg') for i in range(1, 6)]

#     # Create a new animated image with a duration of 200ms between frames
#     animated_image = Image.new('RGB', (500, 500))
#     animated_image.save('animation.gif', save_all=True, append_images=images, duration=200, loop=0)
