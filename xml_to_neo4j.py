from tempfile import NamedTemporaryFile
import html

from pyspark.sql.types import StringType, StructType, StructField, ArrayType
from pyspark.sql.functions import concat_ws, lit, translate


schema = StructType([
  StructField("_key", StringType()),
  StructField("title", StringType()),
  StructField("year", StringType()),
  StructField("author", ArrayType(
      StructType([
          StructField("_VALUE", StringType())
      ])
   ))
])

# El fichro tiene caracteres escapadas HTML (como &agrave;), por lo que es
# necesario limpiarlo.

with open('./dblp.xml') as source, NamedTemporaryFile('w') as unescaped_src:
    for line in source:
        unescaped_src.write(html.unescape(line))

    incollections_df = spark.read.format('com.databricks.spark.xml').option(
        "rowTag", "incollection").option('charset', "ISO-8859-1").schema(
        schema).load(unescaped_src.name)
    inproceedings_df = spark.read.format('com.databricks.spark.xml').option(
        "rowTag", "inproceedings").option('charset',
        "ISO-8859-1").schema(schema).load(unescaped_src.name)
    articles_df = spark.read.format('com.databricks.spark.xml').option("rowTag",
        "article").option('charset', "ISO-8859-1").schema(schema).load(
        unescaped_src.name)

    publications_df = incollections_df.withColumn('LABEL',
        lit('Incollection')).union(inproceedings_df.withColumn('LABEL',
        lit('Inproceeding'))).union(articles_df.withColumn('LABEL', lit(
            'Article')))

    publications_df = publications_df.filter(publications_df._key.isNotNull())

    publications_df.withColumn('id', translate('_key', '/', '_')).select('id',
        'title', 'year', 'LABEL').write.option('escape', '"').csv(
        './csv/publications')

    publications_df.withColumn('_author', explode('author._VALUE')).select(
        '_author').write.option('escape', '"').csv('./csv/authors')

    publications_df.withColumn('start', explode('author._VALUE')).withColumn(
        'end', translate('_key', '/', '_')).select('start', 'end').write.option(
            'escape', '"').csv('./csv/rels')

