import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

bot = telebot.TeleBot("7503914601:AAEODGqNNWvd7OVpdxNrXfF8zeo73yYdMpI")

user_prompts = {}

WELCOME_MESSAGE = """
🌟 *Welcome to AI Image Generator Bot* 🌟

I can create amazing images from your descriptions!

🎨 *How to use:*
1. Type `/img` followed by your description
2. Select aspect ratio
3. Get your AI generated image!

✨ *Example:* `/img a magical anime forest with glowing flowers`

Let's create something awesome! 🚀
"""

def aspect_ratio_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton("1:1 (Square) 🟧"))
    keyboard.add(KeyboardButton("16:9 (Wide) 🖥"))
    keyboard.add(KeyboardButton("21:9 (Cinematic) 🎬"))
    keyboard.add(KeyboardButton("2:3 (Portrait) 📱"))
    keyboard.add(KeyboardButton("3:2 (Landscape) 🌅"))
    keyboard.add(KeyboardButton("4:5 (Portrait) 📸"))
    keyboard.add(KeyboardButton("9:16 (Vertical) 📲"))
    keyboard.add(KeyboardButton("9:21 (Vertical Cinema) 🎥"))
    return keyboard

@bot.message_handler(commands=['start'])
def send_welcome(message):
    animation_url = 'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDd5Z3g2Y2wxbXB1NXF4OWRqOW95NnB4NnBxbGx6YnB4ZXJ1aHF6eSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oKIPic2TnThYWVOLe/giphy.gif'
    bot.send_animation(message.chat.id, animation_url)
    bot.reply_to(message, WELCOME_MESSAGE, parse_mode='Markdown')

@bot.message_handler(commands=['img'])
def get_prompt(message):
    try:
        prompt = message.text.split('/img ')[1]
        user_prompts[message.chat.id] = prompt
        bot.reply_to(message, "🎨 Please select aspect ratio for your masterpiece:", reply_markup=aspect_ratio_keyboard())
    except:
        bot.reply_to(message, "⚠️ Please provide a prompt after /img command\n*Example:* `/img cyberpunk city at night`", parse_mode='Markdown')

@bot.message_handler(func=lambda message: any(ratio in message.text for ratio in ["1:1", "16:9", "21:9", "2:3", "3:2", "4:5", "9:16", "9:21"]))
def generate_image(message):
    try:
        aspect_ratio = message.text.split(' ')[0]
        prompt = user_prompts.get(message.chat.id)
        
        if not prompt:
            bot.reply_to(message, "🔄 Please start again with /img command and your prompt")
            return

        # Send a processing message with animation
        processing_animation = 'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNG92bjB1ZXI2ZjBiMWt0MnA3bDN2cWR5ZHd6ZmN0aXBmYWRxY2twbiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7bu3XilJ5BOiSGic/giphy.gif'
        processing_message = bot.send_animation(message.chat.id, processing_animation, caption="🎨 Creating your masterpiece...")

        headers = {
            'authority': '1yjs1yldj7.execute-api.us-east-1.amazonaws.com',
            'accept': '*/*', 
            'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
            'origin': 'https://www.writecream.com',
            'referer': 'https://www.writecream.com/',
            'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        }

        params = {
            'prompt': prompt,
            'aspect_ratio': aspect_ratio,
            'link': 'writecream.com',
        }

        response = requests.get(
            'https://1yjs1yldj7.execute-api.us-east-1.amazonaws.com/default/ai_image',
            params=params,
            headers=headers,
        )
        
        # Delete processing message
        bot.delete_message(message.chat.id, processing_message.message_id)
        
        image_url = response.json()['image_link']
        print(image_url)
        bot.send_photo(
            message.chat.id, 
            image_url, 
            caption="✨ Here's your AI-generated masterpiece!\n\n🎨 *Prompt:* `{}`\n📐 *Aspect Ratio:* `{}`".format(prompt, aspect_ratio),
            parse_mode='Markdown',
            reply_markup=telebot.types.ReplyKeyboardRemove()
        )
        
        # Success animation
        success_animation = 'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcWM1cWd4YnBxM2t6ZXgxbWx6ZHd2bGF4ZnBrbWR0ZWNyZm50YmpraCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/LOcPt9gfuNOSI/giphy.gif'
        bot.send_animation(message.chat.id, success_animation, caption="✨ Creation complete! Want to create another? Just use /img command!")
        
        del user_prompts[message.chat.id]
        
    except Exception as e:
        error_animation = 'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbXFxZWQ2Y2xlNzY0ZjJhM2JlOXR5NnV6Y2xxbWQ5NXVnODMxOHR2ciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/WoWm8YzFQJg5i/giphy.gif'
        bot.send_animation(message.chat.id, error_animation, caption="❌ Oops! Something went wrong. Please try again with /img command.")
        del user_prompts[message.chat.id]

bot.polling()
