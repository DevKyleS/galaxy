# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-05 16:56
from __future__ import unicode_literals

from django.contrib.postgres import indexes as psql_indexes
from django.contrib.postgres import search as psql_search
from django.db import migrations

SET_SEARCH_VECTOR = """
UPDATE main_content
SET search_vector =
  setweight(to_tsvector(name), 'A')
  || setweight(to_tsvector(description), 'C')
  || setweight(to_tsvector(readme), 'D');
"""

CREATE_SEARCH_VECTOR_UPDATE_TRIGGER = """
CREATE FUNCTION update_content_search_vector() RETURNS TRIGGER AS $$
BEGIN
  NEW.search_vector :=
    setweight(to_tsvector(NEW.name), 'A')
    || setweight(to_tsvector(NEW.description), 'C')
    || setweight(to_tsvector(NEW.readme), 'D');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER update_content_search_vector_trigger
BEFORE INSERT OR UPDATE
  ON main_content
  FOR EACH ROW
  EXECUTE PROCEDURE update_content_search_vector();
"""

DROP_SEARCH_VECTOR_UPDATE_TRIGGER = """
DROP TRIGGER update_content_search_vector_trigger ON main_content;
DROP FUNCTION update_content_search_vector();
"""


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0082_apb_content_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='search_vector',
            field=psql_search.SearchVectorField(default=''),
            preserve_default=False,
        ),
        migrations.AddIndex(
            model_name='content',
            index=psql_indexes.GinIndex(
                fields=['search_vector'],
                name='main_conten_search__47815a_gin'),
        ),
        migrations.RunSQL(sql=(SET_SEARCH_VECTOR,
                               CREATE_SEARCH_VECTOR_UPDATE_TRIGGER),
                          reverse_sql=DROP_SEARCH_VECTOR_UPDATE_TRIGGER),
    ]
