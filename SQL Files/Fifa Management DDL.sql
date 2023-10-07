create database Football_WorldCup_Management;
use Football_WorldCup_Management;

CREATE TABLE `Football_Fan` (
  `CNIC` varchar(45),
  `First_Name` varchar(45),
  `Last_Name` varchar(45),
  `Age` int,
  `Email_Address` varchar(100),
  `password` varchar(20),
  `Gender` varchar(10),
  `userType` varchar(30),
  PRIMARY KEY (`CNIC`)
);



CREATE TABLE `Hotels` (
  `Hotel_Name` varchar(45),
  `singleBedPrice` double,
  `doubleBedPrice` double,
  `tripleBedPrice` double,
  `city` varchar(20),
  `address` varchar(50),
  PRIMARY KEY (`Hotel_Name`)
);

CREATE TABLE `Airlines` (
  `airline_code` varchar(20),
  `airline_name` varchar(45),
  `country` varchar(45),
  `telNo_help` varchar(30),
  PRIMARY KEY (`airline_code`)
);

CREATE TABLE `Flights` (
  `Flight_No` int auto_increment,
  `airline_code` varchar(20),
  `capacity` int,
  `arrivalCity` varchar(45),
  `departCity` varchar(45),
  `arrivalTime` datetime,
  `departTime` datetime,
  PRIMARY KEY (`Flight_No`),
  FOREIGN KEY (`airline_code`) REFERENCES `Airlines`(`airline_code`)
);

CREATE TABLE `SeatClasses` (
  `SeatClass` varchar(45),
  `startingPrice` int,
  PRIMARY KEY (`SeatClass`)
);

CREATE TABLE `FlightReservation` (
  `flight_reserve_id` int auto_increment,
  `Flight_No` int,
  `CNIC` varchar(45),
  `SeatClass` varchar(45),
  PRIMARY KEY (`flight_reserve_id`),
  FOREIGN KEY (`CNIC`) REFERENCES `Football_Fan`(`CNIC`),
  FOREIGN KEY (`Flight_No`) REFERENCES `Flights`(`Flight_No`),
  FOREIGN KEY (`SeatClass`) REFERENCES `SeatClasses`(`SeatClass`)
);

CREATE TABLE `Apartments` (
  `Apartment_Name` varchar(45),
  `pricePerUnit` double,
  `city` varchar(20),
  `address` varchar(50),
  PRIMARY KEY (`Apartment_Name`)
);

CREATE TABLE `AccommodationReservations` (
  `acc_reserve_id` int auto_increment,
  `Accommodation_Name` varchar(45),
  `CNIC` varchar(45),
  `Type` varchar(30),
  `No_of_Units_or_Rooms` int,
  `Check_In` datetime,
  `Check_Out` datetime,
  `Price` int,
  `No_of_days_staying` int,
  PRIMARY KEY (`acc_reserve_id`),
  FOREIGN KEY (`Accommodation_Name`) REFERENCES `Hotels`(`Hotel_Name`),
  FOREIGN KEY (`Accommodation_Name`) REFERENCES `Apartments`(`Apartment_Name`),
  FOREIGN KEY (`CNIC`) REFERENCES `Football_Fan`(`CNIC`)
);



CREATE TABLE `Order` (
  `order_No` int auto_increment,
  `CNIC` varchar(45),
  `order_datetime` datetime,
  `delivery_address` varchar(100),
  `city_of_delivery` varchar(45),
  `order_status` varchar(25),
  `totalPrice` double,
  PRIMARY KEY (`order_No`),
  FOREIGN KEY (`CNIC`) REFERENCES `Football_Fan`(`CNIC`)
);


CREATE TABLE `Stadiums` (
  `stadium_name` varchar(45),
  `city` varchar(45),
  `country` varchar(45),
  `capacity` int,
  PRIMARY KEY (`stadium_name`)
);

CREATE TABLE `Match_Schedule` (
  `Match_No` int auto_increment,
  `host_team` varchar(45),
  `opponent_team` varchar(45),
  `date_of_Match` datetime,
  `stadium` varchar(30),
  `city` varchar(45),
  PRIMARY KEY (`Match_No`),
  FOREIGN KEY (`stadium`) REFERENCES `Stadiums`(`stadium_name`)
);

CREATE TABLE `ApplicantStandTypes` (
  `AppType` varchar(45),
  `StandType` varchar(10),
  `ticketPrice` double,
  PRIMARY KEY (`AppType`, `StandType`)
);

CREATE TABLE `MatchTicket` (
  `match_ticket_id` int auto_increment,
  `Match_No` int,
  `CNIC` varchar(45),
  `ApplicantType` varchar(45),
  `stand` varchar(10),
  `totalPrice` int,
  PRIMARY KEY (`match_ticket_id`),
  FOREIGN KEY (`ApplicantType`,`stand` ) REFERENCES `ApplicantStandTypes`(`AppType`,`StandType` ),
  FOREIGN KEY (`CNIC`) REFERENCES `Football_Fan`(`CNIC`)
);

