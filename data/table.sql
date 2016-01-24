CREATE TABLE word_ngram_map
(
    id INT(20) NOT NULL AUTO_INCREMENT,
    word CHAR(20) NOT NULL,
    ngram CHAR(100) NOT NULL,
    PRIMARY KEY (id)
)
ENGINE=InnoDB;
CREATE INDEX word ON word_ngram_map (word);
