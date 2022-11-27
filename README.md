# profile_telegram_bot
When the user send a picture to the bot. At the first, it will crop an square picture from the center of the picture. Then, it will add the foreground.png to the square picture.
Finally the bot send the result back to the user.

# Initialize Database

Change PASSWORD in second line with a powerful password including uppercase and lowercase letters, numbers and symbols

```sql
CREATE DATABASE profilebot;
CREATE USER 'profilebot'@'localhost' IDENTIFIED BY 'PASSWORD';
GRANT ALL PRIVILEGES ON profilebot.* TO 'profilebot'@'localhost';
FLUSH PRIVILEGES;
```
