from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def homepage():

    return """
        <html>
            <head>
                <title>Welcome to FastAPI</title>
                <style>
                    body {
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        justify-content: center;
                        height: 100vh;
                        margin: 0;
                        font-family: Arial, sans-serif;
                        background-color: #f0f8ff;
                        color: #333;
                    }
                    h1 {
                        font-size: 3rem;
                        color: #4CAF50;
                    }
                    p {
                        font-size: 1.2rem;
                        text-align: center;
                    }
                    a {
                        color: #2196F3;
                        text-decoration: none;
                        font-weight: bold;
                    }
                    a:hover {
                        text-decoration: underline;
                    }
                </style>
            </head>
            <body>
                <h1>Hey there! 🎉</h1>
                <p>Welcome to the FastAPI project.</p>
                <p>Please visit the <a href="/docs">/docs</a> URL to explore the available APIs!</p>
            </body>
        </html>
        """
