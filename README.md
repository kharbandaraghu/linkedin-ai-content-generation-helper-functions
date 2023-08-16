# linkedin-ai-content-generation-helper-functions
Helper functions to generate AI content and post on linkedIn

## Prerequisites
* Python 3.6 or higher
* OpenAI API Key
* LinkedIn API Key

## Packages
* requests
* dotenv
* openai

## Usage

### 1. Installation

Begin by installing the required packages listed in the `requirements.txt` file. This can be achieved by executing the following command:

```bash
pip install -r requirements.txt
```

This ensures that all the necessary dependencies are properly set up to enable the smooth execution of the code.

### 2. API Key Setup

To enable communication with both the OpenAI and LinkedIn APIs, you need to set up API keys and environment variables. Perform the following steps:

#### OpenAI API Key

How to obtian API key [_coming soon_]

Create a `.env` file in the project directory.

Inside the `.env` file, add the following line, replacing `<your_openai_api_key>` with your actual OpenAI API key:

```plaintext
OPENAI_API_KEY=<your_openai_api_key>
```

#### LinkedIn API Key

How to obtian API key [_coming soon_]

In the `.env` file, add another line, replacing `<your_linkedin_api_key>` with your LinkedIn API key:

```plaintext
LINKEDIN_API_KEY=<your_linkedin_api_key>
```

### 3. Writing Logic

Now you're ready to start writing your code in the `main.py` file. This is where you'll create the logic for generating AI responses and posting content on LinkedIn.

#### Generating AI Responses

Utilize the `getAiResponse()` function to generate AI responses based on a given context. Here's a sample usage:

```python
from ai_module import getAiResponse

context = "Provide the context or prompt for generating the AI response."
ai_response = getAiResponse(context)
print(ai_response)
```

#### Posting Content on LinkedIn

You can use two functions, `create_linkedin_image_share()` and `create_text_share()`, to post content on LinkedIn.

##### Posting an AI-Generated Image and Text

Here's an example of how to create a post with an AI-generated response and an image on LinkedIn:

```python
from ai_module import create_linkedin_image_share

prompt = "Your prompt or context for the AI response."
ai_response = getAiResponse(prompt)
image_path = "path_to_your_image.jpg"  # Provide the actual path to your image

link_of_post = create_linkedin_image_share(ai_response, image_path)
print("LinkedIn Post URL:", link_of_post)
```

This code snippet retrieves an AI-generated response, associates it with an image, and then posts it on your LinkedIn profile.

By following these detailed instructions and examples, you'll be able to seamlessly integrate the provided codebase into your projects, leveraging both OpenAI's AI capabilities and the LinkedIn API to enhance your applications.

## License
This project is licensed under the MIT License.
