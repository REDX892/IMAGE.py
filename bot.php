<?php
// Telegram Image Generation Bot in PHP
// Requires PHP 7.4+ with cURL extension

// Configuration
define('BOT_TOKEN', '7503914601:AAEODGqNNWvd7OVpdxNrXfF8zeo73yYdMpI');
define('API_URL', 'https://api.telegram.org/bot' . BOT_TOKEN . '/');
define('IMAGE_API_URL', 'https://1yjs1yldj7.execute-api.us-east-1.amazonaws.com/default/ai_image');

// Aspect ratio options with emojis
$ASPECT_RATIOS = [
    "🟦 1:1 (Square)" => "1:1",
    "🌄 16:9 (Wide)" => "16:9",
    "🎬 21:9 (Cinematic)" => "21:9",
    "📸 2:3 (Portrait)" => "2:3",
    "🏞️ 3:2 (Landscape)" => "3:2",
    "📱 4:5 (Portrait)" => "4:5",
    "📲 9:16 (Vertical)" => "9:16",
    "🎥 9:21 (Vertical Cinema)" => "9:21"
];

// Anime loading animations
$LOADING_ANIMATIONS = [
    "🎨 Painting your vision...",
    "✨ Adding magical touches...",
    "🖌️ Brush strokes in progress...",
    "🌈 Coloring outside the lines...",
    "🌀 Reality bending...",
    "⚡ Powering up creativity...",
    "🌌 Warping dimensions..."
];

// User states storage (in production, use a database)
$userStates = [];

// Helper function to send Telegram API requests
function sendTelegramRequest($method, $params = []) {
    $url = API_URL . $method;
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $params);
    $response = curl_exec($ch);
    curl_close($ch);
    return json_decode($response, true);
}

// Handle incoming updates
$update = json_decode(file_get_contents('php://input'), true);

