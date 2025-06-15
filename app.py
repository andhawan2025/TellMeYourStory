from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
import os
from datetime import timedelta

app = Flask(__name__)

# Configure session
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
Session(app)

# Character traits (same as in React app)
#ADJECTIVES = [
#    "Brave", "Mysterious", "Cheerful", "Wise", "Adventurous",
#    "Gentle", "Fierce", "Curious", "Loyal", "Witty",
#    "Compassionate", "Bold", "Clever", "Graceful", "Determined",
#    "Playful", "Noble", "Mischievous", "Confident", "Humble",
#    "Energetic", "Calm", "Ambitious", "Kind"
#]

def count_sentences(text):
    """Count the number of sentences in the text."""
    return len([s for s in text.split('.') if s.strip()])

@app.route('/')
def landing():
    """Landing page route."""
    return render_template('landing.html')

@app.route('/story', methods=['GET', 'POST'])
def story():
    """Story input page route."""
    if request.method == 'GET':
        # Clear session (so that all previous stories and session variables are cleared) on GET (i.e. when story.html is loaded)
        session.clear()
    if request.method == 'POST':
        story_text = request.form.get('story', '').strip()
        sentence_count = count_sentences(story_text)
        if not story_text:
            flash('Please enter your story', 'error')
            return redirect(url_for('story'))
        if sentence_count > 30:
            flash('Story must be 30 sentences or less', 'error')
            return redirect(url_for('story'))
        session['story'] = story_text
        return redirect(url_for('video'))
    return render_template('story.html', story=session.get('story', ''), sentence_count=count_sentences(session.get('story', '')))

@app.route('/generating', methods=['GET'])
def generating():
    """Route to render the generating_video template (simulating video generation)."""
    if 'story' not in session:
        return redirect(url_for('story'))
    return render_template('generating_video.html')

@app.route('/video', methods=['GET', 'POST'])
def video():
    """Video generation page route."""
    if 'story' not in session:
        return redirect(url_for('story'))
    if request.method == 'POST':
        # In a real app, this would trigger video generation (here we just set session['video_generated'] to true)
        session['video_generated'] = True
        return redirect(url_for('video'))
    if session.get('video_generated', False):
        return render_template('video.html', story=session.get('story', ''))
    else:
        return redirect(url_for('generating'))

@app.route('/reset', methods=['POST'])
def reset():
    """Reset the session and start over."""
    session.clear()
    return redirect(url_for('landing'))

if __name__ == '__main__':
    app.run(debug=True) 