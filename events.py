from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from auth import authentication_required
from datetime import datetime
from models.user import User
from models.event import Event
from models.reminder import Reminder

bp = Blueprint("events", __name__)

# html templates
EVENT_INDEX_HTML = "events/index.html"
EVENT_CREATE_HTML = "events/create.html"
EVENT_UPDATE_HTML = "events/update.html"

# number of public events to display on the homepage
DISPLAY_CAPACITY = 10

@bp.route("/")
def events_index():
    """
    Home screen for sassi. Renders DISPLAY_CAPACITY public events.
    """
    public_events = Event.objects(public=True).limit(DISPLAY_CAPACITY)
    events_json = [e.to_json() for e in public_events]
    return render_template(EVENT_INDEX_HTML, events=public_events)

@bp.route("/events", methods=["GET"])
@authentication_required
def render_create_event():
    """
    Renders html for creating an event.
    """
    return render_template(EVENT_CREATE_HTML)


@bp.route("/events", methods=["POST"])
@authentication_required
def create_event():
    """
    Creates an event for the logged in user. 
    Events private by default.
    """
    title = request.form.get("title")
    public = request.form.get("public")
    date = request.form.get("date")
    time = request.form.get("time")
    description = request.form.get("description")

    # DEBUG
    # title_str = f"Title: {title}"
    # desc_str = f"Description: {description}"
    # date_str = f"Date: {date}\nDate type: {type(date)}"
    # time_str = f"Time: {time}\nTime type: {type(time)}"
    # pub_str = f"Public: {public}\nPublic type: {type(public)}"
    # print(f"Got event info:\n{title_str}\n{desc_str}\n{date_str}\n{time_str}\n{pub_str}")

    user_id = g.user.id
    user = User.objects(pk=user_id).first()

    try:
        event_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        Event(title=title,
             user=user,
             description=description,
             time=event_time,
             public=public).save()
    except Exception as e:
        flash(f"Catastrophic failure: {e}")

    return render_template(EVENT_INDEX_HTML)

@bp.route("/events/<int:event_id>", methods=["GET"])
@authentication_required
def render_update_event(event_id):
    """
    Renders html for updating an event.
    """
    event = get_event(event_id)
    return render_template(EVENT_UPDATE_HTML, event=event)
    
@bp.route("/events/<int:event_id>", methods=["PUT"])
@authentication_required
def update_event(event_id):
    """
    Updates existing event for logged in user.
    """
    event = get_event(event_id)

    title = request.form.get("title")
    description = request.form.get("description")
    time = request.form.get("time")
    public = request.form.get("public")

    if not title:
        flash("Event title required.")
        return render_update_event()

    if not time:
        flash("Event time required.")
        return render_update_event()

    try:
        event.title = title
        event.description = description
        event.time = time
        event.public = public
        event.save()
    except Exception as e:
        flash(f"Catastrophic failure: {e}")

    return render_update_event(event_id)

@bp.route("/events/<int:event_id>", methods=["DELETE"])
@authentication_required
def delete(event_id):
    event = get_event(event_id)
    event.delete()
    return redirect(url_for("events.events_index"))

def get_event(event_id, check_author=True):
    """
    Lookup an event by id in the database. Optionally verifies
    that the event belongs to the logged in user.
    """
    event = Event.objects(pk=event_id).first()

    if event is None:
        abort(404, f"Event with id {event.id} doesn't exist.")

    if check_author:
        if event.id != g.user.id:
            abort(403)

    return event

