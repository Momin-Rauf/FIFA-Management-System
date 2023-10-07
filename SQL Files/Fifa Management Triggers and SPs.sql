-- CREATE TRIGGER showUpdatedData AFTER UPDATE, INSERT, DELETE FOR EACH ROW ON teams, managers, managerawardlist, players, playerawardlist, playerstats, teamstats 
USE `football_worldcup_management`;

-- CREATING 3rd STORED PROCEDURE
DROP procedure IF EXISTS `new_procedure`;

DELIMITER $$
USE `football_worldcup_management`$$
CREATE PROCEDURE `new_procedure` (IN category varchar(45))
BEGIN
	SELECT * FROM FIFAProducts WHERE product_category = category;
END$$

DELIMITER ;

-- Altering 3rd Stored Procedure
USE `football_worldcup_management`;
DROP procedure IF EXISTS `football_worldcup_management`.`productcategoryproc`;
;

DELIMITER $$
USE `football_worldcup_management`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `productcategoryproc`(IN category varchar(45))
BEGIN
	SELECT * FROM FIFAProducts WHERE product_category = category;
END$$

DELIMITER ;
;

-- 4th Stored Procedure
USE `football_worldcup_management`;
DROP procedure IF EXISTS `storenotifyproc`;

DELIMITER $$
USE `football_worldcup_management`$$
CREATE PROCEDURE `storenotifyproc` (IN CNIC varchar(45))
BEGIN
	SELECT * FROM football_worldcup_management.order WHERE CNIC = CNIC AND order_status = 'confirmed';
    SELECT * FROM football_worldcup_management.order WHERE CNIC = CNIC AND order_status = 'not confirmed';
END$$

DELIMITER ;

USE `football_worldcup_management`;
DROP procedure IF EXISTS `football_worldcup_management`.`confirmedordersproc`;
;
-- Altering 4th Stored Procedure
DELIMITER $$
USE `football_worldcup_management`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `confirmedordersproc`(IN CNIC varchar(45))
BEGIN
	SELECT * FROM football_worldcup_management.order WHERE CNIC = CNIC AND order_status = 'confirmed';
END$$

DELIMITER ;
;

-- 5th Stored Procedure
USE `football_worldcup_management`;
DROP procedure IF EXISTS `unconfirmedorderproc`;

DELIMITER $$
USE `football_worldcup_management`$$
CREATE PROCEDURE `unconfirmedorderproc` (IN CNIC varchar(45))
BEGIN
	SELECT * FROM football_worldcup_management.order WHERE CNIC = CNIC AND order_status = 'not confirmed';
END$$

DELIMITER ;

-- 6th Stored Procedure
USE `football_worldcup_management`;
DROP procedure IF EXISTS `getProductPriceproc`;

DELIMITER $$
USE `football_worldcup_management`$$
CREATE PROCEDURE `getProductPriceproc` (IN product_id int)
BEGIN
	SELECT price FROM football_worldcup_management.fifaproducts WHERE product_id = product_id;
END$$

DELIMITER ;



