create database acheiobicho;

use acheiobicho;

CREATE TABLE User (
  id INT PRIMARY KEY,
  documentNumber VARCHAR(255) NOT NULL,
  nameUser VARCHAR(255) NOT NULL,
  contact VARCHAR(255) NOT NULL
);

CREATE TABLE Animal (
  id INT PRIMARY KEY,
  nameAnimal VARCHAR(255) NOT NULL,
  gender VARCHAR(10) NOT NULL,
  birthMonth DATE NOT NULL,
  breedName VARCHAR(255) NOT NULL,
  borough VARCHAR(255) NOT NULL,
  zipCode VARCHAR(10) NOT NULL,
  typeAnimal VARCHAR(255) NOT NULL,
  urlImage VARCHAR(255) NOT NULL,
  idUser INT NOT NULL,
  FOREIGN KEY (id) REFERENCES User(id)
);