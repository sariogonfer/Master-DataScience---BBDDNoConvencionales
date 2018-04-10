LOAD CSV WITH HEADERS FROM "file:///authors.csv" AS csvReg
MERGE (p:Author {author: csvReg.author})

LOAD CSV WITH HEADERS FROM "file:///publications.csv" AS csvReg
MERGE (p:Publication {title: csvReg.title, year: csvReg.year, label: csvReg.label})

LOAD CSV WITH HEADERS FROM "file:///author_publication_rel.csv" AS csvLine
MATCH (a:Author { author: csvLine.start}), (p:Publication { title: csvLine.end})
CREATE (a)-[:WRITED]->(p)﻿
