CREATE TABLE `carinfo1` (
  `vechiclesID` int(11) NOT NULL,
  `series` varchar(32) DEFAULT NULL,
  `brand` varchar(32) DEFAULT NULL,
  `carType` varchar(16) DEFAULT NULL,
  `peopleNum` varchar(32) DEFAULT NULL,
  `marketTime` varchar(16) DEFAULT NULL,
  `engine` varchar(32) DEFAULT NULL,
  `displacement` varchar(255) DEFAULT NULL,
  `first_latter` varchar(2) DEFAULT NULL,
  `model` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`vechiclesID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;