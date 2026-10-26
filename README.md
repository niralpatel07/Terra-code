# FocusList

**A to-do list with a built-in Pomodoro timer**

**DEMO LINK:** https://niral.pythonanywhere.com
Built with Python + Flask for [Hack Club Terra](https://terra.hackclub.com).

## Why I made it
My previous practice was to write tasks in one app and time myself in another. This FocusList app is therefore focused to enable you to plan in one place and be productive in the same place.

## Features

**Tasks**
- Add, edit, complete, and delete tasks
- Priorities (high, medium, low) shown as colored stripes on completed tasks which sink to the bottom of the completed list.
- Due dates with an overdue counter
- Filter by All / Active / Done, plus text search
- "Clear completed" and "Clear all"

**Focus timer**
- Focus (25 min) / short break (5 min) / long break (15 min) modes
- Start, pause, and reset
- Beep when a session ends
- Save finished focus sessions, and show sessions and minutes of today's tasks.

**Everything else**
- Dark mode that remembers your choice
- Data saved to JSON files so the program can be restarted with all previous work still there.
- Works on phone and desktop

## Tech stack
| Part | Tools |

| Backend | Python, Flask |
| Pages | Jinja templates, HTML, CSS |
| Timer | JavaScript (`fetch`, Web Audio API) |
| Storage | JSON files |
| Hosting | PythonAnywhere |

## Project structure
```
Terra-code/
├── app.py # routes, saving/loading, filters, sorting
├── templates/:
│ ─ index.html # task page
│ ─ timer.html # timer page + JavaScript
├── requirements.txt
└── README.md
```
`tasks.json` and `sessions.json` are created automatically the first time you use Terra-code.

## Running locally
First you will need to run:
```
git clone https://github.com/niralpatel07/Terra-code.git
cd Terra-code
pip install -r requirements.txt
python app.py
```
Then visit http://127.0.0.1:5000

## Issues faced and what I have learnt
The timer doesn't count down correctly so it's been changed to use the actual time rather than counting down once per second. This is done using Date.now().
If the file doesn't exist or is corrupted then it will not crash. It will use default values by calling load_data().
When I first deployed this I had issues with the buttons saving data. This was because the serverless deployment caused my files to be read only. I then deployed it using PythonAnywhere which uses a normal disk. The paths to my data have also been changed to absolute paths.
I couldn't use the browser console on my iPad so I added a status bar to the page to help me debug.
When reading errors always start at the bottom line.

## Limitations
There are no accounts so everyone viewing the live demo will see the same tasks. Please don't add any personal information.
Using JSON files works well for a small project but wouldn't scale if there were lots of users.
I have to renew my free host each month so the demo may not always be up.
## Features to add

[ ] Weekly focus target with progress bar
[ ] Focus stats page
[ ] Add user accounts with real database
[ ] Quiz mode
## Building

This was coded using my iPad. I used GitHub Codespaces during my first week of Terra. I used Claude (An AI assistant) as a teacher to help me write/debug my code. I tested, fixed and deployed my code myself.
-------------

Niral