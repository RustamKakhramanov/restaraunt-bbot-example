module.exports = {
    apps: [
      {
        name: "bot", // Gunicorn process
        script: "python3",
        args: "src/bot/main.py",
        exec_mode: "fork",
        autorestart: true,
        watch: false,
        interpreter: "/home/truck-spot-backend/venv/bin/python",
      },
    ],
  };
