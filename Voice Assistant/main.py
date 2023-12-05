import speech_recognition as sr
import requests

def greet():
    return "Hello! How can I help you today?"

def get_time():
    # Implement the logic to get the current time
    return "The current time is 15:45:20."

def get_date():
    # Implement the logic to get the current date
    return "Today's date is December 1, 2023."

def search_web(query):
    search_url = "https://www.googleapis.com/customsearch/v1"
    api_key = "AIzaSyBwbxMFUGqtNEzk1D6zGgUYRqy7FLq0UDg"
    cx = "817bec7b8feb544bc"
    params = {"q": query, "key": api_key, "cx": cx}

    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()  # Check for HTTP errors

        results = response.json()

        # Check if 'items' key exists in the response
        if 'items' in results:
            # Limit the results to the first 5 items
            limited_results = results['items'][:5]
            formatted_results = "\n".join([f"{i + 1}. {item['title']} - {item['link']}" for i, item in enumerate(limited_results)])
            return f"Here are the first 5 search results:\n{formatted_results}"
        else:
            return "No search results found."

    except requests.exceptions.RequestException as e:
        return f"Error with the search request: {e}"
    except KeyError:
        return "Unexpected response format from the search API."

def main():
    recognizer = sr.Recognizer()

    print("Voice Assistant is running. Say 'exit' to stop.")

    while True:
        with sr.Microphone() as source:
            print("\nSay something...")
            try:
                audio = recognizer.listen(source, timeout=5)  # Set a timeout to prevent waiting indefinitely
            except sr.WaitTimeoutError:
                print("Timeout. No speech detected.")
                continue  # Go to the next iteration of the loop

        try:
            user_input = recognizer.recognize_google(audio).lower()
            print("You said:", user_input)

            if "exit" in user_input or "stop" in user_input:
                print("Exiting voice assistant.")
                break

            if "hello" in user_input:
                response = greet()
            elif "time" in user_input:
                response = get_time()
            elif "date" in user_input:
                response = get_date()
            elif "search" in user_input:
                query = user_input.split("search")[1].strip()
                response = search_web(query)
                print("Assistant:", response)
                
                # Add a condition to handle a new search
                if "search" in response.lower():
                    print("Please provide a more specific search query.")
                    continue  # Continue to the next iteration of the loop for a new search
            else:
                response = "Sorry, I couldn't understand that. You can ask about the time, date, or perform a search."

            print("Assistant:", response)

        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
        except sr.RequestError as e:
            print(f"Error with the speech recognition service; {e}")

if __name__ == "__main__":
    main()