if (isset($update['message'])) {
    $message = $update['message'];
    $chatId = $message['chat']['id'];
    $userId = $message['from']['id'];
    $text = $message['text'] ?? '';
    
    // Check if user is selecting aspect ratio
    if (isset($userStates[$userId]) {
        handleAspectRatioSelection($chatId, $userId, $text);
        return;
    }
    
    // Handle commands
    if (strpos($text, '/start') === 0) {
        sendWelcomeMessage($chatId);
    } elseif (strpos($text, '/help') === 0) {
        sendHelpMessage($chatId);
    } elseif (strpos($text, '/img') === 0) {
        handleImageCommand($chatId, $userId, $text);
    }
}

function sendWelcomeMessage($chatId) {
    $gifUrl = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDl1dWQ1b3V1ZGJmZ3Q5Z2N6eHZ5b2V6dG5zY2R6eGZxZ3V6aGZ5diZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/26n6WywJyh39n1pBu/giphy.gif";
    $caption = "✨ *Welcome to AnimeGen Bot!* ✨\nI can generate amazing anime-style images for you!\nUse /img command to start creating.\n\nExample: `/img mystical forest at sunset`";
    
    sendTelegramRequest('sendAnimation', [
        'chat_id' => $chatId,
        'animation' => $gifUrl,
        'caption' => $caption,
        'parse_mode' => 'Markdown'
    ]);
}

function sendHelpMessage($chatId) {
    global $ASPECT_RATIOS;
    
    $gifUrl = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcWJ5bWZxZ2N1a2JtY2JmZ3Q5Z2N6eHZ5b2V6dG5zY2R6eGZxZ3V6aGZ5diZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7TKTDn976uzhK1GM/giphy.gif";
    $aspectList = implode("\n", array_map(function($k) { return "- $k"; }, array_keys($ASPECT_RATIOS)));
    
    $caption = "🌟 *AnimeGen Bot Help* 🌟\n\n"
             . "🎨 *How to create images:*\n"
             . "1. Type `/img` followed by your creative prompt\n"
             . "   Example: `/img neon samurai in rain`\n"
             . "2. Select an aspect ratio from the options\n"
             . "3. Watch the magic happen!\n\n"
             . "📐 *Available Aspect Ratios:*\n$aspectList\n\n"
             . "✨ *Pro Tip:* The more descriptive your prompt, the better the results!";
    
    sendTelegramRequest('sendAnimation', [
        'chat_id' => $chatId,
        'animation' => $gifUrl,
        'caption' => $caption,
        'parse_mode' => 'Markdown'
    ]);
}

function handleImageCommand($chatId, $userId, $text) {
    global $userStates, $ASPECT_RATIOS;
    
    $prompt = trim(substr($text, 4));
    if (empty($prompt)) {
        $gifUrl = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcWJ5bWZxZ2N1a2JtY2JmZ3Q5Z2N6eHZ5b2V6dG5zY2R6eGZxZ3V6aGZ5diZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7TKTDn976uzhK1GM/giphy.gif";
        sendTelegramRequest('sendAnimation', [
            'chat_id' => $chatId,
            'animation' => $gifUrl,
            'caption' => "⚠️ *Please provide a prompt!* ⚠️\nUsage: `/img your creative description`\n\nExample: `/img cyberpunk city rain`",
            'parse_mode' => 'Markdown'
        ]);
        return;
    }
    
    // Store user state
    $userStates[$userId] = [
        'prompt' => $prompt,
        'waiting_for_ratio' => true
    ];
    
    // Create keyboard for aspect ratios
    $keyboard = array_chunk(array_keys($ASPECT_RATIOS), 2);
    $replyMarkup = [
        'keyboard' => $keyboard,
        'resize_keyboard' => true,
        'one_time_keyboard' => true
    ];
    
    $gifUrl = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcWJ5bWZxZ2N1a2JtY2JmZ3Q5Z2N6eHZ5b2V6dG5zY2R6eGZxZ3V6aGZ5diZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7TKTDn976uzhK1GM/giphy.gif";
    sendTelegramRequest('sendAnimation', [
        'chat_id' => $chatId,
        'animation' => $gifUrl,
        'caption' => "🎨 *Prompt received:* `$prompt`\n\n📐 *Please select an aspect ratio:*",
        'reply_markup' => json_encode($replyMarkup),
        'parse_mode' => 'Markdown'
    ]);
}

function handleAspectRatioSelection($chatId, $userId, $text) {
    global $userStates, $ASPECT_RATIOS, $LOADING_ANIMATIONS;
    
    if (!isset($userStates[$userId]['waiting_for_ratio']) {
        return;
    }
    
    if (!isset($ASPECT_RATIOS[$text])) {
        $gifUrl = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcWJ5bWZxZ2N1a2JtY2JmZ3Q5Z2N6eHZ5b2V6dG5zY2R6eGZxZ3V6aGZ5diZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7TKTDn976uzhK1GM/giphy.gif";
        sendTelegramRequest('sendAnimation', [
            'chat_id' => $chatId,
            'animation' => $gifUrl,
            'caption' => "❌ *Invalid selection!* ❌\nPlease choose an aspect ratio from the options.",
            'parse_mode' => 'Markdown'
        ]);
        return;
    }
    
    $aspectRatio = $ASPECT_RATIOS[$text];
    $prompt = $userStates[$userId]['prompt'];
    
    // Clean up user state
    unset($userStates[$userId]);
    
    // Send loading message
    $loadingMessage = $LOADING_ANIMATIONS[array_rand($LOADING_ANIMATIONS)] . " " . $text;
    $message = sendTelegramRequest('sendMessage', [
        'chat_id' => $chatId,
        'text' => $loadingMessage
    ]);
    
    // Generate image
    $imageUrl = generateImage($prompt, $aspectRatio);
    
    if ($imageUrl) {
        // Send success message
        $successGif = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcWJ5bWZxZ2N1a2JtY2JmZ3Q5Z2N6eHZ5b2V6dG5zY2R6eGZxZ3V6aGZ5diZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7TKTDn976uzhK1GM/giphy.gif";
        sendTelegramRequest('sendAnimation', [
            'chat_id' => $chatId,
            'animation' => $successGif,
            'caption' => "🎉 *Image generated successfully!* 🎉",
            'parse_mode' => 'Markdown'
        ]);
        
        // Send the image
        sendTelegramRequest('sendPhoto', [
            'chat_id' => $chatId,
            'photo' => $imageUrl,
            'caption' => "🖼️ *Your Anime-Style Creation:*\n"
                       . "📝 *Prompt:* `$prompt`\n"
                       . "📐 *Aspect Ratio:* $text\n\n"
                       . "✨ Want to create another? Use /img again!",
            'parse_mode' => 'Markdown'
        ]);
    } else {
        $errorGif = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcWJ5bWZxZ2N1a2JtY2JmZ3Q5Z2N6eHZ5b2V6dG5zY2R6eGZxZ3V6aGZ5diZlcD12MV9pbnRl
