
-- Views for 8 Groups of Teams
CREATE VIEW GroupATeams AS
	SELECT * FROM Teams WHERE Group_Name = 'A';
CREATE VIEW GroupBTeams AS
	SELECT * FROM Teams WHERE Group_Name = 'B';
CREATE VIEW GroupCTeams AS
	SELECT * FROM Teams WHERE Group_Name = 'C';
CREATE VIEW GroupDTeams AS
	SELECT * FROM Teams WHERE Group_Name = 'D';
CREATE VIEW GroupETeams AS
	SELECT * FROM Teams WHERE Group_Name = 'E';
CREATE VIEW GroupFTeams AS
	SELECT * FROM Teams WHERE Group_Name = 'F';
CREATE VIEW GroupGTeams AS
	SELECT * FROM Teams WHERE Group_Name = 'G';
CREATE VIEW GroupHTeams AS
	SELECT * FROM Teams WHERE Group_Name = 'H';
    
CREATE  OR REPLACE VIEW `productsForOrder` AS
SELECT * FROM football_worldcup_management.order NATURAL JOIN productsbought;
