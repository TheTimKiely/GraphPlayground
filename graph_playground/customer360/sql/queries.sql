SELECT * FROM owes o
join customer c on c.customer_id = o.customer_id
join loan l on l.loan_id = o.loan_id;


drop table owns;
drop table owes;
drop table customer;
drop table account;
drop table accounts;
drop table credit_card;
drop table loan;