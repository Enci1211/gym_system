-- MySQL Script generated by MySQL Workbench
-- Thu Mar  9 11:48:03 2023
-- Model: Fitness Web App   Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema sweat_society_gym`
-- -----------------------------------------------------
DROP DATABASE IF EXISTS sweat_society_gym;
CREATE SCHEMA IF NOT EXISTS sweat_society_gym DEFAULT CHARACTER SET latin1 ;
USE sweat_society_gym ;


-- -----------------------------------------------------
-- Table `sweat_society_gym``.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sweat_society_gym`.`user` (
  `userid`  INT NOT NULL AUTO_INCREMENT,
  `password` VARCHAR(10) NOT NULL,
  `role` ENUM('admin','member','trainer') NOT NULL,
  PRIMARY KEY (`userid`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sweat_society_gym``.`member`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sweat_society_gym`.`member` (
  `member_id`INT NOT NULL AUTO_INCREMENT,
  `userid` INT NOT NULL,
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `phone` VARCHAR(10) NOT NULL,
  `address` VARCHAR(45) NOT NULL,
  `date_of_birth` DATE NULL,
  `subscription_status` TINYINT(1) NULL,
  `subscription_start_date` DATE NULL,
  `subscription_end_date` DATE NULL,
  `balance` DECIMAL(10,2) NULL,
  PRIMARY KEY (`member_id`),
  INDEX `userid_idx` (`userid` ASC),
  CONSTRAINT `userid`
    FOREIGN KEY (`userid`)
    REFERENCES `sweat_society_gym`.`user` (`userid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 10001;



-- -----------------------------------------------------
-- Table `sweat_society_gym`.`payment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sweat_society_gym`.`payment` (
  `payment_id` INT NOT NULL AUTO_INCREMENT,
  `member_id` INT NOT NULL,
  `amount` DECIMAL(10,2) NOT NULL,
  `date` DATE NOT NULL,
  `time` TIME NOT NULL,
  `type` VARCHAR(50) NOT NULL COMMENT 'subscription, personal training session',
  `status` VARCHAR(50) NOT NULL COMMENT 'paid, pending',
  PRIMARY KEY (`payment_id`),
  INDEX `member_id_idx` (`member_id` ASC),
  CONSTRAINT `member_id`
    FOREIGN KEY (`member_id`)
    REFERENCES `sweat_society_gym`.`member` (`userid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 10;


-- -----------------------------------------------------
-- Table `sweat_society_gym``.`trainer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sweat_society_gym`.`trainer` (
  `staff_id` INT NOT NULL AUTO_INCREMENT,
  `userid` INT NOT NULL,
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `phone` VARCHAR(10) NOT NULL,
  `address` VARCHAR(45) NULL,
  `date_of_birth` DATE NULL,
  `specialties` VARCHAR(45) NULL,
  PRIMARY KEY (`staff_id`),
  INDEX `userid_idx` (`userid` ASC),
  CONSTRAINT `userid_trainer`
    FOREIGN KEY (`userid`)
    REFERENCES `sweat_society_gym`.`user` (`userid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 1001;



-- -----------------------------------------------------
-- Table `sweat_society_gym``.`trainer_sessions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sweat_society_gym`.`trainer_sessions` (
  `sessions_id` VARCHAR(20) NOT NULL,
  `staff_id` INT NOT NULL,
  `date` DATE NOT NULL,
  `fee` DECIMAL(10,2) NOT NULL,
  `time` TIME NOT NULL,
  `session_status`ENUM('booked', 'available') NOT NULL DEFAULT 'available',
  PRIMARY KEY (`sessions_id`),
  INDEX `staff_id_idx` (`staff_id` ASC),
  CONSTRAINT `staff_id`
    FOREIGN KEY (`staff_id`)
    REFERENCES `sweat_society_gym`.`trainer` (`staff_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `ck_sessions_id_format`
    CHECK (`sessions_id` REGEXP '^TS[0-9]'))
ENGINE = InnoDB;

DELIMITER $$
CREATE TRIGGER `sweat_society_gym`.`trainer_sessions_BEFORE_INSERT` 
BEFORE INSERT ON `trainer_sessions` FOR EACH ROW 
BEGIN
  DECLARE lastId INT;
  SET lastId = (SELECT MAX(SUBSTR(sessions_id, 3)) FROM trainer_sessions WHERE sessions_id LIKE 'TS%');
  IF lastId IS NULL THEN
    SET NEW.sessions_id = 'TS1001';
  ELSE
    SET NEW.sessions_id = CONCAT('TS', LPAD(lastId + 1, 4, '0'));
  END IF;
END$$
DELIMITER ;



-- -----------------------------------------------------
-- Table `sweat_society_gym``.`group_class`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sweat_society_gym`.`group_class` (
  `class_id` VARCHAR(20)  NOT NULL,
  `userid` INT NOT NULL,
  `class_name` VARCHAR(255) NOT NULL,
  `date` DATE NOT NULL,
  `time` TIME NOT NULL,
  `book_space` INT NOT NULL,
  `max_space` INT NOT NULL DEFAULT 30,
  PRIMARY KEY (`class_id`),
  CONSTRAINT `trainer`
    FOREIGN KEY (`userid`)
    REFERENCES `sweat_society_gym`.`trainer` (`userid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `ck_class_id_format`
    CHECK (`class_id` REGEXP '^GC[0-9]'))
ENGINE = InnoDB;

DELIMITER $$
CREATE TRIGGER `sweat_society_gym`.`group_class_BEFORE_INSERT` 
BEFORE INSERT ON `group_class` FOR EACH ROW 
BEGIN
  DECLARE lastId INT;
  SET lastId = (SELECT MAX(SUBSTR(class_id, 3)) FROM group_class WHERE class_id LIKE 'GC%');
  IF lastId IS NULL THEN
    SET NEW.class_id = 'GC1001';
  ELSE
    SET NEW.class_id = CONCAT('GC', LPAD(lastId + 1, 4, '0'));
  END IF;
END$$
DELIMITER ;


-- -----------------------------------------------------
-- Table `sweat_society_gym``.`attendance`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sweat_society_gym`.`attendance` (
    `attendance_id` INT NOT NULL AUTO_INCREMENT,
    `member_id` INT NOT NULL,
    `date` DATE NOT NULL,
    `timein` TIME NULL,
    `timeout` TIME NULL,
    PRIMARY KEY (`attendance_id`),
    CONSTRAINT `fk_attendance_member_id`
        FOREIGN KEY (`member_id`)
        REFERENCES `sweat_society_gym`.`member`(`userid`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION) 
ENGINE = InnoDB
AUTO_INCREMENT = 101;


-- -----------------------------------------------------
-- Table `sweat_society_gym``.`booking`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sweat_society_gym`.`booking` (
  `booking_id` INT NOT NULL AUTO_INCREMENT,
  `class_id` VARCHAR(20) NULL,
  `session_id` VARCHAR(20) NULL,
  `date` DATE NOT NULL,
  `booking_status` ENUM('booked', 'completed','no-show') NOT NULL,
  `member_id` INT NOT NULL,
  PRIMARY KEY (`booking_id`),
  FOREIGN KEY (`session_id`) REFERENCES `sweat_society_gym`.`trainer_sessions` (`sessions_id`) ON DELETE CASCADE,
    FOREIGN KEY (`class_id`) REFERENCES `sweat_society_gym`.`group_class` (`class_id`) ON DELETE CASCADE,
    FOREIGN KEY (`member_id`) REFERENCES `sweat_society_gym`.`member` (`userid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION) 
    ENGINE = InnoDB;

-- -----------------------------------------------------
-- INSERT DATA in the model
-- -----------------------------------------------------


-- Inserting data into user table
INSERT INTO `sweat_society_gym`.`user` (`userid`,`password`, `role`) VALUES
(1, 'aaa000', 'admin'),
(1001, 'aaa000', 'member'),
(1002, 'aaa000', 'member'),
(1003, 'aaa000', 'member'),
(1004, 'aaa000', 'member'),
(1005, 'aaa000', 'member'),
(1006, 'aaa000', 'member'),
(1007, 'aaa000', 'member'),
(1008, 'aaa000', 'member'),
(1009, 'aaa000', 'member'),
(1010, 'aaa000', 'member'),
(1011, 'aaa000', 'member'),
(2001, 'aaa000', 'trainer'),
(2002, 'aaa000', 'trainer'),
(2003, 'aaa000', 'trainer'),
(2004, 'aaa000', 'trainer'),
(2005, 'aaa000', 'trainer');


-- Inserting data into member table
INSERT INTO `member` (`userid`, `first_name`, `last_name`, `email`, `phone`, `address`, `date_of_birth`, `subscription_status`, `subscription_start_date`, `subscription_end_date`, `balance`) VALUES 
(1001, 'John', 'Doe', 'johndoe@example.com', '555-1234', '123 Main St, Anytown, USA', '1990-01-01', 1, '2022-01-01', '2023-03-20', 0),
(1002, 'Jane', 'Doe', 'janedoe@example.com', '555-5678', '456 High St, Anytown, USA', '1995-06-15', 1, '2022-01-01', '2023-03-20', -40),
(1003, 'Bob', 'Smith', 'bobsmith@example.com', '555-9876', '789 Elm St, Anytown, USA', '1985-11-30', 0, '2022-01-01', '2023-03-20', -40),
(1004, 'Sarah', 'Johnson', 'sarahjohnson@example.com', '555-4321', '987 Oak St, Anytown, USA', '2000-04-23', 1, '2022-01-01', '2023-03-20', 0),
(1005, 'Michael', 'Lee', 'michaellee@example.com', '555-8765', '321 Maple St, Anytown, USA', '1978-09-05', 1, '2022-01-01', '2023-03-20', -40),
(1006, 'Emily', 'Davis', 'emilydavis@example.com', '555-2345', '234 Pine St, Anytown, USA', '1992-07-10', 1, '2022-01-01', '2023-03-20', -20),
(1007, 'David', 'Brown', 'davidbrown@example.com', '555-6543', '567 Cedar St, Anytown, USA', '1980-03-20', 1, '2022-01-01', '2023-03-20', -20),
(1008, 'Ava', 'Wilson', 'avawilson@example.com', '555-7890', '890 Birch St, Anytown, USA', '1997-12-12', 1, '2022-01-01', '2023-03-20', -40),
(1009, 'Oliver', 'Taylor', 'olivertaylor@example.com', '555-3456', '345 Oak St, Anytown, USA', '1975-04-09', 1, '2022-01-01', '2023-03-20', -20),
(1010, 'Emma', 'Anderson', 'emmaanderson@example.com', '555-9012', '678 Cedar St, Anytown, USA', '1999-10-28', 1, '2022-01-01', '2023-03-20', 0),
(1011, 'William', 'Martin', 'williammartin@example.com', '555-6789', '901 Pine St, Anytown, USA', '1994-02-14', 1, '2022-01-01','2023-03-20', 0);

 
-- Inserting data into payment table
INSERT INTO payment (member_id, amount, date, time, type, status)
VALUES
(1002, 50.0, '2023-01-01', '10:00:00', 'subscription', 'paid'),
(1002, 20.0, '2023-01-01', '11:00:00', 'personal training session', 'paid'),
(1003, 50.0, '2023-01-01', '12:00:00', 'subscription', 'paid'),
(1002, 50.0, '2023-02-01', '10:00:00', 'subscription', 'pending'),
(1002, 30.0, '2023-02-01', '11:00:00', 'personal training session', 'pending'),
(1003, 60.0, '2023-02-01', '12:00:00', 'subscription', 'pending'),
(1004, 40.0, '2023-02-02', '13:00:00', 'subscription', 'paid'),
(1005, 25.0, '2023-02-02', '14:00:00', 'personal training session', 'pending'),
(1006, 30.0, '2023-02-03', '15:00:00', 'subscription', 'transferred'),
(1007, 20.0, '2023-02-03', '16:00:00', 'personal training session', 'pending'),
(1008, 35.0, '2023-02-04', '17:00:00', 'subscription', 'paid'),
(1009, 45.0, '2023-02-04', '18:00:00', 'personal training session', 'paid'),
(1010, 40.0, '2023-02-05', '19:00:00', 'subscription', 'pending'),
(1001, 30.0, '2023-02-05', '20:00:00', 'personal training session', 'pending'),
(1002, 50.0, '2023-02-06', '10:00:00', 'subscription', 'paid'),
(1003, 20.0, '2023-02-06', '11:00:00', 'personal training session', 'paid'),
(1003, 20.0, '2023-03-06', '11:00:00', 'personal training session', 'paid');

-- Inserting data into trainer table
INSERT INTO `sweat_society_gym`.`trainer`
(`userid`, `first_name`, `last_name`, `email`, `phone`, `address`, `date_of_birth`, `specialties`)
VALUES
(2001, 'John', 'Doe', 'john.doe@gmail.com', '555-1234', '123 Main St', '1985-01-01', 'Weightlifting'),
(2002, 'Jane', 'Doe', 'jane.doe@gmail.com', '555-5678', '456 High St', '1987-02-02', 'Yoga'),
(2003, 'Bob', 'Smith', 'bob.smith@gmail.com', '555-9876', '789 Pine St', '1990-03-03', 'Cardio'),
(2004, 'Sarah', 'Johnson', 'sarah.johnson@gmail.com', '555-2468', '321 Oak St', '1992-04-04', 'Pilates'),
(2005, 'David', 'Lee', 'david.lee@gmail.com', '555-1357', '555 Elm St', '1995-05-05', 'CrossFit');



-- Inserting data into trainer_sessions table
INSERT INTO `trainer_sessions` (`staff_id`, `date`, `fee`, `time`, `session_status`)
VALUES 
(2001, '2023-03-15', 50.00, '09:00:00', 'available'),
(2001, '2023-03-15', 50.00, '10:00:00', 'booked'),
(2001, '2023-03-15', 50.00, '11:00:00', 'booked'),
(2002, '2023-03-16', 60.00, '12:00:00', 'booked'),
(2002, '2023-03-16', 60.00, '13:00:00', 'booked'),
(2002, '2023-03-16', 60.00, '14:00:00', 'booked'),
(2003, '2023-03-17', 40.00, '15:00:00', 'booked'),
(2003, '2023-03-17', 40.00, '16:00:00', 'booked'),
(2003, '2023-03-17', 40.00, '17:00:00', 'booked'),
(2004, '2023-03-18', 70.00, '18:00:00', 'booked'),
(2004, '2023-03-18', 70.00, '19:00:00', 'booked'),
(2004, '2023-03-18', 70.00, '20:00:00', 'booked'),
(2005, '2023-03-19', 80.00, '10:00:00', 'booked'),
(2005, '2023-03-19', 80.00, '11:00:00', 'booked'),
(2005, '2023-03-19', 80.00, '12:00:00', 'booked'),
(2001, '2023-03-20', 50.00, '09:00:00', 'booked'),
(2001, '2023-03-20', 50.00, '10:00:00', 'booked'),
(2001, '2023-03-20', 50.00, '11:00:00', 'available'),
(2002, '2023-03-21', 60.00, '12:00:00', 'booked'),
(2002, '2023-03-21', 60.00, '13:00:00', 'booked'),
(2002, '2023-03-21', 60.00, '14:00:00', 'available'),
(2003, '2023-03-22', 40.00, '15:00:00', 'booked'),
(2003, '2023-03-22', 40.00, '16:00:00', 'available'),
(2003, '2023-03-22', 40.00, '17:00:00', 'available'),
(2004, '2023-03-23', 70.00, '18:00:00', 'booked'),
(2004, '2023-03-23', 70.00, '19:00:00', 'booked'),
(2004, '2023-03-23', 70.00, '20:00:00', 'available'),
(2005, '2023-03-24', 80.00, '10:00:00', 'booked'),
(2005, '2023-03-24', 80.00, '11:00:00', 'booked'),
(2005, '2023-03-24', 80.00, '12:00:00', 'available'),
(2001, '2023-03-25', 50.00, '14:00:00', 'booked'),
(2001, '2023-03-25', 50.00, '15:00:00', 'available'),
(2001, '2023-03-25', 50.00, '16:00:00', 'available'),
(2002, '2023-03-26', 60.00, '14:00:00', 'booked'),
(2002, '2023-03-26', 60.00, '15:00:00', 'available'),
(2002, '2023-03-26', 60.00, '16:00:00', 'available'),
(2003, '2023-03-26', 40.00, '14:00:00', 'booked'),
(2003, '2023-03-26', 40.00, '15:00:00', 'available'),
(2003, '2023-03-26', 40.00, '16:00:00', 'available'),
(2004, '2023-03-30', 70.00, '14:00:00', 'available'),
(2004, '2023-03-30', 70.00, '15:00:00', 'available'),
(2004, '2023-03-30', 70.00, '16:00:00', 'available'),
(2005, '2023-03-31', 80.00, '14:00:00', 'available'),
(2005, '2023-03-31', 80.00, '15:00:00', 'available'),
(2005, '2023-03-31', 80.00, '16:00:00', 'available'),
(2001, '2023-04-02', 55.00, '14:00:00', 'available'),
(2001, '2023-04-02', 55.00, '15:00:00', 'available'),
(2001, '2023-04-02', 55.00, '16:00:00', 'available'),
(2002, '2023-04-03', 65.00, '14:00:00', 'available'),
(2002, '2023-04-03', 65.00, '15:00:00', 'available'),
(2002, '2023-04-03', 65.00, '16:00:00', 'available'),
(2001, '2023-04-04', 50.00, '14:00:00', 'available'),
(2001, '2023-04-04', 50.00, '15:00:00', 'available'),
(2001, '2023-04-04', 50.00, '16:00:00', 'available'),
(2002, '2023-04-05', 60.00, '17:00:00', 'available'),
(2002, '2023-04-05', 60.00, '18:00:00', 'available'),
(2002, '2023-04-05', 60.00, '19:00:00', 'available'),
(2003, '2023-04-06', 40.00, '14:00:00', 'available'),
(2003, '2023-04-06', 40.00, '15:00:00', 'available'),
(2003, '2023-04-06', 40.00, '16:00:00', 'available'),
(2004, '2023-04-07', 70.00, '17:00:00', 'available'),
(2004, '2023-04-07', 70.00, '18:00:00', 'available'),
(2004, '2023-04-07', 70.00, '19:00:00', 'available'),
(2005, '2023-04-08', 80.00, '14:00:00', 'available'),
(2005, '2023-04-08', 80.00, '15:00:00', 'available'),
(2005, '2023-04-08', 80.00, '16:00:00', 'available'),
(2001, '2023-04-09', 55.00, '14:00:00', 'available'),
(2001, '2023-04-09', 55.00, '15:00:00', 'available'),
(2001, '2023-04-09', 55.00, '16:00:00', 'available'),
(2002, '2023-04-10', 65.00, '17:00:00', 'available'),
(2002, '2023-04-10', 65.00, '18:00:00', 'available'),
(2002, '2023-04-10', 65.00, '19:00:00', 'available'),
(2003, '2023-04-11', 45.00, '14:00:00', 'available'),
(2003, '2023-04-11', 45.00, '15:00:00', 'available'),
(2003, '2023-04-11', 45.00, '16:00:00', 'available'),
(2002, '2023-04-12', 60.00, '17:00:00', 'available'),
(2002, '2023-04-12', 60.00, '18:00:00', 'available'),
(2002, '2023-04-12', 60.00, '19:00:00', 'available'),
(2003, '2023-04-13', 40.00, '14:00:00', 'available'),
(2003, '2023-04-13', 40.00, '15:00:00', 'available'),
(2003, '2023-04-13', 40.00, '16:00:00', 'available'),
(2004, '2023-04-14', 70.00, '17:00:00', 'available'),
(2004, '2023-04-14', 70.00, '18:00:00', 'available'),
(2004, '2023-04-14', 70.00, '19:00:00', 'available'),
(2005, '2023-04-15', 80.00, '14:00:00', 'available'),
(2005, '2023-04-15', 80.00, '15:00:00', 'available'),
(2005, '2023-04-15', 80.00, '16:00:00', 'available'),
(2001, '2023-04-16', 55.00, '14:00:00', 'available'),
(2001, '2023-04-16', 55.00, '15:00:00', 'available'),
(2001, '2023-04-16', 55.00, '16:00:00', 'available');



-- Inserting data into group_class table
INSERT INTO `group_class` (`userid`, `class_name`, `date`, `time`, `book_space`, `max_space`) VALUES
(2001, 'Yoga', '2023-03-13', '09:00:00', 15, 30),
(2002, 'Pilates', '2023-03-13', '10:00:00', 20, 30),
(2003, 'Zumba', '2023-03-13', '11:00:00', 10, 30),
(2004, 'Spinning', '2023-03-13', '12:00:00', 10, 30),
(2005, 'Kickboxing', '2023-03-13', '13:00:00', 12, 30),
(2001, 'Yoga', '2023-03-14', '09:00:00', 15, 30),
(2002, 'Pilates', '2023-03-14', '10:00:00', 16, 30),
(2003, 'Zumba', '2023-03-14', '11:00:00', 18, 30),
(2004, 'Spinning', '2023-03-14', '12:00:00', 20, 30),
(2005, 'Kickboxing', '2023-03-14', '13:00:00', 10, 30),
(2001, 'Yoga', '2023-03-15', '09:00:00', 20, 30),
(2002, 'Pilates', '2023-03-15', '10:00:00', 10, 30),
(2003, 'Zumba', '2023-03-15', '11:00:00', 28, 30),
(2004, 'Spinning', '2023-03-15', '12:00:00', 5, 30),
(2005, 'Kickboxing', '2023-03-15', '13:00:00', 8, 30),
(2001, 'Yoga', '2023-03-16', '09:00:00', 10, 30),
(2002, 'Pilates', '2023-03-16', '10:00:00', 12, 30),
(2003, 'Zumba', '2023-03-16', '11:00:00', 15, 30),
(2004, 'Spinning', '2023-03-16', '12:00:00', 12, 30),
(2005, 'Kickboxing', '2023-03-16', '13:00:00', 14, 30),
(2001, 'Yoga', '2023-03-17', '09:00:00', 16, 30),
(2002, 'Pilates', '2023-03-17', '10:00:00', 18, 30),
(2003, 'Zumba', '2023-03-17', '11:00:00', 12, 30),
(2004, 'Spinning', '2023-03-17', '12:00:00', 10, 30),
(2005, 'Kickboxing', '2023-03-17', '13:00:00', 19, 30),
(2001, 'Yoga', '2023-03-18', '09:00:00', 20, 30),
(2002, 'Pilates', '2023-03-18', '10:00:00', 12, 30),
(2003, 'Zumba', '2023-03-18', '11:00:00', 18, 30),
(2004, 'Spinning', '2023-03-18', '12:00:00', 10, 30),
(2005, 'Kickboxing', '2023-03-18', '13:00:00', 9, 30),
(2001, 'Yoga', '2023-03-19', '09:00:00', 10, 30),
(2002, 'Pilates', '2023-03-19', '10:00:00', 23, 30),
(2003, 'Zumba', '2023-03-19', '11:00:00', 21, 30),
(2004, 'Spinning', '2023-03-19', '12:00:00', 18, 30),
(2005, 'Kickboxing', '2023-03-19', '13:00:00', 15, 30),
(2001, 'Yoga', '2023-03-20', '09:00:00', 29, 30),
(2002, 'Pilates', '2023-03-20', '10:00:00', 18, 30),
(2003, 'Zumba', '2023-03-20', '11:00:00', 15, 30),
(2004, 'Spinning', '2023-03-20', '12:00:00', 15, 30),
(2005, 'Kickboxing', '2023-03-20', '13:00:00', 19, 30),
(2001, 'Yoga', '2023-03-21', '09:00:00', 23, 30),
(2002, 'Pilates', '2023-03-21', '10:00:00', 25, 30),
(2003, 'Zumba', '2023-03-21', '11:00:00', 25, 30),
(2004, 'Spinning', '2023-03-21', '12:00:00', 30, 30),
(2005, 'Kickboxing', '2023-03-21', '13:00:00', 21, 30),
(2001, 'Yoga', '2023-03-22', '09:00:00', 18, 30),
(2002, 'Pilates', '2023-03-22', '10:00:00', 10, 30),
(2003, 'Zumba', '2023-03-22', '11:00:00', 30, 30),
(2004, 'Spinning', '2023-03-22', '12:00:00', 16, 30),
(2005, 'Kickboxing', '2023-03-22', '13:00:00', 18, 30),
(2001, 'Yoga', '2023-03-23', '09:00:00', 20, 30),
(2002, 'Pilates', '2023-03-23', '10:00:00', 19, 30),
(2003, 'Zumba', '2023-03-23', '11:00:00', 30, 30),
(2004, 'Spinning', '2023-03-23', '12:00:00', 28, 30),
(2005, 'Kickboxing', '2023-03-23', '13:00:00', 19, 30),
(2001, 'Yoga', '2023-03-24', '09:00:00', 22, 30),
(2002, 'Pilates', '2023-03-24', '10:00:00', 23, 30),
(2003, 'Zumba', '2023-03-24', '11:00:00', 21, 30),
(2004, 'Spinning', '2023-03-24', '12:00:00', 19, 30),
(2005, 'Kickboxing', '2023-03-24', '13:00:00', 17, 30),
(2001, 'Yoga', '2023-03-25', '09:00:00', 16, 30),
(2002, 'Pilates', '2023-03-25', '10:00:00', 20, 30),
(2003, 'Zumba', '2023-03-25', '11:00:00', 21, 30),
(2004, 'Spinning', '2023-03-25', '12:00:00', 10, 30),
(2005, 'Kickboxing', '2023-03-25', '13:00:00', 28, 30),
(2001, 'Yoga', '2023-03-26', '09:00:00', 25, 30),
(2002, 'Pilates', '2023-03-26', '10:00:00', 22, 30),
(2003, 'Zumba', '2023-03-26', '11:00:00', 23, 30),
(2004, 'Spinning', '2023-03-26', '12:00:00', 21, 30),
(2005, 'Kickboxing', '2023-03-26', '13:00:00', 19, 30),
(2001, 'Yoga', '2023-03-27', '09:00:00', 0, 30),
(2002, 'Pilates', '2023-03-27', '10:00:00', 0, 30),
(2003, 'Zumba', '2023-03-27', '11:00:00', 0, 30),
(2004, 'Spinning', '2023-03-27', '12:00:00', 0, 30),
(2005, 'Kickboxing', '2023-03-27', '13:00:00', 0, 30),
(2001, 'Yoga', '2023-03-28', '09:00:00', 0, 30),
(2002, 'Pilates', '2023-03-28', '10:00:00', 0, 30),
(2003, 'Zumba', '2023-03-28', '11:00:00', 0, 30),
(2004, 'Spinning', '2023-03-28', '12:00:00', 0, 30),
(2005, 'Kickboxing', '2023-03-28', '13:00:00', 0, 30),
(2001, 'Yoga', '2023-03-29', '09:00:00', 30, 30),
(2002, 'Pilates', '2023-03-29', '10:00:00', 10, 30),
(2003, 'Zumba', '2023-03-29', '11:00:00', 5, 30),
(2004, 'Spinning', '2023-03-29', '12:00:00', 22, 30),
(2005, 'Kickboxing', '2023-03-29', '13:00:00', 1, 30),
(2001, 'Yoga', '2023-03-30', '09:00:00', 11, 30),
(2002, 'Pilates', '2023-03-30', '10:00:00', 23, 30),
(2003, 'Zumba', '2023-03-30', '11:00:00', 28, 30),
(2004, 'Spinning', '2023-03-30', '12:00:00', 22, 30),
(2005, 'Kickboxing', '2023-03-30', '13:00:00', 20, 30),
(2001, 'Yoga', '2023-03-31', '09:00:00', 10, 30),
(2002, 'Pilates', '2023-03-31', '10:00:00', 10, 30),
(2003, 'Zumba', '2023-03-31', '11:00:00', 8, 30),
(2004, 'Spinning', '2023-03-31', '12:00:00', 6, 30),
(2005, 'Kickboxing', '2023-03-31', '13:00:00', 7, 30),
(2001, 'Yoga', '2023-04-01', '09:00:00', 9, 30),
(2002, 'Pilates', '2023-04-01', '10:00:00', 0, 30),
(2003, 'Zumba', '2023-04-01', '11:00:00', 8, 30),
(2004, 'Spinning', '2023-04-01', '12:00:00', 0, 30),
(2005, 'Kickboxing', '2023-04-01', '13:00:00', 9, 30),
(2001, 'Yoga', '2023-04-02', '09:00:00', 17, 30),
(2002, 'Pilates', '2023-04-02', '10:00:00', 5, 30),
(2003, 'Zumba', '2023-04-02', '11:00:00', 4, 30),
(2004, 'Spinning', '2023-04-02', '12:00:00', 4, 30),
(2005, 'Kickboxing', '2023-04-02', '13:00:00', 6, 30),
(2001, 'Yoga', '2023-04-03', '09:00:00', 8, 30),
(2002, 'Pilates', '2023-04-03', '10:00:00', 9, 30),
(2003, 'Zumba', '2023-04-03', '11:00:00', 10, 30),
(2004, 'Spinning', '2023-04-03', '12:00:00', 12, 30),
(2005, 'Kickboxing', '2023-04-03', '13:00:00', 5, 30),
(2001, 'Yoga', '2023-04-04', '09:00:00', 7, 30),
(2002, 'Pilates', '2023-04-04', '10:00:00', 7, 30),
(2003, 'Zumba', '2023-04-04', '11:00:00', 0, 30),
(2004, 'Spinning', '2023-04-04', '12:00:00', 8, 30),
(2005, 'Kickboxing', '2023-04-04', '13:00:00', 0, 30),
(2001, 'Yoga', '2023-04-05', '09:00:00', 0, 30),
(2002, 'Pilates', '2023-04-05', '10:00:00', 15, 30),
(2003, 'Zumba', '2023-04-05', '11:00:00', 0, 30),
(2004, 'Spinning', '2023-04-05', '12:00:00', 13, 30),
(2005, 'Kickboxing', '2023-04-05', '13:00:00', 0, 30),
(2001, 'Yoga', '2023-04-06', '09:00:00', 11, 30),
(2002, 'Pilates', '2023-04-06', '10:00:00', 4, 30),
(2003, 'Zumba', '2023-04-06', '11:00:00', 14, 30),
(2004, 'Spinning', '2023-04-06', '12:00:00', 0, 30),
(2005, 'Kickboxing', '2023-04-06', '13:00:00', 65, 30),
(2001, 'Yoga', '2023-04-07', '09:00:00', 0, 30),
(2002, 'Pilates', '2023-04-07', '10:00:00', 0, 30),
(2003, 'Zumba', '2023-04-07', '11:00:00', 0, 30),
(2004, 'Spinning', '2023-04-07', '12:00:00', 0, 30),
(2005, 'Kickboxing', '2023-04-07', '13:00:00', 0, 30),
(2001, 'Yoga', '2023-04-08', '09:00:00', 0, 30),
(2002, 'Pilates', '2023-04-08', '10:00:00', 0, 30),
(2003, 'Zumba', '2023-04-08', '11:00:00', 0, 30),
(2004, 'Spinning', '2023-04-08', '12:00:00', 0, 30),
(2005, 'Kickboxing', '2023-04-08', '13:00:00', 0, 30),
(2001, 'Yoga', '2023-04-09', '09:00:00', 0, 30),
(2002, 'Pilates', '2023-04-09', '10:00:00', 0, 30),
(2003, 'Zumba', '2023-04-09', '11:00:00', 0, 30),
(2004, 'Spinning', '2023-04-09', '12:00:00', 0, 30),
(2005, 'Kickboxing', '2023-04-09', '13:00:00', 0, 30),
(2001, 'Yoga', '2023-04-10', '09:00:00', 0, 30),
(2002, 'Pilates', '2023-04-10', '10:00:00', 0, 30),
(2003, 'Zumba', '2023-04-10', '11:00:00', 0, 30),
(2004, 'Spinning', '2023-04-10', '12:00:00', 0, 30),
(2005, 'Kickboxing', '2023-04-10', '13:00:00', 0, 30),
(2001, 'Yoga', '2023-04-11', '09:00:00', 0, 30),
(2002, 'Pilates', '2023-04-11', '10:00:00', 0, 30),
(2003, 'Zumba', '2023-04-11', '11:00:00', 0, 30),
(2004, 'Spinning', '2023-04-11', '12:00:00', 0, 30),
(2005, 'Kickboxing', '2023-04-11', '13:00:00', 0, 30),
(2001, 'Yoga', '2023-04-12', '09:00:00', 0, 30),
(2002, 'Pilates', '2023-04-12', '10:00:00', 0, 30),
(2003, 'Zumba', '2023-04-12', '11:00:00', 0, 30),
(2004, 'Spinning', '2023-04-12', '12:00:00', 0, 30),
(2005, 'Kickboxing', '2023-04-12', '13:00:00', 0, 30),
(2001, 'Yoga', '2023-04-13', '09:00:00', 0, 30),
(2002, 'Pilates', '2023-04-13', '10:00:00', 0, 30),
(2003, 'Zumba', '2023-04-13', '11:00:00', 0, 30),
(2004, 'Spinning', '2023-04-13', '12:00:00', 0, 30),
(2005, 'Kickboxing', '2023-04-13', '13:00:00', 0, 30),
(2001, 'Yoga', '2023-04-14', '09:00:00', 0, 30),
(2002, 'Pilates', '2023-04-14', '10:00:00', 0, 30),
(2003, 'Zumba', '2023-04-14', '11:00:00', 0, 30),
(2004, 'Spinning', '2023-04-14', '12:00:00', 0, 30),
(2005, 'Kickboxing', '2023-04-14', '13:00:00', 0, 30),
(2001, 'Yoga', '2023-04-15', '09:00:00', 0, 30),
(2002, 'Pilates', '2023-04-15', '10:00:00', 0, 30),
(2003, 'Zumba', '2023-04-15', '11:00:00', 0, 30),
(2004, 'Spinning', '2023-04-15', '12:00:00', 0, 30),
(2005, 'Kickboxing', '2023-04-15', '13:00:00', 0, 30),
(2001, 'Yoga', '2023-04-16', '09:00:00', 0, 30),
(2002, 'Pilates', '2023-04-16', '10:00:00', 0, 30),
(2003, 'Zumba', '2023-04-16', '11:00:00', 0, 30),
(2004, 'Spinning', '2023-04-16', '12:00:00', 0, 30),
(2005, 'Kickboxing', '2023-04-16', '13:00:00', 0, 30),
(2001, 'Yoga', '2023-04-17', '09:00:00', 0, 30),
(2002, 'Pilates', '2023-04-17', '10:00:00', 0, 30),
(2003, 'Zumba', '2023-04-17', '11:00:00', 0, 30),
(2004, 'Spinning', '2023-04-17', '12:00:00', 0, 30),
(2005, 'Kickboxing', '2023-04-17', '13:00:00', 0, 30);


-- Inserting data into attendance table
INSERT INTO `attendance` (`member_id`, `date`, `timein`, `timeout`)
VALUES
(1002, '2023-03-09', '08:00:00', '10:00:00'),
(1003, '2023-03-09', '09:30:00', '11:00:00'),
(1003, '2023-03-10', '10:00:00', '12:00:00'),
(1002, '2023-03-10', '09:30:00', '11:00:00'),
(1003, '2023-03-11', '10:00:00', '12:00:00'),
(1004, '2023-03-11', '08:00:00', '10:00:00'),
(1005, '2023-03-12', '09:30:00', '11:00:00'),
(1006, '2023-03-12', '10:00:00', '12:00:00'),
(1007, '2023-03-13', '08:00:00', '10:00:00'),
(1008, '2023-03-13', '09:30:00', '11:00:00'),
(1009, '2023-03-14', '10:00:00', '12:00:00'),
(1010, '2023-03-14', '08:00:00', '10:00:00'),
(1011, '2023-03-15', '09:30:00', '11:00:00');

-- Inserting data into booking table
INSERT INTO `booking` (`class_id`, `session_id`, `date`, `booking_status`, `member_id`)
VALUES(NULL,'TS1002', '2023-03-15','completed', '1002'),
(NULL, 'TS1001', '2023-03-15','no-show', '1003'),
(NULL, 'TS1005', '2023-03-16','completed', '1001'),
(NULL, 'TS1008', '2023-03-17', 'completed', '1005'),
(NULL, 'TS1011', '2023-03-18', 'completed','1002'),
(NULL, 'TS1015', '2023-03-19', 'completed', '1004'),
('GC1001', NULL, '2023-03-13', 'completed', '2001'),
('GC1002', NULL, '2023-03-13', 'completed', '2002'),
('GC1003', NULL, '2023-03-13', 'completed','2003'),
('GC1004', NULL, '2023-03-13', 'completed', '2004'),
('GC1005', NULL, '2023-03-13', 'completed','2005'),
('GC1006', NULL, '2023-03-14', 'completed', '2001'),
('GC1007', NULL, '2023-03-14', 'completed', '2002'),
('GC1008', NULL, '2023-03-14', 'completed', '2003'),
('GC1009', NULL, '2023-03-14', 'completed','2004'),
('GC1010', NULL, '2023-03-14', 'completed', '2005'),
('GC1011', NULL, '2023-03-15', 'completed', '2001'),
('GC1012', NULL, '2023-03-15', 'completed', '2002'),
('GC1013', NULL, '2023-03-15', 'completed','2003'),
('GC1014', NULL, '2023-03-15', 'completed','2004'),
('GC1015', NULL, '2023-03-15', 'completed','2005'),
('GC1001', NULL, '2023-03-20','booked', '1002'),
('GC1005', NULL, '2023-03-20','booked', '1004'),
('GC1008', NULL, '2023-03-21','booked', '1001'),
('GC1011', NULL, '2023-03-22','booked', '1005'),
('GC1015', NULL, '2023-03-22','booked', '1003'),
('GC1020', NULL, '2023-03-23', 'booked', '1002'),
('GC1025', NULL, '2023-03-24','booked', '1001'),
('GC1028', NULL,  '2023-03-25','booked', '1004'),
('GC1030', NULL, '2023-03-25','booked', '1003'),
('GC1035', NULL, '2023-03-26','booked', '1005'),
(NULL, 'TS1011', '2023-03-21','booked', '1002'),
(NULL, 'TS1015', '2023-03-22','booked', '1002'),
(NULL, 'TS1018', '2023-03-23', 'booked', '1002')
;