CREATE TABLE `category` (
  `product_category` varchar(45),
  `quantity` int,
  `category_description` varchar(255),
  PRIMARY KEY (`product_category`)
);

CREATE TABLE `fifaProducts` (
  `product_id` int auto_increment,
  `product_category` varchar(45),
  `product_name` varchar(20),
  `product_description` varchar(255),
  `price` double,
  PRIMARY KEY (`product_id`),
  FOREIGN KEY (`product_category`) REFERENCES `category`(`product_category`)
);

CREATE TABLE `ProductsBought` (
  `order_No` int,
  `product_id` int,
  PRIMARY KEY (`order_No`, `product_id`),
  FOREIGN KEY (`order_No`) REFERENCES `Order`(`order_No`),
  FOREIGN KEY (`product_id`) REFERENCES `fifaProducts`(`product_id`)
);

CREATE TABLE `Ticket` (
  `Ticket_No` int auto_increment,
  `CNIC` varchar(45),
  `acc_reserve_id` int,
  `flight_reserve_id` int,
  `match_ticket_id` int,
  `ticket_date` datetime,
  `totalPrice` int,
  PRIMARY KEY (`Ticket_No`),
  FOREIGN KEY (`CNIC`) REFERENCES `Football_Fan`(`CNIC`)
);


CREATE TABLE `Payments` (
  `payment_id` int auto_increment,
  `Ticket_No` int,
  `CNIC` varchar(45),
  `account_no` int,
  `payment_method` varchar(45),
  `payment_date` datetime,
  PRIMARY KEY (`payment_id`),
  FOREIGN KEY (`CNIC`) REFERENCES `Football_Fan`(`CNIC`)
);

CREATE TABLE `Manager` (
  `manager_name` varchar(45),
  `contract_date` datetime,
  `contract_expiry_date` datetime,
  `manager_salary` double,
  PRIMARY KEY (`manager_name`)
);

CREATE TABLE `Teams` (
  `team_name` varchar(45),
  `team_manager` varchar(45),
  `team_coach` varchar(45),
  `team_captain_id` int,
  `world_ranking` int,
  PRIMARY KEY (`team_name`),
  FOREIGN KEY (`team_manager`) REFERENCES `Manager`(`manager_name`)
);

CREATE TABLE `Players` (
  `player_id` int auto_increment,
  `player_number` int,
  `player_team` varchar(45),
  `player_name` varchar(45),
  `player_position` varchar(25),
  PRIMARY KEY (`player_id`),
  FOREIGN KEY (`player_team`) REFERENCES `Teams`(`team_name`)
);

CREATE TABLE `TeamStats` (
  `team_name` varchar(45),
  `matches_played` int,
  `wins` int,
  `losses` int,
  `draws` int,
  `goals_scored` int,
  `goals_conceded` int,
  `goals_difference` int,
  `worldcup_wins` int,
  `team_points` double,
  PRIMARY KEY (`team_name`),
  FOREIGN KEY (`team_name`) REFERENCES `Teams`(`team_name`)

);

CREATE TABLE `PlayerAwardList` (
  `player_id` int,
  `award_name` varchar(45),
  `year_of_award` int,
  PRIMARY KEY (`player_id`, `award_name`),
  FOREIGN KEY (`player_id`) REFERENCES `Players`(`player_id`)
);

CREATE TABLE `ManagerAwardList` (
  `manager_name` varchar(45),
  `award_name` varchar(45),
  `year_of_award` int,
  PRIMARY KEY (`manager_name`, `award_name`),
  FOREIGN KEY (`manager_name`) REFERENCES `Manager`(`manager_name`)
);

CREATE TABLE `WorldCupMatches` (
  `match_no` int auto_increment,
  `match_datetime` datetime,
  `team_one` varchar(45),
  `team_two` varchar(45),
  `team_one_score` int,
  `team_two_score` int,
  `stadium` varchar(30),
  PRIMARY KEY (`match_no`),
  FOREIGN KEY (`team_one`) REFERENCES `Teams`(`team_name`),
  FOREIGN KEY (`team_two`) REFERENCES `Teams`(`team_name`),
  FOREIGN KEY (`stadium`) REFERENCES `Stadiums`(`stadium_name`)
);


-- Altering Tables and Adding Foreign Key Constraints to some tables after creating them
ALTER TABLE Payments ADD CONSTRAINT Ticket_No FOREIGN KEY(Ticket_No) REFERENCES Ticket(Ticket_No);
ALTER TABLE Ticket ADD CONSTRAINT acc_reserve_id FOREIGN KEY(acc_reserve_id) REFERENCES accommodationreservations(acc_reserve_id),
	ADD CONSTRAINT flight_reserve_id FOREIGN KEY(flight_reserve_id) REFERENCES flightreservation(flight_reserve_id),
   	ADD CONSTRAINT match_ticket_id FOREIGN KEY(match_ticket_id) REFERENCES matchticket(match_ticket_id);
