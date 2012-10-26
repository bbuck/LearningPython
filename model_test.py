from person import Person

brandon = Person()
brandon.load({ "fname": "Brandon" })
kim = Person()
kim.load({ "fname": "Kim" })

print brandon.display_info
print "\n----------\n"
print kim.display_info