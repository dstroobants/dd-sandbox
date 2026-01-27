var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", () => Results.Content("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hello World - Cat Edition</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            text-align: center;
            max-width: 600px;
            width: 100%;
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 2.5rem;
        }
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1rem;
        }
        .cat-container {
            position: relative;
            width: 100%;
            max-width: 400px;
            margin: 0 auto 20px;
            border-radius: 15px;
            overflow: hidden;
            background: #f0f0f0;
            min-height: 300px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        #cat-image {
            max-width: 100%;
            max-height: 400px;
            border-radius: 15px;
            transition: opacity 0.3s ease;
        }
        #cat-image.loading {
            opacity: 0.5;
        }
        .timer {
            color: #764ba2;
            font-size: 1rem;
            margin-top: 15px;
        }
        .refresh-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            font-size: 1rem;
            border-radius: 25px;
            cursor: pointer;
            margin-top: 20px;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .refresh-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
        .loader {
            display: none;
            width: 50px;
            height: 50px;
            border: 5px solid #f3f3f3;
            border-top: 5px solid #764ba2;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            position: absolute;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Hello World from IIS!</h1>
        <p class="subtitle">Featuring a random cat every 10 seconds</p>
        <div class="cat-container">
            <div class="loader" id="loader"></div>
            <img id="cat-image" src="https://cataas.com/cat?t=0" alt="Random Cat" />
        </div>
        <p class="timer">Next cat in <span id="countdown">10</span> seconds</p>
        <button class="refresh-btn" onclick="loadNewCat()">Get New Cat Now!</button>
    </div>

    <script>
        let countdown = 10;
        const countdownEl = document.getElementById('countdown');
        const catImage = document.getElementById('cat-image');
        const loader = document.getElementById('loader');

        function loadNewCat() {
            loader.style.display = 'block';
            catImage.classList.add('loading');
            
            // Add timestamp to prevent caching
            const newSrc = 'https://cataas.com/cat?t=' + Date.now();
            
            const tempImg = new Image();
            tempImg.onload = function() {
                catImage.src = newSrc;
                catImage.classList.remove('loading');
                loader.style.display = 'none';
            };
            tempImg.onerror = function() {
                catImage.classList.remove('loading');
                loader.style.display = 'none';
            };
            tempImg.src = newSrc;
            
            countdown = 10;
            countdownEl.textContent = countdown;
        }

        // Update countdown every second
        setInterval(() => {
            countdown--;
            if (countdown <= 0) {
                loadNewCat();
            } else {
                countdownEl.textContent = countdown;
            }
        }, 1000);
    </script>
</body>
</html>
""", "text/html"));

app.MapGet("/health", () => Results.Ok(new { status = "healthy", timestamp = DateTime.UtcNow }));

app.Run();
