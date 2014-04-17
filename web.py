from flask import Flask, render_template, redirect, request, url_for
import govapp
#set project root directory as the static folder, you can set others
app = Flask(__name__, static_url_path='', static_folder='static')

# @app.route("/")
# def index():
# 	user_list = model.session.query(model.User).limit(5).all()
# 	print "User list is ", len(user_list)
# 	return render_template("user_list.html", users=user_list)

#j.py is app object and used to map the fnx to the path /. this is done using
#the @app.route() decorator 


@app.route("/")
def index():
	#my_officials = govapp.session.query(Official).filter_by(name="some guy").all()
	return render_template("ReppinIt.html")
		#officials=my_officials)

#zip in my table 
#szipcode: variable 
#replst is the url it should route to
@app.route("/replst", methods=["POST"])
def repslist():
	if request.form.get("zipcode"): #jinja framework-html variable
		szipcode = int(request.form.get("zipcode"))# assigned the var
		z = govapp.session.query(govapp.Zip_code).filter_by(zip=szipcode).join(govapp.Zip_code.official).order_by(govapp.Official.rank).all()
	else:
		sbill = request.form.get("bills")
		
		# z = govapp.session.query.filter_by(govapp.Bill.like(sbill+'%')).all()
		z = govapp.session.query(govapp.Bill).filter(govapp.Bill.name.ilike(sbill+'%')).all()

# order by 
	off = []
	for dbbill in z:
		off.append(dbbill.official)

	# print "off", off

	#orange= name on html page
	#white=look above variable
	return render_template("replst.html", 	officials=off)
                                            	
@app.route('/rep_by_id/<int:id>')
def rep_by_id(id):
    #oneperson = request.form.get("representative")
    f = govapp.session.query(govapp.Official).filter_by(id=id).one()
    
    first_name = f.first_name
    # args_dict = {'last_name': f.last_name,
    # 'first_name' : f.first_name,
    # 'state' : f.state,
    # 'party_affiliation' : f.party_affiliation,
    # 'title' : f.title,
    # 'chamber' : f.title,
    # 'email' : f.email,
    # 'phone' : f.phone, 
    # 'address' : f.address,
    # 'facebook' : f.facebook,
    # 'twitter' : f.twitter }

    # f.update(args_dict)
  

    return render_template("rep_by_id.html", id=id, official=f, first_name=first_name)

@app.route('/rep_by_id', methods=["POST"])
def onerepresentative():
	
	representative = request.form.get("representative")
	last_name = representative.title()
	
	repp = govapp.session.query(govapp.Official).filter_by(last_name=last_name).first()
	repp_id = repp.id 
	# print representative, repp_id

	return redirect(url_for("rep_by_id", id=repp_id))
	# return render_template("rep_by_id.html", id=id)








# import os
# @app.route('/js/<path:path>')
# def static_proxy(path):
#     # send_static_file will guess the correct MIME type
#     return app.send_static_file(os.path.join('js', path))



# @app.route('/register' , methods=['GET','POST'])
# def register():
# 	retu
#     if request.method == 'GET':
#         return render_template('register.html')
#     user = User(request.form['username'] , request.form['password'],request.form['email'])
#     db.session.add(user)
#     db.session.commit()
#     flash('User successfully registered')
#     return redirect(url_for('login'))
 

if __name__ == "__main__":
	app.run(debug = True)


# official(/{{}})


# <!-- from google.html
# <html>
# <body>
# 	<p> my zipcode is {{ szipcode }}</p>
# </body>
# </html>

# {% for official in off %}
# 	{{off.first_name}}
# 	{{official.last_name}}
# 	{{official.title}}
# 	{{official.static/img/politician(official.id)}}
# {% endfor %}

# <img src="{{person.img}}" />

# #img src="static/img/{{pic}}.jpg"-- html page 


# <img src="/static/img/official.{{official.id}}.jpg" /> -->