-- Table names are flush left, and column definitions are
-- indented by at least one space or tab. Blank lines and
-- lines beginning with a double hyphen are comments.

department
    dept_id serial primary key
    name varchar(20) not null

branch
    branch_id integer generated always as identity primary key
    name varchar(20) not null
    address varchar(30)
    city varchar(20)
    state varchar(2)
    zip varchar(12)

employee
    emp_id integer generated always as identity primary key
    fname varchar(20) not null
    lname varchar(20) not null
    start_date date not null
    end_date date
    superior_emp_id smallint REFERENCES employee(emp_id)
    dept_id smallint REFERENCES department
    title varchar(20)
    assigned_branch_id smallint REFERENCES branch

product_type
    product_type_cd varchar(10) not null primary key
    name varchar(50) not null

product
    product_cd varchar(10) not null primary key
    name varchar(50) not null
    product_type_cd varchar(10) not null references product_type(product_type_cd)
    date_offered date
    date_retired date

-- manually run: CREATE TYPE customer_type AS ENUM('I', 'B');
customer
    cust_id integer generated always as identity primary key
    fed_id varchar(12) not null
    cust_type_cd customer_type not null
    address varchar(30)
    city varchar(20)
    state varchar(20)
    postal_code varchar(10)

individual
    cust_id integer references customer
    fname varchar(30) not null
    lname varchar(30) not null
    birth_date date

business
    cust_id integer references customer
    name varchar(40) not null
    state_id varchar(10) not null
    incorp_date date

officer
    officer_id integer generated always as identity primary key
    cust_id integer references customer
    fname varchar(30) not null
    lname varchar(30) not null
    title varchar(20)
    start_date date not null
    end_date date

-- manually run: CREATE TYPE account_status AS ENUM('ACTIVE','CLOSED','FROZEN');

account
    account_id integer generated always as identity primary key
    product_cd varchar(10) not null
    cust_id integer REFERENCES customer not null
    open_date date not null
    close_date date
    last_activity_date date
    status account_status
    open_branch_id smallint REFERENCES branch
    open_emp_id smallint REFERENCES employee(emp_id)
    avail_balance double precision
    pending_balance double precision

-- manually run: CREATE TYPE txn_type_cd AS ENUM('DBT','CDT');

transaction
    txn_id integer generated always as identity primary key
    txn_date timestamp not null
    account_id smallint REFERENCES account(account_id) not null
    txn_type_cd txn_type_cd
    amount double precision not null
    teller_emp_id smallint REFERENCES employee(emp_id)
    execution_branch_id smallint REFERENCES branch
    funds_avail_date timestamp
