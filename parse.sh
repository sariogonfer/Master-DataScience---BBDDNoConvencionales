GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}Eliminando directorios de salida json y csv...${NC}"
rm -rf csv
rm -rf json

echo -e "${GREEN}Ejecutando script de parseo de XML...${NC}"
python parser.py

echo -e "${GREEN}Agrupando json de carga de MongoDB...${NC}"
cat json/articles/part-* > json/articles.json
echo -e "${GREEN}>  Generado json/articles.json${NC}"
cat json/incollections/part-* > json/incollections.json
echo -e "${GREEN}>  Generado json/incollections.json${NC}"
cat json/inproceedings/part-* > json/inproceedings.json
echo -e "${GREEN}>  Generado json/inproceedings.json${NC}"

