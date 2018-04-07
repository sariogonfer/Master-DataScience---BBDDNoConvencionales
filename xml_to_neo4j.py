from pyspark.sql.types import StringType, StructType, StructField, ArrayType
from pyspark.sql.functions import explode, lit, translate


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

incollections_df = spark.read.format('com.databricks.spark.xml').option(
        "rowTag", "incollection").option('charset', "ISO-8859-1").schema(
                schema).load('./dblp.xml')
inproceedings_df = spark.read.format('com.databricks.spark.xml').option(
        "rowTag", "inproceedings").option('charset',
                "ISO-8859-1").schema(schema).load('./dblp.xml')
articles_df = spark.read.format('com.databricks.spark.xml').option("rowTag",
        "articles").option('charset', "ISO-8859-1").schema(schema).load(
                './dblp.xml')

publications_df = incollections_df.withColumn('LABEL',
        lit('incollection;publication')).union(inproceedings_df.withColumn(
            'LABEL', lit('inproceedings;publication'))).union(
                    articles_df.withColumn('LABEL',
                        lit('articles;publication')))

publications_df.withColumn('id', translate('_key', '/', '_')).select('id',
        'title', 'year', 'LABEL').write.option('escape', '"').csv(
                './csv/publications')

publications_df.withColumn('_author', explode('author._VALUE')).withColumn(
        'LABEL', lit('author')).select('_author', 'LABEL').write.option(
                'escape', '"').csv('./csv/authors')

publications_df.withColumn('start', explode('author._VALUE')).withColumn(
        'end', translate('_key', '/', '_')).withColumn('TYPE',
                lit('WRITES')).select('start', 'end', 'TYPE').write.option(
                        'escape', '"').csv('./csv/author_publication_rel')

