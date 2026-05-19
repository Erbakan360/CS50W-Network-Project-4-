# CS50W-Network-Project-4 

A Twitter-like social network for posting and following users.

Key Features: Includes a global "All Posts" feed, individual profile pages with follower/following counts, and a personalized "Following" feed. Features include "liking" posts via AJAX (no page refresh) and the ability to edit existing posts inline.

Tech: JavaScript, Python, Django, SQL, HTML, CSS.

Requirements: https://cs50.harvard.edu/web/projects/4/network/

 Setup Instructions:
--------------------------------------------------
0. Download code/ Clone repository
   ```
   git clone https://github.com/Erbakan360/CS50W-Network-Project-4.git
   ```
1. Change directory to the wiki
   ```
   cd Network
   ```

2. Install dependencies:
   ```
   pip install django markdown2
   ```

3. Run database migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
  
4. Start the development server]
    ```
    python manage.py runserver
    ```
