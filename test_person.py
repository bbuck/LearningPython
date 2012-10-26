from person import Person

brandon = Person()
success = brandon.load({"fname": "Brandon"})
if not success:
    print "Need to create entry"
    brandon.set({"fname": "Brandon", "lname": "Buck",
                 "address": {"street": "12345 Some Road", "city": "Shreveport",
                             "state": "LA", "zipcode": "71104"},
                 "phone_number": "111.555.1111"})
    brandon.save()


print brandon.display_info
