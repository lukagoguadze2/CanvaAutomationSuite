# CanvaBot

CanvaBot is a Python script designed for automating tasks on Canva, such as login, text and image manipulation, and other actions.

## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
- [Usage](#usage)
  - [CanvaBot](#canvabot)
  - [CanvaImage](#canvaimage)
  - [CanvaVideo](#canvavideo)
- [License](#license)

## Features
- Automated login to Canva using Google Sign-In.
- Automated editing Image.
- Automated editing Video.
- Uploading and downloading images and videos on Canva.

## Getting Started

### Prerequisites
- Required Python packages:
  - undetected-chromedriver
  - selenium
  - beautifulsoup4
  - shutil

## Usage

### CanvaBot
```python
from CanvaBot import CanvaBot

# Create an instance of CanvaBot to automate login
bot = CanvaBot()
```
The `CanvaBot` class is initialized to automate the login process on Canva using a preconfigured Google account. It includes methods to connect to Google, open a new browser window, and navigate to the Canva login page.

```python

# Close the CanvaBot instance
bot.Close()
```
Creating an instance of CanvaBot will only automate login, nothing more.

# CanvaImage

The `CanvaImage` class is a subclass of the `CanvaBot` class and represents a specialized instance for working with Canva's image workspace. It provides automation features for tasks related to Canva's image editing functionalities.

## Initialization

```python
from CanvaBot import CanvaImage

# Create an instance of CanvaImage to automate login to the Canva image workspace
image_bot = CanvaImage()
```

Upon initialization, the `CanvaImage` instance inherits the login automation features from the `CanvaBot` class and navigates to the Canva image workspace.

## Actions and Methods

### `change_text(text: str) -> bool`
Change the text content on a Canva design element.

#### Parameters
- `text`: The new text content to be set.

#### Returns
- `True` if the text change is successful; `False` otherwise.

#### Example
```python
success = image_bot.change_text("New Text Content")
```

### `change_photo(pictures: str, btn=0) -> dict`
Change the photo on a Canva design by uploading and downloading a new image.

#### Parameters
- `pictures`: The path to the image file to be uploaded.
- `btn` (optional): A parameter indicating whether a specific (save) button is clicked or not. 'btn' must be parsed when using this function in an iteration.

#### Returns
A dictionary containing edited image download link and button click status.

#### Example
```python
result = image_bot.change_photo("~path/to/your/image.jpg")
```

## Additional Notes

- The `CanvaImage` class utilizes the `CanvaBot` functionalities for login and navigation to the image workspace.
- Image-related actions, such as changing text content and uploading images, can be performed using the provided methods.

## Closing the Instance

```python
# Close the CanvaImage instance
image_bot.Close()
```

The `Close` method is called to quit the Chrome webdriver and close the browser window associated with the `CanvaImage` instance.

## Single use Example

```python
from CanvaBot import CanvaImage

bot = CanvaImage()

change_text = bot.change_text("New Text Content")

change_image = bot.change_photo(".path/to/image.jpg")

print(change_image["imagelink"])

bot.Close()
```

## Used in iteration

```python
from CanvaBot import CanvaImage

texts = ["Former Text Content", "Latter Text Content"]
image_paths = ["path/to/image1.jpg", "path/to/image2.jpg"]
bot = CanvaImage()

click_count = 0
for text, image_path in zip(texts, image_paths):
  change_text = bot.change_text(text)
  if not change_text:
    print("Error while changing a text")
    break

  change_image = bot.change_photo(image_path, btn=click_count)
  if change_image["imagelink"]:
    # do something with download link
    click_count = change_image["buttonclicked"]
  else:
    print("Error while changing a image")
    break

bot.Close()

```



# CanvaVideo
The `CanvaVideo` class is an extension of the `CanvaBot` class and represents a specialized instance for working with Canva's video workspace. It provides automation features for tasks related to Canva's video editing functionalities.

## Initialization

```python
from CanvaBot import CanvaVideo

# Create an instance of CanvaVideo to automate login to the Canva video workspace
video_bot = CanvaVideo()
```

Upon initialization, the `CanvaVideo` instance inherits the login automation features from the `CanvaBot` class and navigates to the Canva video workspace.

## Actions and Methods

### `change_video_text(text: str) -> bool`
Change the text caption of a video element in Canva, adjusting the font size as needed.

#### Parameters
- `text`: The new text to be set as the caption.

#### Returns
- `True` if the text caption is successfully changed, `False` otherwise.

#### Example
```python
success = video_bot.change_video_text("New Text Content")
```

### `change_video(video_path: str, foldername=None) -> bool`
Upload a video to Canva, set it as a background, and transfer the edited video to a designated folder.

#### Parameters
- `video_path`: The path to the video file to be uploaded.
- `foldername` (optional): The name of the google drive folder. Should be provided if [DriveUpload](CanvaBot.py#L658-L666) lines are not commented.

#### Returns
- `True` if the video is successfully processed and transferred, `False` otherwise.

#### Example
```python
success = video_bot.change_video('~path/to/your/video.mp4', 'custom_folder')
```

## Additional Notes

- The `CanvaVideo` class utilizes the `CanvaBot` functionalities for login and navigation to the video workspace.
- Video-related actions, such as changing text captions and uploading videos, can be performed using the provided methods.

## Closing the Instance

```python
# Close the CanvaVideo instance
video_bot.Close()
```

The `Close` method is called to quit the Chrome webdriver and close the browser window associated with the `CanvaVideo` instance.

## Single Use Example
```python
from CanvaBot import CanvaVideo

bot = CanvaVideo()

change_text = bot.change_video_text("Video Text Content")

change_video = bot.change_video(".path/to/video.mp4")

bot.Close()

```

# Used in iteration
```python
from CanvaBot import CanvaVideo

texts = ["Former Text Content", "Latter Text Content"]
video_paths = ["path/to/video1.mp4", "path/to/video2.mp4"]
bot = CanvaVideo()

for text, video_path in zip(texts, video_paths):
  change_text = bot.change_text(text)
  if not change_text:
    print("Error while changing a text")
    break

  change_video = bot.change_video(image_path)
  if not change_video:
    print("Error while changing a video")
    break

bot.Close()
```


## License
This project is licensed under the [MIT License](LICENSE).
