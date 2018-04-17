GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}Importando articles.json...${NC}"
mongoimport --db=dblp --collection=articles json/articles.json
echo -e "${GREEN}Importando incollections.json...${NC}"
mongoimport --db=dblp --collection=incollections json/incollections.json
echo -e "${GREEN}Importando inproceedings.json...${NC}"
mongoimport --db=dblp --collection=inproceedings json/inproceedings.json
echo -e "${GREEN}Importación finalizada${NC}"