ALTER TABLE Match_Schedule ADD CONSTRAINT Host_Team FOREIGN KEY(Host_Team) REFERENCES Teams(team_name),
ADD CONSTRAINT Opponent_Team FOREIGN KEY(Opponent_Team) REFERENCES Teams(team_name);
ALTER TABLE Teams ADD COLUMN Group_Name char(1);
ALTER TABLE accommodationreservations ADD COLUMN status varchar(10);
ALTER TABLE flightreservation ADD COLUMN status varchar(10);
ALTER TABLE flightreservation MODIFY COLUMN status varchar(20);
ALTER TABLE matchticket ADD COLUMN status varchar(10);
ALTER TABLE flights modify arrivalTime varchar(45), modify departTime varchar(45);
ALTER TABLE match_schedule modify date_of_Match varchar(45);
ALTER TABLE football_worlcup_management.order MODIFY COLUMN order_datetime varchar(40);
ALTER TABLE AccommodationReservations MODIFY COLUMN Check_In varchar(40),
MODIFY COLUMN Check_Out varchar(40);
ALTER TABLE Ticket MODIFY COLUMN ticket_date varchar(40);
ALTER TABLE Payments MODIFY COLUMN payment_date varchar(40);
ALTER TABLE WorldCupMatches MODIFY match_datetime varchar(40);
ALTER TABLE accommodationreservations DROP COLUMN No_of_days_staying;

-- select CONSTRAINT_NAME
-- from INFORMATION_SCHEMA.TABLE_CONSTRAINTS
-- where TABLE_NAME = 'productsbought';

-- SELECT *
-- FROM INFORMATION_SCHEMA.COLUMNS
-- WHERE TABLE_NAME = 'hotelreservations'
--     AND COLUMN_NAME = 'hotel_reserve_id'
--     AND DATA_TYPE = 'int'
--     AND COLUMN_DEFAULT IS NULL
--     AND IS_NULLABLE = 'NO'
--     AND EXTRA like '%auto_increment%';


ALTER TABLE accommodationreservations DROP CONSTRAINT accommodationreservations_ibfk_1, 
	DROP CONSTRAINT accommodationreservations_ibfk_2, 
	DROP CONSTRAINT accommodationreservations_ibfk_3;

ALTER TABLE accommodationreservations RENAME AS hotelreservations;
ALTER TABLE accommodationreservations DROP COLUMN type;
ALTER TABLE accommodationreservations CHANGE COLUMN `acc_reserve_id` `hotel_reserve_id` INT auto_increment NULL DEFAULT NULL,
	CHANGE COLUMN `Accommodation_Name` `hotel_name` varchar(45) NULL DEFAULT NULL,
	CHANGE COLUMN `No_of_Units_or_Rooms` `No_of_Rooms` int NULL DEFAULT NULL;
    

ALTER TABLE Ticket DROP CONSTRAINT acc_reserve_id;

ALTER TABLE `football_worldcup_management`.`ticket` 
CHANGE COLUMN `acc_reserve_id` `hotel_reserve_id` INT NULL DEFAULT NULL;

ALTER TABLE hotelreservations ADD CONSTRAINT hotel_reserve_id FOREIGN KEY(hotel_name) REFERENCES hotels(Hotel_Name);
ALTER TABLE hotelreservations ADD CONSTRAINT cnic_fk FOREIGN KEY(CNIC) REFERENCES football_fan(CNIC);

ALTER TABLE Ticket ADD CONSTRAINT hotel_reserve_id_fk FOREIGN KEY(hotel_reserve_id) REFERENCES hotelreservations(hotel_reserve_id);

CREATE TABLE `AppartmentsReservations` (
  `apart_reserve_id` int auto_increment,
  `Apartment_Name` varchar(45),
  `CNIC` varchar(45),
  `No_of_Units` int,
  `Check_In` datetime,
  `Check_Out` datetime,
  `Price` int,
  `status` varchar(10),
  PRIMARY KEY (`apart_reserve_id`),
  FOREIGN KEY (`Apartment_Name`) REFERENCES `Apartments`(`Apartment_Name`),
  FOREIGN KEY (`CNIC`) REFERENCES `Football_Fan`(`CNIC`)
);
ALTER TABLE appartmentsreservations modify Check_In varchar(45), modify Check_Out varchar(45);
ALTER TABLE football_worldcup_management.fifaproducts modify product_name varchar(100);

ALTER TABLE seatclasses ADD COLUMN Flight_No int;
ALTER TABLE `football_worldcup_management`.`seatclasses` 
CHANGE COLUMN `Flight_No` `Flight_No` INT NOT NULL ,
DROP PRIMARY KEY,
ADD PRIMARY KEY (`SeatClass`, `Flight_No`);
;

-- SET foreign_key_checks = 0;
-- SET foreign_key_checks = 1;