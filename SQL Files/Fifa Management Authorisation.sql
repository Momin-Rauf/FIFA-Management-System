USE Football_WorldCup_Management;

-- Creating different types of Users for granting privileges
CREATE USER Football_Fan identified by 'fan';
CREATE USER Match_Ticketing_Mgr identified by 'tktmgr';
CREATE USER Flight_Reservation_Mgr identified by 'flightmgr';
CREATE USER Accommodation_Mgr identified by 'accmgr';
CREATE USER Fifa_Store_Mgr identified by 'fifastoremgr';
CREATE USER Match_Scheduling_Mgr identified by 'matchmgr';

-- Granting different privileges to different users
-- Privileges for Football_Fan (MOSTLY SELECT PRIVILEGES)
GRANT INSERT ON accommodationreservations to Football_Fan;
GRANT INSERT ON matchticket to Football_Fan;
GRANT INSERT ON flightreservation to Football_Fan;
GRANT INSERT,UPDATE ON football_fan to Football_Fan;
GRANT SELECT ON hotels to Football_Fan;
GRANT SELECT ON apartments to Football_Fan;
GRANT SELECT ON match_schedule to Football_Fan;
GRANT SELECT ON flights to Football_Fan;
GRANT SELECT ON airlines to Football_Fan;
GRANT SELECT ON applicantstandtypes to Football_Fan;
GRANT SELECT ON category to Football_Fan;
GRANT SELECT ON fifaproducts to Football_Fan;
GRANT SELECT ON managerawardlist to Football_Fan;
GRANT SELECT ON playerawardlist to Football_Fan;
GRANT SELECT ON players to Football_Fan;
GRANT SELECT ON productsbought to Football_Fan;
GRANT SELECT ON seatclasses to Football_Fan;
GRANT SELECT ON stadiums to Football_Fan;
GRANT SELECT ON teams to Football_Fan;
GRANT SELECT ON teamstats to Football_Fan;
GRANT SELECT ON ticket to Football_Fan;
GRANT SELECT ON worldcupmatches to Football_Fan;

-- PRIVILEGES for Match Ticketing Manager
GRANT INSERT, UPDATE, DELETE, SELECT ON matchticket TO Match_Ticketing_Mgr;
GRANT INSERT, UPDATE, DELETE, SELECT ON match_schedule TO Match_Ticketing_Mgr;
GRANT INSERT, UPDATE, DELETE, SELECT ON applicantstandtypes TO Match_Ticketing_Mgr;
GRANT INSERT, UPDATE, DELETE, SELECT ON payments TO Match_Ticketing_Mgr;
GRANT INSERT, UPDATE, DELETE, SELECT ON stadiums TO Match_Ticketing_Mgr;



-- PRIVILEGES for Flight Reservation Manager
GRANT INSERT, UPDATE, DELETE, SELECT ON flights TO Flight_Reservation_Mgr;
GRANT INSERT, UPDATE, DELETE, SELECT ON airlines TO Flight_Reservation_Mgr;
GRANT INSERT, UPDATE, DELETE, SELECT ON flightreservation TO Flight_Reservation_Mgr;
GRANT INSERT, UPDATE, DELETE, SELECT ON seatclasses TO Flight_Reservation_Mgr;
GRANT INSERT, UPDATE, DELETE, SELECT ON payments TO Match_Ticketing_Mgr;
GRANT INSERT, UPDATE, DELETE, SELECT ON ticket TO Match_Ticketing_Mgr;


-- PRIVILEGES for Accommodation Manager
GRANT INSERT, UPDATE, DELETE, SELECT ON accommodationreservations TO Accommodation_Mgr;
GRANT INSERT, UPDATE, DELETE, SELECT ON hotels TO Accommodation_Mgr;
GRANT INSERT, UPDATE, DELETE, SELECT ON apartments TO Accommodation_Mgr;
GRANT INSERT, UPDATE, DELETE, SELECT ON accommodationreservations TO Accommodation_Mgr;
GRANT INSERT, UPDATE, DELETE, SELECT ON payments TO Match_Ticketing_Mgr;
GRANT INSERT, UPDATE, DELETE, SELECT ON ticket TO Match_Ticketing_Mgr;

-- PRIVILEGES for FIFA Store Manager
GRANT INSERT, UPDATE, DELETE, SELECT ON fifaproducts TO Fifa_Store_Mgr;
GRANT INSERT, UPDATE, DELETE, SELECT ON football_worldcup_management.order TO Fifa_Store_Mgr;
GRANT INSERT, UPDATE, DELETE, SELECT ON productsbought TO Fifa_Store_Mgr;
GRANT INSERT, UPDATE, DELETE, SELECT ON category TO Fifa_Store_Mgr;

-- PRIVILEGES for Match Scheduling Manager
GRANT INSERT, UPDATE, DELETE, SELECT ON manager TO Match_Scheduling_Mgr;
GRANT INSERT, UPDATE, DELETE, SELECT ON managerawardlist TO Match_Scheduling_Mgr;
GRANT INSERT, UPDATE, DELETE, SELECT ON players TO Match_Scheduling_Mgr;
GRANT INSERT, UPDATE, DELETE, SELECT ON playerawardlist TO Match_Scheduling_Mgr;
GRANT INSERT, UPDATE, DELETE, SELECT ON teams TO Match_Scheduling_Mgr;
GRANT INSERT, UPDATE, DELETE, SELECT ON match_schedule TO Match_Scheduling_Mgr;
GRANT INSERT, UPDATE, DELETE, SELECT ON worlcupmatches TO Match_Scheduling_Mgr;
GRANT INSERT, UPDATE, DELETE, SELECT ON teamstats TO Match_Scheduling_Mgr;
GRANT INSERT, UPDATE, DELETE, SELECT ON playerstats TO Match_Scheduling_Mgr;
GRANT INSERT, UPDATE, DELETE, SELECT ON stadiums TO Match_Scheduling_Mgr;














