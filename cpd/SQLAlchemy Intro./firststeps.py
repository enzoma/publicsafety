from sqlalchemy import *

# opens connection to database being used
dbV= create_engine('sqlite:///tutorial.db')
	# db = create_engine(engine://vbashyakarla:AtL3RET2TdLH@dssgpg:5432/vbashyakarla)
	# Format: db = create_engine(engine://user:password@host:port/database)
	# If I were connecting to the CPD database, use "CDP" in place of "vbashyakarla"
	# and ignore the stuff below 
dbV.echo = True  # Try changing this to True and see what happens

# Table definitions (col. names, their data types) are metadata
# Thus, the Metadata object manages this metadata.
# There are two types of metadata objects: bound and dynamic
metadata = MetaData(dbV)

# This creates a "users" table in the database.  It has 4 columns.
# The 4 columns are user_id, name, age, and password.
users = Table('users', metadata,
    Column('user_id', Integer, primary_key=True),
    Column('name', String(40)),
    Column('age', Integer),
    Column('password', String),
)
# users.create() # comment this out if the table was already created
# If the users table had already existed, we would've done:
# users = Table('users', metadata, autoload=True)
# instead

# The following line is a "SQL statement object, " which tells SQL
# to do something we want, and the execute() translates this into 
# raw SQL.  Here, we act on the users table created above.
i = users.insert()
# Calling the i.execute() tells SQLAlchemy to generate the 
# corresponding "INSERT INTO users VALUES (...)"
# We can choose which of the two syntatical forms below suits our
# preference; both are valid.
# Unfilled slots (eg: password) are filled with NULL by default, but
# the user_id (b/c it's the primary key) will be assigned a unique value.
i.execute(name='Mary', age=30, password='secret')
i.execute({'name': 'John', 'age': 42},
          {'name': 'Susan', 'age': 57},
          {'name': 'Carl', 'age': 33})
s = users.select()
# Selects users
rs = s.execute()
# Exectuing a select statement returns a result set (here, the filled
# in user data)

# View the first row of the users table!  Different syntatical options
row = rs.fetchone()
print 'Id:', row[0]
print 'Name:', row['name']
print 'Age:', row.age
print 'Password:', row[users.c.password]

# Run thru a forloop printing user names and ages
for row in rs:
    print row.name, 'is', row.age, 'years old'