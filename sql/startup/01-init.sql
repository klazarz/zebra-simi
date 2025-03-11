 --privileged user
CONN system/<password>@freepdb1;


create user sh identified by <password>;


grant db_developer_role to sh;


grant unlimited tablespace to sh;



grant
   create any directory
to sh;

grant
   create mining model
to sh;


create or replace directory demo_py_dir as '/tmp';

grant read,write on directory demo_py_dir to sh;


exit;