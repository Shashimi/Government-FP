# rsync -avz --delete --delete-excluded --exclude **/text-versions/ govtrack.us::govtrackdata/congress/113/bills .
#votes
for i in range(112, 114) :
		command = "rsync -avz --delete --delete-excluded --exclude **/text-versions/ govtrack.us::govtrackdata/congress/" + str(i) + "/votes " + str(i) + " &"
		print command
#bills
for i in range(112, 114) :
		command = "rsync -avz --delete --delete-excluded --exclude **/text-versions/ govtrack.us::govtrackdata/congress/" + str(i) + "/bills " + str(i) + " &"
		print command
