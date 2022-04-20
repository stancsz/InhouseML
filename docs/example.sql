CREATE FUNCTION ihml_get_dataset_describe(name text, features text[], labels text[])
    RETURNS JSON
AS
$$
   from inhouseml import tfRunner
   job = tfRunner(name=name, features=features, labels=labels)
   job.load_dataset(plpy.execute(job.get_query()))
   return job.get_dataset_describe()
$$ LANGUAGE plpython3u;


SELECT * FROM ihml_get_dataset_describe('autompg', ARRAY ['horsepower','cylinders'], ARRAY ['mpg']);

DROP FUNCTION ihml_get_dataset_describe;