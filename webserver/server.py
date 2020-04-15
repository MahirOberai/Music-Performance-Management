
"""
@author Mahir Oberai mo2654
@author Greg Sansolo gds2127

Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@35.243.220.243/proj1part2
#
# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://gravano:foobar@35.243.220.243/proj1part2"


DATABASEURI = "postgresql://gds2127:6010@35.231.103.173/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)


@app.before_request
def before_request():
  """  
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """ 
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """

  try:
    g.conn.close()
  except Exception as e:
    pass

#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print(request.args)

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  
  #context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html") #, **context) 

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
@app.route('/manager')
def manager():
  
  cursor = g.conn.execute("SELECT * FROM manager ORDER BY manager_id;")
  manager = []
  for result in cursor:
    manager.append([result['manager_id'], result['name']])
  cursor.close()

  context = dict(data = manager)

  return render_template("manager.html", **context)

@app.route('/artist')
def artist():

  cursor = g.conn.execute("SELECT * FROM artist ORDER BY artist_id;")
  artist = []
  for result in cursor:
    artist.append([result['artist_id'], result['manager_id'], result['name'], result['genre']])
  cursor.close()

  context = dict(data = artist)

  return render_template("artist.html", **context)

@app.route('/setlist')
def setlist():
  
  cursor = g.conn.execute("SELECT * FROM setlist ORDER BY setlist_id;")
  setlist = []
  for result in cursor:
    setlist.append([result['setlist_id'], result['artist_id'], result['song_id'], result['number_of_songs'], result['duration']])
  cursor.close()

  context = dict(data = setlist)

  return render_template("setlist.html", **context)

@app.route('/song')
def song():
  cursor = g.conn.execute("SELECT * FROM song ORDER BY song_id;")
  song = []
  for result in cursor:
    song.append([result['song_id'], result['title'], result['duration']])
  cursor.close()

  context = dict(data = song)

  return render_template("song.html", **context)  

@app.route('/venue')
def venue():

  cursor = g.conn.execute("SELECT * FROM venue ORDER BY venue_id;")
  venue = []
  for result in cursor:
    venue.append([result['venue_id'], result['name'], result['location']])
  cursor.close()

  context = dict(data = venue)

  return render_template("venue.html", **context)

@app.route('/seat')
def seat():
  
  cursor = g.conn.execute("SELECT * FROM seat ORDER BY seat_id;")
  seat = []
  for result in cursor:
    seat.append([result['seat_id'], result['venue_id']])
  cursor.close()

  context = dict(data = seat)

  return render_template("seat.html", **context)

@app.route('/ticket_holder')
def ticket_holder():
  
  cursor = g.conn.execute("SELECT * FROM ticket_holder ORDER BY holder_id;")
  ticket_holder = []
  for result in cursor:
    ticket_holder.append([result['holder_id'], result['venue_id'], result['seat_id'], result['name'], result['email']])
  cursor.close()

  context = dict(data = ticket_holder)

  return render_template("ticket_holder.html", **context) 

@app.route('/contains_song')
def contains_song():
  
  cursor = g.conn.execute("SELECT * FROM contains_song ORDER BY setlist_id;")
  contains_song = []
  for result in cursor:
    contains_song.append([result['setlist_id'], result['song_id']])
  cursor.close()

  context = dict(data = contains_song)

  return render_template("contains_song.html", **context)  

@app.route('/decides_venue')
def decides_venue():
  
  cursor = g.conn.execute("SELECT * FROM decides_venue ORDER BY manager_id;")
  decides_venue = []
  for result in cursor:
    decides_venue.append([result['manager_id'], result['venue_id']])
  cursor.close()

  context = dict(data = decides_venue)

  return render_template("decides_venue.html", **context) 

@app.route('/example1')
def example1():
  
  #This query displays the occupancies of the venues

  cursor = g.conn.execute("""
  SELECT v.name as venue_name, count(s.seat_id) as occupancy
  FROM seat s
  JOIN venue v ON v.venue_id = s.venue_id
  GROUP BY v.name
  ;""")
  venue_occupancy = []
  for result in cursor:
    venue_occupancy.append([result['venue_name'], result['occupancy']])
  cursor.close()

  context = dict(data = venue_occupancy)
  
  return render_template("example1.html", **context)

@app.route('/example2')
def example2():
  
  #This query displays the artists and sorts by genre

  cursor = g.conn.execute("""
  SELECT a.name as artist_name, a.genre as artist_genre, a.venue_id as venue_id
  FROM artist a
  ORDER BY artist_genre
  ;""")
  artists_by_genre = []
  for result in cursor:
    artists_by_genre.append([result['artist_name'], result['artist_genre'], result['venue_id']])
  cursor.close()

  context = dict(data = artists_by_genre)
  
  return render_template("example2.html", **context)

@app.route('/example3')
def example3():

  #This query displays the venues along with their artists, genres, setlist durations

  cursor = g.conn.execute("""
  SELECT v.name as venue_name, a.name as artist_name, a.genre as artist_genre, sl.duration as setlist_duration
  FROM venue v
  JOIN artist a on a.venue_id = v.venue_id
  JOIN setlist sl on sl.artist_id = a.artist_id
  GROUP BY venue_name, artist_name, artist_genre, setlist_duration
  ORDER BY venue_name
  ;""")
  venue_artists = []
  for result in cursor:
    venue_artists.append([result['venue_name'], result['artist_name'], result['artist_genre'], result['setlist_duration']])
  cursor.close()

  context = dict(data = venue_artists)
  
  return render_template("example3.html", **context)

@app.route('/example4')
def example4():

  #This query displays the venues along with their artists, genres, setlist durations

  cursor = g.conn.execute("""
  SELECT v.name as venue_name, sum(sl.duration) as total_duration
  FROM venue v
  JOIN artist a on a.venue_id = v.venue_id
  JOIN setlist sl on sl.artist_id = a.artist_id
  GROUP BY venue_name
  ORDER BY venue_name
  ;""")
  venue_durations = []
  for result in cursor:
    venue_durations.append([result['venue_name'], result['total_duration']])
  cursor.close()

  context = dict(data = venue_durations)
  
  return render_template("example4.html", **context)


#This method allows user to add rows to the decides_manager table
@app.route('/add', methods=['POST'])
def add():
  manager_id = request.form['manager_id']
  venue_id = request.form['venue_id']
  g.conn.execute('INSERT INTO decides_venue(manager_id, venue_id) VALUES (%s, %s)', manager_id, venue_id)
  return redirect('/decides_venue')

#This method allows user to update the email field given the holder name of the ticket_holder table
@app.route('/update', methods=['POST'])
def update():
  email = request.form['email']
  name = request.form['name']
  g.conn.execute('UPDATE ticket_holder SET email = (%s) WHERE name = (%s)', email, name)
  return redirect('/ticket_holder')  

#This method allows user to update the email field given the holder name of the ticket_holder table
@app.route('/update_artist_venue', methods=['POST'])
def update_artist_venue():
  venue_id = request.form['venue_id']
  artist_name = request.form['artist_name']
  g.conn.execute('UPDATE artist SET venue_id = (%s) WHERE name = (%s)', venue_id, artist_name)
  return redirect('/example2')   

@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='https://35.196.94.251')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()
