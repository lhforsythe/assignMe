<img width="150" alt="image" src="https://github.com/user-attachments/assets/459a2e1e-0ac8-4b71-a860-8938cb6b5a6e" />

# assignMe
#### School assignment manager made with Python/Django/MySQL as a backend, and HTML/CSS/JS as frontend--wrapped in a Docker container. Works with Canvas and Blackboard. WIP.
<img width="721" alt="image" src="https://github.com/user-attachments/assets/d96dbf05-b0e5-40ee-8ed2-0a9e8fb7cb6f" /> <img height="598" alt="image" src="https://github.com/user-attachments/assets/b4236b0a-ec52-4c7b-9580-165a6751591c" />

Take a look at how it works -> https://www.youtube.com/embed/B85vgXKiDNA?si=HH0UuQOF8qPEkm3j

## Requirements:
``docker`` and ``docker-compose`` are required dependencies.

## How to Build Locally:
1. Clone repository with ``git clone https://github.com/lhforsythe/assignMe.git``
2. ``cd`` into the cloned project directory
3. Run ``docker compose -f Docker/docker-compose.yml up --build``
4. Visit ``localhost:8000`` to access the webapp.

## Page Map:
* ``/`` is the index of the webapp.
* ``/accounts/login`` is the user login page.
* ``/accounts/signup`` is the user creation page.
* ``/accounts/dashboard`` is the main view for the webapp (user must be signed in to view)
* ``/accounts/setup`` is the user setup page which requests Canvas or Blackboard session key (user is redirected here upon initial account creation)

#### Used for webapp logic via template POSTs:
* ``accounts/dashboard/filter`` is used to handle due date logic (i.e. <7 days until due)
* ``accounts/dashboard/completed/`` is used to handle "checking off" an assignment
* ``accounts/dashboard/toggleView`` is used to handle the view (row and grid) logic
* ``accounts/dashboard/addAssignment`` is used to handle the assignment add logic
* ``accounts/dashboard/changeHeader`` is used to handle the logic for changing the header photo
