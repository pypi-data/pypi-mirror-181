proc sql;
create table {temp_table} as
{sql};
quit;

filename file1 '{temp_filename}';
proc json nofmtcharacter nosastags out=file1;
export {temp_table};
run;

proc delete data={temp_table};
run;
