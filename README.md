# Speech Web App (Name TBD!)

This is a simple web application to aid with collection of labelled speech samples given a list of texts to be spoken

- Lightweight to deploy, no need for complicated deployment pipelines
- Authentication system to tag speech samples with a speaker-specific UUID
- Simple to add more texts to be spoken
- Local-first database using SQLite3


## Checklist
- [x] Basic authentication 
- [x] Upload `wav` file to Flask 
- [x] Utilize proper HTTP server
- [x] Enable HTTPS so that `mediaDevices` can be accessed outside `localhost`
- [ ] Proper configuration secret storage
- [ ] Ensure proper Flask app structure (blueprints, etc)
- [ ] Test cases 
- [ ] Store audio/video files in S3 or Google Cloud Storage 
- [ ] Better UI (possible transition to React)
- [ ] Admin console (nice-to-have)

## Adding More Text
If you require additional text to generate speech samples from, simply add a new `txt` file in the `text/` directory

## Collecting Data
All audio/video samples will be placed in a `data/` directory, where each subdirectory is a user's UUID, and each file inside `data/<user UUID>` is a file of form `<name of text>.webm`

## Installation
Simply clone this repo, install dependencies, and run the app with `gunicorn --bind 0.0.0.0:80 wsgi:app`