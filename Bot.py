import requests
from telegram import Update, ReplyKeyboardMarkup, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import logging
import random
from io import BytesIO
import time

# Bot Token
TOKEN = "7503914601:AAEODGqNNWvd7OVpdxNrXfF8zeo73yYdMpI"

# Aspect ratio options with emojis
ASPECT_RATIOS = {
    "🟦 1:1 (Square)": "1:1",
    "🌄 16:9 (Wide)": "16:9",
    "🎬 21:9 (Cinematic)": "21:9",
    "📸 2:3 (Portrait)": "2:3",
    "🏞️ 3:2 (Landscape)": "3:2",
    "📱 4:5 (Portrait)": "4:5",
    "📲 9:16 (Vertical)": "9:16",
    "🎥 9:21 (Vertical Cinema)": "9:21"
}

# Anime loading animations
LOADING_ANIMATIONS = [
    "🎨 Painting your vision...",
    "✨ Adding magical touches...",
    "🖌️ Brush strokes in progress...",
    "🌈 Coloring outside the lines...",
    "🌀 Reality bending...",
    "⚡ Powering up creativity...",
    "🌌 Warping dimensions..."
]

# User states
class UserState:
    def __init__(self):
        self.prompt = None
        self.waiting_for_ratio = False

# Dictionary to store user states
user_states = {}

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message with anime style."""
    anime_gif = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDl1dWQ1b3V1ZGJmZ3Q5Z2N6eHZ5b2V6dG5zY2R6eGZxZ3V6aGZ5diZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/26n6WywJyh39n1pBu/giphy.gif"
    await update.message.reply_animation(
        animation=anime_gif,
        caption="✨ *Welcome to AnimeGen Bot!* ✨\n"
                "I can generate amazing anime-style images for you!\n"
                "Use /img command to start creating.\n\n"
                "Example: `/img mystical forest at sunset`",
        parse_mode="Markdown"
    )

async def img_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /img command with anime style."""
    user_id = update.message.from_user.id
    
    # Check if prompt is provided
    if not context.args:
        anime_gif = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcWJ5bWZxZ2N1a2JtY2JmZ3Q5Z2N6eHZ5b2V6dG5zY2R6eGZxZ3V6aGZ5diZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7TKTDn976uzhK1GM/giphy.gif"
        await update.message.reply_animation(
            animation=anime_gif,
            caption="⚠️ *Please provide a prompt!* ⚠️\n"
                    "Usage: `/img your creative description`\n\n"
                    "Example: `/img cyberpunk city rain`",
            parse_mode="Markdown"
        )
        return
    
    prompt = " ".join(context.args)
    user_states[user_id] = UserState()
    user_states[user_id].prompt = prompt
    user_states[user_id].waiting_for_ratio = True
    
    # Create keyboard for aspect ratios
    reply_keyboard = [list(ASPECT_RATIOS.keys())[i:i+2] for i in range(0, len(ASPECT_RATIOS), 2)]
    
    anime_gif = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcWJ5bWZxZ2N1a2JtY2JmZ3Q5Z2N6eHZ5b2V6dG5zY2R6eGZxZ3V6aGZ5diZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7TKTDn976uzhK1GM/giphy.gif"
    await update.message.reply_animation(
        animation=anime_gif,
        caption=f"🎨 *Prompt received:* `{prompt}`\n\n"
                "📐 *Please select an aspect ratio:*",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
        parse_mode="Markdown"
    )

async def handle_aspect_ratio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle aspect ratio selection with anime style."""
    user_id = update.message.from_user.id
    
    # Check if user is in the correct state
    if user_id not in user_states or not user_states[user_id].waiting_for_ratio:
        return
    
    selected_ratio = update.message.text
    if selected_ratio not in ASPECT_RATIOS:
        anime_gif = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcWJ5bWZxZ2N1a2JtY2JmZ3Q5Z2N6eHZ5b2V6dG5zY2R6eGZxZ3V6aGZ5diZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7TKTDn976uzhK1GM/giphy.gif"
        await update.message.reply_animation(
            animation=anime_gif,
            caption="❌ *Invalid selection!* ❌\n"
                    "Please choose an aspect ratio from the options.",
            parse_mode="Markdown"
        )
        return
    
    aspect_ratio = ASPECT_RATIOS[selected_ratio]
    prompt = user_states[user_id].prompt
    
    # Clean up user state
    del user_states[user_id]
    
    # Send loading animation
    loading_message = await update.message.reply_text(
        random.choice(LOADING_ANIMATIONS) + " " + selected_ratio
    )
    
    # Simulate loading with progress updates
    for i in range(1, 4):
        time.sleep(1)
        await loading_message.edit_text(
            random.choice(LOADING_ANIMATIONS) + " " + selected_ratio + " " + "🔵" * i
        )
    
    try:
        # Prepare API request
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

        # Make API request
        response = requests.get(
            'https://1yjs1yldj7.execute-api.us-east-1.amazonaws.com/default/ai_image',
            params=params,
            headers=headers,
        )
        
        # Get image URL from response
        image_url = response.json()['image_link']
        print("Generated Image URL:", image_url)
        
        # Send success animation
        success_gif = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcWJ5bWZxZ2N1a2JtY2JmZ3Q5Z2N6eHZ5b2V6dG5zY2R6eGZxZ3V6aGZ5diZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7TKTDn976uzhK1GM/giphy.gif"
        await update.message.reply_animation(
            animation=success_gif,
            caption="🎉 *Image generated successfully!* 🎉"
        )
        
        # Send the image directly to the user
        await update.message.reply_photo(
            image_url,
            caption=f"🖼️ *Your Anime-Style Creation:*\n"
                    f"📝 *Prompt:* `{prompt}`\n"
                    f"📐 *Aspect Ratio:* {selected_ratio}\n\n"
                    f"✨ Want to create another? Use /img again!",
            parse_mode="Markdown"
        )
        
    except Exception as e:
        logger.error(f"Error generating image: {e}")
        error_gif = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcWJ5bWZxZ2N1a2JtY2JmZ3Q5Z2N6eHZ5b2V6dG5zY2R6eGZxZ3V6aGZ5diZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7TKTDn976uzhK1GM/giphy.gif"
        await update.message.reply_animation(
            animation=error_gif,
            caption="❌ *Oops! Something went wrong!* ❌\n"
                   "The magic failed this time. Please try again later!",
            parse_mode="Markdown"
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send help message with anime style."""
    anime_gif = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcWJ5bWZxZ2N1a2JtY2JmZ3Q5Z2N6eHZ5b2V6dG5zY2R6eGZxZ3V6aGZ5diZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7TKTDn976uzhK1GM/giphy.gif"
    await update.message.reply_animation(
        animation=anime_gif,
        caption="🌟 *AnimeGen Bot Help* 🌟\n\n"
               "🎨 *How to create images:*\n"
               "1. Type `/img` followed by your creative prompt\n"
               "   Example: `/img neon samurai in rain`\n"
               "2. Select an aspect ratio from the options\n"
               "3. Watch the magic happen!\n\n"
               "📐 *Available Aspect Ratios:*\n" +
               "\n".join(f"- {ratio}" for ratio in ASPECT_RATIOS.keys()) + "\n\n"
               "✨ *Pro Tip:* The more descriptive your prompt, the better the results!",
        parse_mode="Markdown"
    )

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("img", img_command))
    
    # Handle aspect ratio selection
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_aspect_ratio))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
